#!/bin/bash
sleep 2

tc qdisc add dev eth0 root handle 1: tbf rate 1mbit burst 32kbit latency 400ms || true

exec dotnet /app/publish/registration.dll