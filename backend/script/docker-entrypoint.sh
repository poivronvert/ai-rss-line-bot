#! /bin/ash

# create database
python /bin/init_db_script.py;

# alembic upgrade
python -m my_journalist.alembic upgrade head;

# initialize RSS data
python -c "from my_journalist.database.crud import init_rss; init_rss()";

# Add cron job to crontab

(crontab -l; echo "0 12 * * * python /bin/parse_rss_script.py >/proc/1/fd/1 2>&1"; echo "00 13 * * * python /bin/trigger_broadcast_script.py >/proc/1/fd/1 2>&1") | crontab -

# Start the cron service
crond -b;

# Start uvicorn
uvicorn "my_journalist.app:app" --host 0.0.0.0  --port 8000;