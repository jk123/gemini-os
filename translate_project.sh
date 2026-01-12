#!/bin/bash
# Rename directories and files to English
mv ~/gemini-api ~/gemini-core-api 2>/dev/null
mv ~/bin/pytxtar.py ~/bin/tx_engine.py 2>/dev/null

# Update Systemd service name and content
sudo systemctl stop gemini-api
sudo mv /etc/systemd/system/gemini-api.service /etc/systemd/system/gemini-core.service

sudo tee /etc/systemd/system/gemini-core.service << EOF > /dev/null
[Unit]
Description=Gemini OS Core API
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/gemini-core-api
Environment="PATH=/home/ubuntu/bin:/usr/bin:/bin"
Environment="GOOGLE_API_KEY=$GOOGLE_API_KEY"
ExecStart=/usr/bin/gunicorn --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable gemini-core
sudo systemctl start gemini-core

echo "Project translated to English and Core service restarted."
