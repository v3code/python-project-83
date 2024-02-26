#!/usr/bin/env bash
make install-prod && psql -a -d $DATABASE_URI -f database.sql