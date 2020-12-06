#!/usr/bin/env bash

until python3.9 check_connection.py; do
    echo "pg lezhit";
    sleep 1;
done
echo "pg gotov";


python3.9 nsq_dump_to_db.py
