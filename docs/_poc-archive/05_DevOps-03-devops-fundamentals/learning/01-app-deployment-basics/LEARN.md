# Ch01. 앱 배포의 기초

**핵심 질문**: "앱을 프로덕션에 배포하려면 최소한 무엇이 필요한가?"

---

## 🎯 학습 목표

이 챕터를 마치면 다음을 할 수 있다.

- 로컬 개발 환경과 프로덕션 환경의 구조적 차이를 설명할 수 있다
- Fly.io를 사용해 애플리케이션을 PaaS 방식으로 배포할 수 있다
- EC2 인스턴스에 nginx + systemd 조합으로 애플리케이션을 직접 서빙할 수 있다
- PaaS, IaaS, 컨테이너 배포 방식의 트레이드오프를 상황에 맞게 선택할 수 있다
- 모든 배포에 공통으로 필요한 Health Check, Rollback 계획, 모니터링 구성을 설명할 수 있다
- DevOps 배포 방식이 수동 FTP부터 AI-Ops까지 어떤 이유로 진화했는지 흐름을 추적할 수 있다

---

## 1. 배포란 무엇인가

개발자의 노트북에서 동작하는 코드를 다른 사람이 접근할 수 있는 서버에서 실행하는 행위를 배포(deployment)라고 부른다. 이 정의는 단순해 보이지만, 실제로 로컬과 프로덕션 사이에는 생각보다 큰 간극이 존재한다.

### 로컬 개발 환경 vs 프로덕션 환경

로컬에서는 `npm run dev` 또는 `go run main.go` 한 줄로 앱이 뜬다. 파일을 바꾸면 핫 리로드가 되고, 에러가 나도 터미널에서 바로 확인할 수 있다. 반면 프로덕션에서는 다음 조건을 모두 만족해야 한다.

**가용성(Availability)**: 서버가 재시작되거나 프로세스가 죽어도 자동으로 다시 올라와야 한다. 개발 중엔 터미널을 닫으면 프로세스도 종료되지만, 프로덕션에서 그런 일이 생기면 서비스가 중단된다.

**네트워킹**: 외부에서 80/443 포트로 접근할 수 있어야 하고, 도메인과 TLS 인증서가 연결되어 있어야 한다. 앱 자체는 내부 포트(예: 3000, 8080)에서 수신하고, nginx 같은 리버스 프록시가 외부 요청을 앱으로 전달하는 구조가 일반적이다.

**환경 변수**: 데이터베이스 비밀번호, API 키 같은 민감한 값은 코드에 하드코딩하지 않고 환경 변수로 분리해야 한다. 로컬에선 `.env` 파일로 관리하더라도, 프로덕션에선 시스템 수준의 비밀 관리가 필요하다.

**로그**: `console.log`가 터미널에 출력되는 것이 로컬이라면, 프로덕션에서는 로그가 파일이나 중앙 로그 시스템으로 수집되어 나중에 검색하고 분석할 수 있어야 한다.

```
로컬 개발                         프로덕션
─────────────────────────         ─────────────────────────
• 수동 시작/종료                   • 자동 시작, 크래시 복구
• localhost:3000 접근              • 도메인 + HTTPS 접근
• .env 파일 사용                   • 시크릿 매니저 또는 환경 변수
• 터미널에 로그 출력               • 파일/중앙 로그 시스템
• 단일 프로세스                    • 프로세스 매니저 (systemd, PM2)
• 개발자 머신 스펙                 • 스케일 가능한 인프라
```

이 간극을 채우는 방법은 크게 세 가지로 분류된다. 복잡함을 플랫폼이 대신 처리해주는 PaaS, 직접 서버를 구성하는 IaaS, 그리고 컨테이너를 중간 레이어로 두는 방식이다.

---

## 2. PaaS 배포: Fly.io로 시작하는 가장 간단한 배포

PaaS(Platform as a Service)는 서버 운영체제 설정, nginx 설치, 프로세스 관리 같은 인프라 작업을 플랫폼이 대신 처리한다. 개발자는 애플리케이션 코드와 최소한의 설정만 제공하면 된다.

Fly.io를 선택하는 이유는 무엇일까? Heroku의 무료 플랜이 종료된 이후 가장 개발자 친화적인 PaaS로 자리잡았기 때문이다. 전 세계 30개 이상의 리전에 컨테이너를 배포할 수 있고, 소규모 앱은 무료 티어로 운영할 수 있다.

### Fly.io 배포 전체 흐름

```bash
# 1. CLI 설치 (macOS)
brew install flyctl

# 2. 로그인
fly auth login

# 3. 앱 초기화 (현재 디렉토리에서 실행)
# fly.toml 생성 + Dockerfile 자동 감지 또는 생성
fly launch
# 대화형 프롬프트에서:
# - App name: my-go-app
# - Region: nrt (Tokyo)
# - PostgreSQL: No (지금은 불필요)
# - Redis: No
# 결과: fly.toml 생성됨

# 4. 시크릿(환경 변수) 설정
fly secrets set DATABASE_URL="postgres://user:pass@host/db"
fly secrets set API_KEY="sk-xxxx"

# 5. 배포
fly deploy
# 내부 동작: Docker 이미지 빌드 → Fly 레지스트리 Push → 컨테이너 기동 → Health check

# 6. 앱 상태 확인
fly status
fly logs          # 실시간 로그
fly logs --tail   # 지속 스트리밍

# 7. 배포된 앱 접속
fly open

# 8. 스케일 조정 (필요 시)
fly scale count 2          # 인스턴스 2개로
fly scale memory 512       # 메모리 512MB로

# 9. 롤백 (문제 발생 시)
fly releases               # 배포 이력 조회
fly deploy --image registry.fly.io/my-go-app:v2  # 이전 버전으로
```

Fly.io 설정 파일 `fly.toml`은 앱의 배포 명세서 역할을 한다.

```toml
# fly.toml
# 왜 이 파일이 필요한가: 배포 설정을 코드로 관리(IaC)해서 재현 가능하게 만들기 위함

app = "my-go-app"
primary_region = "nrt"  # 기본 배포 리전: 도쿄

[build]
  # 왜 Dockerfile을 지정하는가: 빌드 환경을 일관되게 유지하기 위함
  dockerfile = "Dockerfile"

[env]
  # 민감하지 않은 환경 변수만 여기에 (DB 비밀번호는 fly secrets 사용)
  PORT = "8080"
  APP_ENV = "production"

[http_service]
  internal_port = 8080       # 앱이 수신하는 포트
  force_https = true         # HTTP → HTTPS 강제 리다이렉트
  auto_stop_machines = true  # 트래픽 없을 때 자동 중지 (비용 절감)
  auto_start_machines = true # 요청 오면 자동 시작

  [http_service.concurrency]
    type = "connections"
    hard_limit = 25    # 동시 접속 최대치 초과 시 새 인스턴스 기동
    soft_limit = 20

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256

# 왜 health check가 필요한가: 배포 중 트래픽을 새 인스턴스로 전환하기 전,
# 앱이 실제로 요청을 처리할 준비가 됐는지 확인하기 위함
[[services.tcp_checks]]
  grace_period = "10s"   # 기동 후 체크 시작까지 대기 시간
  interval = "15s"
  timeout = "2s"
  restart_limit = 3

[deploy]
  strategy = "rolling"   # 무중단 배포: 구 버전 내리기 전 신 버전 올림
```

Health Check 엔드포인트는 앱 코드에 직접 구현해야 한다. Fly.io뿐 아니라 모든 배포 환경에서 필요하다.

```go
// main.go — 최소한의 Go HTTP 서버 + 헬스체크
// 왜 /health를 별도로 만드는가: 로드밸런서/오케스트레이터가
// 앱의 준비 상태를 프로브(probe)하는 표준 엔드포인트이기 때문

package main

import (
    "encoding/json"
    "fmt"
    "net/http"
    "os"
    "time"
)

func main() {
    port := os.Getenv("PORT")
    if port == "" {
        port = "8080"
    }

    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintln(w, "Hello, Production!")
    })

    // 헬스체크: 앱이 살아있고 요청을 받을 준비가 됐음을 알리는 엔드포인트
    http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "application/json")
        w.WriteHeader(http.StatusOK)
        json.NewEncoder(w).Encode(map[string]interface{}{
            "status":    "ok",
            "timestamp": time.Now().UTC().Format(time.RFC3339),
        })
    })

    fmt.Printf("Server starting on :%s\n", port)
    if err := http.ListenAndServe(":"+port, nil); err != nil {
        fmt.Fprintf(os.Stderr, "Server failed: %v\n", err)
        os.Exit(1)
    }
}
```

---

## 3. IaaS 배포: EC2 + nginx + systemd

IaaS(Infrastructure as a Service)는 가상 서버(VM)만 제공하고, 그 위에 무엇을 설치하고 어떻게 운영할지는 전적으로 운영자의 몫이다. AWS EC2가 가장 대표적이다. PaaS보다 손이 많이 가지만, 자유도가 높고 무슨 일이 일어나는지 직접 볼 수 있어 학습 가치가 크다.

다음 스크립트는 EC2 Ubuntu 서버를 처음부터 배포 가능한 상태로 만드는 전체 프로세스를 담고 있다.

```bash
#!/bin/bash
# provision.sh — EC2 Ubuntu 22.04 서버 초기 세팅 스크립트
# 실행 위치: EC2 인스턴스 내부 (SSH 접속 후)
# 또는 EC2 User Data로 인스턴스 시작 시 자동 실행 가능

set -euo pipefail  # 왜 이 옵션인가: 오류 시 즉시 중단(e), 미정의 변수 오류(u), 파이프 실패 전파(o pipefail)

APP_NAME="my-go-app"
APP_USER="appuser"
APP_DIR="/opt/${APP_NAME}"
APP_BINARY="${APP_DIR}/${APP_NAME}"
APP_PORT="8080"

echo "=== 1. 시스템 패키지 업데이트 ==="
# 왜 upgrade를 먼저 하는가: 보안 패치를 적용하고 의존성 충돌을 방지하기 위함
apt-get update -y
apt-get upgrade -y

echo "=== 2. nginx 설치 ==="
# 왜 nginx를 별도로 두는가: 앱 서버는 내부 포트(8080)에서만 수신하고,
# 외부 80/443 요청은 nginx가 처리한 후 앱으로 전달(리버스 프록시)
# 이 구조로 TLS 처리, 정적 파일 서빙, 요청 로깅을 nginx에 위임할 수 있음
apt-get install -y nginx

echo "=== 3. 전용 시스템 사용자 생성 ==="
# 왜 전용 사용자를 만드는가: root로 앱을 실행하면 앱이 해킹됐을 때
# 서버 전체를 탈취당할 수 있음. 최소 권한 원칙(Principle of Least Privilege)
if ! id "${APP_USER}" &>/dev/null; then
    useradd --system --no-create-home --shell /bin/false "${APP_USER}"
    echo "사용자 ${APP_USER} 생성 완료"
fi

echo "=== 4. 앱 디렉토리 준비 ==="
mkdir -p "${APP_DIR}"
chown "${APP_USER}:${APP_USER}" "${APP_DIR}"

echo "=== 5. 바이너리 배포 ==="
# 왜 빌드를 서버에서 직접 하지 않는가: 서버에 Go 컴파일러를 설치하면
# 공격 면적(attack surface)이 늘어남. 로컬 또는 CI에서 빌드 후 바이너리만 전송
# 이 예시에서는 SCP로 미리 빌드된 바이너리를 전송했다고 가정
# 실제 CI/CD에서는 S3, GitHub Releases, 또는 컨테이너 레지스트리 사용
if [ -f "/tmp/${APP_NAME}" ]; then
    cp "/tmp/${APP_NAME}" "${APP_BINARY}"
    chmod 755 "${APP_BINARY}"
    chown "${APP_USER}:${APP_USER}" "${APP_BINARY}"
fi

echo "=== 6. 환경 변수 파일 생성 ==="
# 왜 파일로 환경 변수를 관리하는가: systemd 서비스에서 EnvironmentFile 지시자로
# 안전하게 로드할 수 있고, 코드 저장소에는 절대 포함하지 않음
cat > "${APP_DIR}/.env" << 'EOF'
APP_ENV=production
PORT=8080
# DATABASE_URL=postgres://user:pass@localhost/mydb
# API_KEY=실제_값으로_교체
EOF
chmod 600 "${APP_DIR}/.env"     # 소유자만 읽기/쓰기 가능
chown "${APP_USER}:${APP_USER}" "${APP_DIR}/.env"

echo "=== 7. systemd 서비스 파일 생성 ==="
# 왜 systemd를 사용하는가: Linux의 표준 프로세스 관리 도구.
# 부팅 시 자동 시작, 크래시 시 자동 재시작, 로그 수집(journald)을 제공함
cat > "/etc/systemd/system/${APP_NAME}.service" << EOF
[Unit]
Description=${APP_NAME} Web Application
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=${APP_USER}
Group=${APP_USER}
WorkingDirectory=${APP_DIR}
EnvironmentFile=${APP_DIR}/.env
ExecStart=${APP_BINARY}

# 왜 Restart=always인가: 예기치 않은 크래시 시 자동 복구하기 위함
Restart=always
RestartSec=5s       # 재시작 전 5초 대기 (연속 크래시 폭풍 방지)

# 보안 강화 설정
NoNewPrivileges=yes         # 프로세스가 권한 상승 불가
ProtectSystem=strict        # 시스템 파일 쓰기 불가
ProtectHome=yes             # 홈 디렉토리 접근 불가
PrivateTmp=yes              # 격리된 /tmp 사용

# 로그는 journald로 자동 수집 (journalctl -u ${APP_NAME} -f 로 확인)
StandardOutput=journal
StandardError=journal

[Install]
# 왜 multi-user.target인가: 일반적인 서버 모드에서 자동 시작한다는 의미
WantedBy=multi-user.target
EOF

echo "=== 8. systemd 리로드 및 서비스 활성화 ==="
systemctl daemon-reload
systemctl enable "${APP_NAME}"   # 부팅 시 자동 시작 등록
systemctl start "${APP_NAME}"    # 즉시 시작
systemctl status "${APP_NAME}"

echo "=== 9. nginx 리버스 프록시 설정 ==="
cat > "/etc/nginx/sites-available/${APP_NAME}" << EOF
server {
    listen 80;
    server_name _;  # 모든 도메인 수신 (운영 시 실제 도메인으로 교체)

    # 왜 리버스 프록시를 쓰는가: 앱은 내부 포트만 열고,
    # nginx가 외부 요청을 받아 앱으로 전달. TLS, 로깅, 캐싱을 nginx에서 처리
    location / {
        proxy_pass http://127.0.0.1:${APP_PORT};

        # 왜 이 헤더들이 필요한가: 프록시를 거치면 원래 클라이언트 IP가 소실됨
        # X-Real-IP, X-Forwarded-For로 원본 IP를 앱에 전달
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        # 연결 타임아웃 설정
        proxy_connect_timeout 10s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }

    # 헬스체크는 nginx 레벨에서 직접 처리 (앱 우회 가능)
    location /health {
        proxy_pass http://127.0.0.1:${APP_PORT}/health;
        access_log off;  # 헬스체크 로그는 노이즈가 많으므로 꺼둠
    }
}
EOF

# sites-enabled에 심볼릭 링크 생성 (nginx 활성화 방식)
ln -sf "/etc/nginx/sites-available/${APP_NAME}" "/etc/nginx/sites-enabled/"
# default 설정 비활성화
rm -f /etc/nginx/sites-enabled/default

# nginx 설정 문법 검사
nginx -t

systemctl reload nginx
echo "=== 프로비저닝 완료 ==="
echo "앱: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
```

### 이후 배포(업데이트) 스크립트

초기 프로비저닝과 달리, 코드 업데이트 시에는 바이너리 교체와 서비스 재시작만 하면 된다.

```bash
#!/bin/bash
# deploy.sh — 새 버전 배포 스크립트 (로컬 또는 CI에서 실행)
# 사용법: ./deploy.sh <EC2_IP> <새_바이너리_경로>

set -euo pipefail

EC2_IP="${1:?EC2 IP 필요}"
BINARY_PATH="${2:?바이너리 경로 필요}"
APP_NAME="my-go-app"
KEY_FILE="~/.ssh/my-key.pem"

echo "1. 바이너리 빌드 확인"
file "${BINARY_PATH}" | grep -q "ELF 64-bit" || {
    echo "Linux 64-bit 바이너리가 아님. GOOS=linux GOARCH=amd64로 빌드 필요"
    exit 1
}

echo "2. EC2로 바이너리 전송"
scp -i "${KEY_FILE}" "${BINARY_PATH}" "ubuntu@${EC2_IP}:/tmp/${APP_NAME}"

echo "3. 서버에서 교체 및 재시작"
ssh -i "${KEY_FILE}" "ubuntu@${EC2_IP}" << 'REMOTE'
    set -e
    APP_NAME="my-go-app"

    # 왜 잠시 멈추고 교체하는가: 실행 중인 바이너리를 직접 덮어쓰면 오류 발생
    # (Linux에서는 실행 중인 inode를 교체하는 방식으로 안전하게 처리 가능하지만 명시적 절차가 더 안전)
    sudo systemctl stop "${APP_NAME}"
    sudo cp "/tmp/${APP_NAME}" "/opt/${APP_NAME}/${APP_NAME}"
    sudo chmod 755 "/opt/${APP_NAME}/${APP_NAME}"
    sudo chown appuser:appuser "/opt/${APP_NAME}/${APP_NAME}"
    sudo systemctl start "${APP_NAME}"

    # 기동 확인 (최대 15초 대기)
    for i in $(seq 1 15); do
        if curl -sf http://localhost:8080/health > /dev/null 2>&1; then
            echo "헬스체크 통과 (${i}초)"
            exit 0
        fi
        sleep 1
    done
    echo "헬스체크 실패 — 이전 버전으로 롤백 필요"
    exit 1
REMOTE
echo "배포 완료"
```

---

## 4. DevOps 배포 방식의 9단계 진화

배포 방식은 기술이 발전하면서 다음과 같은 경로로 진화해왔다. 각 단계는 이전 단계의 고통을 해결하기 위해 등장했다는 점을 기억해두자.

```mermaid
flowchart LR
    A["① 수동 FTP\n파일 직접 업로드\n(오류, 불일치)"]
    B["② 배포 스크립트\nSSH + bash\n(반복 가능)"]
    C["③ CI\n자동 빌드/테스트\n(품질 게이트)"]
    D["④ CD\n자동 배포\n(속도)"]
    E["⑤ 컨테이너\nDocker\n(환경 일관성)"]
    F["⑥ 오케스트레이션\nKubernetes\n(스케일)"]
    G["⑦ GitOps\nArgoCD/Flux\n(선언적)"]
    H["⑧ Platform Eng.\nInternal Dev Platform\n(셀프서비스)"]
    I["⑨ AI-Ops\nML 기반 이상 감지\n자동 복구"]

    A --> B --> C --> D --> E --> F --> G --> H --> I

    style A fill:#ffd6d6,stroke:#cc0000,color:#333
    style B fill:#ffe6cc,stroke:#cc6600,color:#333
    style C fill:#fff3cc,stroke:#cc9900,color:#333
    style D fill:#e6ffcc,stroke:#339900,color:#333
    style E fill:#ccf5ff,stroke:#0099cc,color:#333
    style F fill:#cce0ff,stroke:#0033cc,color:#333
    style G fill:#e6ccff,stroke:#6600cc,color:#333
    style H fill:#ffccf5,stroke:#cc0099,color:#333
    style I fill:#f0f0f0,stroke:#666666,color:#333
```

**① 수동 FTP**: 개발자가 FileZilla 같은 FTP 클라이언트로 서버에 파일을 직접 업로드하던 시절이다. 어떤 파일을 올렸는지 기록도 없고, 팀원들이 서로 다른 버전을 올리는 충돌이 빈번했다.

**② 배포 스크립트**: `deploy.sh` 같은 스크립트로 SSH를 통해 파일을 전송하고 서버를 재시작하는 방식이다. 재현 가능하지만 여전히 수동 트리거가 필요하다.

**③ CI**: 코드를 커밋할 때마다 자동으로 빌드와 테스트가 실행된다. "내 머신에서는 됐는데"라는 변명을 제거한다.

**④ CD**: 테스트를 통과하면 자동으로 배포까지 진행된다. 배포 빈도가 주 1회에서 하루 수십 회로 늘어난다.

**⑤ 컨테이너**: Docker로 앱과 실행 환경을 함께 패키징한다. "환경 차이로 인한 버그"가 사라진다.

**⑥ 오케스트레이션**: 수백 개의 컨테이너를 Kubernetes가 관리한다. 스케일 아웃, 자동 복구, 배포 전략이 선언적으로 정의된다.

**⑦ GitOps**: Git 저장소가 클러스터 상태의 단일 진실 공급원(Single Source of Truth)이 된다. ArgoCD가 저장소 변경을 감지해 클러스터에 자동 적용한다.

**⑧ Platform Engineering**: 개발팀이 인프라 없이도 앱을 배포할 수 있는 Internal Developer Platform을 구축한다. "황금 경로(Golden Path)"라고 부르기도 한다.

**⑨ AI-Ops**: ML 모델이 메트릭을 분석해 이상 징후를 사전에 감지하고 자동으로 대응한다. 아직 완전히 성숙한 단계는 아니지만 빠르게 발전 중이다.

---

## 5. PaaS vs IaaS vs 컨테이너 비교

세 가지 방식의 트레이드오프를 이해하면 상황에 맞는 선택을 할 수 있다.

| 항목 | PaaS (Fly.io, Render) | IaaS (EC2 + nginx) | 컨테이너 (Docker + ECS/K8s) |
|---|---|---|---|
| **설정 복잡도** | 낮음 (CLI 몇 줄) | 높음 (서버 직접 구성) | 중간~높음 |
| **제어 수준** | 낮음 (플랫폼 결정) | 높음 (모든 것 직접) | 높음 |
| **비용 예측성** | 명확 (플랜 기반) | 복잡 (리소스 과금) | 복잡 |
| **학습 곡선** | 낮음 | 높음 (Linux 운영 필요) | 높음 (Docker/K8s 필요) |
| **스케일 용이성** | 극히 쉬움 | 수동 작업 필요 | 극히 쉬움 |
| **비용 (소규모)** | 무료~저렴 | 상시 EC2 과금 | 중간 |
| **장애 원인 추적** | 제한적 (플랫폼 블랙박스) | 완전한 접근 가능 | 가능 |
| **적합한 상황** | MVP, 사이드 프로젝트 | 레거시 앱, 특수 요구사항 | 마이크로서비스, 팀 프로덕션 |

**선택 기준을 요약하면 이렇다**: 빠르게 배포하고 운영보다 개발에 집중하고 싶다면 PaaS, 인프라를 완전히 제어하거나 기존 환경에 통합해야 한다면 IaaS, 팀이 여럿이고 여러 서비스를 독립적으로 배포해야 한다면 컨테이너 기반을 선택한다.

---

## 6. 모든 배포에 공통으로 필요한 체크리스트

배포 방식이 무엇이든 다음 세 가지는 빠져서는 안 된다.

### Health Check

앱이 시작됐다고 해서 정상적으로 동작한다는 보장은 없다. 데이터베이스 연결 실패, 포트 바인딩 오류, 설정 파일 누락 등 다양한 이유로 앱이 기동됐지만 요청을 처리하지 못하는 상태가 될 수 있다. `/health` 엔드포인트는 이 상태를 외부에서 확인할 수 있게 해준다.

좋은 Health Check는 두 가지를 구분한다. Liveness(앱이 살아있는가)와 Readiness(앱이 트래픽을 받을 준비가 됐는가)이다. Kubernetes 환경이라면 둘을 분리하고, 그 외에는 하나의 `/health`로 통합해도 충분하다.

### Rollback 계획

"배포가 잘못됐을 때 어떻게 이전 상태로 돌아가는가?"를 배포 전에 미리 정의해두어야 한다.

- **PaaS**: `fly deploy --image <이전_이미지>` 또는 대시보드에서 이전 릴리스 클릭
- **IaaS**: 이전 바이너리 백업 유지 + `deploy.sh` 로 재배포
- **Kubernetes**: `kubectl rollout undo deployment/<이름>`

### 모니터링의 최소 구성

아무리 작은 프로젝트라도 다음 세 가지는 갖춰야 한다.

1. **에러 추적**: Sentry 같은 도구로 예외가 발생했을 때 알림을 받는다
2. **업타임 모니터링**: UptimeRobot(무료)으로 앱이 다운됐을 때 이메일 알림을 받는다
3. **로그 접근**: `fly logs`, `journalctl -u my-app`, 또는 CloudWatch로 실시간 로그를 볼 수 있어야 한다

---

## 7. 흔한 배포 실수와 올바른 패턴

배포 경험이 쌓이면 특정 패턴의 실수가 반복된다는 것을 알게 된다. 미리 알아두면 같은 실수를 피할 수 있다.

### Bad vs Good: 환경 변수 관리

```bash
# BAD — 비밀값을 코드에 하드코딩
# 이렇게 하면 Git 이력에 영원히 남는다
DATABASE_URL="postgres://admin:supersecret@prod-db.example.com/mydb"
API_KEY="sk-prod-1234567890abcdef"

# GOOD — 환경 변수로 분리
DATABASE_URL="${DATABASE_URL:?DATABASE_URL 환경변수가 설정되지 않음}"
API_KEY="${API_KEY:?API_KEY 환경변수가 설정되지 않음}"
# :? 문법: 변수가 비어있으면 오류 메시지와 함께 스크립트 종료
# 왜 이렇게 하는가: 비밀값 누락을 런타임 오류로 조기에 감지하기 위함
```

### Bad vs Good: 배포 후 확인 없이 완료 선언

```bash
# BAD — 서비스 시작 명령만 내리고 성공으로 간주
sudo systemctl start my-app
echo "배포 완료!"

# GOOD — 실제로 앱이 응답하는지 확인
sudo systemctl start my-app

# 헬스체크 폴링 (최대 30초 대기)
for i in $(seq 1 30); do
    if curl -sf http://localhost:8080/health > /dev/null 2>&1; then
        echo "앱 기동 확인 완료 (${i}초 소요)"
        exit 0
    fi
    echo "기동 대기 중... ${i}/30"
    sleep 1
done

# 30초 안에 응답 없으면 실패 처리 — 자동 롤백 트리거
echo "기동 실패 — 이전 버전으로 롤백"
sudo systemctl stop my-app
sudo cp /opt/my-app/my-app.backup /opt/my-app/my-app
sudo systemctl start my-app
exit 1
```

### Bad vs Good: 로그 없이 운영

프로덕션 서버에서 문제가 생겼을 때 로그가 없으면 원인을 알 수 없다. 가장 흔한 실수는 앱을 배포했지만 로그를 어디서 봐야 하는지 모르는 상황이다.

```bash
# 로그 확인 명령어 요약
# systemd 서비스 로그
journalctl -u my-app -f               # 실시간 스트리밍
journalctl -u my-app --since "1 hour ago"  # 최근 1시간
journalctl -u my-app -n 100           # 최근 100줄

# nginx 접근/에러 로그
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Fly.io 로그
fly logs --app my-go-app
```

### 배포 전 최종 체크리스트

```
배포 전:
□ 로컬에서 프로덕션 빌드 테스트 (GOOS=linux GOARCH=amd64)
□ 환경 변수 목록 확인 (누락된 설정 없는가)
□ 롤백 절차 확인 (이전 버전 바이너리 또는 이미지 태그 메모)
□ 배포 시간 확인 (피크 트래픽 시간대 피하기)

배포 중:
□ 헬스체크 통과 확인
□ 에러 로그 급증 여부 확인
□ 주요 기능 수동 스모크 테스트

배포 후 (15분 관찰):
□ 에러율 정상 범위 유지
□ 응답 시간 이상 없음
□ 메모리/CPU 급증 없음
```

---

## 8. 교차 참조

이 챕터는 배포의 기초를 다룬다. 각 주제의 깊이는 다음 프로젝트에서 다룬다.

- **컨테이너화 상세**: `poc/03_CloudNative/01-docker/` — Docker 이미지 빌드, 멀티스테이지 빌드, docker-compose 등
- **CI/CD 파이프라인 상세**: `poc/05_DevOps/01-jenkins/` — Jenkins Pipeline, 빌드/테스트/배포 자동화
- **CI/CD 패턴 상세**: `poc/05_DevOps/02-cicd-patterns/` — Blue-Green, Canary, Rolling 배포 전략
- **Kubernetes 오케스트레이션**: `poc/03_CloudNative/02-kubernetes/` — Deployment, Service, Ingress 설정
- **GitOps**: `poc/03_CloudNative/02-kubernetes/` Ch18 이후 — ArgoCD, Flux

---

## 📝 핵심 정리

배포의 본질은 로컬에서 동작하는 코드를 **지속적으로**, **안정적으로**, **재현 가능하게** 서버에서 실행하는 것이다. PaaS는 인프라 복잡성을 플랫폼이 가져가고, IaaS는 그 복잡성을 직접 다루는 대신 완전한 제어권을 가진다. 컨테이너는 두 세계의 중간 어딘가에 있다.

어떤 방식을 선택하든 Health Check, Rollback 계획, 모니터링의 삼각형은 반드시 갖춰야 한다. 이 세 가지가 없는 배포는 "일단 올려놓고 기도하는" 방식에 불과하다.

다음 챕터(IaC)에서는 이 서버 설정 과정을 Terraform으로 코드화해서 클릭 한 번에 재현 가능하게 만드는 방법을 다룬다.
