#!/bin/bash

# Prompt the user to enter the database name
read -p "Enter the database name: " database_name

# Use the AWS CLI to list the tables in the specified database
aws glue get-tables --database-name "$database_name"
