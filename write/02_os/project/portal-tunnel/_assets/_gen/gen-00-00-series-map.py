# 타입 스펙: type-dependency
# 사실 출처: handoff relay-agy-pt-0004.md §담을 것 2·3, 00-common-brief.md §시리즈 목적, relay-agy-pt-0051.md
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 1000, 420
d = D(W, H, "PORTAL-TUNNEL · READING DEPENDENCY",
      "portal-tunnel 시리즈 장별 읽기 순서와 의존 구조",
      "00 지도에서 01 Transport 코어를 거쳐 02 TLS와 03 Identity로 갈라진 뒤 04 표면과 05 리뷰로 수렴하는 읽기 순서와 의존 관계",
      lead="지도로 전체 구조를 잡고 코어 배관과 보안·신원을 거쳐 기여 표면·리뷰로 나아갑니다")

def node(x, y, w, h, ch_num, title, sub, code_range, badge=None, focal=False):
    fill_col = f"{ACC}14" if focal else PAPER2
    stroke_col = ACC if focal else RULE
    sw = 1.4 if focal else 0.9
    d.box(x, y, w, h, fill=fill_col, stroke=stroke_col, sw=sw, r=6)

    # 챕터 번호 및 배지
    d.t(x + 14, y + 22, ch_num, 11, ACC if focal else INFO, MONO, "start", 600)
    if badge:
        bw = len(badge) * 11 + 10
        bx = x + w - bw - 10
        d.o.append(f'<rect x="{bx}" y="{y + 10}" width="{bw}" height="18" rx="3" fill="{INK}10" stroke="{RULE}" stroke-width="0.7"/>')
        d.t(bx + bw / 2, y + 22, badge, 10, ACC if focal else SOFT, KR, "middle", 600)

    # 제목 및 부제
    d.t(x + 14, y + 46, title, 13, INK, KR, "start", 600)
    d.t(x + 14, y + 64, sub, 11, MUTED, KR, "start")
    d.t(x + 14, y + 82, code_range, 10, SOFT, KR, "start")

# 5개 Ranks
# Rank 0: 00 지도
node(36, 166, 136, 96, "00", "00 지도", "개념과 책임 분리", "00-01 · 00-02", badge="시작")

# Rank 1: 01 Transport 코어
node(216, 166, 176, 96, "01", "01 Transport 코어", "제어 평면 · 역방향 풀", "01-01~02 기초 · 01-03~07", badge="코어 배관")

# Rank 2: 02 TLS / 03 Identity (병렬 분기)
node(436, 110, 176, 96, "02", "02 TLS·신뢰 경계", "SNI · keyless TLS", "02-01 기초 · 02-02~05", badge="병렬 선택")
node(436, 226, 176, 96, "03", "03 Identity·정책", "secp256k1 · SIWE · 임대", "03-01 기초 · 03-02~04", badge="병렬 선택")

# Rank 3: 04 표면(SDK·CLI·기여) - 수렴점 (focal)
node(656, 166, 160, 96, "04", "04 표면 계층", "SDK · CLI · e2e 하네스", "04-01 ~ 04-03", badge="02·03 합류", focal=True)

# Rank 4: 05 리뷰
node(860, 166, 110, 96, "05", "05 리뷰", "코드 리뷰 · 개선안", "05-01", badge="종합")

# 연결선
# 00 지도 -> 01 Transport 코어
d.arrow([(172, 214), (214, 214)], MUTED, "ar", 1.4)

# 01 -> 02 (상단 분기)
d.path("M 392 196 C 408 196, 416 158, 434 158", MUTED, 1.4, m="ar")

# 01 -> 03 (하단 분기)
d.path("M 392 232 C 408 232, 416 274, 434 274", MUTED, 1.4, m="ar")

# 02 -> 04 (상단 수렴)
d.path("M 612 158 C 630 158, 638 196, 654 196", ACC, 1.4, m="acc")

# 03 -> 04 (하단 수렴)
d.path("M 612 274 C 630 274, 638 232, 654 232", ACC, 1.4, m="acc")

# 04 -> 05
d.arrow([(816, 214), (858, 214)], MUTED, "ar", 1.4)

# 하단 읽기 안내 라벨 (순수 명사구)
d.line(24, 350, W - 24, 350, RULE, 0.8)
d.t(24, 374, "순차 탐색: 00 지도 → 01 Transport (각 장 기초 포함)", 11, SOFT, KR, "start")
d.t(420, 374, "병렬 선택: 02 TLS 경계와 03 신원 정책 중 관심사 우선 탐색", 11, SOFT, KR, "start")
d.t(790, 374, "수렴: 04 표면 거쳐 05 종합 리뷰", 11, ACC, KR, "start")

out_svg = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "00-00-series-map.svg"))
d.save(out_svg)
print(f"saved: {out_svg}")
