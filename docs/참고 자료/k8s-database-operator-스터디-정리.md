# ('22) 쿠버네티스 데이터베이스 오퍼레이터 소개 및 글 모음

> 출처: [가시다(gasida) Notion](https://gasidaseo.notion.site/22-49a7bd791f674dc38093598f9d88d4c2)
> CloudNet@ DOIK 스터디 멤버들의 기술 포스팅 및 스터디 내용 정리

---

## 쿠버네티스에서 DB를 컨테이너로 운영 가능한가?

충분히 운영 가능하다. 아래 커뮤니티와 실제 사례가 이를 뒷받침한다.

### 커뮤니티

- **DoK Community**: K8s 환경에서 DB를 운영하는 사람들을 위한 커뮤니티 - [사이트](https://dok.community/) / [Youtube](https://www.youtube.com/c/DoKcommunity)

### Use Case (실제 사례)

| 발표 | 주제 | 링크 |
|------|------|------|
| 카카오 if 2020 | DB를 컨테이너로 운영하게 될 줄 몰랐다 | [영상](https://if.kakao.com/2020/session/75) |
| K8S Korea Group | K8S 기반 DB 서비스 운영 경험 공유 | [영상](https://youtu.be/GqHDR-1mVFI) |
| K8S Korea Group | MariaDB Galera Cluster on K8s | [영상](https://youtu.be/G3uvPb8wJ_M) |
| if(kakao) | 쿠버네티스 레디스 클러스터 구축기 | [영상](https://if.kakao.com/session/52) / [블로그](https://tech.kakao.com/2022/02/09/k8s-redis/) |
| NDC21 | 게임 서버를 품은 쿠버네티스 (용찬호) | [영상](https://youtu.be/8R4DDEqjc0I?t=1049) |

---

## 쿠버네티스 플랫폼 기본 지식

DB 오퍼레이터 이해를 위해 반드시 알아야 할 K8s 관련 지식: **플랫폼 특징, StatefulSet, 스토리지, 네트워크**

| 주제 | 링크 |
|------|------|
| StatefulSet & Headless Service | [링크](https://gain-yoo.github.io/database/DOIK-1%EC%B0%A8%EC%8B%9C-(2)/) |
| Kubernetes Storage | [링크](https://gain-yoo.github.io/database/DOIK-1%EC%B0%A8%EC%8B%9C-%EC%8A%A4%ED%84%B0%EB%94%94/) |
| StatefulSet vs Deployment 비교 | [링크](https://flavono123.github.io/posts/statefulset-vs-deployment/) |
| StatefulSet과 Headless Service | [링크](https://chhanz.github.io/kubernetes/2022/05/25/kubernetes-statefulset/) |

---

## 쿠버네티스 오퍼레이터

- 오퍼레이터 동작 예시 (inlets-operator): [고해상도 GIF](https://iximiuz.com/kubernetes-operator-pattern/kube-operator-example-full.gif)
- Operator 소개: [링크](https://lifeoncloud.kr/k8s/doik-operator-1/)
- Controller and Operator 소개: [링크](https://fullmoon-hwi.tistory.com/11)
- Kubernetes Operator 란?: [링크](https://velog.io/@kubernetes/Kubernetes-Operator-%EB%9E%80)
- Operator와 Database 기본 개념: [링크](https://blog.hojaelee.com/252)
- Nginx 오퍼레이터 직접 만들어 보기: [링크](https://blog.naver.com/mplugs/222788655217)

---

## 스터디 멤버 블로그 정리

### 악분일상 님 - [블로그](https://malwareanalysis.tistory.com/) / [Youtube](https://www.youtube.com/c/%EC%95%85%EB%B6%84%EC%9D%BC%EC%83%81/videos)

| 주차 | 주제 | 링크 |
|------|------|------|
| 1주차 | StatefulSet이란 | [링크](https://malwareanalysis.tistory.com/338) |
| 1주차 | 실습 | [링크](https://malwareanalysis.tistory.com/339) |
| 1주차 | Headless 서비스 | [링크](https://malwareanalysis.tistory.com/340) |
| 2주차 | MySQL Operator 설치 | [링크](https://malwareanalysis.tistory.com/341) |
| 2주차 | MySQL Operator Router 설정 확인 | [링크](https://malwareanalysis.tistory.com/342) |
| 2주차 | MySQL Operator 장애 테스트 | [링크](https://malwareanalysis.tistory.com/343) |
| 3주차 | 메세지/이벤트 브로커란 | [링크](https://malwareanalysis.tistory.com/344) |
| 3주차 | Strimzi로 카프카 클러스터 설치 | [링크](https://malwareanalysis.tistory.com/346) |
| 3주차 | Strimzi로 카프카 토픽 생성 | [링크](https://malwareanalysis.tistory.com/348) |
| 3주차 | Strimzi로 카프카 토픽 읽기/쓰기 | [링크](https://malwareanalysis.tistory.com/349) |
| 5주차 | CloudNativePG (PostgreSQL) 오퍼레이터 | [링크](https://malwareanalysis.tistory.com/360) |
| - | [Youtube] StatefulSet 컨셉 | [영상](https://youtu.be/-24U0Am7qaQ) |
| - | [Youtube] Operator 컨셉 | [영상](https://youtu.be/sL2dVvDq32E) |

### Ssoon 님 - [블로그](https://kschoi728.tistory.com/)

| 주제 | 링크 |
|------|------|
| Operator란? | [링크](https://kschoi728.tistory.com/5) |
| Operator 작동 방식 | [링크](https://kschoi728.tistory.com/4) |
| Operator 추가 | [링크](https://kschoi728.tistory.com/11) |
| CR & CRD 실습 | [링크](https://kschoi728.tistory.com/7) |
| MinIO Operator 실습 | [링크](https://kschoi728.tistory.com/8) |
| MySQL Operator 실습 1 | [링크](https://kschoi728.tistory.com/9) |
| MySQL Operator 실습 2 | [링크](https://kschoi728.tistory.com/10) |
| DBaaS on Kubernetes | [링크](https://kschoi728.tistory.com/13) |
| Percona Operator란? | [링크](https://kschoi728.tistory.com/12) |
| Percona Operator for MongoDB 설치 | [링크](https://kschoi728.tistory.com/14) |
| Percona Operator for MongoDB 기본 사용법 | [링크](https://kschoi728.tistory.com/15) |
| Percona Operator for MongoDB 복제 | [링크](https://kschoi728.tistory.com/16) |
| Percona Operator for MongoDB 장애 | [링크](https://kschoi728.tistory.com/17) |
| Percona Operator for MongoDB 샤딩 | [링크](https://kschoi728.tistory.com/18) |

### 후니 님 - [블로그](https://devops-james.tistory.com/)

| 주차 | 주제 | 링크 |
|------|------|------|
| 1주차 | K8s 스토리지 | [링크](https://devops-james.tistory.com/34) |
| 1주차 | K8s 네트워크 | [링크](https://devops-james.tistory.com/35) |
| 1주차 | StatefulSet, Headless 서비스 | [링크](https://devops-james.tistory.com/36) |
| 1주차 | PHP Guestbook with Redis | [링크](https://devops-james.tistory.com/40) |
| 2주차 | 오퍼레이터 & MySQL 오퍼레이터 | [링크](https://devops-james.tistory.com/37) |
| 2주차 | MySQL 오퍼레이터 설치 및 장애 테스트 | [링크](https://devops-james.tistory.com/38) |
| 3주차 | Kafka & Strimzi 오퍼레이터 | [링크](https://devops-james.tistory.com/25) |
| 4주차 | Percona for MongoDB 오퍼레이터 | [링크](https://devops-james.tistory.com/39) |
| 5주차 | Cloud Native PostgreSQL 오퍼레이터 | [링크](https://devops-james.tistory.com/33) |
| 5주차 | 백업 (AWS S3) & PITR 복원 | [링크](https://devops-james.tistory.com/42) |

### qwerty 님 - [블로그](https://blog.naver.com/qwerty_1234s/)

| 주제 | 링크 |
|------|------|
| Strimzi Kafka Monitoring System 구축 | [링크](https://blog.naver.com/qwerty_1234s/222768094790) |
| PMM & Loki Monitoring System 구축 | [링크](https://blog.naver.com/qwerty_1234s/222789027464) |
| Percona MongoDB Operator 구축 & PMM 모니터링 | [링크](https://blog.naver.com/qwerty_1234s/222789042477) |
| Percona PostgreSQL Operator 구축 & PMM 모니터링 | [링크](https://blog.naver.com/qwerty_1234s/222789058620) |

---

## DB 오퍼레이터 1편: MySQL

**MySQL Operator for Kubernetes**: K8s 클러스터로 MySQL InnoDB Cluster를 관리한다. MySQL 8.0.29와 함께 GA 되었으며, setup/maintenance/upgrades/backups의 전체 라이프사이클을 자동화한다.

- [공식 GA 발표](https://blogs.oracle.com/mysql/post/mysql-operator-for-kubernetes-reaches-general-availability)
- [공식 문서](https://dev.mysql.com/doc/mysql-operator/en/mysql-operator-introduction.html)

### 기본

| 주제 | 링크 |
|------|------|
| MySQL Operator로 K8s에서 MySQL 운영하기 | [링크](https://nangman14.tistory.com/79) |
| MySQL Operator for Kubernetes #1 | [링크](https://velog.io/@kubernetes/MySQL-Operator-for-Kubernetes) |
| MySQL Operator for Kubernetes #2 | [링크](https://velog.io/@kubernetes/MySQL-Operator-for-Kubernetes-2) |
| 장애 테스트 영상 | [영상](https://youtu.be/mnvQ0-OeY_0) |
| MySQL Operator (chhanz) | [링크](https://chhanz.github.io/kubernetes/2022/06/09/mysql-operator/) |
| Kubernetes MySQL Operator (linuxer) | [링크](https://linuxer.name/2022/06/kubernetes-mysql-operator/) |
| MySQL DB K8s Operator | [링크](https://mokpolar.tistory.com/23) |
| MySQL InnoDB Cluster 알아보기 | [링크](https://oct28-yjkim.github.io/posts/database/mysql_operator/) |
| K8S MySQL Operator 설치 | [링크](https://linux-operator.tistory.com/5) |

### 부가 기능

| 주제 | 링크 |
|------|------|
| InnoDB Cluster DR 구성 | [링크](https://github.com/HallsHolicker/k8s-doik-sturdy/blob/master/InnodbCluster-DR/%20Readme.md) |
| PV/PVC에 Backup | [링크](https://medium.com/techblog-hayleyshim/k8s-db-%EC%98%A4%ED%8D%BC%EB%A0%88%EC%9D%B4%ED%84%B0-mysql-%EC%98%A4%ED%8D%BC%EB%A0%88%EC%9D%B4%ED%84%B0-a949f91e8df9) |
| KEDA를 이용한 MySQL 자동 확장 | [링크](https://github.com/nyoung08/nyoung08.github.io/blob/master/_posts/2022-06-12-mysql-operator%EC%99%80-keda-%EC%B2%B4%ED%97%98%EA%B8%B0.md) |
| MySQL Operator + KEDA + Locust 부하 테스트 | [링크1](https://mateon.tistory.com/92) / [링크2](https://mateon.tistory.com/93) |
| Prometheus Metric으로 HPA 조절 | [링크](https://gain-yoo.github.io/database/MySQL-Operator-Install/) |
| Multi-primary-mode Router 부하분산 | [링크](https://blog.naver.com/2nddoctoryun/222769124267) |
| Sysbench로 MySQL Operator 벤치마크 | [링크](https://flavono123.github.io/posts/sysbench-mysql-operator/) |
| KEDA MySQL Scaler 파드 오토스케일링 | [링크](https://flavono123.github.io/posts/keda-mysql/) |

### Percona for MySQL Operator

| 주제 | 링크 |
|------|------|
| MySQL Operator based on Percona | [링크](https://miny0529.tistory.com/17) |
| Percona for MySQL Operator 설치 및 기능 | [링크](https://dangerzo.tistory.com/category/kubernetes/Percona%20MySQL%20Operator) |

---

## DB 오퍼레이터 2편: Strimzi (Kafka)

**Strimzi**: K8s 환경에서 Kafka 운영 관리에 도움을 주는 Operator - [공식 문서](https://strimzi.io/docs/operators/in-development/overview.html)

### 기본

| 주제 | 링크 |
|------|------|
| Kafka란? Strimzi Operator & KEDA 설정 및 모니터링 | [링크](https://nangman14.tistory.com/80) |
| Strimzi Operator로 Kafka 클러스터 구성 | [링크](https://dionkim.tistory.com/2) |
| Kafka & Strimzi Operator (hayley) | [링크](https://medium.com/techblog-hayleyshim/k8s-kafka-strimzi-operator-17a2166f36f9) |
| Kafka & Strimzi Operator (devops-james) | [링크](https://devops-james.tistory.com/25) |
| Strimzi Kafka Operator 실습 | [링크](https://jerryljh.tistory.com/75) |
| Kafka 토픽 생성 | [링크](https://jerryljh.tistory.com/76) |
| Kafka와 K8s Strimzi Operator | [링크](https://sshine.tistory.com/73) |
| Kafka Operator 설치 및 테스트 | [링크](https://sogkyc.tistory.com/17) |
| Kafka & Strimzi Operator (1) 설치 | [링크](https://gain-yoo.github.io//database/kafka-&-strimzi/) |
| Kafka & Strimzi Operator (2) HTTP Bridge Sidecar | [링크](https://gain-yoo.github.io/database/HTTP-Bridge_Sidecar/) |

### 모니터링

- Strimzi Kafka Monitoring System 구축: [링크](https://blog.naver.com/qwerty_1234s/222768094790)

---

## DB 오퍼레이터 3편: Percona for MongoDB Operator

**Percona Operator for MongoDB**: PSMDB를 생성/변경/삭제를 관리. 지원 버전: MongoDB v4.2, v4.4, v5.0

- [공식 문서](https://www.percona.com/doc/kubernetes-operator-for-psmongodb/expose.html)

| 주제 | 링크 |
|------|------|
| Percona for MongoDB Operator (hayley) | [링크](https://medium.com/techblog-hayleyshim/k8s-percona-distribution-for-mongodb-operator-72554c904b54) |
| Percona Operator for MongoDB 옵션 변경 | [링크](https://linux-operator.tistory.com/12) |
| NoSQL과 MongoDB Operator | [링크](https://sshine.tistory.com/74) |
| MongoDB 오퍼레이터 기본 설치 | [링크](https://miny0529.tistory.com/10) |
| MongoDB 오퍼레이터 복제 | [링크](https://miny0529.tistory.com/11) |
| MongoDB 오퍼레이터 샤딩 | [링크](https://miny0529.tistory.com/12) |
| MongoDB Operator + KEDA 오토스케일링 | [링크](https://github.com/nyoung08/nyoung08.github.io/blob/master/_posts/2022-06-26-mongoDB-operator%EC%99%80-keda-%EC%B2%B4%ED%97%98%EA%B8%B0.md) |
| Robo 3T 연결 | [링크](https://dionkim.tistory.com/3) |
| NoSQL 학습 정리 | [링크](https://dev-hojae.tistory.com/266) |
| Percona Operator for MongoDB 소개 | [링크](https://lifeoncloud.github.io/k8s/doik-operator-2/) |

---

## DB 오퍼레이터 4편: CloudNativePG (PostgreSQL)

**CloudNativePG**: K8s 환경에서 PostgreSQL 워크로드를 관리한다. EDB가 개발 후 Apache License 2.0으로 공개, 2022년 4월 CNCF Sandbox에 제출되었다. RW 요청을 프라이머리로 전달하는 구조를 가진다.

- [공식 문서](https://cloudnative-pg.io/documentation/1.15.1/)

| 주제 | 링크 |
|------|------|
| Cloud Native PostgreSQL Operator (chhanz) | [링크](https://chhanz.github.io/kubernetes/2022/06/23/postgresql-operator/) |
| Cloud Native PostgreSQL 오퍼레이터 | [링크](https://miny0529.tistory.com/16) |
| Cloud Native PostgreSQL Operator #1 | [링크](https://velog.io/@kubernetes/Cloud-Native-PostgreSQL-1) |
| Cloud Native PostgreSQL Operator #2 | [링크](https://velog.io/@kubernetes/Cloud-Native-PostgreSQL-2) |
| 장애 테스트 영상 | [영상](https://youtu.be/ff9a1j_okfs) |

---

## DB 오퍼레이터 5편: Redis Operator

**Redis Operator**: K8s 클러스터로 Redis 클러스터를 관리한다.

- [Redis & Redis Operator Tutorial 전체](https://github.com/jangjaelee/tutorials-redis-operator/wiki)

| 챕터 | 주제 | 링크 |
|------|------|------|
| 1 | Introduction to Redis & Redis Operator | [링크](https://github.com/jangjaelee/tutorials-redis-operator/wiki/1%29-Introduction-to-Redis---Redis-Operator) |
| 2 | Redis Operator for Redis Cluster (by opstree) | [링크](https://github.com/jangjaelee/tutorials-redis-operator/wiki/2%29-Redis-Operator-for-Redis-Cluster-(by-opstree)) |
| 3 | Redis Operator API Docs (by opstree) | [링크](https://github.com/jangjaelee/tutorials-redis-operator/wiki/3%29-Redis-Operator-API-Docs-(by-opstree)) |
| 4 | Redis Operator for Sentinel (by spotahome) | [링크](https://github.com/jangjaelee/tutorials-redis-operator/wiki/4%29-Redis-Operator-for-Sentinel-(by-spotahome)) |
| 5 | Redis Operator API Docs (by spotahome) | [링크](https://github.com/jangjaelee/tutorials-redis-operator/wiki/5%29-Redis-Operator-API-Docs-(by-spotahome)) |

---

## 그 외 오퍼레이터

| 오퍼레이터 | 주제 | 링크 |
|-----------|------|------|
| **Prometheus** | Prometheus & Prometheus Operator Tutorial | [링크](https://github.com/jangjaelee/tutorials-prometheus/wiki) |
| **Prometheus** | Setup Prometheus Monitoring (Used Operator) | [링크](https://cr4ft-ing.tistory.com/237) |
| **Elasticsearch** | Elasticsearch Operator 통합 로깅 시스템 Part 1 | [링크](https://medium.com/@tkdgy0801/building-an-integrated-logging-system-using-elasticsearch-operator-part-1-84896f335447) |
| **ECK** | ECK 오퍼레이터 | [링크](https://github.com/HallsHolicker/k8s-doik-sturdy/blob/master/K8S-Logging/Readme.md) |
| **ArgoCD** | ArgoCD Operator 구축 테스트 | [링크](https://ersiajin.blogspot.com/2022/06/studyk8s-operator-argocd-operator.html) |
| **ArgoCD** | ArgoCD Operator 기능 테스트 | [링크](https://ersiajin.blogspot.com/2022/06/studyk8s-operator-argocd-operator_11.html) |
| **ArgoCD** | ArgoCD Operator on K8s with OLM | [링크](https://whitegoblincom.tistory.com/32) |
| **MinIO** | MinIO Operator | [링크](https://github.com/ejpark78/study/blob/main/doik/mid-assignment.md) |

---

## 그 외 정보

| 주제 | 링크 |
|------|------|
| K8s에 Zookeeper 제대로 배포하기 | [링크](https://sungchul-p.github.io/zookeeper-on-k8s) |
| Helm으로 K8S에 MariaDB Galera 설치 | [링크](https://miny0529.tistory.com/5) |
| Kubeflow 설치 및 CR/CRD 분석 | [링크](https://sogkyc.tistory.com/18) |
