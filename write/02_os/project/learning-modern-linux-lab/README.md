---
title: learning-modern-linux-lab — 프로젝트 인덱스
tags: [moc, study-index, lab, linux, logging, journald, rsyslog]
status: draft
source:
  - ~/study/runners-lab/os/learning-modern-linux  # 8장 공용 실습 lab, OrbStack Debian 12·Rocky 9.8·Ubuntu 24.04 머신
related:
  - ../../book/learning-modern-linux/README.md
  - ../../docs/cmd/README.md
updated: "2026-11-16"
---

# learning-modern-linux-lab — 프로젝트 인덱스

---

> 『Learning Modern Linux』 정독 노트가 적은 동작을 실제 리눅스 머신에서 다시 확인하는 실습의 기록 폴더입니다. 실행 환경과 명령은 실습 저장소에 두고, 이 폴더에는 장면마다 예측·관측·해석만 적습니다.

## 이 폴더는 무엇인가

> 노트의 Phase 1 에서 틀렸거나 몰랐던 장면을 머신에서 돌려 보고, 예측과 실제 출력을 맞댑니다. 개념 설명은 책 노트에 있으므로 여기서는 링크로 대신합니다.

8장 08-01 학습에서 막힌 곳은 대부분 「누가 이 일을 하나」였습니다. 수집 주체를 rsyslog 로 보거나, 파일 이름과 압축 여부를 「OS 가 정한다」고 읽었습니다. 그래서 같은 명령을 Debian 12 와 Rocky 9 에서 나란히 돌려, 결과를 가르는 것이 배포판인지 도구의 설정인지를 눈으로 확인합니다.

실습 환경은 `~/study/runners-lab/os/learning-modern-linux`(GitHub 모노레포 `scofe97/StudyLab`)에 있습니다. 맥북의 OrbStack 2.2.5 로 머신 세 대(`lml-deb`, `lml-rocky`, `lml-ubuntu`)를 띄웁니다. Ubuntu 24.04 는 실무에서 가장 많이 쓰는 배포판이라 결과를 한 번 더 맞대 보려고 둡니다.

## 진행 방식

> 장면마다 결과를 먼저 예측하고, 명령을 직접 돌린 뒤 예측과 비교합니다.

예측은 실행 전에 적고 실행 뒤에도 고치지 않습니다. 어긋난 자리가 다음에 다시 볼 곳이기 때문입니다.

## 08-01 로그 한 줄의 흐름

> 로그 한 줄의 일생(생산 → 수집 → 분배 → 조회 → 정리)을 따라 다섯 장면을 차례로 돌립니다.

뒤 장면이 앞 장면의 결과를 쓰므로 순서대로 진행합니다. 노트는 [08-01](../../book/learning-modern-linux/08-01.재는%20것은%20바깥이고%20알고%20싶은%20것은%20안이다.md)입니다.

| # | 장면 | 확인하는 것 | 상태 |
|---|---|---|---|
| 1 | `logger -t nginx` 로 보낸 줄과 서비스가 낸 줄의 필드 비교, grep 과 `journalctl -u` 비교 | 신뢰 필드는 journald 가 커널에서 얻어 적는다 | 대기 |
| 2 | `Storage=none` 뒤 Debian `/var/log/syslog` 와 Rocky `/var/log/messages` | journald 가 밀어 주는 길과 rsyslog 가 읽어 가는 길의 차이 | 대기 |
| 3 | `*.err` 규칙을 더하고 `crit`·`info` 줄 보내기 | 선택자의 심각도는 문턱이다 | 대기 |
| 4 | `/var/log/journal` 이 없을 때 재부팅 뒤 `journalctl -b -1` | 저널이 메모리에만 있으면 재부팅 때 사라진다 | 대기 |
| 5 | 활성 저널 파일을 `rm` 한 뒤 `df` 와 새 줄, 그다음 `--vacuum-size` | 열린 파일 기술자가 inode 를 붙잡는다, 저널 정리는 journald 몫이다 | 대기 |
