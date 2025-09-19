#!/bin/bash
sleep 2
tc qdisc add dev eth0 root tbf rate 1mbit burst 32kbit latency 400ms || true

exec uvicorn user_microservice.main.web:app --host 0.0.0.0 --port 8000 --reload
