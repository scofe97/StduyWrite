---
title: 99_ETC/대본 — 쿠버네티스와 리눅스 커널 강의 대본
tags: [moc, kubernetes, linux, kernel, transcript]
status: final
related:
  - ../README.md
updated: 2026-09-05
---

# 99_ETC/대본
---
> 쿠버네티스와 리눅스 커널을 다루는 강의 3편의 대본입니다. 자동 생성 자막(DownSub)을 사람이 읽기 좋게 정리한 것으로, 강사의 설명 흐름과 말투는 그대로 두고 음성인식 오타와 줄바꿈만 교정했습니다.

## 보는 순서

세 편은 이어지는 한 강의입니다. 커널이 무엇을 하는지 본 뒤(Ch-01), 그 커널에 kubectl 이 어떻게 닿는지 보고(Ch-02), 마지막으로 격리의 실체인 네임스페이스로 내려갑니다(Ch-03).

| 회차 | 대본 | 원본 | 길이 |
|------|------|------|------|
| Ch-01 | [쿠버네티스와 리눅스 커널](./2026-06-08_%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4%EC%99%80%20%EB%A6%AC%EB%88%85%EC%8A%A4%20%EC%BB%A4%EB%84%90%20%EB%8C%80%EB%B3%B8.md) | [영상](https://www.youtube.com/watch?v=OjoUal1JPcM) | 1:49:05 |
| Ch-02 | [kubectl과 리눅스 커널](./2026-06-08_kubectl%EA%B3%BC%20%EB%A6%AC%EB%88%85%EC%8A%A4%20%EC%BB%A4%EB%84%90%20%EB%8C%80%EB%B3%B8.md) | [영상](https://www.youtube.com/watch?v=XsgYsvgA0Ow) | 1:12:17 |
| Ch-03 | [리눅스 네임스페이스](./2026-06-08_%EB%A6%AC%EB%88%85%EC%8A%A4%20%EB%84%A4%EC%9E%84%EC%8A%A4%ED%8E%98%EC%9D%B4%EC%8A%A4%20%EB%8C%80%EB%B3%B8.md) | [영상](https://www.youtube.com/watch?v=oMKB93KuPsk) | 1:45:10 |

파일명은 [99_ETC 규칙](../README.md)에 따라 `날짜_주제`입니다. 세 편이 같은 날 들어와 날짜만으로는 순서가 서지 않으므로, 회차는 이 표와 각 문서의 제목(`[Ch-01] …`)이 갖습니다.

## 읽는 법

섹션 옆 `[mm:ss]` / `[h:mm:ss]`는 SRT 자막 기준 실제 영상 시각이며 섹션이 시작하는 지점입니다. 영상을 틀어 두고 같이 읽도록 만든 문서라, 요약본이 아니라 발화를 그대로 옮긴 분량입니다.
