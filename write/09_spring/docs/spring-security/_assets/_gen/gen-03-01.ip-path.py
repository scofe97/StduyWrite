# 사실 출처: Nginx 프록시 전달과 Spring Boot forward-headers-strategy 기본값(none) 예시 IP
# 타입 스펙: type-architecture
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 560
d = D(
    W, H,
    "ARCHITECTURE · CLIENT IP PROPAGATION",
    "사용자 PC에서 Spring까지 구간마다 보이는 IP",
    "클라이언트 요청이 VPN과 Docker 프록시를 통과할 때 각 홉에서 관측되는 출발지 IP 변화",
    "예제 배포 IP 기준"
)

# 1. 존 영역 3개 (헤더 단일행)
def draw_zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="{RULE}" stroke-width="0.9"/>')
    d.t(x + 16, y + 24, label, 11, SOFT, KR, "start", 600)

# Zone 1: 사용자 PC
draw_zone(24, 116, 212, 290, "사용자 PC (VPN 10.8.0.7)")
# Zone 2: VPN 게이트웨이
draw_zone(256, 116, 204, 290, "VPN 게이트웨이")
# Zone 3: Docker 호스트 (폭 460으로 칩 포함 여유 확보)
draw_zone(480, 116, 456, 290, "Docker 호스트 (172.18.0.0/24)")

# ── 각 존 상단 관측 IP 정보 (y=166부터 시작) ──
# Zone 1 상단
d.t(130, 172, "출발지 클라이언트", 12, INK, KR, "middle", 600)
d.t(130, 192, "VPN IP: 10.8.0.7", 11, INFO, MONO, "middle")
d.t(130, 210, "VPN 터널 연결", 11, MUTED, KR, "middle")

# Zone 2 상단: ① 게이트웨이가 봄
d.t(358, 172, "① 게이트웨이가 봄", 12, INFO, KR, "middle", 600)
d.t(358, 192, "10.8.0.7", 12, INFO, MONO, "middle", 600)
d.t(358, 210, "VPN 직접 수신 IP", 11, MUTED, KR, "middle")

# Zone 3 상단 좌측: ② Nginx가 봄
d.t(596, 166, "② Nginx가 봄", 12, INK, KR, "middle", 600)
d.t(596, 186, "10.8.0.7 (라우팅 시)", 11, OK, MONO, "middle")
d.t(596, 204, "GW IP (MASQUERADE 시)", 11, WARN, MONO, "middle")
d.chip(596, 224, "확인 필요", WARN, 11)

# Zone 3 상단 우측: ③ Spring이 봄
d.t(826, 166, "③ Spring이 봄", 12, BAD, KR, "middle", 600)
d.t(826, 186, "172.18.0.2", 12, BAD, MONO, "middle", 600)
d.t(826, 204, "헤더 설정 없음", 11, BAD, KR, "middle")
d.chip(826, 224, "모든 사용자 동일", BAD, 11)

# ── 노드 배치 ──
Y_NODE = 260
H_NODE = 54

# 노드 1: 사용자 브라우저
d.box(48, Y_NODE, 164, H_NODE, PAPER2, INFO, 1.1)
d.t(130, Y_NODE + 24, "사용자 브라우저", 13, INK, KR, "middle", 600)
d.t(130, Y_NODE + 42, "요청 전송", 11, MUTED, KR, "middle")

# 노드 2: VPN 게이트웨이
d.box(278, Y_NODE, 160, H_NODE, PAPER2, RULE, 1.0)
d.t(358, Y_NODE + 24, "게이트웨이", 13, INK, KR, "middle", 600)
d.t(358, Y_NODE + 42, "패킷 라우팅", 11, MUTED, KR, "middle")

# 노드 3: Nginx
d.box(516, Y_NODE, 160, H_NODE, PAPER2, OK, 1.1)
d.t(596, Y_NODE + 24, "Nginx", 13, INK, MONO, "middle", 600)
d.t(596, Y_NODE + 42, "172.18.0.2", 11, MUTED, MONO, "middle")
# Nginx 노드 하단 칩: X-Forwarded-For 덧붙임 (OK)
d.chip(596, Y_NODE + H_NODE + 24, "X-Forwarded-For 덧붙임", OK, 11)

# 노드 4: Spring Boot
d.box(746, Y_NODE, 160, H_NODE, PAPER2, BAD, 1.2)
d.t(826, Y_NODE + 24, "Spring Boot", 13, INK, MONO, "middle", 600)
d.t(826, Y_NODE + 42, "172.18.0.3", 11, MUTED, MONO, "middle")
# Spring Boot 노드 하단 칩: RemoteIpValve 미설정 (BAD)
d.chip(826, Y_NODE + H_NODE + 24, "RemoteIpValve 미설정", BAD, 11)

# ── 연결 화살표 ──
Y_ARR = Y_NODE + H_NODE / 2

# 화살표 ①
d.arrow([(212, Y_ARR), (276, Y_ARR)], INFO, "info", 1.4)
d.t(244, Y_ARR - 8, "①", 11, INFO, MONO, "middle", 600)

# 화살표 ②
d.arrow([(438, Y_ARR), (514, Y_ARR)], WARN, "warn", 1.4)
d.t(476, Y_ARR - 8, "②", 11, WARN, MONO, "middle", 600)

# 화살표 ③
d.arrow([(676, Y_ARR), (744, Y_ARR)], BAD, "bad", 1.4)
d.t(710, Y_ARR - 8, "③", 11, BAD, MONO, "middle", 600)

# 하단 안내선 및 주석
d.line(40, 436, 920, 436, RULE, 0.8, dash="4 4")
d.t(480, 460, "헤더를 읽지 않으면 모든 요청이 Nginx IP 로 보임 · 시도 횟수 제한·감사 로그가 사용자를 구분하지 못함", 11, MUTED, KR, "middle")

# 범례
d.legend(H - 44, [
    ("위험 (동일 IP 오인)", BAD),
    ("확인 필요 (NAT 의심)", WARN),
    ("정상 IP·헤더 부가", OK),
    ("클라이언트 원본 IP", INFO),
])

out_path = Path(__file__).parent.parent / "03-01.ip-path.svg"
d.save(str(out_path))
print(f"생성 완료: {out_path}")
