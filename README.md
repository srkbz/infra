# Infra

```
apt-get update
apt-get install -y git curl
git clone https://github.com/srkbz/infra.git
cd infra
./main.py
```

## Configure ssh

### Add login with authorized keys
```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
touch ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
vim ~/.ssh/authorized_keys
```

### Disable password authentication
```bash
printf "%s\n" "PasswordAuthentication no" "AllowUsers $USER" > /etc/ssh/sshd_config.d/srkbz.conf
systemctl restart sshd
```
