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
        max_length=255,
        label=_("State or province name"),
        help_text=_("Enter its full name"),
    )
    localityName = forms.CharField(
        max_length=255,
        label=_("Locality name"),
        help_text=_("eg, city name"),
    )
    organizationName = forms.CharField(
        max_length=255,
        label=_("Organisation Name"),
        help_text=_("eg, company name"),
    )
    organizationalUnitName = forms.CharField(
        max_length=255,
        label=_("Organisation Unit"),
        help_text=_("Section, Department, ... eg, IT Departement"),
        required=False,
    )
    commonName = forms.CharField(
        max_length=255,
        label=_("Common Name"),
        help_text=_("Domain name, including 'www.' if applicable. "
                    "eg, www.example.com")
    )
    emailAddress = forms.EmailField(
        max_length=255,
        label=_("Email address"),
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
