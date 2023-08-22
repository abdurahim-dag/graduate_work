#!/bin/bash

/bin/bash -c "/home/init.sh"
clickhouse-client --queries-file /home/table.sql
