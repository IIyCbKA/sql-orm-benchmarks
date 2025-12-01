#!/bin/sh

gunzip -c /docker-entrypoint-initdb.d/demo-20250901-3m.sql.gz | psql -U postgres
