---
title: 04_messaging/docs/franz-go — franz-go Kafka 클라이언트 읽기 지도
tags: [moc, franz-go, kgo, kadm, kafka-client, go, official-docs]
status: draft
source:
  - https://raw.githubusercontent.com/twmb/franz-go/v1.22.2/README.md
  - https://pkg.go.dev/github.com/twmb/franz-go/pkg/kgo@v1.22.2
  - https://pkg.go.dev/github.com/twmb/franz-go/pkg/kadm@v1.19.0
related:
  - ../README.md
  - ../../README.md
  - ../../04_BrokerArchitecture/06-02.AdminClient 설정·컨슈머그룹·클러스터.md
  - ../../04_BrokerArchitecture/01-05.오프셋 커밋 API.md
created: 2026-11-25
updated: 2026-11-25
---

# 04_messaging/docs/franz-go — franz-go Kafka 클라이언트 읽기 지도

---

> franz-go 는 순수 Go 로 만든 Kafka 클라이언트입니다. 이 폴더는 그 패키지 문서(pkg.go.dev)를 1차 자료로 삼아 `kgo` 와 `kadm` 을 한 편에 정리합니다.

## 문서 목록

> 아직 한 편뿐이라 읽는 순서는 없습니다. 편이 늘면 연재처럼 번호를 붙일지 그때 정합니다.

| 문서 | 공식 주소 | 한 줄 소개 |
|------|----------|-----------|
| [kgo·kadm](kgo·kadm.md) | [kgo](https://pkg.go.dev/github.com/twmb/franz-go/pkg/kgo@v1.22.2) · [kadm](https://pkg.go.dev/github.com/twmb/franz-go/pkg/kadm@v1.19.0) | 클라이언트 생성과 동기 발행, 그룹 소비의 자동 커밋과 직접 커밋, `kadm` 으로 컨슈머 lag 계산 |



## 이 폴더가 다른 노트와 나누는 일

> Kafka 의 개념은 번호 폴더의 노트가 맡고, 이 폴더는 Go 클라이언트의 옵션과 함수를 맡습니다.

오프셋 커밋과 컨슈머 lag 의 개념은 Java 클라이언트 기준으로 이미 있습니다. 이 폴더의 편은 개념을 다시 풀지 않고 아래 노트로 잇습니다.

| 노트 | 그 노트에서 볼 것 |
|------|------------------|
| [AdminClient 설정·컨슈머그룹·클러스터](../../04_BrokerArchitecture/06-02.AdminClient%20설정·컨슈머그룹·클러스터.md) | 커밋 오프셋과 파티션 최신 오프셋의 차이로 lag 을 구하는 흐름 |
| [오프셋 커밋 API](../../04_BrokerArchitecture/01-05.오프셋%20커밋%20API.md) | 자동 커밋·동기 커밋·비동기 커밋의 동작 차이 |



## 1차 자료

> 주소는 모두 버전을 고정했습니다. 버전 없는 주소는 다음 릴리스가 나오면 다른 문서를 보여 줍니다.

- franz-go README (v1.22.2): <https://raw.githubusercontent.com/twmb/franz-go/v1.22.2/README.md>
- `kgo` 패키지 문서 (v1.22.2): <https://pkg.go.dev/github.com/twmb/franz-go/pkg/kgo@v1.22.2>
- `kadm` 패키지 문서 (v1.19.0): <https://pkg.go.dev/github.com/twmb/franz-go/pkg/kadm@v1.19.0>



## 관련 문서

- [docs MOC](../README.md) — 04_messaging/docs 폴더 규칙과 전체 목록
- [04_messaging MOC](../../README.md) — 메시징 카테고리 전체 지도
