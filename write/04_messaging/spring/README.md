---
title: 04_messaging/spring — 해체 안내 (2026-05-23)
tags: [redirect, migration]
status: archived
related:
  - ../README.md
updated: 2026-05-23
---

# spring/ 폴더 해체 안내

> 이 폴더는 2026-05-23 에 해체됐다. 기존 16개 파일은 *기술 출처*(spring) 기준 분리에서 *주제 기준* 분리로 재배치됐다. 이 README는 검색·구 링크 추적용 redirect 표만 남긴다.

## 옛 위치 → 새 위치 매핑

| 옛 파일 (spring/) | 새 위치 |
|---|---|
| `01-01.CloudEventsHeaderInterceptor.md` | [`../01_MessageContract/01-09.CloudEventsHeaderInterceptor.md`](../01_MessageContract/01-09.CloudEventsHeaderInterceptor.md) |
| `01-02.TopicConfig와 파티션 설계.md` | [`../02_TopicDesign/02-04.TopicConfig와 파티션 설계.md`](../02_TopicDesign/02-04.TopicConfig와%20파티션%20설계.md) |
| `02-01.Avro Consumer 수신 패턴.md` | [`../01_MessageContract/01-08.Avro Consumer 수신 패턴.md`](../01_MessageContract/01-08.Avro%20Consumer%20수신%20패턴.md) |
| `03-01.Spring Kafka DLT와 Producer Config.md` | [`../04_ConsistencyPattern/04-10.Spring Kafka DLT와 Producer Config.md`](../04_ConsistencyPattern/04-10.Spring%20Kafka%20DLT와%20Producer%20Config.md) |
| `03-02.DlqConsumer.md` | [`../04_ConsistencyPattern/04-11.DlqConsumer.md`](../04_ConsistencyPattern/04-11.DlqConsumer.md) |
| `03-03.Kafka 예외 처리 통합.md` | [`../04_ConsistencyPattern/04-12.Kafka 예외 처리 통합.md`](../04_ConsistencyPattern/04-12.Kafka%20예외%20처리%20통합.md) |
| `03-04.KafkaErrorConfig DLT 헤더 폭증 사고.md` | [`../04_ConsistencyPattern/04-13.KafkaErrorConfig DLT 헤더 폭증 사고.md`](../04_ConsistencyPattern/04-13.KafkaErrorConfig%20DLT%20헤더%20폭증%20사고.md) |
| `03-05.Backoff 전략 비교와 선택.md` | [`../04_ConsistencyPattern/04-14.Backoff 전략 비교와 선택.md`](../04_ConsistencyPattern/04-14.Backoff%20전략%20비교와%20선택.md) |
| `04-01.trace-id와 traceparent.md` | [`../01_MessageContract/01-10.trace-id와 traceparent.md`](../01_MessageContract/01-10.trace-id와%20traceparent.md) |
| `05-01.Spring Kafka 운영 고급.md` | [`../03_BrokerArchitecture/03-09.Spring Kafka 운영 고급.md`](../03_BrokerArchitecture/03-09.Spring%20Kafka%20운영%20고급.md) |
| `05-02.Manual Ack와 Offset Commit 정책.md` | [`../03_BrokerArchitecture/03-10.Manual Ack와 Offset Commit 정책.md`](../03_BrokerArchitecture/03-10.Manual%20Ack와%20Offset%20Commit%20정책.md) |
| `05-03.Batch Listener와 부분 실패 처리.md` | [`../03_BrokerArchitecture/03-11.Batch Listener와 부분 실패 처리.md`](../03_BrokerArchitecture/03-11.Batch%20Listener와%20부분%20실패%20처리.md) |
| `06-01.message-lib config 5개 클래스 종합.md` | [`../03_BrokerArchitecture/03-12.message-lib config 5개 클래스 종합.md`](../03_BrokerArchitecture/03-12.message-lib%20config%205개%20클래스%20종합.md) |
| `06-02.message-lib config 학습 검증.md` | [`../03_BrokerArchitecture/03-13.message-lib config 학습 검증.md`](../03_BrokerArchitecture/03-13.message-lib%20config%20학습%20검증.md) |
| `06-03.message-lib config 운영 이식 가이드.md` | [`../03_BrokerArchitecture/03-14.message-lib config 운영 이식 가이드.md`](../03_BrokerArchitecture/03-14.message-lib%20config%20운영%20이식%20가이드.md) |

## 해체 사유

옛 분담 (개념은 상위 / 코드 디테일은 spring/) 은 같은 주제(예: Avro 직렬화)가 두 폴더에 흩어져 학습 동선이 끊겼다. *주제* 축 하나로 재배치하면서 "왜 → 어떻게 → 사고 회고"가 한 폴더에 모이도록 했다. 폴더 안 넘버링으로 *개념 → 코드 → 운영* 서브그룹을 구분한다.

상세 컨텍스트는 상위 [`../README.md`](../README.md) "경계 기준" 섹션과 "변경 요약" 노트 참조.
