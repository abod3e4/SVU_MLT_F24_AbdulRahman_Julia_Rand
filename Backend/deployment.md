# Deployment Guide for Linux Server

## 1. Server Requirements

Install required system packages:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv  git
```

## 2. Project Setup

1. Clone your repository:

```bash
git clone <your-repository-url>
cd <project-directory>
```

2. Create and activate virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install project dependencies:

```bash
pip install fastapi uvicorn pandas numpy matplotlib seaborn scikit-learn
```

## 3. Nginx Configuration

1. Create Nginx configuration file:

```bash
sudo nano /etc/nginx/sites-available/mlt
```

2. Add the following configuration:

```nginx
server {
    listen 80;
    server_name your_domain.com;  # Replace with your domain

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

3. Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/loan-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 4. Running the Application

1. Create a systemd service file:

```bash
sudo nano /etc/systemd/system/loan-api.service
```

2. Add the following content:

```ini
[Unit]
Description=Loan Approval API
After=network.target

[Service]
User=your_username
WorkingDirectory=/path/to/your/project
Environment="PATH=/path/to/your/project/venv/bin"
ExecStart=/path/to/your/project/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

3. Start and enable the service:

```bash
sudo systemctl start loan-api
sudo systemctl enable loan-api
```

## 5. Monitoring and Logs

- Check application status:

```bash
sudo systemctl status loan-api
```

- View application logs:

```bash
sudo journalctl -u loan-api
```

- View Nginx logs:

```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## 6. Security Considerations

1. Set up SSL/TLS with Let's Encrypt:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain.com
```

2. Configure firewall:

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

## 7. Troubleshooting

1. If the application doesn't start:

- Check the service status: `sudo systemctl status loan-api`
- Check the logs: `sudo journalctl -u loan-api`

2. If Nginx doesn't work:

- Check Nginx status: `sudo systemctl status nginx`
- Check Nginx configuration: `sudo nginx -t`
- Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`
