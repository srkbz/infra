import textwrap

DIRECTORIES = {
    "public": {"path": "/srv/public", "owner": ["root", "root"], "perm": "755"},
}

MINIDLNA_ENABLED = True
MINIDLNA_FRIENDLY_NAME = "Raspberry Pi"
MINIDLNA_DIRECTORY_ID = "public"

CADDY_ENABLED = False
CADDY_CADDYFILES = [
    textwrap.dedent(
        """
        :80 {
            respond "Hello World!"
        }
        """
    ).lstrip()
]
