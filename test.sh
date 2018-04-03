#!/bin/sh
docker-compose -f docker-compose.test.yml up --abort-on-container-exit | grep FAIL; test $? -eq 1
