# Ch01. Oracle Cloud Always Free Tier 구독과 VM 생성

> **핵심 요약**
> GCP 무료 크레딧은 3개월이면 소진되지만, Oracle Cloud Always Free Tier는 **기간 제한 없이** ARM 4 OCPU / 24GB RAM 서버를 무료로 제공한다. 가입 시 홈 리전 선택이 영구 고정되므로 신중해야 하며, 신용카드는 인증용으로만 사용된다. 30일 무료 체험($300) 종료 후에도 Always Free 리소스는 계속 유지된다.

---

## 학습 목표

1. Oracle Cloud Always Free Tier가 제공하는 리소스 범위와 제약을 정확히 이해한다
2. 가입 절차에서 주의할 점(홈 리전 고정, 유료 업그레이드 차이)을 설명할 수 있다
3. ARM VM(A1.Flex)을 최대 스펙으로 생성할 수 있다
4. GCP/AWS 무료 티어와의 차이점을 비교할 수 있다

---

## 1. Always Free Tier가 제공하는 것

Oracle Cloud의 무료 제공은 두 단계로 나뉜다. 처음 30일간은 $300 크레딧을 포함한 무료 체험(Free Trial)이 제공되고, 이후에는 Always Free 리소스만 남는다. 핵심은 **Always Free 리소스에는 기간 제한이 없다**는 점이다.

### 1.1 Always Free 리소스 전체 목록

| 리소스 | 스펙 | 비고 |
|--------|------|------|
| **ARM VM** (A1.Flex) | 총 4 OCPU + 24GB RAM | 1~4개 VM으로 분할 가능 |
| **AMD VM** (E2.1.Micro) | 1/8 OCPU + 1GB RAM x 2대 | 매우 약함, 보조용 |
| **부트 볼륨** | 총 200GB | VM당 최소 47GB |
| **블록 볼륨** | 총 200GB (2개) | 추가 스토리지 |
| **Object Storage** | 20GB | S3 호환 API |
| **로드밸런서** | 1개 (10Mbps) | Network LB |
| **네트워크** | 월 10TB 아웃바운드 | 대부분의 용도에 충분 |
| **Autonomous DB** | 2개 (각 1 OCPU, 20GB) | Oracle DB 또는 JSON DB |

ARM VM 4 OCPU + 24GB RAM은 GCP의 e2-micro(0.25 vCPU, 1GB)나 AWS의 t2.micro(1 vCPU, 1GB)와 비교하면 압도적인 스펙이다. 이것이 Oracle Cloud Free Tier를 선택하는 가장 큰 이유다.

### 1.2 분할 운영 전략

A1.Flex의 4 OCPU / 24GB는 하나의 VM에 몰아줄 수도 있고, 여러 VM으로 나눌 수도 있다.

```
전략 1: 단일 VM (권장 — 관리 단순)
└── VM1: 4 OCPU / 24GB — Docker로 여러 서비스 운영

전략 2: 2대 분할
├── VM1: 3 OCPU / 18GB — 메인 서버 (앱 + DB)
└── VM2: 1 OCPU / 6GB  — 모니터링/CI

전략 3: 3대 분할
├── VM1: 2 OCPU / 12GB — 앱 서버
├── VM2: 1 OCPU / 6GB  — DB 서버
└── VM3: 1 OCPU / 6GB  — 유틸리티
```

단일 VM에 Docker Compose로 여러 서비스를 올리는 전략이 관리 포인트가 가장 적다. 분할은 서비스 격리가 정말 필요할 때만 고려한다.

---

## 2. 가입 절차

### 2.1 단계별 과정

```
1. https://cloud.oracle.com/free 접속
2. Google 계정 또는 이메일로 가입
3. 홈 리전 선택 (⚠️ 영구 고정! 서울/도쿄/오사카 추천)
4. 신용카드 등록 (인증용, 과금 없음)
5. 30일 무료 체험 ($300 크레딧) 시작
6. 체험 종료 후 Always Free 리소스만 유지됨
```

### 2.2 주의사항 3가지

**홈 리전은 변경 불가**

가입 시 선택한 리전이 영구히 고정된다. Always Free 리소스는 홈 리전에서만 생성 가능하므로, 한국에서 사용한다면 **서울(ap-seoul-1)** 또는 **도쿄(ap-tokyo-1)**를 선택해야 한다. 지연 시간 측면에서 서울이 가장 좋지만, 서울 리전은 인기가 높아 ARM VM 생성 시 capacity 부족이 더 자주 발생한다.

**유료 업그레이드는 선택사항**

Always Free 리소스는 무료 계정(Free Tier)으로도 계속 사용 가능하다. 유료 계정(Pay As You Go)으로 업그레이드하면 Always Free 초과 리소스도 쓸 수 있고, 계정 안정성이 높아진다는 장점이 있다. 하지만 무료 범위를 넘는 리소스를 실수로 생성하면 과금되므로 주의해야 한다.

**30일 체험 종료 후 동작**

체험 기간이 끝나면 Always Free가 아닌 리소스(체험 중 생성한 유료 리소스)는 자동 삭제된다. Always Free 범위 내 리소스는 영향 없이 계속 유지된다.

---

## 3. ARM VM 생성

### 3.1 콘솔에서 생성

OCI 콘솔(cloud.oracle.com) > Compute > Instances > Create Instance에서 다음과 같이 설정한다.

```
이미지:     Ubuntu 22.04 또는 24.04 (Canonical 공식)
            Oracle Linux 8/9도 가능하지만 Ubuntu가 커뮤니티 지원이 넓음
Shape:      VM.Standard.A1.Flex (ARM — Ampere Altra)
OCPU:       4 (최대치)
Memory:     24GB (최대치)
Boot Volume: 50GB (기본) ~ 200GB (최대)
Networking: 새 VCN 자동 생성 또는 기존 VCN 선택
SSH Key:    로컬 ~/.ssh/id_rsa.pub 업로드
```

### 3.2 SSH 접속

VM 생성 후 Public IP가 할당되면 바로 접속할 수 있다.

```bash
# Ubuntu 이미지의 기본 사용자는 ubuntu
ssh -i ~/.ssh/id_rsa ubuntu@<PUBLIC_IP>

# Oracle Linux 이미지의 기본 사용자는 opc
ssh -i ~/.ssh/id_rsa opc@<PUBLIC_IP>
```

### 3.3 "Out of Host Capacity" 대응

ARM VM 생성 시 가장 흔한 문제는 `Out of Host Capacity` 에러다. 해당 리전/AD(Availability Domain)에 물리 서버 여유가 없다는 뜻이다.

대응 방법은 세 가지다.

1. **시간대를 바꿔 재시도**: 새벽 시간대(UTC 기준)에 성공 확률이 높다
2. **자동 재시도 스크립트**: OCI CLI로 주기적 생성 시도를 자동화
3. **다른 AD 선택**: 해당 리전에 AD가 여러 개면 다른 AD를 시도

```bash
# OCI CLI로 자동 재시도 (crontab에 등록)
# 이미 인스턴스가 있으면 skip, 없으면 생성 시도
oci compute instance launch \
  --availability-domain "Uxxx:AP-SEOUL-1-AD-1" \
  --compartment-id $COMPARTMENT_ID \
  --shape "VM.Standard.A1.Flex" \
  --shape-config '{"ocpus": 4, "memoryInGBs": 24}' \
  --image-id $IMAGE_ID \
  --subnet-id $SUBNET_ID \
  --ssh-authorized-keys-file ~/.ssh/id_rsa.pub \
  --display-name "free-arm-server"
```

---

## 4. GCP/AWS Free Tier 비교

| 항목 | Oracle Always Free | GCP Free Tier | AWS Free Tier |
|------|-------------------|---------------|---------------|
| **기간** | 영구 | 영구 (일부) | 12개월 (대부분) |
| **VM 스펙** | 4 OCPU / 24GB ARM | 1 e2-micro (0.25 vCPU / 1GB) | 1 t2.micro (1 vCPU / 1GB) |
| **스토리지** | 200GB boot + 200GB block | 30GB | 30GB EBS |
| **네트워크** | 10TB/월 | 1GB/월 (무료 추가) | 100GB/월 (12개월) |
| **DB** | 2x Autonomous DB (20GB) | 없음 | 없음 (RDS는 12개월) |
| **가입 카드** | 필요 (인증용) | 필요 | 필요 |

Oracle이 압도적으로 넉넉한 이유는 시장 점유율 확보를 위한 전략이다. AWS/GCP 대비 클라우드 후발 주자인 Oracle은 개발자 유입을 위해 파격적인 무료 티어를 제공하고 있다.

---

## 체크포인트

- [ ] Oracle Cloud 계정 생성 완료 (홈 리전: 서울)
- [ ] ARM VM (4 OCPU / 24GB) 생성 완료
- [ ] SSH 접속 확인
- [ ] 기본 OS 업데이트 (`sudo apt update && sudo apt upgrade`)

---

## 참고 자료

- [Oracle Cloud Free Tier 공식](https://www.oracle.com/cloud/free/)
- [Always Free 리소스 문서](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm)
- [Oracle Cloud Free Tier FAQ](https://www.oracle.com/cloud/free/faq/)
