# Ch09 - Linkerd 관측성 실습
---
> 대응 학습 문서: `learning/09-linkerd-observability/LEARN.md`

## 사전 조건

- Kind 클러스터 실행 중 (`make cluster-up`)
- Linkerd + viz 설치 완료 (`make mesh-linkerd` 후 `linkerd viz install | kubectl apply -f -`)
- emojivoto 앱 배포 및 메시 적용 완료 (`make app-emojivoto`)
- linkerd CLI 설치

## 실습 항목

| # | 개념 | 실습 내용 | 검증 방법 |
|---|------|----------|----------|
| 1 | stat | 배포별 성공률·RPS 조회 | 숫자 표시 확인 |
| 2 | top | 실시간 요청 스트리밍 | 요청 흐름 실시간 출력 |
| 3 | tap | 요청 상세 스트리밍 | HTTP 메서드·경로·상태코드 확인 |
| 4 | routes | 라우트별 메트릭 | 경로별 성공률 확인 |
| 5 | Grafana | Linkerd Deployment 대시보드 | 레이턴시·RPS 그래프 확인 |
| 6 | 오류 주입 후 관찰 | 의도적 실패 → 성공률 변화 | stat에서 성공률 하락 확인 |

## 실습 상세

### 1. linkerd viz stat — 서비스별 골든 시그널

**목표**: `stat` 명령어로 각 Deployment의 성공률(SR), 초당 요청수(RPS), P50/P95/P99 레이턴시를 한눈에 확인한다. 골든 시그널(Latency, Traffic, Errors, Saturation) 중 세 가지를 한 번에 본다.

**단계**:
1. emojivoto 네임스페이스 전체 조회
   ```bash
   linkerd viz stat deploy -n emojivoto
   ```
2. 특정 Deployment만 조회
   ```bash
   linkerd viz stat deploy/web -n emojivoto
   ```
3. 네임스페이스 단위 집계
   ```bash
   linkerd viz stat ns emojivoto
   ```
4. Pod 단위 조회
   ```bash
   linkerd viz stat pod -n emojivoto
   ```

**검증**:
```
NAME      MESHED   SUCCESS      RPS   LATENCY_P50   LATENCY_P95   LATENCY_P99
emoji        1/1   100.00%   2.0rps           1ms           2ms           3ms
voting       1/1   100.00%   2.0rps           1ms           2ms           3ms
web          1/1   100.00%   2.0rps           5ms          10ms          20ms
```
MESHED 컬럼이 `1/1`, SUCCESS가 100%에 가까운 값이 출력된다.

### 2. linkerd viz top — 실시간 요청 모니터링

**목표**: `top`은 htop처럼 실시간으로 가장 많은 요청을 받는 경로와 소스를 보여준다. 트래픽 패턴을 빠르게 파악할 때 유용하다.

**단계**:
1. web Deployment로 들어오는 요청 실시간 확인
   ```bash
   linkerd viz top deploy/web -n emojivoto
   ```
2. 별도 터미널에서 트래픽 발생 (vote-bot이 자동으로 트래픽을 보내므로 기다려도 됨)
   ```bash
   kubectl port-forward svc/web-svc 8080:80 -n emojivoto &
   for i in $(seq 1 20); do
     curl -s http://localhost:8080/ > /dev/null
   done
   ```
3. 전체 네임스페이스 요청 확인
   ```bash
   linkerd viz top deploy -n emojivoto
   ```

**검증**: 화면에 요청 경로별 RPS, 성공률이 실시간으로 갱신되어 출력된다.
```
(press q to quit)
SOURCE             DESTINATION          METHOD   PATH          COUNT    BEST   WORST    LAST  SUCCESS
vote-bot           web                  POST     /api/vote         5    1ms     5ms     2ms   100.00%
web                emoji-svc            GET      /emojis           3    1ms     3ms     1ms   100.00%
```

### 3. linkerd viz tap — 요청 스트리밍

**목표**: `tap`은 실시간으로 개별 요청 스트림을 보여준다. 특정 요청의 응답 코드와 레이턴시를 실시간으로 추적할 수 있다.

**단계**:
1. web Deployment 요청 스트리밍
   ```bash
   linkerd viz tap deploy/web -n emojivoto
   ```
2. 특정 경로만 필터링
   ```bash
   linkerd viz tap deploy/web -n emojivoto \
     --path /api/vote
   ```
3. 특정 소스에서 오는 요청만 필터링
   ```bash
   linkerd viz tap deploy/emoji -n emojivoto \
     --from deploy/web
   ```
4. 출력 포맷 변경 (JSON)
   ```bash
   linkerd viz tap deploy/web -n emojivoto -o json | head -20
   ```

**검증**:
```
req id=0:0 proxy=in  src=10.244.x.x:xxxxx dst=10.244.x.x:8080 \
  tls=true :method=POST :authority=web-svc :path=/api/vote
rsp id=0:0 proxy=in  src=10.244.x.x:xxxxx dst=10.244.x.x:8080 \
  tls=true :status=200 latency=2ms
```
`tls=true` 로 mTLS가 적용된 상태임을 확인할 수 있다.

### 4. linkerd viz routes — 라우트별 메트릭

**목표**: `routes`는 ServiceProfile이 정의된 경우 경로별 메트릭을 보여준다. 어떤 API 엔드포인트가 실패율이 높은지 파악하는 데 사용한다.

**단계**:
1. ServiceProfile 생성 (emojivoto/web 서비스용)
   ```bash
   kubectl apply -f - <<EOF
   apiVersion: linkerd.io/v1alpha2
   kind: ServiceProfile
   metadata:
     name: web-svc.emojivoto.svc.cluster.local
     namespace: emojivoto
   spec:
     routes:
       - name: GET /
         condition:
           method: GET
           pathRegex: /
       - name: POST /api/vote
         condition:
           method: POST
           pathRegex: /api/vote
       - name: GET /api/list
         condition:
           method: GET
           pathRegex: /api/list
   EOF
   ```
2. 라우트별 메트릭 조회
   ```bash
   linkerd viz routes deploy/web -n emojivoto
   ```
3. 1분간 집계 후 재조회
   ```bash
   sleep 30 && linkerd viz routes deploy/web -n emojivoto
   ```

**검증**:
```
ROUTE             SERVICE    SUCCESS      RPS   LATENCY_P50   LATENCY_P95   LATENCY_P99
GET /             web-svc     100.00%   0.5rps           3ms           8ms          15ms
POST /api/vote    web-svc      85.71%   1.0rps           2ms           5ms          10ms
GET /api/list     web-svc     100.00%   0.5rps           1ms           2ms           3ms
```

### 5. Grafana 대시보드 확인

**목표**: Linkerd viz에 번들된 Grafana에서 시각화된 메트릭을 확인한다. `stat` CLI 출력과 동일한 데이터를 그래프로 볼 수 있다.

**단계**:
1. Grafana 포트 포워딩
   ```bash
   kubectl port-forward svc/grafana 3000:3000 -n linkerd-viz &
   ```
2. 브라우저에서 접속
   ```
   http://localhost:3000
   ```
   기본 계정: admin / admin
3. Linkerd 대시보드 찾기
   - 좌측 메뉴 → Dashboards → Browse
   - "Linkerd Deployment" 대시보드 선택
   - Namespace: `emojivoto`, Deployment: `web` 선택
4. 확인할 패널
   - Request Rate (RPS)
   - Success Rate (%)
   - Latency (P50, P95, P99)
   - Inbound/Outbound TCP connections

**검증**: Grafana 대시보드에서 emojivoto/web의 실시간 RPS와 레이턴시 그래프가 표시된다.

### 6. 의도적 오류 발생 후 성공률 변화 관찰

**목표**: 인위적으로 실패를 유발해 `stat` 성공률이 하락하는 것을 확인한다. 알림 임계값 설정 시 기준점을 체감한다.

**단계**:
1. 현재 성공률 기록
   ```bash
   linkerd viz stat deploy/voting -n emojivoto
   ```
2. voting 서비스 Pod를 0으로 스케일다운 (응답 불가 상태 만들기)
   ```bash
   kubectl scale deploy/voting -n emojivoto --replicas=0
   ```
3. 약 30초 간격으로 stat 조회
   ```bash
   watch -n 5 'linkerd viz stat deploy -n emojivoto'
   ```
4. voting에 의존하는 web의 성공률 변화 확인
   ```bash
   linkerd viz stat deploy/web -n emojivoto
   ```
5. tap으로 실패 요청 확인
   ```bash
   linkerd viz tap deploy/web -n emojivoto --path /api/vote 2>&1 | \
     grep -E ":status=5|:status=0|error"
   ```
6. 복구 후 성공률 회복 확인
   ```bash
   kubectl scale deploy/voting -n emojivoto --replicas=1
   kubectl rollout status deploy/voting -n emojivoto
   linkerd viz stat deploy -n emojivoto
   ```

**검증**:
- `voting` 스케일다운 후 `web`의 SUCCESS 컬럼이 100% → 70~80% 수준으로 하락한다.
- `voting` 복구 후 SUCCESS가 다시 100% 근처로 회복된다.

```
# 실패 상태 예시
NAME     MESHED   SUCCESS      RPS
emoji       1/1   100.00%   2.0rps
voting      0/1         -        -
web         1/1    78.57%   2.0rps   ← 성공률 하락
```

## 정리 (Cleanup)

```bash
# 포트 포워딩 종료
kill %1 %2 2>/dev/null

# ServiceProfile 삭제
kubectl delete serviceprofile web-svc.emojivoto.svc.cluster.local -n emojivoto

# emojivoto 삭제
kubectl delete namespace emojivoto

# viz 삭제가 필요한 경우
linkerd viz uninstall | kubectl delete -f -
```
