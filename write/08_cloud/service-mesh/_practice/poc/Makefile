.PHONY: cluster-up cluster-down \
        mesh-linkerd mesh-istio mesh-istio-ambient \
        app-emojivoto app-bookinfo \
        linkerd-viz istio-kiali \
        clean help

# ─────────────────────────────────────────────
# Cluster
# ─────────────────────────────────────────────

cluster-up:
	@echo ">>> [cluster] Kind 클러스터 생성 (1 control-plane + 2 workers, name=mesh-lab)"
	@echo "    config: cluster/kind-config.yaml"
	kind create cluster --config cluster/kind-config.yaml
	@echo ">>> [cluster] 클러스터 준비 완료"
	kubectl cluster-info --context kind-mesh-lab

cluster-down:
	@echo ">>> [cluster] Kind 클러스터 삭제 (name=mesh-lab)"
	kind delete cluster --name mesh-lab

# ─────────────────────────────────────────────
# Service Mesh - Linkerd
# ─────────────────────────────────────────────

mesh-linkerd:
	@echo ">>> [linkerd] CRD 설치"
	linkerd install --crds | kubectl apply -f -
	@echo ">>> [linkerd] Control plane 설치"
	linkerd install | kubectl apply -f -
	@echo ">>> [linkerd] 설치 검증 (약 30-60초 소요)"
	linkerd check
	@echo ">>> [linkerd] 설치 완료. 다음 단계: make app-emojivoto"

# ─────────────────────────────────────────────
# Service Mesh - Istio (Sidecar Mode)
# ─────────────────────────────────────────────

mesh-istio:
	@echo ">>> [istio] Sidecar 모드 설치"
	@echo "    config: istio/install/sidecar/istio-values.yaml"
	helm repo add istio https://istio-release.storage.googleapis.com/charts 2>/dev/null || true
	helm repo update istio
	kubectl create namespace istio-system 2>/dev/null || true
	helm install istio-base istio/base -n istio-system --wait
	helm install istiod istio/istiod -n istio-system \
	  -f istio/install/sidecar/istio-values.yaml --wait
	@echo ">>> [istio] default 네임스페이스 sidecar 자동 주입 활성화"
	kubectl label namespace default istio-injection=enabled --overwrite
	@echo ">>> [istio] 설치 완료. 다음 단계: make app-bookinfo"

# ─────────────────────────────────────────────
# Service Mesh - Istio (Ambient Mode)
# ─────────────────────────────────────────────

mesh-istio-ambient:
	@echo ">>> [istio-ambient] Ambient 모드 설치 (sidecar 없음, ztunnel + waypoint)"
	@echo "    config: istio/install/ambient/ambient-values.yaml"
	helm repo add istio https://istio-release.storage.googleapis.com/charts 2>/dev/null || true
	helm repo update istio
	kubectl create namespace istio-system 2>/dev/null || true
	helm install istio-base istio/base -n istio-system --wait
	helm install istiod istio/istiod -n istio-system \
	  -f istio/install/ambient/ambient-values.yaml --wait
	@echo ">>> [istio-ambient] CNI 플러그인 설치"
	helm install istio-cni istio/cni -n istio-system --wait
	@echo ">>> [istio-ambient] ztunnel (per-node L4 proxy) 설치"
	helm install ztunnel istio/ztunnel -n istio-system --wait
	@echo ">>> [istio-ambient] 설치 완료"
	@echo "    네임스페이스를 ambient에 추가하려면:"
	@echo "    kubectl label namespace <ns> istio.io/dataplane-mode=ambient"

# ─────────────────────────────────────────────
# Sample Apps
# ─────────────────────────────────────────────

app-emojivoto:
	@echo ">>> [app] emojivoto 배포 (Linkerd 데모 앱)"
	@echo "    kustomize로 https://run.linkerd.io/emojivoto.yml 적용"
	kubectl apply -k apps/emojivoto/
	@echo ">>> [app] emojivoto 배포 완료"
	@echo "    접속: kubectl port-forward svc/web-svc -n emojivoto 8080:80"
	@echo "    URL:  http://localhost:8080"

app-bookinfo:
	@echo ">>> [app] bookinfo 네임스페이스 생성 (istio-injection=enabled)"
	kubectl apply -f apps/bookinfo/namespace.yaml
	@echo ">>> [app] bookinfo 앱 배포 (Istio 설치 디렉토리의 samples 사용)"
	@echo "    ISTIO_DIR 환경변수를 설정하거나 아래 경로를 직접 지정하세요"
	@if [ -n "$$ISTIO_DIR" ]; then \
	  kubectl apply -f $$ISTIO_DIR/samples/bookinfo/platform/kube/bookinfo.yaml -n bookinfo; \
	  kubectl apply -f $$ISTIO_DIR/samples/bookinfo/networking/bookinfo-gateway.yaml -n bookinfo; \
	else \
	  echo "    ISTIO_DIR 미설정. 수동 설치:"; \
	  echo "    export ISTIO_DIR=~/istio-<version>"; \
	  echo "    make app-bookinfo"; \
	  echo "    또는: apps/bookinfo/README.md 참조"; \
	fi

# ─────────────────────────────────────────────
# Observability
# ─────────────────────────────────────────────

linkerd-viz:
	@echo ">>> [linkerd-viz] Linkerd 대시보드 확장 설치"
	linkerd viz install | kubectl apply -f -
	linkerd viz check
	@echo ">>> [linkerd-viz] 대시보드 실행"
	@echo "    자동으로 브라우저가 열립니다 (Ctrl+C로 종료)"
	linkerd viz dashboard

istio-kiali:
	@echo ">>> [kiali] Kiali 대시보드 설치 (Prometheus, Jaeger 포함)"
	helm repo add kiali https://kiali.org/helm-charts 2>/dev/null || true
	helm repo update kiali
	kubectl create namespace istio-system 2>/dev/null || true
	@echo ">>> [kiali] Prometheus 설치"
	kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.23/samples/addons/prometheus.yaml
	@echo ">>> [kiali] Kiali 설치"
	helm install kiali-server kiali/kiali-server -n istio-system --wait
	@echo ">>> [kiali] 대시보드 접속"
	@echo "    kubectl port-forward svc/kiali -n istio-system 20001:20001"
	@echo "    URL: http://localhost:20001"

# ─────────────────────────────────────────────
# Cleanup
# ─────────────────────────────────────────────

clean:
	@echo ">>> [clean] 클러스터 전체 삭제 (name=mesh-lab)"
	kind delete cluster --name mesh-lab
	@echo ">>> [clean] 완료. 로컬 kubeconfig 항목도 제거되었습니다."

# ─────────────────────────────────────────────
# Help
# ─────────────────────────────────────────────

help:
	@echo ""
	@echo "Service Mesh Lab - 사용 가능한 타겟"
	@echo "======================================"
	@echo ""
	@echo "  클러스터"
	@echo "    cluster-up           Kind 클러스터 생성 (mesh-lab, 3 nodes)"
	@echo "    cluster-down         Kind 클러스터 삭제"
	@echo ""
	@echo "  서비스 메시 설치"
	@echo "    mesh-linkerd         Linkerd 설치 (sidecar, mTLS 자동)"
	@echo "    mesh-istio           Istio 설치 (sidecar 모드)"
	@echo "    mesh-istio-ambient   Istio 설치 (ambient 모드, sidecar 없음)"
	@echo ""
	@echo "  샘플 앱"
	@echo "    app-emojivoto        emojivoto 배포 (Linkerd 전용)"
	@echo "    app-bookinfo         bookinfo 배포 (Istio 전용)"
	@echo ""
	@echo "  관측성"
	@echo "    linkerd-viz          Linkerd 대시보드 설치 + 실행"
	@echo "    istio-kiali          Kiali + Prometheus 설치"
	@echo ""
	@echo "  정리"
	@echo "    clean                클러스터 전체 삭제"
	@echo ""
	@echo "  일반 워크플로우"
	@echo "    Linkerd: cluster-up → mesh-linkerd → app-emojivoto → linkerd-viz"
	@echo "    Istio:   cluster-up → mesh-istio   → app-bookinfo  → istio-kiali"
	@echo "    Ambient: cluster-up → mesh-istio-ambient → app-bookinfo"
	@echo ""
