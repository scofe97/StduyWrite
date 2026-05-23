# Kubernetes PoC - Practice Makefile
# Minikube / Kind 기반 실습 환경 관리

MINIKUBE_CPUS ?= 4
MINIKUBE_MEMORY ?= 8192
MINIKUBE_DRIVER ?= docker
CLUSTER_NAME ?= k8s-lab

.PHONY: help cluster-up cluster-down cluster-delete clean-all \
        kind-up kind-down istio-up istio-down harbor-up harbor-down

help:
	@echo "Kubernetes PoC Practice Commands"
	@echo ""
	@echo "Kind Cluster (1 control-plane + 3 workers):"
	@echo "  make kind-up          - Kind 클러스터 생성"
	@echo "  make kind-down        - Kind 클러스터 삭제"
	@echo "  make istio-up         - Istio 설치"
	@echo "  make istio-down       - Istio 제거"
	@echo "  make harbor-up        - Harbor 설치"
	@echo "  make harbor-down      - Harbor 제거"
	@echo ""
	@echo "Minikube Cluster:"
	@echo "  make cluster-up       - Start minikube cluster"
	@echo "  make cluster-down     - Stop minikube cluster"
	@echo "  make cluster-delete   - Delete minikube cluster"
	@echo ""
	@echo "Chapter Commands (format: <chapter>-up/down):"
	@echo "  make core-up          - Ch02: Core Workloads"
	@echo "  make storage-up       - Ch03: Storage"
	@echo "  make network-up       - Ch04: Networking"
	@echo "  make helm-up          - Ch05: Helm Charts"
	@echo "  make mysql-up         - Ch08: MySQL Operator"
	@echo "  make pg-up            - Ch09: PostgreSQL"
	@echo "  make redis-up         - Ch10: Redis Cluster"
	@echo "  make kafka-up         - Ch11: Kafka"
	@echo "  make jenkins-up       - Ch12: Jenkins"
	@echo "  make sonarqube-up     - Ch13: SonarQube"
	@echo "  make argocd-up        - Ch14: ArgoCD"
	@echo "  make monitoring-up    - Ch15: Monitoring"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean-all        - Delete all chapter namespaces"
	@echo ""
	@echo "Kind 워크플로우: kind-up → istio-up → harbor-up"

# =============================================================================
# Cluster Management
# =============================================================================

cluster-up:
	@echo "Starting minikube cluster..."
	bash cluster/minikube-start.sh

cluster-down:
	@echo "Stopping minikube cluster..."
	minikube stop

cluster-delete:
	@echo "Deleting minikube cluster..."
	minikube delete

# =============================================================================
# Kind Cluster (1 control-plane + 3 workers)
# =============================================================================

kind-up:
	@echo ">>> [kind] 클러스터 생성 (1 control-plane + 3 workers, name=$(CLUSTER_NAME))"
	kind create cluster --config cluster/kind-config.yaml
	@echo ">>> [kind] 클러스터 준비 완료"
	kubectl cluster-info --context kind-$(CLUSTER_NAME)
	kubectl get nodes

kind-down:
	@echo ">>> [kind] 클러스터 삭제 (name=$(CLUSTER_NAME))"
	kind delete cluster --name $(CLUSTER_NAME)

# =============================================================================
# Istio (Kind 클러스터용)
# =============================================================================

istio-up:
	@echo ">>> [istio] Helm 리포지토리 추가"
	helm repo add istio https://istio-release.storage.googleapis.com/charts 2>/dev/null || true
	helm repo update istio
	@echo ">>> [istio] istio-system 네임스페이스 생성"
	kubectl create namespace istio-system 2>/dev/null || true
	@echo ">>> [istio] base CRD 설치"
	helm install istio-base istio/base -n istio-system --wait
	@echo ">>> [istio] istiod 설치"
	helm install istiod istio/istiod -n istio-system \
	  -f istio/values.yaml --wait
	@echo ">>> [istio] Ingress Gateway 설치"
	helm install istio-ingressgateway istio/gateway -n istio-system --wait
	@echo ">>> [istio] default 네임스페이스 sidecar 자동 주입 활성화"
	kubectl label namespace default istio-injection=enabled --overwrite
	@echo ">>> [istio] 설치 완료"
	kubectl get pods -n istio-system

istio-down:
	@echo ">>> [istio] 제거"
	helm uninstall istio-ingressgateway -n istio-system 2>/dev/null || true
	helm uninstall istiod -n istio-system 2>/dev/null || true
	helm uninstall istio-base -n istio-system 2>/dev/null || true
	kubectl delete namespace istio-system --ignore-not-found

# =============================================================================
# Harbor (Kind 클러스터용)
# =============================================================================

harbor-up:
	@echo ">>> [harbor] Helm 리포지토리 추가"
	helm repo add harbor https://helm.goharbor.io 2>/dev/null || true
	helm repo update harbor
	@echo ">>> [harbor] Harbor 설치 (NodePort: 30000)"
	helm install harbor harbor/harbor \
	  -n harbor --create-namespace \
	  -f harbor/values.yaml --wait --timeout 10m
	@echo ">>> [harbor] 설치 완료"
	@echo "    UI: http://localhost:30000"
	@echo "    Credentials: admin / Harbor12345"
	kubectl get pods -n harbor

harbor-down:
	@echo ">>> [harbor] 제거"
	helm uninstall harbor -n harbor 2>/dev/null || true
	kubectl delete namespace harbor --ignore-not-found

# =============================================================================
# Ch02: Core Workloads (Pod, Deployment, Service)
# =============================================================================

core-up:
	@echo "Setting up Ch02: Core Workloads..."
	kubectl create ns ch02-core --dry-run=client -o yaml | kubectl apply -f -
	@echo "Namespace 'ch02-core' created. Deploy resources manually."

core-down:
	@echo "Cleaning up Ch02: Core Workloads..."
	kubectl delete ns ch02-core --ignore-not-found

# =============================================================================
# Ch03: Storage (PV, PVC, StatefulSet)
# =============================================================================

storage-up:
	@echo "Setting up Ch03: Storage..."
	kubectl create ns ch03-storage --dry-run=client -o yaml | kubectl apply -f -
	@echo "Namespace 'ch03-storage' created. Deploy storage resources manually."

storage-down:
	@echo "Cleaning up Ch03: Storage..."
	kubectl delete ns ch03-storage --ignore-not-found

# =============================================================================
# Ch04: Networking (Ingress, NetworkPolicy)
# =============================================================================

network-up:
	@echo "Setting up Ch04: Networking..."
	kubectl create ns ch04-network --dry-run=client -o yaml | kubectl apply -f -
	@echo "Namespace 'ch04-network' created. Deploy network resources manually."
	@echo "Note: Ensure 'ingress' addon is enabled (minikube addons enable ingress)"

network-down:
	@echo "Cleaning up Ch04: Networking..."
	kubectl delete ns ch04-network --ignore-not-found

# =============================================================================
# Ch05: Helm Charts
# =============================================================================

helm-up:
	@echo "Setting up Ch05: Helm Charts..."
	kubectl create ns ch05-helm --dry-run=client -o yaml | kubectl apply -f -
	@echo "Installing sample-app Helm chart..."
	helm upgrade --install sample-app helm-charts/sample-app \
		-n ch05-helm \
		--create-namespace
	@echo "Helm chart deployed. Check with: helm list -n ch05-helm"

helm-down:
	@echo "Cleaning up Ch05: Helm Charts..."
	helm uninstall sample-app -n ch05-helm --ignore-not-found
	kubectl delete ns ch05-helm --ignore-not-found

# =============================================================================
# Ch08: MySQL Operator (InnoDB Cluster)
# =============================================================================

mysql-up:
	@echo "Setting up Ch08: MySQL Operator..."
	kubectl create ns ch08-mysql --dry-run=client -o yaml | kubectl apply -f -
	@echo "Adding MySQL Operator Helm repository..."
	helm repo add mysql-operator https://mysql.github.io/mysql-operator/ || true
	helm repo update
	@echo "Installing MySQL Operator..."
	helm upgrade --install mysql-operator mysql-operator/mysql-operator \
		-n ch08-mysql \
		--create-namespace
	@echo "Waiting for operator to be ready..."
	kubectl wait --for=condition=available --timeout=120s \
		deployment/mysql-operator -n ch08-mysql || true
	@echo "Applying InnoDB Cluster CR..."
	kubectl apply -f operators/mysql/innodb-cluster.yaml -n ch08-mysql
	@echo "MySQL InnoDB Cluster deployed. Check status with:"
	@echo "  kubectl get innodbcluster -n ch08-mysql"

mysql-down:
	@echo "Cleaning up Ch08: MySQL Operator..."
	kubectl delete -f operators/mysql/innodb-cluster.yaml -n ch08-mysql --ignore-not-found
	helm uninstall mysql-operator -n ch08-mysql --ignore-not-found
	kubectl delete ns ch08-mysql --ignore-not-found

# =============================================================================
# Ch09: PostgreSQL (CloudNativePG)
# =============================================================================

pg-up:
	@echo "Setting up Ch09: PostgreSQL (CloudNativePG)..."
	kubectl create ns ch09-pg --dry-run=client -o yaml | kubectl apply -f -
	@echo "Adding CloudNativePG Helm repository..."
	helm repo add cnpg https://cloudnative-pg.github.io/charts || true
	helm repo update
	@echo "Installing CloudNativePG Operator..."
	helm upgrade --install cnpg cnpg/cloudnative-pg \
		-n ch09-pg \
		--create-namespace
	@echo "Waiting for operator to be ready..."
	kubectl wait --for=condition=available --timeout=120s \
		deployment/cnpg-cloudnative-pg -n ch09-pg || true
	@echo "Applying PostgreSQL Cluster CR..."
	kubectl apply -f operators/postgresql/pg-cluster.yaml -n ch09-pg
	@echo "PostgreSQL Cluster deployed. Check status with:"
	@echo "  kubectl get cluster -n ch09-pg"

pg-down:
	@echo "Cleaning up Ch09: PostgreSQL..."
	kubectl delete -f operators/postgresql/pg-cluster.yaml -n ch09-pg --ignore-not-found
	helm uninstall cnpg -n ch09-pg --ignore-not-found
	kubectl delete ns ch09-pg --ignore-not-found

# =============================================================================
# Ch10: Redis Cluster (OpsTree Redis Operator)
# =============================================================================

redis-up:
	@echo "Setting up Ch10: Redis Cluster..."
	kubectl create ns ch10-redis --dry-run=client -o yaml | kubectl apply -f -
	@echo "Adding OpsTree Redis Operator Helm repository..."
	helm repo add ot-helm https://ot-container-kit.github.io/helm-charts/ || true
	helm repo update
	@echo "Installing Redis Operator..."
	helm upgrade --install redis-operator ot-helm/redis-operator \
		-n ch10-redis \
		--create-namespace
	@echo "Waiting for operator to be ready..."
	kubectl wait --for=condition=available --timeout=120s \
		deployment/redis-operator -n ch10-redis || true
	@echo "Applying Redis Cluster CR..."
	kubectl apply -f operators/redis/redis-cluster.yaml -n ch10-redis
	@echo "Redis Cluster deployed. Check status with:"
	@echo "  kubectl get rediscluster -n ch10-redis"

redis-down:
	@echo "Cleaning up Ch10: Redis Cluster..."
	kubectl delete -f operators/redis/redis-cluster.yaml -n ch10-redis --ignore-not-found
	helm uninstall redis-operator -n ch10-redis --ignore-not-found
	kubectl delete ns ch10-redis --ignore-not-found

# =============================================================================
# Ch11: Kafka (Strimzi)
# =============================================================================

kafka-up:
	@echo "Setting up Ch11: Kafka (Strimzi)..."
	kubectl create ns ch11-kafka --dry-run=client -o yaml | kubectl apply -f -
	@echo "Adding Strimzi Helm repository..."
	helm repo add strimzi https://strimzi.io/charts/ || true
	helm repo update
	@echo "Installing Strimzi Operator..."
	helm upgrade --install strimzi-kafka-operator strimzi/strimzi-kafka-operator \
		-n ch11-kafka \
		--create-namespace
	@echo "Waiting for operator to be ready..."
	kubectl wait --for=condition=available --timeout=120s \
		deployment/strimzi-cluster-operator -n ch11-kafka || true
	@echo "Applying Kafka Cluster CR..."
	kubectl apply -f operators/kafka/kafka-cluster.yaml -n ch11-kafka
	@echo "Waiting for Kafka cluster to be ready..."
	sleep 10
	@echo "Applying Kafka Topic CR..."
	kubectl apply -f operators/kafka/kafka-topic.yaml -n ch11-kafka
	@echo "Kafka Cluster deployed. Check status with:"
	@echo "  kubectl get kafka -n ch11-kafka"
	@echo "  kubectl get kafkatopic -n ch11-kafka"

kafka-down:
	@echo "Cleaning up Ch11: Kafka..."
	kubectl delete -f operators/kafka/kafka-topic.yaml -n ch11-kafka --ignore-not-found
	kubectl delete -f operators/kafka/kafka-cluster.yaml -n ch11-kafka --ignore-not-found
	helm uninstall strimzi-kafka-operator -n ch11-kafka --ignore-not-found
	kubectl delete ns ch11-kafka --ignore-not-found

# =============================================================================
# Ch12: Jenkins
# =============================================================================

jenkins-up:
	@echo "Setting up Ch12: Jenkins..."
	kubectl create ns ch12-jenkins --dry-run=client -o yaml | kubectl apply -f -
	@echo "Adding Jenkins Helm repository..."
	helm repo add jenkins https://charts.jenkins.io || true
	helm repo update
	@echo "Installing Jenkins..."
	helm upgrade --install jenkins jenkins/jenkins \
		-n ch12-jenkins \
		--create-namespace \
		-f devtools/jenkins/values.yaml
	@echo "Jenkins deployed. Get admin password with:"
	@echo "  kubectl get secret jenkins -n ch12-jenkins -o jsonpath='{.data.jenkins-admin-password}' | base64 -d"
	@echo "Access Jenkins with port-forward:"
	@echo "  kubectl port-forward svc/jenkins 8080:8080 -n ch12-jenkins"

jenkins-down:
	@echo "Cleaning up Ch12: Jenkins..."
	helm uninstall jenkins -n ch12-jenkins --ignore-not-found
	kubectl delete ns ch12-jenkins --ignore-not-found

# =============================================================================
# Ch13: SonarQube
# =============================================================================

sonarqube-up:
	@echo "Setting up Ch13: SonarQube..."
	kubectl create ns ch13-sonarqube --dry-run=client -o yaml | kubectl apply -f -
	@echo "Adding SonarQube Helm repository..."
	helm repo add sonarqube https://SonarSource.github.io/helm-chart-sonarqube || true
	helm repo update
	@echo "Installing SonarQube..."
	helm upgrade --install sonarqube sonarqube/sonarqube \
		-n ch13-sonarqube \
		--create-namespace \
		-f devtools/sonarqube/values.yaml
	@echo "SonarQube deployed. Default credentials: admin/admin"
	@echo "Access SonarQube with port-forward:"
	@echo "  kubectl port-forward svc/sonarqube-sonarqube 9000:9000 -n ch13-sonarqube"

sonarqube-down:
	@echo "Cleaning up Ch13: SonarQube..."
	helm uninstall sonarqube -n ch13-sonarqube --ignore-not-found
	kubectl delete ns ch13-sonarqube --ignore-not-found

# =============================================================================
# Ch14: ArgoCD (GitOps)
# =============================================================================

argocd-up:
	@echo "Setting up Ch14: ArgoCD..."
	kubectl create ns ch14-argocd --dry-run=client -o yaml | kubectl apply -f -
	@echo "Adding ArgoCD Helm repository..."
	helm repo add argo https://argoproj.github.io/argo-helm || true
	helm repo update
	@echo "Installing ArgoCD..."
	helm upgrade --install argocd argo/argo-cd \
		-n ch14-argocd \
		--create-namespace \
		-f devtools/argocd/values.yaml
	@echo "ArgoCD deployed. Get admin password with:"
	@echo "  kubectl get secret argocd-initial-admin-secret -n ch14-argocd -o jsonpath='{.data.password}' | base64 -d"
	@echo "Access ArgoCD with port-forward:"
	@echo "  kubectl port-forward svc/argocd-server 8080:443 -n ch14-argocd"

argocd-down:
	@echo "Cleaning up Ch14: ArgoCD..."
	helm uninstall argocd -n ch14-argocd --ignore-not-found
	kubectl delete ns ch14-argocd --ignore-not-found

# =============================================================================
# Ch15: Monitoring (Prometheus + Grafana)
# =============================================================================

monitoring-up:
	@echo "Setting up Ch15: Monitoring..."
	kubectl create ns ch15-monitoring --dry-run=client -o yaml | kubectl apply -f -
	@echo "Adding Prometheus Community Helm repository..."
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts || true
	helm repo update
	@echo "Installing kube-prometheus-stack..."
	helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
		-n ch15-monitoring \
		--create-namespace \
		-f monitoring/values.yaml
	@echo "Monitoring stack deployed."
	@echo "Access Grafana with port-forward:"
	@echo "  kubectl port-forward svc/kube-prometheus-stack-grafana 3000:80 -n ch15-monitoring"
	@echo "Default Grafana credentials: admin/prom-operator"

monitoring-down:
	@echo "Cleaning up Ch15: Monitoring..."
	helm uninstall kube-prometheus-stack -n ch15-monitoring --ignore-not-found
	kubectl delete ns ch15-monitoring --ignore-not-found

# =============================================================================
# Cleanup
# =============================================================================

clean-all:
	@echo "Deleting all chapter namespaces..."
	kubectl delete ns ch02-core --ignore-not-found
	kubectl delete ns ch03-storage --ignore-not-found
	kubectl delete ns ch04-network --ignore-not-found
	kubectl delete ns ch05-helm --ignore-not-found
	kubectl delete ns ch06-hpa --ignore-not-found
	kubectl delete ns ch07-scheduling --ignore-not-found
	kubectl delete ns ch08-mysql --ignore-not-found
	kubectl delete ns ch09-pg --ignore-not-found
	kubectl delete ns ch10-redis --ignore-not-found
	kubectl delete ns ch11-kafka --ignore-not-found
	kubectl delete ns ch12-jenkins --ignore-not-found
	kubectl delete ns ch13-sonarqube --ignore-not-found
	kubectl delete ns ch14-argocd --ignore-not-found
	kubectl delete ns ch15-monitoring --ignore-not-found
	@echo "All namespaces deleted."
