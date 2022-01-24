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
	docker compose stop

.PHONY: restart-flask
restart-flask: ## Restart pontedera server
	docker restart pontedera

.PHONY: pip
pip: ## Runs pip install on requirements on container
	docker exec -it pontedera pip install --no-cache-dir -r requirements.txt

.PHONY: shell
shell: ## Opens a shell on pontedera server
	docker exec -it pontedera /bin/bash

.PHONY: redis-cli
redis-cli: ## Opens a shell on redis
	docker exec -it pontedera-redis /usr/local/bin/redis-cli

.PHONY: generate-pwd-hash
generate-pwd-hash: ## Launch script to generate password hashes
	docker exec -it pontedera python3 src/utils/pwdhash.py

.PHONY: print-queued-jobs
print-queued-jobs: ## Launch script to print queued jobs
	docker exec -it pontedera python3 src/utils/printerScript.py

.PHONY: after-prod-build
after-prod-build: ## Permorm extra actions after production build
	docker exec -it pontedera ssh-keygen
	docker exec -it pontedera ssh-copy-id -i /root/.ssh/id_rsa.pub `cat .env | grep WORKER_USER | cut -d= -f2`@`cat .env | grep WORKER_IP | cut -d= -f2`
