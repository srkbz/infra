#!/usr/bin/env python3
from ipaddress import ip_address, ip_network
from sys import argv
from os import makedirs
from os.path import join, exists
from subprocess import run

WG_PORT = 51820
VPN_NETWORK = ip_network("10.0.0.0/24")
HOME_NETWORK = ip_network("192.168.1.0/24")

SERVER_IP = ip_address("10.0.0.1")
SERVER_PUBLIC_ADDRESS = "vpn.srk.bz"

HOME_GATEWAY_IP = ip_address("10.0.0.2")
HOME_GATEWAY_DEFAULT_INTERFACE = "eth0"

CLIENTS = [("phone", ip_address("10.0.0.3"))]

assert SERVER_IP in VPN_NETWORK
assert HOME_GATEWAY_IP in VPN_NETWORK
for _, ip in CLIENTS:
    assert ip in VPN_NETWORK


def main():
    if len(argv) <= 1:
        print("Usage: configure.py <server|home-gateway>")
        exit(1)

    match argv[1]:
        case "server":
            server_configure()
        case "home-gateway":
            home_gateway_configure()
        case _:
            print("Unrecognized option " + argv[1])
            exit(1)


def server_configure():
    if not exists("/opt/vpn/server/private.key"):
        makedirs("/opt/vpn/server", exist_ok=True)
        run(
            ["bash", "-c", "wg genkey | tee private.key | wg pubkey>public.key"],
            cwd="/opt/vpn/server",
        )

    if not exists("/opt/vpn/home-gateway/private.key"):
        makedirs("/opt/vpn/home-gateway", exist_ok=True)
        run(
            ["bash", "-c", "wg genkey | tee private.key | wg pubkey>public.key"],
            cwd="/opt/vpn/home-gateway",
        )

    for client_name, client_ip in CLIENTS:
        if not exists(join("/opt/vpn/clients", client_name, "private.key")):
            makedirs(join("/opt/vpn/clients", client_name), exist_ok=True)
            run(
                ["bash", "-c", "rm -rf *"],
                cwd=join("/opt/vpn/clients", client_name),
            )
            run(
                ["bash", "-c", "wg genkey | tee private.key | wg pubkey>public.key"],
                cwd=join("/opt/vpn/clients", client_name),
            )

        with open(join("/opt/vpn/clients", client_name, "home_lan.conf"), "w") as f:
            for line in client_home_lan_wireguard_config(client_name, client_ip):
                f.write(line + "\n")

    with open("/opt/vpn/server/wg0.conf", "w") as f:
        for line in server_wireguard_config():
            f.write(line + "\n")


def client_home_lan_wireguard_config(client_name, client_ip):
    yield "[Interface]"
    yield "PrivateKey = " + read_file(
        join("/opt/vpn/clients", client_name, "private.key")
    ).strip()
    yield f"Address = {client_ip}/32"
    yield ""
    yield "[Peer]"
    yield "PublicKey = " + read_file("/opt/vpn/server/public.key").strip()
    yield f"AllowedIPs = {VPN_NETWORK}, {HOME_NETWORK}"
    yield f"Endpoint = {SERVER_PUBLIC_ADDRESS}:{WG_PORT}"


def server_wireguard_config():
    yield "[Interface]"
    yield f"Address = {SERVER_IP}/{VPN_NETWORK.prefixlen}"
    yield f"ListenPort = {WG_PORT}"
    yield "PrivateKey = " + read_file("/opt/vpn/private.key").strip()
    yield ""
    yield "PostUp = iptables -A FORWARD -i wg0 -o wg0 -j ACCEPT"
    yield "PostDown = iptables -D FORWARD -i wg0 -o wg0 -j ACCEPT"
    yield ""
    yield "# Home Gateway"
    yield "[Peer]"
    yield "PublicKey = " + read_file("/opt/vpn/home-gateway/public.key").strip()
    yield f"AllowedIPs = {HOME_GATEWAY_IP}/32,{HOME_NETWORK}"
    yield ""
    for client_name, client_ip in CLIENTS:
        yield f"# Client: {client_name}"
        yield "[Peer]"
        yield "PublicKey = " + read_file(
            f"/opt/vpn/clients/{client_name}/public.key"
        ).strip()
        yield f"AllowedIPs = {client_ip}/32"


def home_gateway_configure():
    print("[Interface]")
    print(f"Address = {HOME_GATEWAY_IP}/{VPN_NETWORK.prefixlen}")
    print(f"ListenPort = {WG_PORT}")
    print("PrivateKey = " + read_file("iface-keys/private").strip())
    print("")
    print(
        "PostUp = "
        + "; ".join(
            [
                f"iptables -t nat -A POSTROUTING -o {HOME_GATEWAY_DEFAULT_INTERFACE} -j MASQUERADE",
                f"iptables -A FORWARD -i wg0 -o {HOME_GATEWAY_DEFAULT_INTERFACE} -j ACCEPT",
                f"iptables -A FORWARD -i {HOME_GATEWAY_DEFAULT_INTERFACE} -o wg0 -m state --state RELATED,ESTABLISHED -j ACCEPT",
            ]
        )
    )
    print(
        "PostDown = "
        + "; ".join(
            [
                f"iptables -t nat -D POSTROUTING -o {HOME_GATEWAY_DEFAULT_INTERFACE} -j MASQUERADE",
                f"iptables -D FORWARD -i wg0 -o {HOME_GATEWAY_DEFAULT_INTERFACE} -j ACCEPT",
                f"iptables -D FORWARD -i {HOME_GATEWAY_DEFAULT_INTERFACE} -o wg0 -m state --state RELATED,ESTABLISHED -j ACCEPT",
            ]
        )
    )
    print("")
    print("# Server")
    print("[Peer]")
    print("PublicKey = " + read_file(f"peer-data/server.public-key").strip())
    print(f"AllowedIPs = {VPN_NETWORK}")
    print(f"Endpoint = {SERVER_PUBLIC_ADDRESS}:{WG_PORT}")
    print("PersistentKeepalive = 15")


def read_file(path):
    with open(path, "r") as f:
        return f.read()


if __name__ == "__main__":
    main()
