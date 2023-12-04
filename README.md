# OpanonBot

For receiving anonymous messages in Telegram.

English: https://t.me/OpanonBot
Farsi: https://t.me/NashenasBot

## Development

### Running Locally

You will just need to set the env variables in `src/.env.local` (need to create the file) and run `make local`,
then set your test bot's webhook accordingly.
Checkout [docs/env_vars.md](env_vars page) for more info.

When you stop, you need to run `make stoplocal` so serveo will actually stop in the background.

If you face any problems, please let me know so I add more information or make a demo video.

### Make commands

- `make local`: runs in local mode (with local dynamodb).
- `make stoplocal`: the local run can't clean up fully after itself. This will do it.
- `make shell`: gives a shell in the local app (local dynamo).
- `make test`: runs the tests (with a local dynamodb instance).
