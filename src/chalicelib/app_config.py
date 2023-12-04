import os

# AWS Region where everything is deployed. Make sure it matches the AWS config in deployment
THE_AWS_REGION = os.environ["THE_AWS_REGION"]

# Whether running in testing mode - just in case some functions need to behave differently
TESTING = os.environ.get("TESTING", False) in ["1", "True", "true"]

# The stage name (set in chalice config according to stage)
STAGE = os.environ["STAGE"]

# Stage's first letter + this number should be the API gateway stage
STAGE_VERSION: int = int(os.environ["STAGE_VERSION"])

# Different tables for different stages but not for different versions
DYNAMO_TABLES_PREFIX = f"OpanonBot_{STAGE}_"

# Admin auth token injected from env vars - not using AWS SSM because $$
ADMIN_AUTH_TOKEN = os.environ["ADMIN_AUTH_TOKEN"]

# Sentry DSN - This can be retrieved from Sentry again if needed
SENTRY_DSN = os.environ["SENTRY_DSN"]

# Dynamo host will be localhost:port when running in local
DYNAMODB_HOST = os.environ.get("DYNAMODB_HOST", "")
if DYNAMODB_HOST.strip() == "":
    DYNAMODB_HOST = None

# TG Bot Tokens
BOT_TOKEN_EN = os.environ["BOT_TOKEN_EN"]
BOT_TOKEN_FA = os.environ["BOT_TOKEN_FA"]

# Telegram ID of admin
ADMIN_TG_ID = os.environ["ADMIN_TG_ID"]
