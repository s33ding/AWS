#!/bin/bash

# Change to the directory you want to use Git in
cd /path/to/directory

# Initialize a new Git repository
git init

# Add all files in the directory to the repository
git add .

# Commit the changes with a message
git commit -m "Initial commit"

# Add a remote repository to push changes to
git remote add origin <remote repository URL>

# Push the changes to the remote repository
git push -u origin master

