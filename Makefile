.PHONY: deploy
deploy:
	@if [ -e chalice_config.json.back ]; then \
        echo "Config backup present! Last deploy must've failed. Fix manually."; \
        exit 1; \
    fi
	@cp src/.chalice/config.json chalice_config.json.back
	@python src/scripts/inject_env_vars.py
# 	@./src/scripts/sync_deploy_files.sh download
# 	@[ -e "src/.chalice/deployed/prod.json" ] || { echo "Deploy file not found! Sync must have failed."; exit 1; }
	@cd src && chalice deploy --stage prod
	@./src/scripts/sync_deploy_files.sh upload
	@cp -f chalice_config.json.back src/.chalice/config.json && rm chalice_config.json.back

.PHONY: dynamodb_local
dynamodb_local:
	@docker container stop local-dynamo || true
	@docker run --rm --name local-dynamo -d -p 7650:8000 amazon/dynamodb-local
	@sleep 3

.PHONY: local
local: dynamodb_local
	@python src/scripts/manage.py local setup
	@python src/scripts/manage.py local run

.PHONY: logs
logs:
	@cd src && chalice logs

# The way we wrote the "local" recipe, it still runs in the background when you ctrl + c for some reason.
.PHONY: stoplocal
stoplocal:
	@kill $$(pgrep -f chalice) & docker container stop local-dynamo

.PHONY: shell
shell: dynamodb_local
	@python src/scripts/manage.py local shell

# If the first argument is "test", we might have arguments after
ifeq (test,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "test"
  TEST_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(TEST_ARGS):;@:)
endif

.PHONY: test
test: dynamodb_local
	@python src/scripts/manage.py local test $(TEST_ARGS)
	@docker container stop local-dynamo
