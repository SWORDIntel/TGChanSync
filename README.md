Sync shit from 1 channel to your own,so you can hate on it..simples!


[Unit]
Description=Telegram Forwarder Script
After=network.target

[Service]
User=your_user_name
WorkingDirectory=/path/to/your/script
ExecStart=/usr/bin/python3 /vxpy.py
Restart=always

[Install]
WantedBy=multi-user.target
