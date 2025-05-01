# Infra

```bash
apt-get update
apt-get install -y git curl
git clone https://github.com/srkbz/infra.git
cd infra
./ebrow
```

## Disable password login in ssh

```bash
echo "PasswordAuthentication no" > /etc/ssh/sshd_config.d/srkbz.conf
systemctl restart sshd
```

## Nuke user

```bash
passwd --delete $the_user
userdel --remove $the_user
```
