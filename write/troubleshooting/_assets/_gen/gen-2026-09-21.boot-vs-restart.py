# 2026-09-21 A(배포하지 않은 아침) 문항 · 원인 분석 — 사건.
# 논지는 "같은 두 주체가 같은 표에 손대는데, 누가 먼저냐에 따라 결과가 갈린다" 이다.
# 노드 하나의 라우팅 테이블을 두 순서로 옮겨 그린다. 무대는 two-writers-one-table 이 맡는다.
# 타입 스펙: type-timeline — 사건이 순서 위에 놓인다. 축은 시각이 아니라 순서라 간격은 같게 둔다.
#           같은 표를 네 컷으로 세워 어느 줄이 언제 생기고 언제 걷히는지 대조한다.
#           type-sequence 는 주체 사이 메시지가 논지가 아니라 기각, type-swimlane 은 두 줄이 주체가 아니라 시나리오라 기각.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, OK, BAD, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 600
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-21 A",
      "누가 먼저 표에 손대느냐가 결과를 가릅니다",
      "노드 하나의 라우팅 테이블을 두 순서로 놓았다. 부팅할 때는 networkd 가 먼저 뜨고 CNI 가 뒤에 Pod 대역 줄을 넣어, "
      "networkd 가 볼 때 지울 남의 줄이 아직 없다. 돌던 노드에서 자동 업데이트가 networkd 만 다시 띄우면 "
      "그때는 CNI 의 줄이 이미 표에 있고, networkd 는 자기 설정에 없는 그 줄을 지운다.",
      lead="두 주체도 같고 표도 같습니다. 다른 것은 순서 하나입니다")

COLW, STRIDE, X0 = 200, 232, 48
BH = 140

# (제목, 부제, default 줄 상태, Pod 줄 상태, 결과) — 상태는 have / none / gone
TRACKS = [
    (132, "정상 부팅 · 새 노드와 재부팅 노드", [
        ("부팅 시작", "표가 비어 있음", "none", "none", None),
        ("networkd 기동", "자기 경로만", "have", "none", None),
        ("CNI 기동", "Pod 대역 줄 추가", "have", "have", None),
        (None, None, None, None, ("Pod 통신 정상", OK)),
    ]),
    (344, "돌던 노드 · 06:00~07:00 UTC", [
        ("평소 운영", "두 줄 모두 있음", "have", "have", None),
        ("타이머 발동", "systemd 패키지 갱신", "have", "have", None),
        ("networkd 재시작", "설정에 없는 줄 삭제", "have", "gone", "focal"),
        (None, None, None, None, ("Pod 통신 끊김", BAD)),
    ]),
]


def row(x, y, label, color, state):
    w = COLW - 28
    if state == "have":
        d.box(x, y, w, 26, PAPER, color, 0.9, 4)
        d.t(x + 10, y + 17, label, 11, color, MONO, "start")
    elif state == "none":
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="4" fill="none" '
                   f'stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="3 3"/>')
        d.t(x + 10, y + 17, "아직 없음", 11, SOFT, KR, "start")
    else:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="4" fill="{BAD}14" '
                   f'stroke="{BAD}" stroke-width="0.9" stroke-dasharray="3 3"/>')
        d.t(x + 10, y + 17, "지워짐", 11, BAD, KR, "start")


for ty, name, steps in TRACKS:
    d.t(X0, ty - 12, name, 11, SOFT, MONO, "start")
    for i, (title, sub, s_def, s_pod, extra) in enumerate(steps):
        x = X0 + i * STRIDE
        if i < len(steps) - 1:
            d.arrow([(x + COLW, ty + BH // 2), (x + STRIDE - 2, ty + BH // 2)], MUTED, "ar", 1.2)
        if title is None:
            text, c = extra
            d.tone(x, ty + 36, COLW, BH - 72, c, 6)
            d.t(x + COLW // 2, ty + BH // 2 + 5, text, 13, c, KR, "middle", 600)
            continue
        if extra == "focal":
            d.tone(x, ty, COLW, BH, ACC, 6)
            tc = ACC
        else:
            d.box(x, ty, COLW, BH, PAPER2, RULE, 0.9, 6)
            tc = INK
        d.t(x + 14, ty + 24, title, 13, tc, KR, "start", 600)
        d.t(x + 14, ty + 44, sub, 11, MUTED, KR, "start")
        row(x + 14, ty + 62, "default via …", INFO, s_def)
        row(x + 14, ty + 98, "Pod 대역 via …", OK, s_pod)

d.t(X0, 520, "축은 시각이 아니라 순서", 11, SOFT, KR, "start")

d.legend(H - 56, [("networkd 가 넣은 줄", INFO), ("CNI 가 넣은 줄", OK), ("지워진 줄", BAD), ("사고가 나는 순간", ACC)])
d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-21.boot-vs-restart.svg"))
print("ok")
