IMAGES := base hadoop spark consumer-hadoop

# All
all: build up

# Build all service images
build:
	docker build -t base ./base
	docker build -t hadoop ./hadoop
	docker build -t spark ./spark
	docker build -t consumer-hadoop ./consumer

# Start all services
up:
	docker-compose up -d

# Stop and remove all services
down:
	docker-compose down

# Refresh Project
re: down all

.PHONY: build up down re