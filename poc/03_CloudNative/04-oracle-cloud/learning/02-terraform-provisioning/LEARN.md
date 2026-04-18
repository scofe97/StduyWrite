# Ch02. Terraform으로 OCI 인프라 프로비저닝

> **핵심 요약**
> Oracle은 공식 Terraform provider(`hashicorp/oci`)를 제공하며, GCP/AWS와 동일한 `init → plan → apply` 워크플로우로 인프라를 코드로 관리할 수 있다. 초기 설정에서 API Key(PEM 파일) 생성이 필요한 점이 GCP의 `gcloud auth`보다 번거롭지만, 한 번 설정하면 이후 워크플로우는 동일하다. OCI Resource Manager라는 내장 Terraform 서비스도 있어 웹 콘솔에서 바로 실행할 수도 있다.

---

## 학습 목표

1. OCI API Key를 생성하고 `~/.oci/config`를 설정할 수 있다
2. Terraform으로 VCN, 서브넷, Security List, ARM VM을 프로비저닝할 수 있다
3. OCI Resource Manager와 로컬 Terraform의 차이를 이해한다
4. GCP Terraform 설정과의 차이점을 설명할 수 있다

---

## 1. 두 가지 Terraform 실행 방법

Oracle Cloud에서 Terraform을 실행하는 방법은 두 가지다.

| 방법 | 장점 | 단점 |
|------|------|------|
| **로컬 Terraform** | 익숙한 워크플로우, Git 관리 가능 | OCI API Key 설정 필요 |
| **OCI Resource Manager** | 웹 콘솔에서 바로 실행, 키 설정 불필요 | 커스터마이징 제한적, 로컬 상태 관리 불가 |

로컬 Terraform이 범용적이고 Git으로 버전 관리가 가능하므로 이 문서에서는 로컬 방식을 다룬다.

---

## 2. OCI CLI와 API Key 설정

### 2.1 설치

```bash
# macOS
brew install oci-cli
brew install terraform

# 설치 확인
oci --version
terraform --version
```

### 2.2 API Key 생성

OCI API와 통신하려면 RSA 키 쌍이 필요하다. `oci setup config` 명령으로 대화식으로 생성할 수 있다.

```bash
oci setup config
```

이 명령은 다음을 수행한다.
1. `~/.oci/` 디렉토리 생성
2. RSA 키 쌍 생성 (`oci_api_key.pem`, `oci_api_key_public.pem`)
3. `~/.oci/config` 파일 생성 (사용자/테넌시 OCID 입력 필요)

### 2.3 공개 키 등록

생성된 공개 키를 OCI 콘솔에 등록해야 한다.

```
OCI Console > Identity > Users > 내 사용자 > API Keys > Add API Key
→ "Paste Public Key" 선택
→ ~/.oci/oci_api_key_public.pem 내용 붙여넣기
```

### 2.4 config 파일 확인

```ini
# ~/.oci/config
[DEFAULT]
user=ocid1.user.oc1..aaaaaaaxxxxxxxxx
fingerprint=aa:bb:cc:dd:ee:ff:00:11:22:33:44:55:66:77:88:99
tenancy=ocid1.tenancy.oc1..aaaaaaaxxxxxxxxx
region=ap-seoul-1
key_file=~/.oci/oci_api_key.pem
```

각 값의 의미는 다음과 같다.
- **user**: OCI Console > Identity > Users에서 확인
- **fingerprint**: API Key 등록 시 자동 생성
- **tenancy**: OCI Console > Administration > Tenancy Details에서 확인
- **region**: 홈 리전 식별자 (서울은 `ap-seoul-1`)
- **key_file**: 비밀 키 파일 경로

---

## 3. Terraform 프로젝트 구성

### 3.1 디렉토리 구조

```
oci-free-tier/
├── main.tf          # 핵심 리소스 (VCN, 서브넷, VM)
├── variables.tf     # 변수 정의
├── outputs.tf       # 출력값 (Public IP 등)
├── terraform.tfvars # 실제 값 (Git에서 제외)
└── .gitignore
```

### 3.2 provider 설정 (main.tf 상단)

```hcl
terraform {
  required_providers {
    oci = {
      source  = "oracle/oci"
      version = "~> 5.0"
    }
  }
}

provider "oci" {
  # ~/.oci/config의 [DEFAULT] 프로필을 자동으로 읽는다
  # 명시적으로 지정하려면 아래 주석 해제
  # tenancy_ocid = var.tenancy_ocid
  # user_ocid    = var.user_ocid
  # fingerprint  = var.fingerprint
  # private_key_path = var.private_key_path
  # region       = var.region
}
```

### 3.3 variables.tf

```hcl
variable "compartment_id" {
  description = "OCI Compartment OCID"
  type        = string
}

variable "ssh_public_key" {
  description = "SSH 공개 키 내용"
  type        = string
}

variable "availability_domain" {
  description = "가용 도메인 이름"
  type        = string
}

variable "image_id" {
  description = "VM 이미지 OCID (Ubuntu 22.04 ARM)"
  type        = string
}
```

### 3.4 핵심 리소스 (main.tf)

```hcl
# --- 네트워크 ---

resource "oci_core_vcn" "main" {
  compartment_id = var.compartment_id
  cidr_blocks    = ["10.0.0.0/16"]
  display_name   = "free-tier-vcn"
  dns_label      = "freetier"
}

resource "oci_core_internet_gateway" "main" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_vcn.main.id
  display_name   = "free-tier-igw"
  enabled        = true
}

resource "oci_core_route_table" "main" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_vcn.main.id
  display_name   = "free-tier-rt"

  route_rules {
    destination       = "0.0.0.0/0"
    network_entity_id = oci_core_internet_gateway.main.id
  }
}

resource "oci_core_security_list" "main" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_vcn.main.id
  display_name   = "free-tier-sl"

  # SSH
  ingress_security_rules {
    protocol = "6" # TCP
    source   = "0.0.0.0/0"
    tcp_options {
      min = 22
      max = 22
    }
  }

  # HTTP
  ingress_security_rules {
    protocol = "6"
    source   = "0.0.0.0/0"
    tcp_options {
      min = 80
      max = 80
    }
  }

  # HTTPS
  ingress_security_rules {
    protocol = "6"
    source   = "0.0.0.0/0"
    tcp_options {
      min = 443
      max = 443
    }
  }

  # 모든 아웃바운드 허용
  egress_security_rules {
    protocol    = "all"
    destination = "0.0.0.0/0"
  }
}

resource "oci_core_subnet" "main" {
  compartment_id    = var.compartment_id
  vcn_id            = oci_core_vcn.main.id
  cidr_block        = "10.0.1.0/24"
  display_name      = "free-tier-subnet"
  dns_label         = "subnet1"
  route_table_id    = oci_core_route_table.main.id
  security_list_ids = [oci_core_security_list.main.id]
}

# --- Compute ---

resource "oci_core_instance" "arm_server" {
  compartment_id      = var.compartment_id
  availability_domain = var.availability_domain
  display_name        = "free-arm-server"
  shape               = "VM.Standard.A1.Flex"

  shape_config {
    ocpus         = 4
    memory_in_gbs = 24
  }

  source_details {
    source_type = "image"
    source_id   = var.image_id
    boot_volume_size_in_gbs = 100
  }

  create_vnic_details {
    subnet_id        = oci_core_subnet.main.id
    assign_public_ip = true
  }

  metadata = {
    ssh_authorized_keys = var.ssh_public_key
  }
}
```

### 3.5 outputs.tf

```hcl
output "instance_public_ip" {
  description = "VM의 Public IP"
  value       = oci_core_instance.arm_server.public_ip
}

output "instance_id" {
  description = "VM의 OCID"
  value       = oci_core_instance.arm_server.id
}
```

### 3.6 terraform.tfvars (Git 제외)

```hcl
compartment_id      = "ocid1.compartment.oc1..aaaaaaaxxxxxxxxx"
availability_domain = "Uxxx:AP-SEOUL-1-AD-1"
image_id            = "ocid1.image.oc1.ap-seoul-1..aaaaaaaxxxxxxxxx"
ssh_public_key      = "ssh-rsa AAAA..."
```

`compartment_id`는 OCI Console > Identity > Compartments에서, `image_id`는 Console > Compute > Custom Images 또는 [OCI 이미지 목록](https://docs.oracle.com/en-us/iaas/images/)에서 확인한다.

---

## 4. 실행

```bash
cd oci-free-tier/

# 초기화 — provider 다운로드
terraform init

# 변경 사항 미리보기
terraform plan

# 실제 적용
terraform apply

# 삭제 (필요 시)
terraform destroy
```

`apply` 완료 후 `instance_public_ip` 출력값으로 SSH 접속이 가능하다.

---

## 5. GCP Terraform과의 차이점

| 항목 | GCP | OCI |
|------|-----|-----|
| **인증** | `gcloud auth application-default login` | `~/.oci/config` + PEM 키 |
| **Provider** | `hashicorp/google` | `oracle/oci` |
| **방화벽** | `google_compute_firewall` | `oci_core_security_list` |
| **VM** | `google_compute_instance` | `oci_core_instance` |
| **네트워크** | VPC + Subnet (자동 모드 가능) | VCN + Subnet (수동 설정) |
| **설정 난이도** | 쉬움 (gcloud CLI가 토큰 관리) | 중간 (API Key PEM 직접 관리) |

가장 큰 차이는 인증이다. GCP는 `gcloud auth`로 브라우저 OAuth를 거치면 끝이지만, OCI는 RSA 키 쌍을 생성하고 공개 키를 콘솔에 등록하는 과정이 필요하다. 그 외 Terraform 워크플로우(init/plan/apply)는 동일하다.

---

## 6. 참고 프로젝트

로컬에서 처음부터 작성하기 번거롭다면 아래 오픈소스를 참고할 수 있다.

- [oracle-cloud-terraform](https://github.com/bestrocker221/oracle-cloud-terraform) — Free Tier VM + Ansible 자동화
- [oci-free-tier-terraform-module](https://github.com/anotherglitchinthematrix/oci-free-tier-terraform-module) — A1.Flex 전용 모듈
- [OCI 공식 Terraform 튜토리얼](https://docs.oracle.com/en/learn/oci-terraform-for-beginners/index.html)
- [ARM Terraform 배포 가이드](https://learn.arm.com/learning-paths/servers-and-cloud-computing/oci-terraform/tf-oci/)

---

## 체크포인트

- [ ] OCI CLI 설치 및 `oci setup config` 완료
- [ ] API Key를 OCI 콘솔에 등록
- [ ] `terraform init` 성공
- [ ] `terraform plan`으로 리소스 6개 확인 (VCN, IGW, RT, SL, Subnet, Instance)
- [ ] `terraform apply`로 VM 생성 및 SSH 접속 성공
