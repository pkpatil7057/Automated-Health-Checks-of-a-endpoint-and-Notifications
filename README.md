# Automated Health Checks and Notifications

This project contains a Python script for monitoring an application's health. It regularly pings an endpoint and sends notifications if the endpoint is down.

## Features

- Checks an endpoint's health at specified intervals
- Sends notifications via email and/or Slack if the endpoint is unreachable
- Automated setup with cron job for regular execution

## Configuration

Update the `config.json` file with the endpoint URL, notification settings, and interval between checks.

## Setup Instructions

1. **Install Required Packages**:
   ```bash
   pip install requests

