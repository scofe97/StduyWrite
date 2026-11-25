---
title: 02_os/docs/filesystem — 파일시스템 배치와 구현
tags: [moc, linux, filesystem, fhs, ostree, storage]
status: final
related:
  - ../../os-keywords.md
  - ../../README.md
  - ../kernel/README.md
  - ../../book/learning-modern-linux/05-01.모든 것이 파일이라는 말은 손잡이가 하나라는 뜻이다.md
updated: 2026-11-25
---

# 02_os/docs/filesystem

---

> 리눅스 파일시스템의 두 축인 디렉터리 배치 표준(FHS·불변 OS)과 파일시스템 종류·구현(ext4·XFS·tmpfs, inode·저널링)을 정리합니다. OverlayFS 와 마운트 propagation 은 [docs/kernel/](../kernel/README.md)이 정본입니다.

## 범위와 경계

> 이 폴더는 디렉터리 계층 규칙과 로컬 파일시스템 구현 두 주제를 함께 맡으며, 커널 마운트·컨테이너 레이어 메커니즘과 경계를 나눕니다.

- 디렉터리 배치(FHS 두 축, `/opt` 번들, 불변 OS): 이번 01-01 문서에서 다룹니다. 기본 12개 폴더 표와 바인드 마운트 기초는 [LML 05-01 §6](../../book/learning-modern-linux/05-01.%EB%AA%A8%EB%93%A0%20%EA%B2%83%EC%9D%B4%20%ED%8C%8C%EC%9D%BC%EC%9D%B4%EB%9D%BC%EB%8A%94%20%EB%A7%90%EC%9D%80%20%EC%86%90%EC%9E%A1%EC%9D%B4%EA%B0%80%20%ED%95%98%EB%82%98%EB%9D%BC%EB%8A%94%20%EB%9C%BB%EC%9D%B4%EB%8B%A4.md#6-%EC%96%B4%EB%94%94%EC%97%90-%EB%AC%B4%EC%97%87%EC%9D%84-%EB%91%90%EB%8A%94%EA%B0%80)가 정본입니다.
- 파일시스템 종류·구현(ext4·XFS·tmpfs, inode·저널링 — How Linux Works 4장): 예정입니다.
- 경계: OverlayFS 와 mount propagation 은 [docs/kernel/](../kernel/README.md)이 정본입니다.



## 문서

> 공통 개념은 번호 파일(`NN-NN.`)로 순서를 매겨 배치합니다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 01-01 | [FHS와 불변 OS — 파일을 어디에 두는가](./01-01.FHS%EC%99%80%20%EB%B6%88%EB%B3%80%20OS%20%E2%80%94%20%ED%8C%8C%EC%9D%BC%EC%9D%84%20%EC%96%B4%EB%94%94%EC%97%90%20%EB%91%90%EB%8A%94%EA%B0%80.md) | FHS 두 축과 관리 주체로 경로가 어떻게 갈리고, OSTree 불변 OS 와 컨테이너에서는 그 경계가 어떻게 바뀌는가? |
| 예정 | 파일시스템 종류·구현 (ext4·XFS·tmpfs, inode·저널링) | 로컬 파일시스템의 디스크 구조와 저널링은 어떻게 동작하는가? (How Linux Works 4장, 미작성) |



## 관련 문서

- 통합 경로: [OS 학습 로드맵](../../os-keywords.md) — 1단계 Linux 사용 진입점
- 상위: [02_os/ MOC](../../README.md)
- 이웃: [02_os/docs/kernel/](../kernel/README.md) — OverlayFS·mount propagation 정본
- 기초 정본: [LML 05-01 §6 어디에 무엇을 두는가](../../book/learning-modern-linux/05-01.%EB%AA%A8%EB%93%A0%20%EA%B2%83%EC%9D%B4%20%ED%8C%8C%EC%9D%BC%EC%9D%B4%EB%9D%BC%EB%8A%94%20%EB%A7%90%EC%9D%80%20%EC%86%90%EC%9E%A1%EC%9D%B4%EA%B0%80%20%ED%95%98%EB%82%98%EB%9D%BC%EB%8A%94%20%EB%9C%BB%EC%9D%B4%EB%8B%A4.md#6-%EC%96%B4%EB%94%94%EC%97%90-%EB%AC%B4%EC%97%87%EC%9D%84-%EB%91%90%EB%8A%94%EA%B0%80) — FHS 12개 폴더 표·바인드 마운트
- 활용처: [08_cloud/docs/kubernetes/](../../../08_cloud/docs/kubernetes/README.md) — 컨테이너·스토리지 운영
