#!/usr/bin/env bash

until python3.9 check_connection.py; do
    echo "pg lezhit";
    sleep 1;
done
echo "pg gotov";


flask run --host=0.0.0.0
