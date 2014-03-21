import re
import uuid
import os

from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings

from OpenSSL import crypto
from darkknight.models import CertificateSigningRequest

KEY_SIZE = 2048
WWW = 'www.'


class GenerateForm(forms.Form):
    countryName = forms.CharField(
        max_length=2,
        label=_("Country Name"),
        help_text=_("Two letters code"),
    )
    stateOrProvinceName = forms.CharField(
        label=_("State or province name"),
        help_text=_("Enter its full name"),
    )
    localityName = forms.CharField(
        label=_("Locality name"),
        help_text=_("eg, city name"),
    )
    organizationName = forms.CharField(
        label=_("Organisation Name"),
        help_text=_("eg, company name"),
    )
    organizationalUnitName = forms.CharField(
        label=_("Organisation Unit"),
        help_text=_("Section, Department, ... eg, IT Departement"),
        required=False,
    )
    commonName = forms.CharField(
        label=_("Common Name"),
        help_text=_("Domain name, including 'www.' if applicable. "
                    "eg, www.example.com")
    )
    emailAddress = forms.EmailField(
        label=_("Email address"),
        required=False,
    )

    def clean_countryName(self):
        country = self.cleaned_data['countryName']
        if not re.match('^[a-z]{2}$', country, flags=re.IGNORECASE):
            raise forms.ValidationError(_("Please enter a two-letters code"))
        return country.upper()

    def generate(self):
        pkey = crypto.PKey()
        pkey.generate_key(crypto.TYPE_RSA, KEY_SIZE)

        req = crypto.X509Req()
        req.set_pubkey(pkey)

        subject = req.get_subject()
        for attr, value in self.cleaned_data.items():
            if value:
                setattr(subject, attr, value)

        name = uuid.uuid4().hex
        cn = self.cleaned_data['commonName']

        # Strip www. from the common name
        if cn.startswith(WWW):
            cn = cn[len(WWW):]

        req.sign(pkey, "sha1")

        key = crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey)
        csr = crypto.dump_certificate_request(crypto.FILETYPE_PEM, req)

        keyfname = os.path.join(settings.DARKKNIGHT_STORAGE, '%s.key' % name)
        csrfname = os.path.join(settings.DARKKNIGHT_STORAGE, '%s.csr' % name)

        assert not os.path.exists(keyfname)

        with open(keyfname, 'w') as f:
            f.write(key)
        with open(csrfname, 'w') as f:
            f.write(csr)

        res = CertificateSigningRequest.objects.create(
            key=keyfname, csr=csrfname, domain=cn)
        return res


class UploadCertificateForm(forms.Form):
    certificate_file = forms.FileField(
        required=False,
    )
    certificate_content = forms.CharField(
        widget=forms.Textarea,
        required=False
    )

    def clean(self):
        cleaned_data = super(UploadCertificateForm, self).clean()

        fields = ('certificate_file', 'certificate_content', )
        if not any(cleaned_data[f] for f in fields):
            raise forms.ValidationError(_("Please upload a certificate or "
                                          "copy its content."))

        if cleaned_data['certificate_file']:
            certificate = self.clean_certificate(
                self.cleaned_data['certificate_file'].read())
        else:
            assert cleaned_data['certificate_content']
            certificate = self.clean_certificate(
                self.cleaned_data['certificate_content'])

        return dict(certificate=certificate)

    def clean_certificate(self, content):
        if 'CERTIFICATE REQUEST' in content:
            raise forms.ValidationError(
                _("You should upload a certificate, not a certificate request."
                  " This is the file given to you by your certificate "
                  "authority.")
            )
        elif 'PKCS #7' in content:
            return self.load_pkcs7(content)
        elif 'CERTIFICATE' in content:
            return self.load_cert(content)
        else:
            raise forms.ValidationError(
                _("Unknown certificate type. If this certificate was given by "
                  "your Certificate Authority. Please contact the "
                  "administrator of this website.")
            )

    def load_cert(self, content):
        try:
            cert = crypto.load_certificate(crypto.FILETYPE_PEM, content)
            assert False
        except crypto.Error:
            raise forms.ValidationError(
                _("The Apache certificate format has been recognized. But we "
                  "weren't able to read it. Please double check your "
                  "certificate.")
            )

    def load_pkcs7(self, content):
        try:
            pkcs7 = crypto.load_pkcs7_data(crypto.FILETYPE_PEM, content)
            assert False
        except crypto.Error:
            raise forms.ValidationError(
                _("The IIS certificate format has been recognized. But we "
                  "weren't able to read it. Please double check your "
                  "certificate.")
            )
