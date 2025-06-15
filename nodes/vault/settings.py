from framework.utils.fs import read_file

VPN_PROFILE = "vault"
VPN_VAULT_PRIVATE_KEY = read_file(
    ".secrets/VPN_VAULT_PRIVATE_KEY", must_exist=True
).strip()
VPN_FACADE_PUBLIC_KEY = read_file(
    ".secrets/VPN_FACADE_PUBLIC_KEY", must_exist=True
).strip()
