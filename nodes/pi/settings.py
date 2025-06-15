from framework.utils.fs import read_file

DIRECTORIES = {
    "public": {"path": "/srv/public", "owner": ["root", "root"], "perm": "755"},
}

MINIDLNA_ENABLED = True
MINIDLNA_FRIENDLY_NAME = "Raspberry Pi"
MINIDLNA_DIRECTORY_ID = "public"

VPN_PROFILE = "vault"
VPN_VAULT_PRIVATE_KEY = read_file(
    ".secrets/VPN_VAULT_PRIVATE_KEY", must_exist=True
).strip()
VPN_FACADE_PUBLIC_KEY = read_file(
    ".secrets/VPN_FACADE_PUBLIC_KEY", must_exist=True
).strip()
