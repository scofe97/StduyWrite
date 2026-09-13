# 타입 스펙: type-architecture — 전/후 두 칸. 칸마다 사용자 → 경로 위 라우터 → 같은 주소를 가진 도쿄·LA 인스턴스.
# 출처: 원문 §5.4.4 "with IP anycast ... the packets from the same TCP connection may be routed to
#       different web server instances" — CDN 이 애니캐스트를 대체로 쓰지 않는 이유.
# 노트의 읽기: 주소 203.0.113.9 · 198.51.100.7 은 문서용 대역(RFC 5737)에서 고른 예시다. 원문은 인스턴스가
#       갈린다는 사실만 적고 RST 까지는 적지 않는다 — RST 는 03-04 의 규칙(맞는 소켓이 없으면 리셋)을 이어 붙인 것이다.
# 2026-09-13: type-sequence 에서 바꿨다. 레인 넷의 시간축으로는 "무엇을 설명하려는지 모르겠다"는 지적을 받았다.
#       같은 주소 둘 · 경로가 바뀌는 자리 · 상태가 어디 있는지를 전/후 망 그림으로 나란히 둔다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, KR, MONO

W, H = 1000, 688
d = D(W, H, "SECTION 5.4.4 · WHY CDNS AVOID ANYCAST",
      "주소는 그대로인데 받는 기계가 바뀌면 연결이 끊깁니다",
      "도쿄와 LA 인스턴스가 같은 주소 203.0.113.9 를 광고한다. 경로가 도쿄일 때 맺은 TCP 연결의 상태는 도쿄에만 있다. "
      "BGP 가 LA 쪽 경로로 갈아타면 같은 연결의 다음 세그먼트가 상태 없는 LA 에 도착하고, LA 는 맞는 소켓이 없어 리셋을 돌려준다.",
      "위는 경로가 바뀌기 전, 아래는 바뀐 뒤입니다. 사용자는 아무것도 하지 않았습니다.")


def node(x, y, w, name, sub, stroke=MUTED, sub_c=MUTED):
    d.box(x, y, w, 56, PAPER2, stroke, 1.0, 7)
    d.t(x + w / 2, y + 24, name, 13, INK, KR, "middle", 600)
    d.t(x + w / 2, y + 44, sub, 12, sub_c, MONO if sub[0].isdigit() else KR)


def chip(cx, cy, txt, c):
    w = len(txt) * 12 + 16
    d.tone(cx - w / 2, cy - 12, w, 24, c, r=4, op="14", sw=1.2)
    d.t(cx, cy + 5, txt, 12, c, KR, "middle", 600)


def panel(y0, title, router_sub, router_c, to_tokyo, to_la, tokyo_chip, la_chip, user_label):
    d.box(24, y0, 952, 236 if y0 > 200 else 192, f"{INK}05", RULE, 1.0, 10)
    d.t(40, y0 + 24, title, 13, INK, KR, "start", 600)
    uy, ty, ly = y0 + 72, y0 + 40, y0 + 112            # 사용자·라우터 / 도쿄 / LA 상자 윗변
    uc, tc, lc = uy + 28, ty + 28, ly + 28
    d.path(f"M 192 {uc} L 308 {uc}", MUTED, 1.4, m="ar")
    d.t(250, uc - 12, user_label, 12, MUTED, KR)
    for (y_out, y_in, style) in ((uc - 8, tc, to_tokyo), (uc + 8, lc, to_la)):
        c, dash, m = style
        d.path(f"M 472 {y_out} L 556 {y_out} L 556 {y_in} L 636 {y_in}", c, 1.4 if dash else 1.8, m=m, dash=dash)
    node(48, uy, 144, "사용자", "198.51.100.7")
    node(312, uy, 160, "경로 위 라우터", router_sub, sub_c=router_c)
    node(640, ty, 200, "도쿄 인스턴스", "203.0.113.9")
    node(640, ly, 200, "LA 인스턴스", "203.0.113.9")
    if tokyo_chip: chip(908, tc, *tokyo_chip)
    if la_chip: chip(908, lc, *la_chip)
    return uc, lc, ly


IDLE = (MUTED, "4 3", None)

# ── 1. 경로가 바뀌기 전 ──
panel(104, "1. 경로가 바뀌기 전", "최선 경로: 도쿄", MUTED,
      (OK, None, "ok"), IDLE, ("소켓 있음", OK), None, "연결 맺기")
d.t(740, 284, "LA 광고도 받았지만 지금은 덜 좋은 경로", 12, MUTED, KR)

# 경로가 바뀌는 순간 — 두 칸 사이
d.t(500, 318, "BGP 가 경로를 다시 고릅니다 · 이제 LA 쪽 광고가 이깁니다", 12, WARN, KR, "middle", 600)

# ── 2. 경로가 바뀐 뒤 ──
uc, lc, ly = panel(328, "2. 경로가 바뀐 뒤", "최선 경로: LA", WARN,
                   IDLE, (WARN, None, "warn"), ("소켓 있음", OK), ("소켓 없음", BAD), "다음 세그먼트")

# focal — 리셋이 사용자에게 돌아간다 (노트의 읽기)
d.path(f"M 740 {ly + 56} L 740 528 L 120 528 L 120 {uc + 32}", ACC, 1.8, m="acc")
d.t(430, 548, "RST · LA 에 이 연결의 소켓이 없음 (노트의 읽기)", 12, ACC, KR, "middle", 600)

d.t(24, 596, "주소는 끝까지 203.0.113.9 하나인데 그 주소를 받는 기계가 도쿄에서 LA 로 바뀌었습니다.", 13, INK, KR, "start", 600)
d.t(24, 620, "연결 상태는 도쿄의 메모리에만 있으므로 LA 는 이 세그먼트를 모릅니다. 사용자는 아무것도 하지 않았는데 연결이 끊깁니다.", 13, MUTED, KR, "start")

d.legend(640, [("연결 상태가 있는 곳", OK), ("BGP 가 새로 고른 경로", WARN), ("상태가 없는 곳", BAD), ("리셋 · 노트의 읽기", ACC)])
d.t(960, 680, "KUROSE-ROSS 9E §5.4.4 · RFC 5737 예시 주소", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-02.anycast-break.svg"
d.save(out)
print("→", out)
