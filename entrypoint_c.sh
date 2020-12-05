#!/usr/bin/env bash

until python3.9 check_connection.py; do
    echo "pg lezhit";
    sleep 1;
done
echo "pg gotov";


# flask db init

# flask db migrate

flask db upgrade

celery --app=app.celery worker -l info
