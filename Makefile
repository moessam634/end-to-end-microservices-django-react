.PHONY: help build up down logs shell backend-shell frontend-shell db-shell migrate makemigrations collectstatic test clean

help: ## Show this help message
	@echo "Gig Router Platform - Development Commands"
	@echo "=========================================="
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build all Docker images
	docker-compose build

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

logs: ## Show logs for all services
	docker-compose logs -f

backend-logs: ## Show backend logs
	docker-compose logs -f backend

frontend-logs: ## Show frontend logs
	docker-compose logs -f frontend

shell: ## Open shell in backend container
	docker-compose exec backend bash

backend-shell: ## Open shell in backend container
	docker-compose exec backend bash

frontend-shell: ## Open shell in frontend container
	docker-compose exec frontend sh

db-shell: ## Open shell in database
	docker-compose exec db psql -U postgres -d gig_router

migrate: ## Run Django migrations
	docker-compose exec backend python manage.py migrate

makemigrations: ## Create Django migrations
	docker-compose exec backend python manage.py makemigrations

collectstatic: ## Collect static files
	docker-compose exec backend python manage.py collectstatic --noinput

createsuperuser: ## Create Django superuser
	docker-compose exec backend python manage.py createsuperuser

test: ## Run Django tests
	docker-compose exec backend python manage.py test

clean: ## Clean up Docker containers and volumes
	docker-compose down -v
	docker system prune -f

restart: ## Restart all services
	docker-compose restart

status: ## Show status of all services
	docker-compose ps

# Development shortcuts
dev: build up ## Build and start development environment
	@echo "Development environment is starting..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo "Database: localhost:5432"
	@echo "Redis: localhost:6379"

quick-start: ## Quick start without building (use existing images)
	docker-compose up -d
	@echo "Services started!"
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"

zap-scan:
	docker run -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t http://localhost:8000