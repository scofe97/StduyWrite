#!/bin/bash
# Kubernetes PoC - Minikube Cluster Setup Script

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 로깅 함수
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 전제 조건 확인
check_prerequisites() {
    log_info "Checking prerequisites..."

    local missing_tools=()

    if ! command -v docker &> /dev/null; then
        missing_tools+=("docker")
    fi

    if ! command -v minikube &> /dev/null; then
        missing_tools+=("minikube")
    fi

    if ! command -v kubectl &> /dev/null; then
        missing_tools+=("kubectl")
    fi

    if ! command -v helm &> /dev/null; then
        missing_tools+=("helm")
    fi

    if [ ${#missing_tools[@]} -ne 0 ]; then
        log_error "Missing required tools: ${missing_tools[*]}"
        log_error "Please install missing tools:"
        log_error "  - Docker: https://docs.docker.com/get-docker/"
        log_error "  - Minikube: https://minikube.sigs.k8s.io/docs/start/"
        log_error "  - kubectl: https://kubernetes.io/docs/tasks/tools/"
        log_error "  - Helm: https://helm.sh/docs/intro/install/"
        exit 1
    fi

    log_info "All prerequisites satisfied."
}

# Docker 실행 확인
check_docker() {
    log_info "Checking Docker status..."

    if ! docker ps &> /dev/null; then
        log_error "Docker is not running. Please start Docker Desktop."
        exit 1
    fi

    log_info "Docker is running."
}

# Minikube 설정값
MINIKUBE_CPUS=${MINIKUBE_CPUS:-4}
MINIKUBE_MEMORY=${MINIKUBE_MEMORY:-8192}
MINIKUBE_DRIVER=${MINIKUBE_DRIVER:-docker}
KUBERNETES_VERSION=${KUBERNETES_VERSION:-v1.28.0}

# Minikube 시작
start_minikube() {
    log_info "Starting Minikube cluster..."
    log_info "Configuration:"
    log_info "  CPUs: ${MINIKUBE_CPUS}"
    log_info "  Memory: ${MINIKUBE_MEMORY}MB"
    log_info "  Driver: ${MINIKUBE_DRIVER}"
    log_info "  Kubernetes Version: ${KUBERNETES_VERSION}"

    # 기존 클러스터 확인
    if minikube status &> /dev/null; then
        log_warn "Minikube cluster already exists."
        read -p "Do you want to delete and recreate? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            log_info "Deleting existing cluster..."
            minikube delete
        else
            log_info "Using existing cluster."
            return 0
        fi
    fi

    # Minikube 시작
    minikube start \
        --cpus="${MINIKUBE_CPUS}" \
        --memory="${MINIKUBE_MEMORY}" \
        --driver="${MINIKUBE_DRIVER}" \
        --kubernetes-version="${KUBERNETES_VERSION}"

    log_info "Minikube cluster started successfully."
}

# Addons 활성화
enable_addons() {
    log_info "Enabling essential addons..."

    local addons=(
        "ingress"
        "metrics-server"
        "dashboard"
        "storage-provisioner"
    )

    for addon in "${addons[@]}"; do
        log_info "Enabling addon: ${addon}"
        minikube addons enable "${addon}"
    done

    log_info "All addons enabled."
}

# 클러스터 정보 출력
print_cluster_info() {
    log_info "Cluster Information:"
    echo ""

    # Cluster info
    kubectl cluster-info
    echo ""

    # Node info
    log_info "Node Status:"
    kubectl get nodes -o wide
    echo ""

    # Addon status
    log_info "Addon Status:"
    minikube addons list | grep enabled
    echo ""

    # Context
    log_info "Current Context:"
    kubectl config current-context
    echo ""

    # Minikube IP
    log_info "Minikube IP:"
    minikube ip
    echo ""

    # Dashboard URL
    log_info "Dashboard URL:"
    echo "  Run: minikube dashboard"
    echo ""

    # Useful commands
    log_info "Useful Commands:"
    echo "  Check status:     minikube status"
    echo "  Stop cluster:     minikube stop"
    echo "  Delete cluster:   minikube delete"
    echo "  SSH to node:      minikube ssh"
    echo "  View dashboard:   minikube dashboard"
    echo ""
}

# 메인 실행
main() {
    log_info "===== Minikube Cluster Setup ====="
    echo ""

    check_prerequisites
    check_docker
    start_minikube
    enable_addons

    echo ""
    log_info "===== Setup Complete ====="
    echo ""

    print_cluster_info

    log_info "Cluster is ready for use!"
}

main "$@"
