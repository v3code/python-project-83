#!/usr/bin/env bash
make install-prod && psql -a -d $DATABASE_URL -f database.sql