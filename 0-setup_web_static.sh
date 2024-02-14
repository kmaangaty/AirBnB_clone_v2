#!/usr/bin/env bash
# Install Nginx if not already installed
if ! command -v nginx &> /dev/null
then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create or update symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ folder to the ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
nginx_config="server {
    listen 80;
    server_name _;

    location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.html;
    }

    location / {
        add_header X-Served-By \$hostname;
        proxy_set_header Host \$host;
        proxy_pass http://localhost:5000;
    }

    error_page 404 /404.html;
    location /404 {
        internal;
        root /usr/share/nginx/html;
    }

    error_page 500 502 503 504 /50x.html;
    location /50x {
        internal;
        root /usr/share/nginx/html;
    }
}
"

# Backup the original default configuration
sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak

# Apply the new configuration
echo "$nginx_config" | sudo tee /etc/nginx/sites-available/default > /dev/null

# Restart Nginx
sudo service nginx restart

exit 0
