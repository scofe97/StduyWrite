> 출처: NotebookLM · 2026-11-16 · SRE 기초 — SLI·SLO·SLA 와 Error Budget (영상 「SRE Fundamentals - Understanding SLIs, SLOs, SLAs & Error Budgets」 자막 분석) · 분야: observability-keywords, devops-keywords · 미검증

## 요점

한 줄: 신뢰성은 무조건 높일 대상이 아니라 쓰도록 정해 둔 예산입니다. SLO 로 목표를 정하고 남은 Error Budget 으로 배포 속도와 안정성 투자를 가릅니다.

- 옛 측정의 함정: 헬스 체크만 보면 모든 요청이 500 을 돌려도 대시보드는 초록입니다. 쉽게 재는 인프라 상태를 쟀을 뿐 사용자 경험을 재지 못한 것입니다.
- 인센티브 충돌: 개발은 출시 속도로, 운영은 가동 시간으로 평가받습니다. 둘 다 합리적으로 움직이지만 둘을 조율할 공통 기준이 없었습니다.
- 세 층 위계:
  - SLI: 사용자가 겪는 품질을 잰 값입니다. 좋은 이벤트 ÷ 유효 이벤트, P95 지연이 예입니다.
  - SLO: SLI 에 건 내부 목표입니다. "30일 동안 요청의 99.95% 가 500ms 안에 끝남" 처럼 적습니다.
  - SLA: 고객과 맺은 계약입니다. 어기면 크레딧을 배상하니 SLO 보다 느슨하게(예: 99.5%) 잡습니다.
- 안전 마진: SLO 와 SLA 를 같게 두면 내부 경고와 계약 위반이 동시에 터집니다. 둘 사이 간격이 계약을 어기기 전에 손쓸 시간입니다.
- 9 하나의 값: 경험칙으로 가용성의 9 를 하나 더할 때마다 비용과 복잡도가 약 10배 늡니다. 장애의 주원인이 변경이라 100% 는 배포를 멈춰야만 닿습니다.
- Error Budget 계산: 30일은 43,200분이고, SLO 99.9% 면 0.1% 인 43.2분이 허용된 불완전성입니다.
- 양방향 통제:
  - 예산을 거의 안 썼다면 더 빨리 실험할 기회를 버린 것입니다.
  - 예산을 넘겼다면 합의한 정책대로 기능 배포를 멈추고 안정화에 인력을 돌립니다.
- 여정별 차등: 결제는 99.99%, 상품 탐색은 99.9%, 주문 내역 조회는 99.5% 처럼 비즈니스 영향에 따라 SLO 를 나눕니다.
- 합성 SLO:
  - 직렬로 거치는 서비스의 가용성은 곱해집니다. 99.9% 다섯 개면 0.999⁵ ≈ 99.5% 이고 월 다운타임은 약 216분으로 다섯 배가 됩니다.
  - 병렬 이중화는 둘 다 실패할 확률만 남깁니다. 99.9% 두 개면 1 − 0.001² = 99.9999% 입니다.
  - 해법은 동기 직렬 호출 줄이기, 비핵심 의존성에 서킷 브레이커와 기능 저하 적용, 종단 간 여정 SLO 우선 계측입니다.
- 운영 모델 비교: Google 은 전담 SRE 팀과 Toil 50% 상한을 둡니다. Netflix 는 전담 팀 없이 각 팀이 책임지고 카오스 엔지니어링으로 검증합니다. Amazon 은 작은 팀이 만든 서비스를 직접 운영합니다.
- 통념 넷:
  - 9 가 많을수록 좋다 → 비핵심 서비스에는 낭비입니다.
  - SLO 는 이름만 바꾼 임계치다 → 위반하면 배포를 멈추는 결정 계약입니다.
  - SRE 는 DevOps 의 동의어다 → DevOps 가 철학이면 SRE 는 그것을 구현한 규범입니다.
  - 마이크로서비스가 있어야 한다 → 모놀리스에서도 똑같이 쓰고 오히려 재기 쉽습니다.



## 핵심 키워드

| 키워드 | 한 줄 | 이미 있음 |
| :--- | :--- | :--- |
| SLI | 좋은 이벤트를 유효 이벤트로 나눠 사용자가 겪는 품질을 잰 비율 | [SLO와 알림](../../06_observability/01_Foundations/01-04.SLO와 알림 — Error Budget, Burn Rate.md) |
| SLO | SLI 에 기간과 함께 건 내부 목표로, 100% 는 목표로 두지 않는 값 | [SLO와 알림](../../06_observability/01_Foundations/01-04.SLO와 알림 — Error Budget, Burn Rate.md) |
| SLA 와 안전 마진 | 배상이 따르는 외부 계약이라 SLO 보다 낮게 잡아 대응 시간을 버는 간격 | [SLO와 알림](../../06_observability/01_Foundations/01-04.SLO와 알림 — Error Budget, Burn Rate.md) |
| 증상 기반 지표 | CPU·메모리 대신 사용자 요청의 성공률과 지연으로 장애를 판단하는 기준 | [SLO와 알림](../../06_observability/01_Foundations/01-04.SLO와 알림 — Error Budget, Burn Rate.md) |
| Error Budget | 100% 에서 SLO 를 뺀, 기간 안에 써도 되는 실패의 양 | [SLO와 알림](../../06_observability/01_Foundations/01-04.SLO와 알림 — Error Budget, Burn Rate.md) |
| Error Budget 정책 | 예산을 다 쓰면 기능 배포를 멈추고 안정화로 돌린다고 미리 합의한 규칙 | [SLO와 알림](../../06_observability/01_Foundations/01-04.SLO와 알림 — Error Budget, Burn Rate.md) |
| 9 하나당 10배 비용 | 가용성의 자릿수를 하나 올릴 때마다 비용과 복잡도가 크게 느는 경험칙 | |
| 핵심 사용자 여정 SLO | 결제·탐색·조회처럼 영향이 다른 여정마다 목표를 나누는 방식 | |
| 합성 SLO | 직렬 의존성은 가용성을 곱해 낮추고 병렬 이중화는 실패 확률을 곱해 줄이는 계산 | [Choreography Saga](../../04_messaging/05_ConsistencyPattern/01-01.Choreography Saga.md) (일부: 2PC 가용성이 참여자 가용성의 곱이라는 언급, 직렬·병렬 계산과 역산 없음) |
| Burn Rate 다중 창 알람 | 예산이 사라지는 속도를 긴 창과 짧은 창에 함께 걸어 급한 장애에만 호출하는 알람 | [SLO와 알림](../../06_observability/01_Foundations/01-04.SLO와 알림 — Error Budget, Burn Rate.md) |
| 요청 기반·윈도우 기반 SLO | 좋은 요청 비율과 좋은 시간 창 비율의 차이, 저트래픽에서 생기는 왜곡 | [SLO 를 Prometheus 로](../../06_observability/book/mastering_prometheus/13-01.SLO 를 Prometheus 로 정의하고 알림하기 — 요청·윈도우 기반과 Sloth·Pyrra.md) |
| Sloth·Pyrra | SLO 선언에서 Prometheus 기록 규칙과 소진율 알람을 만들어 주는 도구 | [SLO 를 Prometheus 로](../../06_observability/book/mastering_prometheus/13-01.SLO 를 Prometheus 로 정의하고 알림하기 — 요청·윈도우 기반과 Sloth·Pyrra.md) |
| 백분위·꼬리 지연 | 평균이 숨기는 느린 요청을 P95·P99 로 드러내는 지연 측정 | [성능 — 응답 시간과 처리량](../../05_data/book/designing-data-intensive-applications/02-02.성능 — 응답 시간과 처리량.md) |
| Toil 상한 | 반복 운영 작업 비율에 상한을 두고 나머지 시간을 자동화에 쓰게 하는 규범 | [How to Monitor Your Systems](../../07_devops/book/fdsd_fundamentals-devops/10-01.How to Monitor Your Systems.md) (일부: Toil 비율 측정과 20% 미만 목표, 50% 상한과 서비스 반납 없음) |
| 비난 없는 사후 검토 | 사람 대신 시스템의 원인을 찾아 재발 방지 작업으로 잇는 장애 기록 | [사고 관리](../../06_observability/book/observability_with_grafana/09-01.사고 관리 — 금은동 지휘·SLI 알림·IRM 도구 셋.md) |
| 카오스 엔지니어링 | 운영 중에 결함을 일부러 넣어 복원 장치가 늘 시험되게 하는 방법 | [신뢰성과 내결함성](../../05_data/book/designing-data-intensive-applications/02-03.신뢰성과 내결함성.md) (일부: 결함 주입의 원리, 인스턴스 무작위 종료 도구 운영 사례 없음) |
| 서킷 브레이커·기능 저하 | 비핵심 의존성의 장애가 여정 전체 실패로 번지지 않게 끊고 대체 응답을 주는 장치 | [실패를 견디는 일을 프록시로](../../08_cloud/book/istio-in-action/06-01.실패를 견디는 일을 프록시로 옮겼을 때.md) (일부: 프록시 서킷 브레이킹 설정, 캐시 폴백 같은 기능 저하 설계 없음) |
| OpenSLO | SLI·SLO·알람 정책을 벤더 중립 YAML 로 적는 명세 | |



## 자료와 실습

- 자료:
  - [SRE Book 4장 Service Level Objectives](https://sre.google/sre-book/service-level-objectives/): SLI 정의, 백분위 선택, SLO 와 예산 정책의 원전입니다. 정독 노트는 [SLO와 알림](../../06_observability/01_Foundations/01-04.SLO와 알림 — Error Budget, Burn Rate.md) 입니다.
  - [SRE Workbook 2장 Implementing SLOs](https://sre.google/workbook/implementing-slos/)·5장 Alerting on SLOs: 임계치 알람을 걷어내고 다중 창 소진율 알람을 설계하는 실무 표준입니다.
  - [OpenSLO 명세](https://openslo.com/): SLO 를 선언형 YAML 로 코드화하는 오픈 표준입니다.
  - [Site Reliability Engineering: Measuring and Managing Reliability (Coursera)](https://www.coursera.org/learn/site-reliability-engineering-slos): SLI 고르기부터 소진율 알람 계산까지 실습하는 강의입니다.
  - [Sloth 문서](https://sloth.dev/): 성공률·지연 메트릭에서 다중 창 소진율 알람을 생성하는 가이드입니다. 정독 노트는 [SLO 를 Prometheus 로](../../06_observability/book/mastering_prometheus/13-01.SLO 를 Prometheus 로 정의하고 알림하기 — 요청·윈도우 기반과 Sloth·Pyrra.md) 입니다.
  - 『Site Reliability Engineering』 1부~2부(3장 위험 수용, 4장 SLO, 5장 Toil 제거, 6장 분산 시스템 모니터링): 영상 전체의 이론 골격입니다.
  - 『The Site Reliability Workbook』 1~5장: SLO 정의·구현·알람 설계와 예산 정책 예시입니다.
  - 『Implementing Service Level Objectives』 1부~2부: 사용자 여정 매핑, 좋은 이벤트 비율의 수학, 의존성 계산, 조직 설득을 다룹니다.
  - 코드: `pyrra-dev/pyrra` 의 `slo/slo.go`(소진율 공식과 1h/5m·6h/30m 다중 창 규칙 생성)를 봅니다. `slok/sloth` 의 `internal/prometheus/recording_rules.go`(쿼리 부하를 줄이는 사전 집계)와 `OpenSLO/osloc` 의 `pkg/manifest/`(SLI·SLO·알람 정책 스키마 검증)도 봅니다.
- 실습:
  - Level 1: 직렬 N개와 병렬 이중화 그룹 M개의 가용성을 받아 합성 가용성과 월 허용 다운타임을 내는 CLI 를 Go 나 Python 으로 만듭니다. 여정 목표 99.9% 를 맞추려면 개별 서비스가 가져야 할 SLO 도 역산합니다. 함정은 직렬 의존성이 10개만 돼도 개별 서비스에 99.99% 를 요구하는 비현실적 값이 나오는 것입니다. 완료: 직렬 다섯 개 99.5%·월 216분, 병렬 결제 둘 99.9999% 가 맞고, 비핵심 의존성을 비동기로 뺐을 때의 개선을 수치로 출력합니다.
  - Level 2: 총 요청과 5xx·500ms 초과 요청을 나눠 노출하는 샘플 API 를 만듭니다. Sloth 나 Pyrra 로 99.9%(30일, 예산 43.2분) SLO 를 선언하고, 1시간에 예산 2% 이상을 태우는(14.4배) 경우에만 울리는 알람을 겁니다. 함정은 새벽처럼 트래픽이 적을 때 에러 1~2건만으로 알람이 오탐으로 울리는 것입니다. 완료: k6·hey 로 100 RPS 를 흘리며 1초 단발 에러에는 알람이 없고 5% 지속 에러에는 울리는 것을 Grafana 의 잔여 예산 추이로 확인합니다.
  - Level 3: Prometheus API 로 잔여 예산을 계산하는 검증기를 GitHub Actions 나 Argo Rollouts 의 배포 전 단계에 붙입니다. 잔여 예산이 10% 미만이면 일반 기능 배포를 막고 `[hotfix]`·`[reliability]` 라벨만 통과시킵니다. 함정은 복구용 핫픽스까지 예산 고갈로 막혀 복구가 늦어지는 교착입니다. 완료: 예산을 0% 로 만든 뒤 일반 배포 차단과 핫픽스 통과가 각각 파이프라인 로그에 차단 사유·잔여 예산과 함께 남습니다.



## 경고

- ⚠ 10배 경험칙: 9 하나당 비용이 약 10배 는다는 것과 단계별 필요 기술 목록은 리포트가 경험칙으로 든 것입니다. 측정 근거와 대조하지 않았습니다.
- ⚠ 장애 사례 수치: Knight Capital 사례의 45분(자막은 35분)·약 4억 4천만 달러 손실과 2017년 S3 장애(명령 오타, 약 4시간)는 리포트의 사실 확인입니다. 1차 자료로 대조하지 않았습니다.
- ⚠ 운영 모델 서술: 전담 SRE 팀의 50:50 구성, Toil 50% 상한과 서비스 반납, 다른 회사의 전담 팀 부재는 리포트의 정리입니다. 정독 노트의 Toil 목표는 20% 미만이라 기준이 다릅니다.
- ⚠ 자막 수치: 자막이 99.9% 의 월 다운타임을 33분으로 말한 대목을 리포트가 43.2분으로 고쳤습니다. 연 기준이면 약 8.76시간(월평균 약 43.8분)입니다.
- ⚠ 코드 경로: pyrra·sloth·osloc 의 파일 경로와 `osloc` 저장소가 지금도 유지되는지 확인하지 않았습니다.
- ⚠ 자막 교정과 뺀 것: 자동 자막의 오인식(`arrow budget`, `tile`, `Night Capital` 등)은 리포트가 고쳤습니다. 책 저자 이름과 인용 발언자 이름은 뺐습니다.
