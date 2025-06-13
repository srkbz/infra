DIRECTORIES = {
    "public": {"path": "/srv/public", "owner": ["root", "root"], "perm": "755"},
}

MINIDLNA_ENABLED = True
MINIDLNA_FRIENDLY_NAME = "Raspberry Pi"
MINIDLNA_DIRECTORY_ID = "public"

STATIC_SITES_ENABLED = True
STATIC_SITES = {
    "sirikon.me": {"repository": "https://github.com/sirikon/sirikon.me.git"}
}
