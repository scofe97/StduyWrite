# 07-01 §6 — 리눅스 네트워크 설정과 NetworkManager 구조.
# 타입 스펙: type-architecture — 사용자 도구, 데몬 관리 계층, 커널 런타임 스택의 3계층 구조.
#           accent 는 디스크 영구 저장소(.nmconnection)와 런타임 직접 수정(ip)의 차이를 보이는 자리.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 620
d = D(W, H, "LEARNING MODERN LINUX · 07-01 §6",
      "NetworkManager 데몬과 커널 런타임 설정의 경계",
      "nmcli 와 설정 파일은 디스크에 프로파일을 영구 보관하고 데몬이 커널을 동기화한다. "
      "반면 ip 명령은 커널 메모리만 즉시 바꾸므로 재부팅 시 소멸한다.",
      "영구 설정 프로파일과 커널 런타임 상태의 이원화 구조")

# 1. 사용자 공간 도구 (상단)
UY, UW, UH = 148, 256, 72
d.box(36, UY, UW, UH, PAPER2, INFO, 1.2, 8)
d.t(36 + UW / 2, UY + 26, "CLI 관리 도구", 14, INFO, KR, "middle", 600)
d.t(36 + UW / 2, UY + 48, "nmcli · nmtui", 12, INK, MONO)

d.box(312, UY, UW, UH, PAPER2, OK, 1.2, 8)
d.t(312 + UW / 2, UY + 26, "영구 설정 파일 (키파일)", 14, OK, KR, "middle", 600)
d.t(312 + UW / 2, UY + 48, "/etc/NetworkManager/system-connections/", 10.5, INK, MONO)

d.box(588, UY, UW, UH, PAPER2, WARN, 1.2, 8)
d.t(588 + UW / 2, UY + 26, "커널 직접 조작 (런타임)", 14, WARN, KR, "middle", 600)
d.t(588 + UW / 2, UY + 48, "ip addr add · ip route add", 11.5, INK, MONO)

# 2. 관리 데몬 계층 (중단)
MY, MW, MH = 264, 532, 104
d.o.append(f'<rect x="36" y="{MY}" width="{MW}" height="{MH}" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(56, MY + 28, "NetworkManager 데몬 (D-Bus 기반 네트워크 관리자)", 14, ACC, KR, "start", 600)
d.t(56, MY + 52, "연결 프로파일(Connection Profile) 수명주기 및 디바이스 상태 관리", 11.5, INK, KR, "start")
d.t(56, MY + 74, "nmcli con up 활성화 · DHCP 리스 갱신 · 파일 직접 수정 시 nmcli con reload", 11, MUTED, KR, "start")

# 연결선: 도구 -> 데몬
d.path(f"M {36 + UW / 2} {UY + UH} L {36 + UW / 2} {MY - 4}", INFO, 1.3, m="ar")
d.path(f"M {312 + UW / 2} {UY + UH} L {312 + UW / 2} {MY - 4}", OK, 1.3, m="ar")

# 3. 커널 런타임 계층 (하단)
KY, KW, KH = 412, 808, 120
d.box(36, KY, KW, KH, PAPER2, RULE, 1.2, 8)
d.t(56, KY + 28, "리눅스 커널 네트워크 스택 (런타임 휘발성 메모리)", 14, INK, KR, "start", 600)

# 커널 내부 세부 블록
BW, BH, BY = 240, 56, KY + 46
d.box(56, BY, BW, BH, PAPER, INFO, 1.0, 6)
d.t(56 + BW / 2, BY + 22, "네트워크 인터페이스", 12, INFO, KR, "middle", 600)
d.t(56 + BW / 2, BY + 40, "eth0 · dummy0 · bond0 (본딩)", 11, MUTED, MONO)

d.box(320, BY, BW, BH, PAPER, OK, 1.0, 6)
d.t(320 + BW / 2, BY + 22, "IP 주소 할당 (IPv4/IPv6)", 12, OK, KR, "middle", 600)
d.t(320 + BW / 2, BY + 40, "기본 IP 및 보조 IP (+ipv4.addresses)", 11, MUTED, KR)

d.box(584, BY, BW, BH, PAPER, ACC, 1.0, 6)
d.t(584 + BW / 2, BY + 22, "FIB 라우팅 테이블 & 정책 룰", 12, ACC, KR, "middle", 600)
d.t(584 + BW / 2, BY + 40, "main 테이블 · table 100 · ip rule", 11, MUTED, MONO)

# 연결선: 데몬 -> 커널 (Netlink)
d.path(f"M {36 + MW / 2} {MY + MH} L {36 + MW / 2} {KY - 4}", ACC, 1.5, m="ar")
d.t(36 + MW / 2 + 10, (MY + MH + KY) / 2 + 4, "Netlink 로 커널에 적용", 11, ACC, KR, "start")

# 연결선: ip 직접 조작 -> 커널 (우측 우회 경로)
d.path(f"M {588 + UW / 2} {UY + UH} L {588 + UW / 2} {KY - 4}", WARN, 1.4, m="ar")
d.t(588 + UW / 2 + 10, (UY + UH + KY) / 2 - 6, "커널 직접 갱신", 11, WARN, KR, "start")
d.t(588 + UW / 2 + 10, (UY + UH + KY) / 2 + 12, "재부팅·재활성화 시 소멸", 11, WARN, KR, "start")

d.legend(560, [("영구 프로파일 및 CLI", INFO), ("키파일 저장소", OK),
               ("중앙 관리 데몬", ACC), ("런타임 전용 명령", WARN)])
d.save("07-01.network-manager.svg")
print("ok 07-01.network-manager")
