.PHONY: help
help: ## Show this help menu
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build: ## Build the container for startup
	docker compose build

.PHONY: up
up: ## Start pontedera server
	docker compose up

.PHONY: stop
stop: ## Stop pontedera server
	docker compose up

.PHONY: pip
pip: ## Runs pip install on requirements on container
	docker exec -it pontedera pip install --no-cache-dir -r requirements.txt

.PHONY: shell
shell: ## Opens a shell on pontedera server
	docker exec -it pontedera /bin/bash

.PHONY: redis-cli
redis-cli: ## Opens a shell on redis
	docker exec -it pontedera-redis /usr/local/bin/redis-cli
