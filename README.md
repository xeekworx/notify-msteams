# Send Microsoft Teams Connector Card

### Description

Sends a custom connector card to a Microsoft Teams channel using a webhook URL.

### Inputs

- `webhook-url` (required):
  - Description: Webhook URL of the Microsoft Teams channel.
- `message-title` (required):
  - Description: The title of the teams connector card.
- `message-body` (required):
  - Description: The body of the message to send.
- `card-color` (optional):
  - Description: The color of the card (hex) or named colors including GREEN, YELLOW, or RED.
  - Default: Not specified.
- `dry-run` (optional):
  - Description: Enable dry run mode. If set to 'true', the action will not send the payload.
  - Default: 'false'.

### Example Usage

```yaml
name: Send Teams Connector Card
on:
  push:
    branches:
      - main

jobs:
  send-connector-card:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout Code
      uses: actions/checkout@v4

    - name: Send Microsoft Teams Connector Card
      uses: xeekworx/notify-msteams@v1
      with:
        webhook-url: ${{ secrets.TEAMS_WEBHOOK_URL }}
        message-title: 'New Release'
        message-body: 'A new version of our software is now available!'
        card-color: 'GREEN'
        dry-run: 'false'