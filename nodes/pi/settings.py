DIRECTORIES = {
    "public": {"path": "/srv/public", "owner": ["root", "root"], "perm": "755"},
}

MINIDLNA_ENABLED = True
MINIDLNA_FRIENDLY_NAME = "Raspberry Pi"
MINIDLNA_DIRECTORY_ID = "public"

STATIC_SITES_ENABLED = False
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
