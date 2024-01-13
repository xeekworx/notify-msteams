# Send Microsoft Teams Connector Card

[![Test Run for Action](https://github.com/xeekworx/notify-msteams/actions/workflows/test.yml/badge.svg)](https://github.com/xeekworx/notify-msteams/actions/workflows/test.yml)

### Description

Sends a custom connector card to a Microsoft Teams channel using a webhook URL.

### Inputs

- `webhook-url` (required):
  - Description: Webhook URL of the Microsoft Teams channel.
  - Documentation: [Create Incoming Webhooks](https://learn.microsoft.com/en-us/microsoftteams/platform/task-modules-and-cards/cards/cards-format?tabs=adaptive-md%2Cdesktop%2Cconnector-html#format-cards-with-markdown])
- `message-title` (required):
  - Description: The title of the teams connector card.
- `message-body` (required):
  - Description: The body of the message to send. Markdown is allowed.
  - Documentation: [Format cards in Microsoft Teams](https://learn.microsoft.com/en-us/microsoftteams/platform/task-modules-and-cards/cards/cards-format?tabs=adaptive-md%2Cdesktop%2Cconnector-html#format-cards-with-markdown)
- `card-color` (optional):
  - Description: The color of the card (hex, eg. #22c74e) or predefined colors including:
    - ![#22c74e](https://placehold.co/20/22c74e/22c74e) GREEN
    - ![#c73022](https://placehold.co/20/c73022/c73022) YELLOW
    - ![#c7bf22](https://placehold.co/20/c7bf22/c7bf22) RED
  - Default: Not specified.
- `buttons` (optional):
  - Description: Buttons to add to the card. Each button is a pair of text and link separated by a new line or semicolon (;).
  - Default: Not specified.
- `dry-run` (optional):
  - Description: Enable dry run mode. If set to 'true', the action will not send the payload.
  - Default: 'false'.
- `output-payload` (optional):
  - Description: Output the JSON payload being sent to the webhook.
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
        buttons: |
          Button One, http://example.com
          Button Two, http://example.com
        dry-run: 'false'
```