# 사실 출처: handoff relay-agy-fl-0049.md §담을 것 2·3, 00-common-brief.md §시리즈 목적, docs/design.md
# 타입 스펙: type-dependency
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 1040, 466
d = D(W, H, "FLATS · READING DEPENDENCY",
      "flats 시리즈 장별 읽기 순서와 의존 구조",
      "00 지도에서 01 콘텐츠를 거쳐 02 런타임·04 에이전트·03 원격 접속으로 분기한 뒤 05 운영과 06 리뷰로 수렴하는 읽기 순서와 의존 관계",
      lead="지도로 전체 구조를 잡고 콘텐츠 불변성과 런타임·원격·보안을 거쳐 운영 데몬과 종합 리뷰로 나아갑니다")

def node(x, y, w, h, ch_num, title, sub, basic_lbl, main_lbl, badge=None, focal=False):
    fill_col = f"{ACC}14" if focal else PAPER2
    stroke_col = ACC if focal else RULE
    sw = 1.4 if focal else 0.9
    d.box(x, y, w, h, fill=fill_col, stroke=stroke_col, sw=sw, r=6)

    # 챕터 번호
    d.t(x + 12, y + 20, ch_num, 11, ACC if focal else INFO, MONO, "start", 600)

    # 배지
    if badge:
        bw = len(badge) * 11 + 12
        bx = x + w - bw - 10
        d.o.append(f'<rect x="{bx}" y="{y + 8}" width="{bw}" height="18" rx="3" fill="{INK}10" stroke="{RULE}" stroke-width="0.7"/>')
        d.t(bx + bw / 2, y + 20, badge, 9.5, ACC if focal else SOFT, KR, "middle", 600)

    # 제목 및 부제
    d.t(x + 12, y + 41, title, 12.5, INK, KR, "start", 600)
    d.t(x + 12, y + 57, sub, 10, MUTED, KR, "start")

    # 장 내부 흐름 (기초 -> 본편)
    flow_y = y + 74
    # 기초 pill
    w1 = len(basic_lbl) * 7.2 + 8
    d.o.append(f'<rect x="{x + 12}" y="{flow_y - 11}" width="{w1}" height="16" rx="3" fill="{PAPER}" stroke="{INFO if not focal else ACC}" stroke-width="0.7"/>')
    d.t(x + 12 + w1 / 2, flow_y + 1, basic_lbl, 9, INFO if not focal else ACC, KR, "middle")

    # 화살표
    arr_x1 = x + 12 + w1 + 3
    arr_x2 = arr_x1 + 13
    d.arrow([(arr_x1, flow_y - 3), (arr_x2, flow_y - 3)], SOFT, "soft", 1.0)

    # 본편 pill
    arr_x2_end = arr_x2 + 3
    w2 = len(main_lbl) * 7.2 + 8
    d.o.append(f'<rect x="{arr_x2_end}" y="{flow_y - 11}" width="{w2}" height="16" rx="3" fill="{PAPER}" stroke="{RULE}" stroke-width="0.7"/>')
    d.t(arr_x2_end + w2 / 2, flow_y + 1, main_lbl, 9, SOFT, KR, "middle")

# 5개 Ranks
# Rank 0: 00 지도
node(24, 186, 136, 92, "00", "00 지도", "개념 · 프로세스 배치", "00-01 개론", "00-02 개념", badge="시작")

# Rank 1: 01 콘텐츠와 수명주기
node(196, 186, 172, 92, "01", "01 콘텐츠·수명주기", "불변 저장소 · CAS 배포", "01-01 기초", "01-02~04", badge="스토리지 코어")

# Rank 2: 02 서버 런타임 (상단), 04 에이전트·보안 (중단), 03 원격 접속 (하단)
node(416, 84, 172, 92, "02", "02 서버 런타임", "QuickJS · WASI · 워커", "02-01 기초", "02-02~04", badge="실행 런타임")
node(416, 186, 172, 92, "04", "04 에이전트·보안", "MCP 36개 · 승인 게이트", "04-01 기초", "04-02~04", badge="에이전트 제어")
node(416, 288, 172, 92, "03", "03 원격 접속", "Tailscale · Portal · 릴레이", "03-01 기초", "03-02~05", badge="외부 노출")

# Rank 2 하단: portal-tunnel 시리즈 연계 노드
d.o.append(f'<rect x="416" y="400" width="172" height="26" rx="4" fill="{PAPER}" stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="3,3"/>')
d.t(502, 416, "portal-tunnel 시리즈 (SDK v2.6.3)", 9.5, SOFT, KR, "middle")

# Rank 3: 05 운영 (수렴점 focal)
node(636, 186, 172, 92, "05", "05 운영", "serve 데몬 조립 · 백업", "05-01 §1", "05-01~02", badge="호스트 조립", focal=True)

# Rank 4: 06 리뷰 (최종 종합)
node(856, 186, 160, 92, "06", "06 리뷰", "CI 게이트 · 6속성 평가", "06-01 CI", "06-02 리뷰", badge="종합 검증")

# 연결선
# 00 지도 -> 01 콘텐츠
d.arrow([(160, 232), (194, 232)], MUTED, "ar", 1.4)

# 01 -> 02 (상단 분기: 버전 산출물 -> 워커 실행)
d.path("M 368 214 C 388 214, 396 130, 414 130", MUTED, 1.4, m="ar")

# 01 -> 04 (중단: 01-03 Version model -> 04-04 파라미터 동결 전제)
d.arrow([(368, 232), (414, 232)], MUTED, "ar", 1.4)

# 01 -> 03 (하단 분기: flat 저장 -> 원격 노출)
d.path("M 368 250 C 388 250, 396 334, 414 334", MUTED, 1.4, m="ar")

# 03 -> portal-tunnel (점선 화살표: 03-04 Portal SDK 임베드)
d.arrow([(502, 380), (502, 398)], SOFT, "soft", 1.2, dash="3,3")

# 02 -> 05 (상단 수렴)
d.path("M 588 130 C 606 130, 614 214, 634 214", ACC, 1.4, m="acc")

# 04 -> 05 (중단 수렴)
d.arrow([(588, 232), (634, 232)], ACC, "acc", 1.4)

# 03 -> 05 (하단 수렴)
d.path("M 588 334 C 606 334, 614 250, 634 250", ACC, 1.4, m="acc")

# 05 -> 06
d.arrow([(808, 232), (854, 232)], MUTED, "ar", 1.4)

# 하단 읽기 안내 라벨
d.line(24, 438, W - 24, 438, RULE, 0.8)
d.t(24, 456, "순차 진입: 00 지도 → 01 콘텐츠·수명주기 (불변 산출물·WAL)", 10.5, SOFT, KR, "start")
d.t(400, 456, "3대 축 분기: 02 런타임 · 04 에이전트/승인 · 03 원격 노출 (03-04는 portal 연계)", 10.5, SOFT, KR, "start")
d.t(870, 456, "수렴: 05 운영 조립 → 06 종합 리뷰", 10.5, ACC, KR, "start")

out_svg = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "00-00-series-map.svg"))
d.save(out_svg)
print(f"saved: {out_svg}")
