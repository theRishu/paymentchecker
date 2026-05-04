# VPS Deployment Guide for Payment Checker

Follow these steps to deploy your payment checker on a Linux VPS (Ubuntu/Debian recommended).

## 1. System Preparation
Update your system and install necessary dependencies:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib screen lsof
```

## 2. Database Setup
Create the PostgreSQL database and user:
```bash
sudo -u postgres psql
```
Inside the psql prompt:
```sql
CREATE DATABASE payment;
CREATE USER postgres WITH PASSWORD '1234';
GRANT ALL PRIVILEGES ON DATABASE payment TO postgres;
\q
```
*Note: If you already have PostgreSQL running with a different password, update your `.env` file accordingly.*

## 3. Project Setup
Clone your project to the VPS and navigate to the directory:
```bash
git clone <your-repo-url>
cd paymentchecker
```

## 4. Environment Configuration
Create a virtual environment and install requirements:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set up your configuration by editing `config.py` directly:
```bash
nano config.py
```
Update the values in `config.py` with your production tokens and URLs.

## 5. Running the Service
You can use the provided `run.sh` script, but for a VPS, it's better to run it inside a `screen` session so it keeps running after you disconnect.

### Using Screen:
1. Start a new screen session:
   ```bash
   screen -S payment
   ```
2. Run the script:
   ```bash
   bash run.sh
   ```
3. Detach from screen: Press `Ctrl + A`, then `D`.
4. To resume later: `screen -r payment`.

### Better Alternative (using PM2):
If you have Node.js installed, `pm2` is excellent for Python too:
```bash
sudo npm install -g pm2
pm2 start main.py --name payment-checker --interpreter ./venv/bin/python3
pm2 save
pm2 startup
```

## 6. Accessing the Dashboard
The dashboard runs on port `8087`. Make sure your VPS firewall allows traffic on this port:
```bash
sudo ufw allow 8087
```
You can then access it at `http://your-vps-ip:8087`.
