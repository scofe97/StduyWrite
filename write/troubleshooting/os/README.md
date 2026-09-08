---
title: troubleshooting/os — 계층 A
tags: [moc, troubleshooting, os]
status: draft
related:
  - ../README.md
  - ../_drill/sources.md
updated: 2026-09-07
---

# troubleshooting/os

---

> 리눅스 호스트 한 대 안에서 생기는 일입니다. 소켓·conntrack·MTU·라우팅·NIC 카운터가 여기 속합니다.

파일명이 증상입니다. 날짜순으로 쌓이니 훑으면 됩니다.

## 이 계층에서 반복되는 습관

> 걷어낸 사례집 41건을 관통하던 것 셋입니다. 계층이 달라도 잘 옮겨 가는 축이라 남깁니다.

죽이기 전에 기록을 남깁니다. 프로세스를 `kill` 하거나 파일을 지우면 원인을 말해 줄 상태가 함께 사라집니다.

응급 조치와 재발 방지를 구분합니다. 상한을 올리는 일은 시간을 버는 것이지 원인을 없애는 것이 아닙니다.

도구가 안 보여 준 것을 없다고 읽지 않습니다. `tcpdump` 는 NIC 를 지난 패킷만 보고 `ss` 는 소켓 계층만 봅니다. 한 도구로 결론을 내면 그 도구의 사각이 그대로 결론의 사각이 됩니다.

## 관련 문서

- [troubleshooting 지도](../README.md) — 계층 표와 여는 절차
- [출제 소스](../_drill/sources.md) — 이 계층의 근거 노트
