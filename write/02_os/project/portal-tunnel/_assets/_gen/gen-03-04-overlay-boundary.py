# 타입 스펙: type-architecture
# 사실 출처: docs/maintainer/architecture.md §Package Boundaries (portal/overlay),
#   docs/src/routes/architecture/+page.md §IVNP-backed overlay networking,
#   portal/overlay/runtime.go:36-46,68,76,115.
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 520
d = D(
    W, H,
    "PORTAL-TUNNEL · OVERLAY NETWORKING ARCHITECTURE",
    "Portal과 IVNP 오버레이 소유권 경계",
    "엔드포인트 인가와 임대 수명은 Portal이 소유하고, 게이트웨이에서 인그레스로 이어지는 네트워크 다중 홉 경로는 IVNP가 독립적으로 소유합니다.",
    "Portal 도메인 (인가·임대·직접 경로) vs IVNP 도메인 (불투명 라우터·내부 홉 순서)의 책임 분리"
)

def zone(x, y, w, h, label, c=RULE):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="{c}" stroke-width="1.0" stroke-dasharray="4 4"/>')
    d.t(x + 14, y + 20, label, 11, c, KR, "start", 600)

# 두 주요 소유권 영역
zone(20, 100, 590, 360, "Portal 소유 영역 (엔드포인트 인가 · 임대 · 역방향 수명주기)", INFO)
zone(640, 100, 300, 360, "IVNP 소유 영역 (내부 토폴로지 · 암호화 터널 · 홉 순서)", WARN)

# Portal 영역 노드 배치
# 1. 공개 클라이언트
d.box(34, 136, 106, 68, PAPER2, RULE, 1.0)
d.t(87, 162, "공개 클라이언트", 11, INK, KR, "middle", 600)
d.t(87, 184, "HTTPS 브라우저", 10, MUTED, KR, "middle")

# 2. 로컬 서비스
d.box(34, 310, 106, 68, PAPER2, RULE, 1.0)
d.t(87, 336, "로컬 서비스", 11, INK, KR, "middle", 600)
d.t(87, 358, "127.0.0.1:3000", 10, MUTED, MONO, "middle")

# 3. Tunnel / SDK
d.box(218, 206, 120, 180, PAPER2, INFO, 1.2)
d.chip(278, 230, "터널 에이전트", INFO, 10)
d.t(278, 260, "sdk.Exposure", 11, INK, MONO, "middle", 600)
d.t(278, 282, "secp256k1 신원", 10, MUTED, KR, "middle")
d.t(278, 312, "엔드포인트 선택 수신", 10, MUTED, KR, "middle")
d.t(278, 334, "직접·오버레이 전환", 10, MUTED, KR, "middle")
d.t(278, 362, "--overlay 플래그", 10, SOFT, MONO, "middle")

# 4. Portal Public Ingress (416..596)
d.box(416, 136, 180, 126, PAPER2, OK, 1.2)
d.chip(506, 158, "공개 인그레스 릴레이", OK, 10)
d.t(506, 186, "Portal Ingress (SNI)", 11, OK, MONO, "middle", 600)
d.t(506, 208, "임대 큐 및 세션 관리", 10, MUTED, KR, "middle")
d.t(506, 230, "ReverseOffer 검증", 10, MUTED, KR, "middle")
d.t(506, 248, "위임 capability 서명", 9, SOFT, MONO, "middle")

# 5. Overlay Gateway (416..596)
d.box(416, 290, 180, 166, PAPER2, ACC, 1.2)
d.chip(506, 312, "오버레이 게이트웨이", ACC, 10)
d.t(506, 338, "Overlay Gateway (runtime)", 10.5, ACC, MONO, "middle", 600)
d.t(506, 360, "GET /sdk/connect 브리지", 10, MUTED, MONO, "middle")
d.t(506, 382, "분당 120회 · burst 16", 10, MUTED, KR, "middle")
d.t(506, 404, "출발지당 16 / 전체 128 슬롯", 10, MUTED, KR, "middle")
d.t(506, 432, "초과 시 HTTP 429 거절", 9, SOFT, KR, "middle")

# IVNP 영역 노드 배치 (650..930)
d.box(650, 136, 280, 310, PAPER2, WARN, 1.1)
d.chip(790, 160, "IVNP 오버레이 메시", WARN, 10)
d.t(790, 186, "불투명 라우팅 네트워크", 11, INK, KR, "middle", 600)
d.t(790, 208, "토폴로지 은닉 (Portal 독립)", 10, MUTED, KR, "middle")

# 내부 홉 라우터들 (4각 노드)
d.box(666, 350, 92, 44, PAPER, RULE, 0.9, r=4)
d.t(712, 376, "라우터 A", 10, SOFT, KR, "middle")

d.box(816, 286, 92, 44, PAPER, RULE, 0.9, r=4)
d.t(862, 312, "라우터 B", 10, SOFT, KR, "middle")

d.box(666, 236, 92, 44, PAPER, RULE, 0.9, r=4)
d.t(712, 262, "라우터 C", 10, SOFT, KR, "middle")

# 내부 홉 화살표
d.arrow([(758, 372), (862, 372), (862, 330)], MUTED, "ar", 1.0, dash="3 3")
d.arrow([(862, 286), (712, 286), (712, 280)], MUTED, "ar", 1.0, dash="3 3")
d.t(790, 420, "내부 홉 순서 자율 결정", 9, SOFT, KR, "middle")

# 연결선 1: 클라이언트 -> 인그레스
d.arrow([(140, 170), (416, 170)], INFO, "ar", 1.4)
d.t(278, 162, "공개 HTTPS 요청", 10, INFO, KR, "middle")

# 연결선 2: 터널 -> 로컬 서비스
d.arrow([(218, 344), (140, 344)], INFO, "ar", 1.4)
d.t(179, 334, "로컬 포워딩", 10, INFO, KR, "middle")

# 연결선 3: 직접 리버스 세션 (기본·폴백)
d.arrow([(338, 236), (416, 236)], OK, "ok", 1.5)
d.t(377, 214, "직접 리버스 세션", 9.5, OK, KR, "middle")
d.t(377, 227, "(기본·폴백)", 8.5, MUTED, KR, "middle")

# 연결선 4: 오버레이 요청 터널 -> 게이트웨이
d.arrow([(338, 348), (416, 348)], ACC, "acc", 1.5)
d.t(377, 336, "오버레이", 9, ACC, KR, "middle")
d.t(377, 360, "connect", 9, ACC, MONO, "middle")

# 연결선 5: 게이트웨이 -> IVNP
d.arrow([(596, 372), (666, 372)], ACC, "acc", 1.5)
d.t(712, 340, "IVNP 스트림 진입", 9, ACC, KR, "middle")

# 연결선 6: IVNP -> 인그레스
d.arrow([(666, 246), (596, 246)], OK, "ok", 1.5)
d.t(712, 224, "ReverseOffer 전달", 9, OK, MONO, "middle")

# 범례
d.legend(470, [
    ("외부 트래픽", INFO),
    ("직접 연결 (기본)", OK),
    ("오버레이 경로 (선택)", ACC),
    ("IVNP 메시", WARN)
])

out_path = _HERE.parent / "03-04-overlay-boundary.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
