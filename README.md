Sync shit from 1 channel to your own,so you can hate on it..simples!


[Unit]
Description=Telegram Forwarder Script
After=network.target

[Service]
User=your_user_name
WorkingDirectory=/path/to/your/script
ExecStart=/usr/bin/python3 /boobies.py
Restart=always

[Install]
WantedBy=multi-user.target

## License

This project is licensed under the **SWORD Restricted Source Licence v1.1 (SRSL-1.1)**. Personal and non-commercial use is permitted under its terms; commercial exploitation requires a separate written agreement. See [LICENSE](LICENSE) and [migration notes](SRSL_MIGRATION.md). Previously distributed SRSL-1.0 copies retain their valid permissions.
