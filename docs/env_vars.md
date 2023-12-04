# Env vars

Some env vars are defined in src/.chalice/config.json but those that are secrets, are put in src/.env.* for the
`scripts/inject_env_vars.py` script to put them in before deployment. The Makefile command should then revert the file.

Here are the secret names in those files if you want them to run the project locally:

- `ADMIN_AUTH_TOKEN`: An admin token for admin operations.
- `SENTRY_DSN`: The sentry DSN for this project. Not required for local.
- `DYNAMODB_HOST`: If using a local dynamodb instance (for testing), the address of that. If you're
using my Make recipes, use `http://localhost:7650`.
- `BOT_TOKEN`: The token for the bot the code should respond to. Set this to your own testing bot
and set your bot's webhook to `<YOUR_HOSTING_ADDRESS>/update/<TOKEN>`.
- `ADMIN_TG_ID`: The admin Telegram account id for admin messages and operations.
- `SERVEO_SUBDOMAIN`: I use Serveo to run the bot locally. This variable allows setting a
fixed subdomain for Serveo so you won't have to change the bot's webhook everytime. If you use
my Make recipe for running locally and set this variable to `abc` then your bot's webhook should be
`abc.serveo.net/update/<TOKEN>`.
