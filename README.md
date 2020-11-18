# SocioMeet

## Deployment
> Open the lightsail ssh
```bash
sudo cd /opt/bitnami/projects/SocioMeet/
sudo git pull origin main

sudo python manage.py collectstatic
sudo /opt/bitnami/ctlscript.sh restart apache
```
