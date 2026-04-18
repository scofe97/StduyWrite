# Docker PoC Practice Makefile
# 각 챕터별 실습 명령어 모음

.PHONY: help build run clean

# 기본 help 타겟
help: ## Show this help message
	@echo "Docker PoC Practice Commands"
	@echo "============================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# =============================================================================
# Ch02, Ch05: Docker CLI 기초
# =============================================================================

cli-basics: ## [Ch02,05] Basic container operations
	@echo "Starting nginx container..."
	docker run --name test-nginx -d -p 8080:80 nginx:alpine
	@echo "✓ Container started"
	@echo "Visit http://localhost:8080"
	@echo "Run 'make cli-cleanup' to stop"

cli-inspect: ## [Ch02] Inspect container
	docker inspect test-nginx
	docker logs test-nginx

cli-exec: ## [Ch02] Execute command in container
	docker exec test-nginx ls -la /usr/share/nginx/html

cli-cleanup: ## [Ch02,05] Clean up CLI containers
	@echo "Cleaning up test containers..."
	docker rm -f test-nginx 2>/dev/null || true
	@echo "✓ Cleanup complete"

# =============================================================================
# Ch06: Dockerfile 빌드
# =============================================================================

build-basic: ## [Ch06] Build basic Node.js image
	@echo "Building basic image..."
	docker build -t docker-poc:basic practice/dockerfile/basic/
	@echo "✓ Build complete"
	docker images | grep docker-poc

build-multistage: ## [Ch06] Build multistage Go image
	@echo "Building multistage image..."
	docker build -t docker-poc:multi practice/dockerfile/multistage/
	@echo "✓ Build complete"
	docker images | grep docker-poc

build-optimization: ## [Ch06] Build optimization comparison
	@echo "Building BAD example (uncached)..."
	time docker build -t docker-poc:bad -f practice/dockerfile/optimization/Dockerfile.bad practice/dockerfile/optimization/
	@echo "\nBuilding GOOD example (cached)..."
	time docker build -t docker-poc:good -f practice/dockerfile/optimization/Dockerfile.good practice/dockerfile/optimization/
	@echo "\nCompare image sizes:"
	docker images | grep docker-poc

run-basic: ## [Ch06] Run basic image
	docker run --name basic-app -d -p 3000:3000 docker-poc:basic
	@echo "Visit http://localhost:3000"
	@echo "Run 'docker rm -f basic-app' to stop"

run-multistage: ## [Ch06] Run multistage image
	docker run --name multi-app -d -p 8080:8080 docker-poc:multi
	@echo "Visit http://localhost:8080/health"
	@echo "Run 'docker rm -f multi-app' to stop"

# =============================================================================
# Ch07: Docker Compose
# =============================================================================

compose-up: ## [Ch07] Start basic compose stack
	@echo "Starting basic compose stack..."
	docker compose -f practice/compose/basic/docker-compose.yml up -d
	@echo "✓ Stack started"
	docker compose -f practice/compose/basic/docker-compose.yml ps

compose-logs: ## [Ch07] View compose logs
	docker compose -f practice/compose/basic/docker-compose.yml logs -f

compose-down: ## [Ch07] Stop basic compose stack
	@echo "Stopping basic compose stack..."
	docker compose -f practice/compose/basic/docker-compose.yml down
	@echo "✓ Stack stopped"

compose-fullstack-up: ## [Ch07] Start fullstack compose
	@echo "Starting fullstack compose..."
	docker compose -f practice/compose/fullstack/docker-compose.yml up -d
	@echo "✓ Stack started"
	docker compose -f practice/compose/fullstack/docker-compose.yml ps

compose-fullstack-down: ## [Ch07] Stop fullstack compose
	docker compose -f practice/compose/fullstack/docker-compose.yml down

compose-profiles-dev: ## [Ch07] Start with dev profile
	docker compose -f practice/compose/profiles/docker-compose.yml --profile dev up -d
	docker compose -f practice/compose/profiles/docker-compose.yml ps

compose-profiles-debug: ## [Ch07] Start with debug profile
	docker compose -f practice/compose/profiles/docker-compose.yml --profile debug up -d
	docker compose -f practice/compose/profiles/docker-compose.yml ps

compose-profiles-down: ## [Ch07] Stop profiles compose
	docker compose -f practice/compose/profiles/docker-compose.yml down

# =============================================================================
# Ch08: Networking
# =============================================================================

net-demo: ## [Ch08] Network demo
	@echo "Running network demo..."
	@bash practice/networking/network-demo.sh

# =============================================================================
# Ch09: Volumes
# =============================================================================

vol-demo: ## [Ch09] Volume demo
	@echo "Running volume demo..."
	@bash practice/volumes/volume-demo.sh

# =============================================================================
# Ch10: Security
# =============================================================================

sec-scan: ## [Ch10] Security scan demo
	@echo "Running security scan..."
	docker scout quickview nginx:alpine
	@echo "\nFor detailed scan, run: make sec-scan-full"

sec-scan-full: ## [Ch10] Full security scan
	@bash practice/security/scan-demo.sh

# =============================================================================
# Sample Apps
# =============================================================================

build-go-api: ## Build go-api sample
	docker build -t sample-go-api:latest practice/sample-apps/go-api/
	docker images | grep sample-go-api

run-go-api: ## Run go-api sample
	docker run --name go-api -d -p 8080:8080 sample-go-api:latest
	@echo "API running at http://localhost:8080"
	@echo "Endpoints: /health, /hello"
	@echo "Stop with: docker rm -f go-api"

build-nginx-static: ## Build nginx-static sample
	docker build -t sample-nginx:latest practice/sample-apps/nginx-static/
	docker images | grep sample-nginx

run-nginx-static: ## Run nginx-static sample
	docker run --name nginx-static -d -p 8081:80 sample-nginx:latest
	@echo "Static site at http://localhost:8081"
	@echo "Stop with: docker rm -f nginx-static"

# =============================================================================
# Cleanup
# =============================================================================

clean-containers: ## Remove all practice containers
	@echo "Removing practice containers..."
	docker rm -f test-nginx basic-app multi-app go-api nginx-static 2>/dev/null || true
	docker compose -f practice/compose/basic/docker-compose.yml down 2>/dev/null || true
	docker compose -f practice/compose/fullstack/docker-compose.yml down 2>/dev/null || true
	docker compose -f practice/compose/profiles/docker-compose.yml down 2>/dev/null || true
	@echo "✓ Containers removed"

clean-images: ## Remove practice images
	@echo "Removing practice images..."
	docker rmi docker-poc:basic docker-poc:multi docker-poc:bad docker-poc:good 2>/dev/null || true
	docker rmi sample-go-api:latest sample-nginx:latest 2>/dev/null || true
	@echo "✓ Images removed"

clean-networks: ## Prune unused networks
	@echo "Pruning networks..."
	docker network prune -f
	@echo "✓ Networks pruned"

clean-volumes: ## Prune unused volumes
	@echo "Pruning volumes..."
	docker volume prune -f
	@echo "✓ Volumes pruned"

clean-all: ## Full cleanup (containers + images + networks + volumes)
	@echo "Full cleanup starting..."
	@make clean-containers
	@make clean-images
	@make clean-networks
	@make clean-volumes
	@echo "✓ Full cleanup complete"

# =============================================================================
# Utilities
# =============================================================================

ps: ## Show running containers
	docker ps

ps-all: ## Show all containers
	docker ps -a

images: ## Show images
	docker images

stats: ## Show container stats
	docker stats --no-stream

system-info: ## Show system info
	docker system df
	@echo ""
	docker system info | grep -E "Images|Containers|Running|Paused|Stopped"
