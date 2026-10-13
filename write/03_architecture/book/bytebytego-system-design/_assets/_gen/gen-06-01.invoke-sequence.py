# 타입 스펙: type-sequence — Lambda 동기 호출 두 번. 첫 호출은 빈 슬롯이 없어 Placement 가 슬롯(microVM)을 만들고, 같은 함수의 두 번째 호출은 같은 슬롯을 재사용해 반환값이 0 에서 1 로 올라간다(레인 5, 메시지 15).
# 사실 출처: Firecracker NSDI'20 논문 §4.1.1(Invoke REST API → frontend 인증·메타데이터 → Worker Manager 의 sticky routing · 빈 슬롯이 없으면 Placement 가 슬롯 생성 요청 · 배치 결정은 대개 20ms 미만 · 시간 제한 lease 로 슬롯을 Worker Manager 에 임대)
#   · §4.1.2(Frontend 가 슬롯과 payload 를 MicroManager 에 전달 → microVM 안 shim → 응답을 Frontend 로) · Listing 1(`var i = 0; handler → return i++`, 직렬 호출에서 숫자가 올라감)
#   https://www.usenix.org/system/files/nsdi20-paper-agache.pdf
#   · Lambda Invoke API: 동기(RequestResponse, 기본) 성공 응답 200 https://docs.aws.amazon.com/lambda/latest/api/API_Invoke.html
#   · 슬롯 상태는 논문 §4.2 의 initializing → idle → (idle ↔ busy). 0 → 1 은 논문 Listing 1 함수를 호출했을 때의 반환값이다.
# Layout conventions: 레인 5·폭 140·간격 167, 호출 한 건의 stride 52(라벨 y-9, 부라벨 y+17), 첫 메시지 y=196, 구분선 한 줄(y=196+8×52+16). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, Seq, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 12, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, sw=1.5):
        x1, x2 = s.LX[a], s.LX[b]
        d_ = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d_} {y} L {x2 - 12 * d_} {y}", c, sw, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 12, MUTED, _kr(sub))

    def chip(s, a, txt, y, c, dx=0):
        x = s.LX[a] + dx
        w = len(txt) * (12 if any("가" <= ch <= "힣" for ch in txt) else 7.8) + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 12, c, _kr(txt))


W, H = 880, 1100
d = SeqKR(W, H, "BYTEBYTEGO · 06-01 §4",
          "같은 함수를 두 번 부르면 슬롯이 한 번 만들어지고 두 번 쓰인다",
          "첫 호출은 Placement 가 슬롯을 만들어 0 을 돌려주고 두 번째 호출은 같은 슬롯에서 1 을 돌려줌 (논문 Listing 1 함수)",
          "슬롯 하나가 microVM 하나이고 함수 하나의 동시 호출 하나만 받습니다")
CL, FE, WM, PL, WK = "클라이언트", "Frontend", "Worker Manager", "Placement", "Worker"
d.lanes([(CL, "호출자"), (FE, "인증 · 메타데이터"), (WM, "슬롯 라우팅"), (PL, "슬롯 배치"), (WK, "microVM 슬롯")], 100, 140)
d.rails(H - 80)

Y0, S = 196, 52
r = lambda k: Y0 + k * S
# 첫 호출: 빈 슬롯 없음
d.msg(CL, FE, "POST …/invocations", r(0), MUTED, "ar", sub="RequestResponse")
d.msg(FE, WM, "슬롯 요청", r(1), MUTED, "ar")
d.msg(WM, PL, "새 슬롯", r(2), WARN, "warn", sub="빈 슬롯 없음")
d.msg(PL, WK, "슬롯 만들기", r(3), WARN, "warn", sub="배치 20 ms 미만")
d.chip(WK, "Init", r(3) + 30, WARN, 0)
d.msg(PL, WM, "슬롯 임대", r(4), MUTED, "ar", dash="5 4", sub="시간 제한 lease")
d.msg(WM, FE, "슬롯 알림", r(5), MUTED, "ar", dash="5 4")
d.chip(WK, "Idle", r(5) + 30, OK, 0)
d.msg(FE, WK, "payload", r(6), MUTED, "ar", sub="MicroManager → shim")
d.chip(WK, "Busy", r(6) + 30, WARN, 0)
d.msg(WK, FE, "반환 0", r(7), MUTED, "ar", dash="5 4")
d.msg(FE, CL, "200 · 0", r(8), MUTED, "ar", dash="5 4")
d.chip(WK, "Idle", r(8) + 30, OK, 0)

# 구분선
ys = r(8) + 52
d.line(24, ys, W - 24, ys, RULE, 0.8, "6 6")
d.t(W / 2, ys - 8, "같은 함수 두 번째 호출", 12, SOFT, KR)

# 두 번째 호출: 빈 슬롯 있음
Y1 = ys + 44
q = lambda k: Y1 + k * S
d.msg(CL, FE, "POST …/invocations", q(0), MUTED, "ar")
d.msg(FE, WM, "슬롯 요청", q(1), MUTED, "ar", sub="빈 슬롯 있음")
d.msg(WM, FE, "같은 슬롯", q(2), OK, "ok", dash="5 4")
d.msg(FE, WK, "payload", q(3), MUTED, "ar")
d.chip(WK, "Busy", q(3) + 30, WARN, 0)
d.msg(WK, FE, "반환 1", q(4), ACC, "acc", dash="5 4")
d.msg(FE, CL, "200 · 1", q(5), ACC, "acc", dash="5 4")
d.chip(WK, "Idle", q(5) + 30, OK, 0)

d.legend(H - 56, [("요청", MUTED), ("슬롯 없음", WARN), ("슬롯 재사용", OK), ("값이 오르는 자리", ACC)])
d.save("06-01.invoke-sequence.svg")
