# Contains segment of wsinstall for cron and rc.local
sudo sed -i '/exit 0/d' /etc/rc.local
echo 'echo "Starting Weather Station daemon..."' | sudo tee -a /etc/rc.local
echo '/home/pi/live/bin/start_daemon' | sudo tee -a /etc/rc.local
echo 'echo "Starting Weather Station webserver..."' | sudo tee -a /etc/rc.local
echo '/home/pi/live/bin/start_webserver' | sudo tee -a /etc/rc.local
echo 'exit 0' | sudo tee -a /etc/rc.local

## Alter crontab for periodic uploads
crontab < crontab.save

echo "All done"