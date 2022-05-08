#!/bin/bash
# Resets the local Django database, adding an admin login and migrations
set -e
echo -e "\n>>> Resetting the database"
sudo docker-compose -f /home/ubuntu/chat-server/docker-compose.prod.yml run chat-server ./manage.py reset_db --close-sessions --noinput
# Stop docker containers
echo -e "\nStopping all running Docker containers"
sudo docker-compose -f /home/ubuntu/chat-server/docker-compose.prod.yml down
# Start docker containers
echo -e "\nStarting Docker containers"
sudo docker-compose -f /home/ubuntu/chat-server/docker-compose.prod.yml up -d
# Making migrations
echo -e "\n>>> Running migrations"
sudo docker-compose -f /home/ubuntu/chat-server/docker-compose.prod.yml run chat-server ./manage.py migrate