# Observability 학습 문서

Observability 이론부터 텔레메트리 파이프라인 실전까지 체계적으로 정리한 학습 자료입니다.

---

## 폴더 구조

```
Observability/
├── README.md                      # 이 파일
├── 01_개념과_이론/                 # Observability 핵심 이론
└── 02_텔레메트리_파이프라인/       # 텔레메트리 파이프라인 실전
```

---

## 학습 경로

### 입문자
```
01_개념과_이론/01_Observability란 → 02 → 03 → 04
```

### 실무 적용
```
01_개념과_이론/05_SLO_기반_알림 → 02_텔레메트리_파이프라인 전체
```

### AI/LLM 관심
```
01_개념과_이론 전체 → 08_LLM을_위한_Observability
```

---

## 폴더별 내용

### 01_개념과_이론
Observability의 핵심 이론과 실무 적용

| 파일 | 내용 | 출처 |
|------|------|------|
| 01_Observability란.md | Observability 정의, 수학적 기원 | OE Ch.1 |
| 02_Observability의_기원.md | 소프트웨어에서의 Observability 역사 | OE Ch.2 |
| 03_Observability_분석_시작하기.md | 분석 시작 가이드, 도구 활용 | OE Ch.3 |
| 04_Observability_주도_개발.md | ODD(Observability Driven Development) | OE Ch.4 |
| 05_SLO_기반_알림과_디버깅.md | SLO/SLI, 알림 설계, 디버깅 | OE Ch.5 |
| 06_효율적_데이터_저장.md | Retriever, 데이터 저장 최적화 | OE Ch.6 |
| 07_성능_엔지니어링.md | Observability와 성능 최적화 | OE Ch.7 |
| 08_LLM을_위한_Observability.md | LLM/AI 시스템 Observability | OE Ch.8 |

### 02_텔레메트리_파이프라인
텔레메트리 데이터 파이프라인 구축과 운영

| 파일 | 내용 | 출처 |
|------|------|------|
| 01_파이프라인의_필요성.md | 파이프라인 필요성, 가치 사슬 | TFP Ch.1 |
| 02_도메인_언어.md | Sources, Processors, Destinations | TFP Ch.2 |
| 03_파이프라인_관리.md | 파이프라인 운영, 모니터링 | TFP Ch.3 |
| 04_비용_관리.md | 비용 최적화 전략 | TFP Ch.4 |
| 05_컴플라이언스.md | 규정 준수, 데이터 보안 | TFP Ch.5 |
| 06_결론.md | 요약 및 다음 단계 | TFP Ch.6 |

---

## 출처 약어

| 약어 | 원본 |
|------|------|
| OE | Observability Engineering (O'Reilly) |
| TFP | The Fundamentals of Telemetry Pipelines |

---

## 핵심 개념

### Observability란?
> 시스템의 **외부 출력(external outputs)**을 통해 **내부 상태(internal state)**를 얼마나 잘 추론하고 디버깅할 수 있는지를 측정하는 속성

### 세 가지 신호 (Three Pillars)
| 신호 | 설명 | 용도 |
|------|------|------|
| **Metrics** | 수치 측정값 | 성능 추세, 알림 |
| **Logs** | 이벤트 기록 | 상세 디버깅 |
| **Traces** | 요청 흐름 추적 | 분산 시스템 분석 |

### 텔레메트리 파이프라인 구조
```
Sources → Processors → Destinations
 (수집)     (처리)      (저장/전송)
```

---

## 학습 체크리스트

### 기본
- [ ] Observability와 Monitoring의 차이 설명
- [ ] 세 가지 신호(Metrics, Logs, Traces) 이해
- [ ] SLO/SLI/SLA 개념 구분

### 실무
- [ ] ODD(Observability Driven Development) 적용
- [ ] 텔레메트리 파이프라인 설계
- [ ] 비용 최적화 전략 수립

### 심화
- [ ] LLM 시스템 Observability 설계
- [ ] 컴플라이언스 요구사항 반영

---

## 참고 자료

### 도서
- **Observability Engineering** - Charity Majors, Liz Fong-Jones, George Miranda
- **The Fundamentals of Telemetry Pipelines** - Cribl

### 공식 문서
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)

---

*마지막 업데이트: 2026-01-25*
