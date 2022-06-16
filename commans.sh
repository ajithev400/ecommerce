[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/project/ecommerce
ExecStart=/home/ubuntu/project/ecommerce/myenv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          ecommerce.wsgi:application

[Install]
WantedBy=multi-user.target