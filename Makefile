# Makefile

# Define variable for docker-compose command to reuse
DC = docker compose

# .PHONY is used to specify that "start" and "stop" are not files.
.PHONY: start stop build

# Recipe to start the service
start:
	@echo "Starting service..."
	$(DC) up -d
	@echo "Service started."

# Recipe to stop the service
build:
	@echo "Starting service..."
	$(DC) up -d --build
	@echo "Service started."

stop:
	@echo "Stopping service..."
	$(DC) down
	@echo "Service stopped."

.DEFAULT_GOAL=help
.PHONY: help
help:
	@echo "make start -> to start telemetry"
	@echo "make stop ->  to stop telemetry"
