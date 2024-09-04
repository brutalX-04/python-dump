# Installation and running in ubuntu server
Install MongoDB Community Edition,
<a href="https://www.mongodb.com/docs/v7.0/tutorial/install-mongodb-on-ubuntu/">Read documentations</a>

If installation succes, Create service for auto run app after vps rebooted
```bash
sudo nano /etc/systemd/system/mongodb.service
```
Then add this into the file.
```bash
[Unit]
Description=MongoDB Database Server
After=network.target

[Service]
User=mongodb
Group=mongodb
ExecStart=/usr/bin/mongod --config /etc/mongod.conf
PIDFile=/var/run/mongodb/mongod.pid
TimeoutStartSec=0
Restart=always

[Install]
WantedBy=multi-user.target
```
Reload systemd
```bash
sudo systemctl daemon-reload
sudo systemctl enable mongodb
sudo systemctl start mongodb
```
Check mongod service status
```bash
sudo systemctl status mongodb
```

Install python-pip & python-virtualenv
```bash
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-venv
```
Go to apiFlask path
```bash
cd apiFlask
```
Create & activate python virtual enviroment
```bash
python3 -m venv venv
source venv/bin/activate
```
Install requirements
```bash
pip install -r requirements.txt
```
Install gunicorn
```bash
pip install gunicorn
```
Test run gunicorn
```bash
gunicorn -b 0.0.0.0:8000 app:app
```
if no errors ( ctrl + c ) to stop gunicorn

Create service for auto run app after vps rebooted
```bash
sudo nano /etc/systemd/system/apiFlask.service
```
Then add this into the file.
```bash
[Unit]
Description=Gunicorn instance for a run apiFlask app
After=network.target
[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/apiFlask
ExecStart=/home/ubuntu/apiFlask/venv/bin/gunicorn -b localhost:8000 app:app
Restart=always
[Install]
WantedBy=multi-user.target
```
note: if server root change /home to /root

Then enable the service:
```bash
sudo systemctl daemon-reload
sudo systemctl start apiFlask
sudo systemctl enable apiFlask
```
Check if the app is running with 
```bash
curl localhost:8000
```
Run Nginx Webserver to accept and route request to Gunicorn
Finally, we set up Nginx as a reverse-proxy to accept the requests from the user and route it to gunicorn.

Install Nginx 
```bash
sudo apt install nginx
```
Start the Nginx service and go to the Public IP address on the browser to see the default nginx landing page
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```
Edit the default file in the sites-available folder.
```bash
sudo nano /etc/nginx/sites-available/default
```
Add the following code at the top of the file (below the default comments)
```bash
upstream apiFlask {
    server 127.0.0.1:8000;
}
```
Add a proxy_pass to flaskhelloworld atlocation /
```bash
location / {
    proxy_pass http://apiFlask;
}
```
Restart Nginx 
```bash
sudo systemctl restart nginx
```

Finished, please repoot to author if errors code
