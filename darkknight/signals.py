from django.dispatch import Signal


# Gives people a chance to do something with the CSR while the key is
# available.
key_created = Signal(providing_args=['instance', 'private_key'])
