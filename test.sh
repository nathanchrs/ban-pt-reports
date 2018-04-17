#!/bin/sh
docker-compose -f docker-compose.test.yml up --abort-on-container-exit | grep -E "(ERROR|FAIL)"; test $? -eq 1
