# Jenkins JVM Tuning Lab

Spring Boot 애플리케이션을 Jenkins가 빌드·배포·호출하는 구조 위에서, JVM 병목을 부하로 재현하고 GC 로그와 덤프로 진단한 뒤, 플래그를 바꿔 같은 부하의 before/after를 숫자로 비교하는 재현 가능한 실험 랩이다.

목표는 "힙을 키웠더니 빨라졌다" 같은 무용담이 아니라, 같은 부하를 두 JVM 설정에 걸어 결과를 수치로 대비하는 **재현 가능한 측정 루프**를 갖추는 것이다. 측정 없는 튜닝은 감이고, 한 번만 재 본 튜닝은 운이다.

## 왜 만드는가

두 가지 목적이 한 지점에서 만난다. 하나는 학습 격차를 메우는 것이다. `write/07_devops/02_Jenkins`의 도메인 허브 격차 분석에서 JVM 튜닝은 가장 큰 공백으로 남아 있고, 그 안에서 Thread dump·Metaspace·Safepoint는 전수 grep 기준 0편이다. 다른 하나는 이력서를 보강하는 것이다. Jenkins는 현재 자기평가에서 가장 약한 항목인데, "Controller JVM을 부하로 재현해 GC pause와 처리량을 개선했다"는 측정 가능한 한 줄은 약점을 성과로 뒤집는다.

기존 두 학습편이 이 자리를 비워 둔 채 서로를 가리킨다는 점이 결정적이다. [`05-07`](../../write/07_devops/02_Jenkins/06_infra/05-07.Jenkins%20성능%20모니터링%20—%20지표·수집%20토폴로지·부하%20실측.md)은 지표를 수집하고 부하를 실측하지만 튜닝은 다루지 않고, [`01-01 §4`](../../write/07_devops/02_Jenkins/06_infra/01-01.Jenkins%20서버%20용량%20산정과%20시스템%20요구사항.md)는 어떤 플래그가 어떤 증상을 막는지 나열하는 데서 멈춘다. 그 사이의 **재현 → 진단 → 플래그 변경 → 재측정 → before/after** 루프를 손으로 도는 편이 없다. 이 랩이 그 빈자리에 들어간다.

## 문서 구성

| 문서 | 내용 |
|------|------|
| [`requirements.md`](requirements.md) | 랩이 갖춰야 할 기능·비기능 요구사항. 아키텍처와 이력서 목표 문장을 여기서 못 박는다 |
| [`roadmap.md`](roadmap.md) | 세 단계 실행 순서. 코드가 먼저 나오고 그 측정 결과가 학습편을 낳는다 |
| [`enhancements.md`](enhancements.md) | 면접·이력서용 고도화 후보 카탈로그. 하나씩 골라 붙이는 옵션 목록이다 |

## 선행 기획과의 관계

이 프로젝트의 최초 기획 1장은 [`write/07_devops/02_Jenkins/_practice/jenkins-jvm-lab/README.md`](../../write/07_devops/02_Jenkins/_practice/jenkins-jvm-lab/README.md)에 있다. 그 문서가 "무엇을 왜"를 정했고, 이 폴더는 그것을 실행 가능한 요구사항·로드맵·고도화 후보로 펼친 것이다. 최초 기획은 Jenkins Controller JVM에 초점을 뒀지만, 이 프로젝트는 기본 틀을 **Spring Boot ↔ Jenkins 호출 구조**로 넓혀 애플리케이션 JVM 최적화까지 사정권에 둔다.

## 상태

계획 단계다. 이 폴더에는 아직 문서만 있고 docker-compose·스크립트·애플리케이션 코드는 없다. 실행은 `roadmap.md`의 1차부터 시작한다.
