import argparse
import json
from operator import contains
import os
import pymsteams
import tools


ENV_NAME_WEBHOOK_URL = 'TEAMS_WEBHOOK_URL'
ENV_NAME_CARD_COLOR = 'TEAMS_CARD_COLOR'
ENV_NAME_MESSAGE_TITLE = 'TEAMS_CARD_MESSAGE_TITLE'
ENV_NAME_MESSAGE_BODY = 'TEAMS_CARD_MESSAGE_BODY'
ENV_NAME_DRY_RUN = 'TEAMS_NOTIFY_DRY_RUN'
ENV_NAME_OUTPUT_PAYLOAD = 'TEAMS_CARD_OUTPUT_PAYLOAD'
ENV_NAME_BUTTONS = 'TEAMS_CARD_BUTTONS'

DEFAULT_WEBHOOK_URL = os.getenv(ENV_NAME_WEBHOOK_URL)
DEFAULT_SELECTED_COLOR = os.getenv(ENV_NAME_CARD_COLOR)
DEFAULT_MESSAGE_TITLE = os.getenv(ENV_NAME_MESSAGE_TITLE)
DEFAULT_MESSAGE_BODY = os.getenv(ENV_NAME_MESSAGE_BODY)
DEFAULT_DRY_RUN = os.getenv(ENV_NAME_DRY_RUN, 'false').lower() == 'true'
DEFAULT_OUTPUT_PAYLOAD = os.getenv(ENV_NAME_OUTPUT_PAYLOAD, 'false').lower() == 'true'
DEFAULT_BUTTONS = os.getenv("TEAMS_CARD_BUTTONS")

NAMED_COLORS = {
    "GREEN": "#22c74e",
    "RED": "#c73022",
    "YELLOW": "#c7bf22"
}

# -----------------------------------------------------------------------------
# Setup Command-Line Arguments & Validate
# -----------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument(
    'title', help=f'The title of the connector card. Default from env: {ENV_NAME_MESSAGE_TITLE}', default=DEFAULT_MESSAGE_TITLE, nargs='?')
parser.add_argument(
    'text', help=f'The text below the title in the connector card. Default from env: {ENV_NAME_MESSAGE_BODY}', default=DEFAULT_MESSAGE_BODY, nargs='?')
parser.add_argument('-w', '--webhook-url',
                    help=f'The Microsoft Teams Webhook URL. If not specified, the environment variable {ENV_NAME_WEBHOOK_URL} is required.', default=DEFAULT_WEBHOOK_URL)
parser.add_argument('-d', '--dry-run', action='store_true',
                    default=DEFAULT_DRY_RUN, help='Do not send the payload')
parser.add_argument('--output-payload', action='store_true',
                    default=DEFAULT_OUTPUT_PAYLOAD, help='Output the payload sent with the webhook URL')
parser.add_argument('-c', '--color', type=str.upper, choices=list(NAMED_COLORS.keys()),
                    help=f'Optional color for the card. Default from env: {ENV_NAME_CARD_COLOR}', default=DEFAULT_SELECTED_COLOR)
parser.add_argument('-b', '--button', action='append', nargs=2,
                    metavar=('text', 'link'), help='Add a button to the card. Repeatable.')
args = parser.parse_args()

# Check if required webhook URL is provided either via command line or environment variable
if not args.webhook_url:
    parser.error(
        f"The --webhook-url argument or {ENV_NAME_WEBHOOK_URL} environment variable is required.")

if not tools.is_valid_url(args.webhook_url):
    parser.error(f"The webhook url is not a valid url:\n{args.webhook_url}")

# Get and validate the color selection.
args.color = NAMED_COLORS.get(args.color, args.color)
if args.color and not tools.is_hex(args.color):
    parser.error(
        f"The selected color '{args.color}' is invalid, use a hex value or one of {list(NAMED_COLORS.keys())}.")

# Get buttons from the environment variable:
if not args.button and DEFAULT_BUTTONS:
    detectedSeparator = '\n' if '\n' in DEFAULT_BUTTONS else ';'
    args.button = []
    for line in DEFAULT_BUTTONS.split(detectedSeparator):
        parts = line.strip().split(',')
        if len(parts) >= 2:
            button_text, button_link = parts
            args.button.append((button_text.strip(), button_link.strip()))
            
# Validate buttons:
if args.button:
    for button in args.button:
        if not tools.is_valid_url(button[1]):
            parser.error(
                f"The button link for '{button[0]}' is not valid:\n{button[1]}")

# -----------------------------------------------------------------------------
# Build The Microsoft Teams Connector Card
# -----------------------------------------------------------------------------

teamsCard = pymsteams.connectorcard(args.webhook_url)

if args.color:
    teamsCard.color(args.color)

teamsCard.title(args.title)
teamsCard.text(args.text)

if args.button:
    for button in args.button:
        teamsCard.addLinkButton(button[0], button[1])

# -----------------------------------------------------------------------------
# Send The Microsoft Teams Connector Card
# -----------------------------------------------------------------------------

if args.output_payload:
    print("Microsoft Teams connector card payload is:")
    print(json.dumps(teamsCard.payload, indent=2))

if args.dry_run:
    print("In dry-run mode. Not sent to teams.")
else:
    print("Microsoft Teams connector card sending...")
    try:
        teamsCard.send()
    except pymsteams.TeamsWebhookException as ex:
        print(
            f"Failed to send Microsoft Teams Connector Card with the error:\n{ex}")
        exit(2)

print("Finished.")
