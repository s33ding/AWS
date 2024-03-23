#!/bin/bash

# Prompt the user to enter the database name
read -p "Enter the database name: " database_name

# Prompt the user to enter the table name
read -p "Enter the table name: " table_name

# Use the AWS CLI to retrieve the schema of the specified table
aws glue get-table --database-name "$database_name" --name "$table_name"

