import textwrap
from ipaddress import ip_address, ip_network

from framework.utils.fs import read_file
from modules import wireguard

import settings

WG_PORT = 51820
VPN_NETWORK = ip_network("10.10.0.0/24")

VAULT_IP = ip_address("10.10.0.1")
FACADE_IP = ip_address("10.10.0.2")
FACADE_PUBLIC_ADDRESS = "facade.srk.bz"

assert VAULT_IP in VPN_NETWORK
assert FACADE_IP in VPN_NETWORK

PROFILE = getattr(settings, "VPN_PROFILE", None)

if PROFILE is not None:
    match PROFILE:
        case "facade":
            FACADE_PRIVATE_KEY = read_file(
                getattr(settings, "VPN_FACADE_PRIVATE_KEY_PATH"), must_exist=True
            ).strip()
            VAULT_PUBLIC_KEY = read_file(
                getattr(settings, "VPN_VAULT_PUBLIC_KEY_PATH"), must_exist=True
            ).strip()

            wireguard.config.add_interface(
                textwrap.dedent(
                    f"""
                    [Interface]
                    Address = {FACADE_IP}/32
                    ListenPort = {WG_PORT}
                    PrivateKey = {FACADE_PRIVATE_KEY}

                    # Vault
                    [Peer]
                    PublicKey = {VAULT_PUBLIC_KEY}
                    AllowedIPs = {VAULT_IP}/32
                    PersistentKeepalive = 5
                    """
                ).lstrip()
            )

        case "vault":
            VAULT_PRIVATE_KEY = read_file(
                getattr(settings, "VPN_VAULT_PRIVATE_KEY_PATH"), must_exist=True
            ).strip()
            FACADE_PUBLIC_KEY = read_file(
                getattr(settings, "VPN_FACADE_PUBLIC_KEY_PATH"), must_exist=True
            ).strip()

            wireguard.config.add_interface(
                textwrap.dedent(
                    f"""
                    [Interface]
                    Address = {VAULT_IP}/32
                    ListenPort = {WG_PORT}
                    PrivateKey = {VAULT_PRIVATE_KEY}

                    # Facade
                    [Peer]
                    PublicKey = {FACADE_PUBLIC_KEY}
                    AllowedIPs = {FACADE_IP}/32
                    Endpoint = {FACADE_PUBLIC_ADDRESS}:{WG_PORT}
                    PersistentKeepalive = 5
                    """
                ).lstrip()
            )
