#!/bin/bash

# Define the absolute path to the Python script
SCRIPT_PATH="$(pwd)/health_check.py"

# Create a cron job that runs the script every 5 minutes
(crontab -l 2>/dev/null; echo "*/5 * * * * python3 $SCRIPT_PATH") | crontab -

echo "Cron job has been set up to run health_check.py every 5 minutes."

