# Infra

```bash
apt-get update
apt-get install -y git curl
git clone https://github.com/srkbz/infra.git
cd infra
./ebrow
```

## Configure ssh

```bash
echo "PasswordAuthentication no" > /etc/ssh/sshd_config.d/srkbz.conf
echo "AllowUsers $USER" >> /etc/ssh/sshd_config.d/srkbz.conf
echo "DenyUsers *" >> /etc/ssh/sshd_config.d/srkbz.conf
systemctl restart sshd
```
