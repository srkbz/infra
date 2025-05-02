#!/usr/bin/env python3
from ipaddress import ip_address, ip_network
from os import makedirs, environ
from os.path import join, exists
from subprocess import run
from sys import stderr

WG_PORT = 51820
VPN_NETWORK = ip_network("10.10.0.0/24")

VAULT_IP = ip_address("10.10.0.1")

FACADE_IP = ip_address("10.10.0.2")
FACADE_PUBLIC_ADDRESS = "facade.srk.bz"

assert VAULT_IP in VPN_NETWORK
assert FACADE_IP in VPN_NETWORK

VPN_CONFIG = environ.get("VPN_CONFIG")


def main():
    vault_dir = join(VPN_CONFIG, "vault")
    facade_dir = join(VPN_CONFIG, "facade")

    vault_private_key, vault_public_key = ensure_keypair(vault_dir)
    facade_private_key, facade_public_key = ensure_keypair(facade_dir)

    def vault_config():
        yield "[Interface]"
        yield f"Address = {VAULT_IP}/32"
        yield f"ListenPort = {WG_PORT}"
        yield f"PrivateKey = {vault_private_key}"
        yield ""
        yield "# Facade"
        yield "[Peer]"
        yield f"PublicKey = {facade_public_key}"
        yield f"AllowedIPs = {FACADE_IP}/32"
        # yield f"Endpoint = {FACADE_PUBLIC_ADDRESS}:{WG_PORT}"
        yield "PersistentKeepalive = 5"

    write_config(join(vault_dir, "wg0.conf"), vault_config)

    def facade_config():
        yield "[Interface]"
        yield f"Address = {FACADE_IP}/32"
        yield f"ListenPort = {WG_PORT}"
        yield f"PrivateKey = {facade_private_key}"
        yield ""
        yield "# Vault"
        yield "[Peer]"
        yield f"PublicKey = {vault_public_key}"
        yield f"AllowedIPs = {VAULT_IP}/32"
        yield "PersistentKeepalive = 5"

    write_config(join(facade_dir, "wg0.conf"), facade_config)


def ensure_keypair(dir: str):
    if not exists(join(dir, "private.key")):
        log("Creating keypair for " + dir)
        makedirs(dir, exist_ok=True)
        run(
            ["bash", "-c", "wg genkey | tee private.key | wg pubkey>public.key"],
            cwd=dir,
        )
    else:
        log("Reusing keypair for " + dir)
    private_key = read_file(join(dir, "private.key")).strip()
    public_key = read_file(join(dir, "public.key")).strip()
    return (private_key, public_key)


def read_file(path):
    with open(path, "r") as f:
        return f.read()


def write_config(path, gen):
    log("Writting config to " + path)
    with open(path, "w") as f:
        for line in gen():
            f.writelines(line + "\n")


def log(msg):
    print(f"### {msg}", file=stderr)


if __name__ == "__main__":
    main()
