# 01-01 §4 — IGMP 스누핑이 없으면 멀티캐스트가 모든 포트로 퍼지고, 켜면 가입 포트로만 간다.
# 본문 요구: "스위치는 그 보고의 수신자가 아니지만 지나가는 IGMP 를 엿봐 가입 포트를 기억합니다.
#            그다음부터 그 그룹의 프레임은 가입 포트로만 보냅니다."
#            문제(모든 포트로 복사)와 해결(가입 포트로만)을 같은 토폴로지에 나란히 두어야
#            무엇이 달라졌는지 — 스위치 칸의 기록 한 줄 — 이 보인다.
# 타입 스펙: type-architecture — 구성요소(라우터 · 스위치 · 포트 셋)와 연결. 흐름은 시퀀스가 아니라
#           토폴로지 위 번호 화살표로 보인다. 두 패널은 같은 좌표 공식(cx 기준 오프셋)을 공유해
#           칸이 줄 단위로 짝이 맞는다. focal 은 오른쪽 스위치가 엿봐 남긴 가입 기록 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 520
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 01-01 §4",
      "IGMP 스누핑 — 가입 보고를 엿봐 가입 포트로만",
      "같은 스위치에 장비 B · 나(분석기) · 그룹 가입자 C 가 붙어 있다. 스누핑이 없으면 그룹 239.1.1.1 의 프레임이 "
      "세 포트 모두에 복사된다. 스누핑을 켜면 C 가 라우터에게 보내는 IGMP 가입 보고를 스위치가 엿봐 C 포트를 기록하고, "
      "그 뒤 그룹 프레임을 C 포트로만 보낸다.",
      "스누핑이 없으면 스위치는 가입자를 몰라 멀티캐스트를 모든 포트로 복사합니다")

PW = 400                                  # 패널 폭
PANELS = [(24, "스누핑 없음", "가입자를 모르는 스위치"), (456, "스누핑 켬", "가입 보고를 엿본 스위치")]
RY, RW, RH = 152, 160, 44                 # 라우터 칸
SY, SW, SH = 244, 352, 60                 # 스위치 칸
PY, PWD, PH = 356, 104, 52                # 포트 칸
BUS = 328                                 # 스위치 아래 버스
OFF = 128                                 # 포트 간격 — B 는 cx-OFF, 나는 cx, C 는 cx+OFF

d.line(440, 100, 440, 452, RULE, 1.0, "4 6")

def port(cx, name, state, kind):
    x = cx - PWD / 2
    if kind == "ok":
        d.tone(x, PY, PWD, PH, OK, 6); col = OK
    elif kind == "warn":
        d.tone(x, PY, PWD, PH, WARN, 6); col = WARN
    else:
        d.o.append(f'<rect x="{x}" y="{PY}" width="{PWD}" height="{PH}" rx="6" fill="{PAPER}" '
                   f'stroke="{SOFT}" stroke-width="1.0" stroke-dasharray="4,3"/>')
        col = SOFT
    d.t(cx, PY + 21, name, 13, INK if kind != "none" else MUTED, KR, "middle", 600)
    d.t(cx, PY + 40, state, 12, col, KR, "middle")

for p, (x0, title, sub) in enumerate(PANELS):
    cx = x0 + PW / 2
    d.t(cx, 112, title, 13, INK, KR, "middle", 600)
    d.t(cx, 132, sub, 12, MUTED, KR, "middle")
    # 라우터
    d.box(cx - RW / 2, RY, RW, RH, PAPER2, RULE, 1.0, 6)
    d.t(cx, RY + 20, "라우터", 13, INK, KR, "middle", 600)
    d.t(cx, RY + 37, "그룹 트래픽 입구", 12, MUTED, KR, "middle")
    # 스위치
    d.box(cx - SW / 2, SY, SW, SH, PAPER2, RULE, 1.0, 8)
    d.t(cx, SY + 20, "스위치", 13, INK, KR, "middle", 600)

    if p == 0:
        # 문제 — 가입 기록이 없어 들어온 포트를 뺀 모든 포트로 복사
        d.t(cx, SY + 44, "가입 기록 없음", 12, MUTED, KR, "middle")
        d.arrow([(cx, RY + RH), (cx, SY - 4)], INFO, "info", 1.4)
        d.t(cx + 10, 224, "239.1.1.1 데이터", 12, INFO, KR, "start")
        d.path(f"M {cx} {SY + SH} V {BUS} M {cx - OFF} {BUS} H {cx + OFF}", INFO, 1.4)
        for dx in (-OFF, 0, OFF):
            d.arrow([(cx + dx, BUS), (cx + dx, PY - 4)], INFO, "info", 1.4)
        port(cx - OFF, "장비 B", "원치 않는 도착", "warn")
        port(cx, "나", "원치 않는 도착", "warn")
        port(cx + OFF, "그룹 가입자 C", "도착", "ok")
        d.t(cx, 436, "B · 나에게도 복사", 13, WARN, KR, "middle", 600)
    else:
        # 해결 — 1 가입 보고를 엿봐 기록, 2 그룹 데이터는 기록된 포트로만
        d.o.append(f'<rect x="{cx - 104}" y="{SY + 28}" width="208" height="24" rx="4" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        d.t(cx, SY + 45, "기록  239.1.1.1 = C 포트", 12, ACC, KR, "middle", 600)
        # 1 — C 에서 라우터로 올라가는 가입 보고 (스위치를 지나며 엿보임)
        d.arrow([(cx + OFF + 16, PY), (cx + OFF + 16, SY + SH + 4)], MUTED, "ar", 1.3, "5 4")
        d.arrow([(cx + 24, SY), (cx + 24, RY + RH + 4)], MUTED, "ar", 1.3, "5 4")
        d.t(cx + 32, 224, "1  IGMP 가입 보고", 12, MUTED, KR, "start")
        # 2 — 라우터에서 C 로만 내려가는 그룹 데이터
        d.arrow([(cx - 24, RY + RH), (cx - 24, SY - 4)], INFO, "info", 1.4)
        d.t(cx - 32, 224, "2  239.1.1.1 데이터", 12, INFO, KR, "end")
        d.arrow([(cx + OFF - 16, SY + SH), (cx + OFF - 16, PY - 4)], INFO, "info", 1.4)
        port(cx - OFF, "장비 B", "안 옴", "none")
        port(cx, "나", "안 옴", "none")
        port(cx + OFF, "그룹 가입자 C", "도착", "ok")
        d.t(cx, 436, "C 포트로만", 13, OK, KR, "middle", 600)

d.legend(H - 48, [("스누핑이 남긴 가입 기록", ACC), ("가입자에게 도착", OK),
                  ("가입 안 했는데 도착", WARN), ("그룹 데이터", INFO)])
d.save("01-01.igmp-snooping.svg")
