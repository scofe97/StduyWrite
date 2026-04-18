# Appendix A. 연습문제 답안 (Answers to Review Questions)

---

## 📌 핵심 요약

> 이 부록은 CKA Study Guide 각 챕터의 연습문제에 대한 상세 답안을 제공한다. 실제 시험에서 자주 사용되는 **명령어 패턴**과 **YAML 매니페스트 작성법**을 실습을 통해 익힐 수 있다. 각 답안은 명령형(Imperative)과 선언형(Declarative) 두 가지 접근법을 모두 보여준다.

---

## 🎯 활용 방법

- [ ] 먼저 스스로 문제를 풀어본 후 답안 확인
- [ ] 명령형 vs 선언형 두 가지 방법 모두 연습
- [ ] 자주 사용되는 명령어 패턴을 암기
- [ ] YAML 매니페스트 구조를 손에 익히기

---

## Chapter 4. 클러스터 설치 및 업그레이드

### 핵심 명령어

```bash
# 노드 목록 확인
kubectl get nodes

# Pod를 특정 노드에서 실행 중인지 확인
kubectl get pod <pod-name> -o jsonpath='{.spec.nodeName}'

# 노드 drain (워크로드 제거)
kubectl drain <node-name> --ignore-daemonsets --force
```

### 클러스터 업그레이드 순서

```bash
# 1. Control Plane 노드 업그레이드
sudo apt-mark unhold kubeadm
sudo apt-get update && sudo apt-get install -y kubeadm=1.32.2-1.1
sudo apt-mark hold kubeadm
sudo kubeadm upgrade apply v1.32.2

# 2. Control Plane의 kubelet/kubectl 업그레이드
kubectl drain <control-plane-node> --ignore-daemonsets
sudo apt-get install -y kubelet=1.32.2-1.1 kubectl=1.32.2-1.1
sudo systemctl daemon-reload
sudo systemctl restart kubelet
kubectl uncordon <control-plane-node>

# 3. Worker 노드도 동일하게 진행 (kubeadm upgrade node 사용)
```

---

## Chapter 5. etcd 백업 및 복원

### etcd 버전 확인

```bash
# etcd Pod 이미지 확인
kubectl get pod etcd-<node-name> -n kube-system \
  -o jsonpath="{.spec.containers[0].image}"
# 출력: registry.k8s.io/etcd:3.5.16-0
```

### etcd 스냅샷 생성 및 복원

```bash
# 스냅샷 생성 (인증서 경로 확인 필수!)
sudo ETCDCTL_API=3 etcdctl \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  snapshot save /opt/etcd.bak

# 스냅샷 복원
sudo ETCDCTL_API=3 etcdutl --data-dir=/var/bak snapshot restore /opt/etcd.bak

# etcd 매니페스트 수정 (hostPath 변경)
sudo vim /etc/kubernetes/manifests/etcd.yaml
# spec.volumes.hostPath.path를 /var/bak으로 변경
```

---

## Chapter 6. 인증, 인가, Admission Control

### ClusterRole 생성

```bash
# 명령형
kubectl create clusterrole service-view --verb=get,list --resource=services

# 선언형 (service-view-clusterrole.yaml)
```

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: service-view
rules:
- apiGroups: [""]
  resources: ["services"]
  verbs: ["get", "list"]
```

### RoleBinding 생성

```bash
# 명령형
kubectl create rolebinding ellasmith-service-view \
  --user=ellasmith --clusterrole=service-view -n development
```

### 권한 확인

```bash
# 특정 사용자의 권한 확인
kubectl auth can-i list services --as=ellasmith --namespace=development
# yes

kubectl auth can-i watch deployments --as=ellasmith --namespace=production
# no
```

### ServiceAccount와 ClusterRoleBinding

```bash
# ServiceAccount 생성
kubectl create serviceaccount api-access -n apps

# ClusterRole 생성
kubectl create clusterrole api-clusterrole \
  --verb=watch,list,get --resource=pods

# ClusterRoleBinding 생성
kubectl create clusterrolebinding api-clusterrolebinding \
  --serviceaccount=apps:api-access --clusterrole=api-clusterrole
```

---

## Chapter 7. CRD와 Operator

### CRD 생성 및 확인

```bash
# CRD 생성
kubectl apply -f https://raw.githubusercontent.com/.../mongodbcommunity.yaml

# CRD 목록 확인
kubectl get crds

# CRD 상세 확인
kubectl describe crd <crd-name>
```

### Custom Resource 생성

```yaml
apiVersion: example.com/v1
kind: Backup
metadata:
  name: nginx-backup
spec:
  cronExpression: "0 0 * * *"
  podName: nginx
  path: /usr/local/nginx
```

---

## Chapter 8. Helm과 Kustomize

### Helm 기본 명령어

```bash
# 레포지토리 추가 및 업데이트
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update prometheus-community

# 차트 검색
helm search hub prometheus-community

# 차트 설치
helm install prometheus prometheus-community/kube-prometheus-stack

# 설치된 차트 목록
helm list

# 차트 삭제
helm uninstall prometheus
```

### Kustomize 기본 사용법

```yaml
# kustomization.yaml
namespace: t012
resources:
- pod.yaml
```

```bash
# 변환된 매니페스트 확인
kubectl kustomize ./

# 적용
kubectl apply -k ./
```

---

## Chapter 9. Pod와 Namespace

### Pod 생성 및 관리

```bash
# 네임스페이스 생성
kubectl create namespace j43

# Pod 생성
kubectl run nginx --image=nginx:1.17.10 --port=80 -n j43

# Pod IP 확인
kubectl get pod nginx -n j43 -o wide

# 임시 Pod로 연결 테스트
kubectl run busybox --image=busybox:1.36.1 --restart=Never --rm -it \
  -n j43 -- wget -O- <pod-ip>:80

# 로그 확인
kubectl logs nginx -n j43

# 컨테이너 접속
kubectl exec -it nginx -n j43 -- /bin/sh
```

### 환경변수 추가 Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx:1.17.10
    ports:
    - containerPort: 80
    env:
    - name: DB_URL
      value: postgresql://mydb:5432
    - name: DB_USERNAME
      value: admin
```

---

## Chapter 10. ConfigMap과 Secret

### ConfigMap 생성

```bash
# 파일에서 생성
kubectl create configmap app-config --from-file=application.yaml
```

### ConfigMap을 Volume으로 마운트

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: backend
spec:
  containers:
  - image: nginx:1.23.4-alpine
    name: backend
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
  volumes:
  - name: config-volume
    configMap:
      name: app-config
```

### Secret 생성 및 사용

```bash
# Secret 생성
kubectl create secret generic db-credentials --from-literal=db-password=passwd
```

```yaml
# Secret을 환경변수로 사용
spec:
  containers:
  - name: backend
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: db-password
```

---

## Chapter 11. Deployment와 ReplicaSet

### Deployment 생성

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  labels:
    tier: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: v1
  template:
    metadata:
      labels:
        app: v1
    spec:
      containers:
      - image: nginx:1.23.0
        name: nginx
```

### Deployment 관리 명령어

```bash
# 이미지 업데이트
kubectl set image deployment/nginx nginx=nginx:1.23.4

# 롤아웃 히스토리
kubectl rollout history deployment nginx
kubectl rollout history deployment nginx --revision=2

# 변경 사유 추가
kubectl annotate deployment nginx kubernetes.io/change-cause="Pick up patch version"

# 스케일링
kubectl scale deployment nginx --replicas=5

# 롤백
kubectl rollout undo deployment/nginx --to-revision=1
```

---

## Chapter 12. 워크로드 스케일링

### HorizontalPodAutoscaler (HPA)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nginx-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nginx
  minReplicas: 3
  maxReplicas: 8
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 75
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 60
```

---

## Chapter 13. 리소스 요구사항, Limits, Quotas

### 리소스 요구사항 정의

```yaml
spec:
  containers:
  - name: hello
    resources:
      requests:
        cpu: 100m
        memory: 500Mi
        ephemeral-storage: 1Gi
      limits:
        memory: 500Mi
        ephemeral-storage: 2Gi
```

### ResourceQuota 확인

```bash
kubectl describe quota app --namespace=rq-demo
```

### LimitRange

```bash
kubectl describe limitrange cpu-limit-range -n d92
```

---

## Chapter 14. Pod 스케줄링

### 노드 레이블 관리

```bash
# 레이블 추가
kubectl label nodes minikube-m02 color=green

# 레이블 확인
kubectl get nodes --show-labels
```

### nodeSelector

```yaml
spec:
  nodeSelector:
    color: green
```

### Node Affinity

```yaml
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: color
            operator: In
            values:
            - green
            - red
```

### Taint와 Toleration

```bash
# Taint 추가
kubectl taint nodes minikube-m03 exclusive=yes:NoExecute

# Taint 제거 (마이너스 기호!)
kubectl taint nodes minikube-m03 exclusive-
```

```yaml
# Pod에 Toleration 추가
spec:
  tolerations:
  - key: "exclusive"
    operator: "Equal"
    value: "yes"
    effect: "NoExecute"
```

---

## Chapter 15. Volumes

### emptyDir Volume

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: alpine
spec:
  volumes:
  - name: shared-vol
    emptyDir: {}
  containers:
  - name: container1
    image: alpine:3.12.0
    volumeMounts:
    - name: shared-vol
      mountPath: /etc/a
  - name: container2
    image: alpine:3.12.0
    volumeMounts:
    - name: shared-vol
      mountPath: /etc/b
```

---

## Chapter 16. Persistent Volumes

### PersistentVolume 생성

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: logs-pv
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
    - ReadOnlyMany
  hostPath:
    path: /var/logs
```

### PersistentVolumeClaim 생성

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: logs-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 2Gi
  storageClassName: ""
```

### Pod에서 PVC 사용

```yaml
spec:
  volumes:
  - name: logs-volume
    persistentVolumeClaim:
      claimName: logs-pvc
  containers:
  - name: nginx
    volumeMounts:
    - mountPath: "/var/log/nginx"
      name: logs-volume
```

---

## Chapter 17. Services

### Service 생성 (NodePort)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: webapp-service
spec:
  type: NodePort
  selector:
    app: webapp
  ports:
  - name: web
    port: 80
    targetPort: 80
    nodePort: 30080
  - name: metrics
    port: 9090
    targetPort: 9090
```

### 포트 포워딩으로 테스트

```bash
kubectl port-forward service/webapp-service 9091:80 &
curl localhost:9091
```

---

## Chapter 18. Ingress

### Ingress 정의

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: webapp-ingress
  namespace: webapp
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
```

### Canary 배포 (가중치 기반)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-canary-weight
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "20"  # 20% 트래픽
spec:
  # ...
```

---

## Chapter 19. Gateway API

### Gateway 정의

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: main-gateway
spec:
  gatewayClassName: nginx
  listeners:
  - name: http
    port: 80
    protocol: HTTP
    hostname: example.local
```

### HTTPRoute 정의

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: app-routes
spec:
  parentRefs:
  - name: main-gateway
  hostnames:
  - example.local
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /web
    backendRefs:
    - name: web-app
      port: 80
```

### 크로스 네임스페이스 접근 (ReferenceGrant)

```yaml
apiVersion: gateway.networking.k8s.io/v1beta1
kind: ReferenceGrant
metadata:
  name: allow-staging-to-gateway
  namespace: production
spec:
  from:
  - group: gateway.networking.k8s.io
    kind: HTTPRoute
    namespace: staging
  to:
  - group: gateway.networking.k8s.io
    kind: Gateway
    name: gateway
```

---

## Chapter 20. Network Policies

### Egress 정책 (DNS 허용 포함)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: alpha-app-policy
  namespace: team-alpha
spec:
  podSelector:
    matchLabels:
      app: alpha-app
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          team: beta
  - to:
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
```

### Default Deny 정책

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
```

### 연결 테스트

```bash
# curl로 연결 테스트
kubectl exec -it frontend-pod -n production -- \
  curl -v --connect-timeout 2 http://backend-service:8080

# 타임아웃 시 NetworkPolicy가 차단 중
```

---

## Chapter 21. 애플리케이션 트러블슈팅

### Distroless 컨테이너 디버깅

```bash
# debug 명령으로 임시 컨테이너 주입
kubectl debug -it date-recorder --image=busybox --target=debian \
  --share-processes
```

### Service 연결 문제 해결

```bash
# Endpoints 확인 (비어있으면 문제)
kubectl get endpoints -n y72

# Service 상세 정보 (selector, targetPort 확인)
kubectl describe service web-app -n y72

# 레이블/포트 불일치 수정 후 테스트
kubectl run tmp --image=busybox:1.36.1 --restart=Never -it --rm -n y72 \
  -- wget web-app
```

### 리소스 메트릭 확인

```bash
kubectl top pods -n stress-test
```

---

## Chapter 22. 클러스터 트러블슈팅

### NotReady 노드 복구

```bash
# 노드 상태 확인
kubectl get nodes
kubectl describe node worker-node-2 | grep -i taint
kubectl describe node worker-node-2 | grep -A10 Conditions

# Uncordon
kubectl uncordon worker-node-2

# kubelet 재시작 (노드에 SSH 후)
sudo systemctl status kubelet
sudo systemctl restart kubelet
```

### Control Plane 컴포넌트 복구

```bash
# kube-system Pod 상태 확인
kubectl get pods -n kube-system | grep -E "scheduler|controller|apiserver|etcd"

# 스케줄러 이미지 문제 확인
kubectl describe pod kube-scheduler-master-node -n kube-system | grep -A5 Events

# 매니페스트 수정 (control plane 노드에서)
sudo vi /etc/kubernetes/manifests/kube-scheduler.yaml
# 이미지 태그를 올바른 버전으로 수정
```

### 특정 노드에 테스트 Pod 배치

```bash
kubectl run test-pod --image=nginx:1.29.1 \
  --overrides='{"spec":{"nodeSelector":{"kubernetes.io/hostname":"worker-node-2"}}}'

kubectl get pod test-pod -o wide
```

---

## 📝 CKA 시험 핵심 패턴

### 자주 사용되는 명령어 조합

| 작업 | 명령어 |
|------|--------|
| 빠른 Pod 생성 | `kubectl run nginx --image=nginx --restart=Never` |
| YAML 생성 (dry-run) | `kubectl run nginx --image=nginx --dry-run=client -o yaml > pod.yaml` |
| 임시 Pod로 테스트 | `kubectl run tmp --image=busybox --rm -it -- wget <service>` |
| 레이블로 Pod 필터 | `kubectl get pods -l app=nginx` |
| 모든 리소스 확인 | `kubectl get all -n <namespace>` |
| JSONPath로 특정 값 추출 | `kubectl get pod -o jsonpath='{.spec.nodeName}'` |

### YAML 매니페스트 빠른 생성

```bash
# Deployment
kubectl create deployment nginx --image=nginx --dry-run=client -o yaml > deploy.yaml

# Service
kubectl expose deployment nginx --port=80 --dry-run=client -o yaml > svc.yaml

# ConfigMap
kubectl create configmap app-config --from-file=config.yaml --dry-run=client -o yaml

# Secret
kubectl create secret generic db-secret --from-literal=password=secret --dry-run=client -o yaml
```

---

## ✅ 체크리스트

- [ ] 각 챕터의 연습문제를 직접 풀어봤는가?
- [ ] 명령형/선언형 두 가지 방법을 모두 연습했는가?
- [ ] 자주 사용하는 명령어 패턴을 암기했는가?
- [ ] 트러블슈팅 시나리오를 실습했는가?
- [ ] YAML 매니페스트를 빠르게 작성할 수 있는가?
