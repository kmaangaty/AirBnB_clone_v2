#!/usr/bin/env bash
# This script sets up the web servers for the deployment of web_static.

# Update and upgrade package lists
sudo apt-get -y update
sudo apt-get -y upgrade

# Install Nginx
sudo apt-get -y install nginx

# Create necessary directory structure for web_static
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Generate a test HTML file in the test directory
echo "This is a test" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Set up a symbolic link to the test directory
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Change ownership of the /data/ directory to the ubuntu user and group
sudo chown -hR ubuntu:ubuntu /data/

# Modify Nginx configuration to serve content from /data/web_static/current/ when accessing /hbnb_static/
# Note: This assumes line 38 is the correct place to insert the new configuration.
# Consider checking the contents of the default configuration file to confirm.
sudo sed -i '38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

# Start the Nginx service
sudo service nginx start
