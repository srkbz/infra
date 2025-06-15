from framework.utils.fs import read_file

CADDY_ENABLED = True

STATIC_SITES_ENABLED = True
STATIC_SITES = {
    "sirikon.me": {"repository": "https://github.com/sirikon/sirikon.me.git"},
    "osoondo.com": {"repository": "https://github.com/sirikon/osoondo.com.git"},
    "egin.sirikon.me": {"repository": "https://github.com/sirikon/egin.git"},
    "ebro.sirikon.me": {
        "repository": "https://github.com/sirikon/ebro.git",
        "build_script": "./meta/docker/build.sh website",
        "directory": "out/website",
    },
    "astenagusia.eus": {"repository": "https://github.com/sirikon/astenagusia.git"},
    "2048.sirikon.me": {"repository": "https://github.com/sirikon/2048.git"},
}

VPN_PROFILE = "facade"
VPN_FACADE_PRIVATE_KEY = read_file(
    ".secrets/VPN_FACADE_PRIVATE_KEY", must_exist=True
).strip()
