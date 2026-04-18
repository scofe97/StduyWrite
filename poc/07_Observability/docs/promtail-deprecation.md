
# Promtail Deprecation 및 Grafana Alloy 마이그레이션 가이드

## 개요
Grafana Labs는 2025년부터 **Promtail**을 공식적으로 **deprecated** 선언하고, 모든 기능을 **Grafana Alloy**로 통합했습니다.  
Promtail은 더 이상 새로운 기능이 개발되지 않으며, 곧 지원이 완전히 종료됩니다.

> **Promtail EOL**: 2026-03-02부로 도달. 마이그레이션 필수.

## Promtail 지원 일정 (공식 발표 기준)

| 단계                  | 날짜                | 내용                                                                 |
|-----------------------|---------------------|----------------------------------------------------------------------|
| Deprecated & LTS 시작 | 2025년 2월 13일    | 새 기능 개발 완전 중단<br>치명적 버그 수정 및 보안 패치만 제공       |
| LTS 종료              | 2026년 2월 28일    | 상업적 지원 종료                                                    |
| **End-of-Life (EOL)** | **2026년 3월 2일** | 모든 업데이트, 버그 수정, 보안 패치 제공 중단<br>**사용 금지 권장** |

## 왜 Promtail이 deprecated 되었나요?
- 과거 Grafana 생태계는 여러 개별 에이전트가 존재했습니다.
  - 로그 수집 → Promtail
  - 메트릭스 수집 → Prometheus Agent
  - 트레이싱 → 별도 도구
- 이제 **하나의 통합 에이전트**로 모든 telemetry 데이터를 처리하고자 함
- **Grafana Alloy**는 OpenTelemetry Collector를 기반으로 하여:
  - 로그 (Loki)
  - 메트릭스 (Prometheus/Mimir)
  - 트레이스 (Tempo)
  - 프로파일링
  을 **하나의 바이너리**로 모두 지원

→ 앞으로 모든 신규 기능 및 업데이트는 **Alloy에서만** 진행됩니다.

## Grafana 스택별 역할 정리

| 컴포넌트    | 역할                          | 수집 대상       | 추천 에이전트       |
|------------|-------------------------------|-----------------|---------------------|
| Loki       | 로그 저장 및 쿼리 백엔드       | 로그            | Grafana Alloy      |
| Tempo      | 분산 트레이싱 저장 및 쿼리 백엔드 | 트레이스 (spans) | Grafana Alloy      |
| Mimir      | 메트릭스 장기 저장 백엔드      | 메트릭스        | Grafana Alloy      |
| Prometheus | 메트릭스 단기 저장 및 쿼리     | 메트릭스        | Grafana Alloy      |

> **Promtail과 Tempo는 서로 다른 목적**입니다.  
> Tempo는 로그를 수집하지 않으며, Promtail은 트레이스를 수집하지 않습니다.

## Grafana Alloy의 장점
- 하나의 에이전트로 로그 + 메트릭스 + 트레이스 수집 → 운영 단순화
- OpenTelemetry 네이티브 지원 (산업 표준 준수)
- Grafana UI에서 구성 그래프 시각화 가능
- 지속적인 업데이트 및 신규 기능 보장
- Promtail 대비 더 나은 성능과 유연성

## 마이그레이션 방법 (Promtail → Alloy)
Grafana에서 제공하는 **자동 변환 도구**를 사용하면 매우 간단합니다.

### 1. 명령어로 변환
```bash
alloy convert --source-format=promtail --output=alloy-config.river promtail-config.yaml
```

### 2. 변환 보고서 확인 (호환성 체크)
```bash
alloy convert --source-format=promtail --report=report.txt promtail-config.yaml
```

- 대부분의 설정이 자동 변환됩니다.
- 변환되지 않는 부분은 보고서에서 확인 후 수동 수정

### 3. 공식 마이그레이션 가이드
https://grafana.com/docs/alloy/latest/set-up/migrate/from-promtail/

### Kubernetes 사용자
- 기존 Promtail Helm 차트/DaemonSet → Grafana Alloy Helm 차트로 교체
- Grafana 공식 Helm 리포지토리에 Alloy 차트 제공

## 결론 및 추천
- **2026년 3월 2일 EOL**이 임박했습니다.
- 기존 Promtail을 사용 중이라면 **지금 바로 Grafana Alloy로 마이그레이션**하세요.
- 신규 구축 시에는 **처음부터 Alloy 사용**을 강력 추천합니다.

Alloy 하나로 모든 observability 데이터를 처리할 수 있어 장기적으로 훨씬 안정적이고 효율적입니다!

## 참고 링크
- Grafana Alloy 공식 문서: https://grafana.com/docs/alloy/latest/
- Promtail → Alloy 마이그레이션 가이드: https://grafana.com/docs/alloy/latest/set-up/migrate/from-promtail/
- Grafana Loki 문서: https://grafana.com/docs/loki/latest/
- Grafana Tempo 문서: https://grafana.com/docs/tempo/latest/