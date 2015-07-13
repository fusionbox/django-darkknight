Django Dark Knight
==================

He's a silent guardian, a watchful protector.
  ~ Lt. Gordon -- Dark Knight (2008)

Django Dark Knight generates, stores and manages private keys and certificate
signing requests.


Dark Knight GPG
---------------

Dark Knight supports retrieving private keys encrypted with gpg. To enable:

  - Install `django-darkknight[gpg]`
  - Add `darkknight_gpg` to ``INSTALLED_APPS``
  - Add the ``apptemplates.Loader`` to ``TEMPLATE_LOADERS``
  - Include the ``darkknight_gpg.urls`` urlpatterns
  - Set ``GPG_PUBLIC_KEY_PATH`` to the path to the file containing the gpg
    key(s) to use as the recipient for the encrypted private keys.
