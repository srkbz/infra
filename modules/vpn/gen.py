#!/usr/bin/env python3
from ipaddress import ip_address, ip_network
from os import makedirs, environ
from os.path import join, exists
from subprocess import run

WG_PORT = 51820
VPN_NETWORK = ip_network("10.10.0.0/24")

VAULT_IP = ip_address("10.10.0.1")

GATEWAY_IP = ip_address("10.10.0.2")
GATEWAY_PUBLIC_ADDRESS = "gateway.srk.bz"

assert VAULT_IP in VPN_NETWORK
assert GATEWAY_IP in VPN_NETWORK

VPN_CONFIG = environ.get("VPN_CONFIG")


def main():
    vault_dir = join(VPN_CONFIG, "vault")
    gateway_dir = join(VPN_CONFIG, "gateway")

    vault_private_key, vault_public_key = ensure_keypair(vault_dir)
    gateway_private_key, gateway_public_key = ensure_keypair(gateway_dir)

    def vault_config():
        yield "[Interface]"
        yield f"Address = {VAULT_IP}/32"
        yield f"ListenPort = {WG_PORT}"
        yield f"PrivateKey = {vault_private_key}"
        yield ""
        yield "# Gateway"
        yield "[Peer]"
        yield f"PublicKey = {gateway_public_key}"
        yield f"AllowedIPs = {GATEWAY_IP}/32"
        yield f"Endpoint = {GATEWAY_PUBLIC_ADDRESS}:{WG_PORT}"
        yield "PersistentKeepalive = 5"

    write_config(join(vault_dir, "wg0.conf"), vault_config)

    def gateway_config():
        yield "[Interface]"
        yield f"Address = {GATEWAY_IP}/32"
        yield f"ListenPort = {WG_PORT}"
        yield f"PrivateKey = {gateway_private_key}"
        yield ""
        yield "# Vault"
        yield "[Peer]"
        yield f"PublicKey = {vault_public_key}"
        yield f"AllowedIPs = {VAULT_IP}/32"
        yield "PersistentKeepalive = 5"

    write_config(join(gateway_dir, "wg0.conf"), gateway_config)


def ensure_keypair(dir: str):
    if not exists(join(dir, "private.key")):
        makedirs(dir, exist_ok=True)
        run(
            ["bash", "-c", "wg genkey | tee private.key | wg pubkey>public.key"],
            cwd=dir,
        )
    private_key = read_file(join(dir, "private.key")).strip()
    public_key = read_file(join(dir, "public.key")).strip()
    return (private_key, public_key)


def read_file(path):
    with open(path, "r") as f:
        return f.read()


def write_config(path, gen):
    with open(path, "w") as f:
        f.writelines(gen())


if __name__ == "__main__":
    main()
