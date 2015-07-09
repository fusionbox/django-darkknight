import re
import os

from django import forms
from django.db import transaction
from django.utils.translation import ugettext as _
from django.forms.formsets import BaseFormSet
from localflavor.us.us_states import US_STATES
from django_countries import countries

from OpenSSL import crypto
from darkknight.models import CertificateSigningRequest, SSLKey

KEY_SIZE = 2048
WWW = 'www.'


def creat(filename, mode):
    fd = os.open(filename, os.O_CREAT | os.O_WRONLY | os.O_EXCL, mode)
    return os.fdopen(fd, 'w')


class GenerateForm(forms.Form):
    countryName = forms.ChoiceField(
        choices=countries,
        label=_("Country Name"),
        initial='US',
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
    subjectAlternativeNames = forms.CharField(
        label=_('Subject Alternative Names (SAN)'),
        required=False,
        help_text=_('Please put one domain name per line'),
        widget=forms.Textarea,
    )

    def clean_countryName(self):
        country = self.cleaned_data['countryName']
        if not re.match('^[a-z]{2}$', country, flags=re.IGNORECASE):
            raise forms.ValidationError(_("Please enter a two-letters code"))
        return country.upper()

    def clean_subjectAlternativeNames(self):
        sans = list(filter(bool, (
            domain.strip() for domain in self.cleaned_data['subjectAlternativeNames'].splitlines()
        )))
        return sans

    def clean(self):
        cd = super(GenerateForm, self).clean()
        if cd.get('countryName') == 'US':
            try:
                if cd['stateOrProvinceName'] not in set(i[1] for i in US_STATES):
                    self.add_error('stateOrProvinceName', 'State should be the full state name, eg "Colorado"')
            except KeyError:
                pass
        return cd


class GenerateBaseFormSet(BaseFormSet):

    def generate(self):
        pkey = crypto.PKey()
        pkey.generate_key(crypto.TYPE_RSA, KEY_SIZE)

        key_obj = SSLKey()

        csr_list = [self._generate_csr(pkey, key_obj, data) for data in self.cleaned_data]

        with transaction.atomic():
            key = crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey)
            assert not os.path.exists(key_obj.key_path)
            with creat(key_obj.key_path, 0000) as f:
                f.write(key)

            key_obj.save()
            CertificateSigningRequest.objects.bulk_create(csr_list)

        return key_obj

    def _generate_csr(self, pkey, key_obj, cleaned_data):
        req = crypto.X509Req()
        req.set_pubkey(pkey)

        subject = req.get_subject()

        for attr, value in cleaned_data.items():
            if value:
                if attr == 'subjectAlternativeNames':
                    req.add_extensions([
                        crypto.X509Extension('subjectAltName', False, ", ".join(
                            "DNS.{i}:{domain}".format(i=i, domain=domain)
                            for i, domain in enumerate(value)
                        ))
                    ])
                else:
                    setattr(subject, attr, value)

        cn = cleaned_data['commonName']
        # Strip www. from the common name
        if cn.startswith(WWW):
            cn = cn[len(WWW):]

        req.sign(pkey, "sha256")
        csr = crypto.dump_certificate_request(crypto.FILETYPE_PEM, req)
        csr_obj = CertificateSigningRequest(domain=cn, key=key_obj, content=csr)
        return csr_obj
