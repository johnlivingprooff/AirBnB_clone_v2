#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static

# update OS
sudo apt update -y

# install nginx
if ! [ -x "$(command -v nginx)" ]; then
    sudo apt install nginx -y
fi

# creating directories
directories="/data/web_static/releases/test/"
if [ ! -d "$directories" ]; then
    sudo mkdir -p "$directories"
fi

dir_shared="/data/web_static/shared/"
if [ ! -d "$dir_shared" ]; then
    sudo mkdir -p "$dir_shared"
fi


# creating HTML file
sudo touch /data/web_static/releases/test/index.html
html="<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>"
echo "$html" | sudo tee /data/web_static/releases/test/index.html

# creating sybolic link
cd /
link="/data/web_static/current"
if [ -L "$link" ]; then
    sudo rm "$link"
fi
sudo ln -s "$directories" "$link"

# ownership
sudo chown -R ubuntu:ubuntu /data

# configure nginx
cfg_file="/etc/nginx/sites-available/default"

# set the hbnb_static lodation
sudo sed -i '53i \\tlocation \/hbnb_static {\n\t\t alias /data/web_static/current;\n\t}' "$cfg_file"

# restart nginx
sudo service nginx restart
