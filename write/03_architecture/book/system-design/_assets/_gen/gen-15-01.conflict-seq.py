# 타입 스펙: type-sequence — 참여자 셋(클라이언트 A · 서버 · 클라이언트 B). 같은 기준 버전 v7 에서 둘이 수정하고 먼저 도착한 A 가 v8 을 만들며 B 는 충돌을 받는다. focal 은 B 의 충돌 응답.
# 사실 출처: 추출본 v2.txt 4504~4520행(먼저 처리된 버전이 이기고 나중 것은 충돌, 사용자 2 에게 로컬 사본과 서버 최신본 둘을 보여 주고 병합 또는 한쪽 덮어쓰기 선택).
#   v7·v8·plan.txt 는 설명용 값이며 충돌을 알아내려면 기준 버전을 최신 버전과 비교해야 한다는 점은 이 도식을 위한 설계 설명이며, 같은 원리의 실제 API 는 Dropbox files.stone L446-L454 WriteMode.update(rev 가 같을 때만 덮어씀, 아니면 conflicted copy)다.
# Layout conventions: 레인 폭 176·중심 x=140·440·740, 메시지 stride 60(y=196부터), 상태 칩 y=292·436·476, 레일 하단 H-80. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO


def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 12


class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.o.append(f'<rect x="{mx - _w(label, 13)/2}" y="{y - 23}" width="{_w(label, 13)}" height="18" fill="{PAPER}"/>')
        s.t(mx, y - 9, label, 13, c, _kr(label), "middle", 600)
        if sub:
            s.o.append(f'<rect x="{mx - _w(sub, 13)/2}" y="{y + 5}" width="{_w(sub, 13)}" height="20" fill="{PAPER}"/>')
            s.t(mx, y + 19, sub, 13, MUTED, _kr(sub))

    def chip(s, a, txt, y, c):
        x = s.LX[a]; w = _w(txt, 13) + 12
        s.o.append(f'<rect x="{x - w/2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{PAPER}"/>')
        s.o.append(f'<rect x="{x - w/2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 13, c, _kr(txt))


W, H = 880, 620
d = SeqKR(W, H, "SYSTEM DESIGN INTERVIEW · 15-01 §4",
          "같은 v7 에서 고친 두 쓰기 중 먼저 온 쪽만 v8 이 된다",
          "서버는 기준 버전을 최신 버전과 비교해, 이미 v8 이 된 파일에 v7 기준 쓰기가 오면 충돌로 돌려보낸다.",
          "먼저 처리된 쪽이 이긴다")

A, S, B = "클라이언트 A", "서버", "클라이언트 B"
d.LX = {A: 140, S: 440, B: 740}
for nm, sub in ((A, "기준 v7"), (S, "plan.txt 최신 v7"), (B, "기준 v7")):
    x = d.LX[nm]
    d.box(x - 88, 100, 176, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 13, INK, _kr(nm), "middle", 600)
    d.t(x, 137, sub, 13, MUTED, _kr(sub))
d.lane_top = 144
d.rails(H - 80)

d.msg(A, S, "PUT plan.txt", 196, INFO, "info", sub="기준 v7")
d.msg(S, A, "저장 · v8", 256, INFO, "info", dash="5 4")
d.chip(S, "최신 = v8", 300, OK)
d.msg(B, S, "PUT plan.txt", 360, WARN, "warn", sub="기준 v7")
d.msg(S, B, "충돌 · 최신 v8", 420, ACC, "acc", dash="5 4")
d.chip(B, "내 사본 v7 + 서버 v8", 468, BAD)
d.chip(B, "병합 또는 한쪽 덮어쓰기", 504, WARN)

d.legend(H - 56, [("먼저 온 쓰기", INFO), ("늦게 온 쓰기", WARN), ("충돌 응답", ACC), ("최신 버전", OK), ("충돌 상태", BAD)])
d.save("15-01.conflict-seq.svg")
