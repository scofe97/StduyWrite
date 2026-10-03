# 06-01 §2 — 바라는 상태가 3초에 바뀌었을 때 폴링 간격별로 컨트롤러가 알아채는 시점과 요청 수.
# 본문 근거: 이 노트 §2 「조정 루프는 세 걸음입니다」 끝 두 문단과 「watch 가 폴링을 대신합니다」.
#            간격 10초·2초와 변경 시각 3초는 설명용 예시 값이다.
# 타입 스펙: type-gantt — 같은 변경 뒤 알아채기까지의 구간 길이와 요청 점의 밀도가 논지다. 가로축은 초.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, BAD, WARN, INFO, KR, MONO

W, H = 880, 470
d = D(W, H, "LEARNING COREDNS · 06-01 §2",
      "폴링은 간격과 부하를 맞바꾸고, watch 는 둘 다 피한다",
      "3초에 바라는 상태가 바뀐다. 10초 간격 폴링은 7초 뒤에야 알고, 2초 간격은 1초 뒤에 알지만 요청이 네 배다. "
      "watch 는 연결 하나를 열어 두고 변경을 밀어 받으므로 바로 안다.",
      "주황 점이 변경을 바로 아는 자리입니다")


def X(t):
    return 220 + t * 20


for t in range(0, 31, 5):
    d.t(X(t), 118, f"{t}s", 12, SOFT, MONO)
    d.line(X(t), 128, X(t), 352, RULE, 0.6, "2 6")
d.line(X(0), 128, X(30), 128, RULE, 1.0)

d.line(X(3), 136, X(3), 352, ACC, 1.2, "4 4")
d.t(X(3) + 6, 146, "3s · Spec 변경", 12, ACC, KR, "start")

lanes = [(190, "폴링 · 10초 간격", "요청 4번", 10, BAD, 10),
         (260, "폴링 · 2초 간격", "요청 16번", 2, WARN, 4),
         (330, "watch", "연결 1개", None, INFO, 3)]
for cy, nm, sub, step, c, seen in lanes:
    d.t(20, cy - 2, nm, 14, INK, KR, "start", 600)
    d.t(20, cy + 18, sub, 12, MUTED, KR, "start")
    if step:
        if seen > 3:
            d.box(X(3), cy - 10, X(seen) - X(3), 20, PAPER, "none", 0, 3)
            d.tone(X(3), cy - 10, X(seen) - X(3), 20, c, 3, "22", 1.0)
        for t in range(0, 31, step):
            d.o.append(f'<circle cx="{X(t)}" cy="{cy}" r="4" fill="{MUTED}"/>')
        d.o.append(f'<circle cx="{X(seen)}" cy="{cy}" r="6" fill="none" stroke="{c}" stroke-width="1.6"/>')
        d.t(X(seen) + 10, cy - 14, f"{seen - 3}초 뒤 앎", 12, c, KR, "start")
    else:
        d.o.append(f'<rect x="{X(0)}" y="{cy - 3}" width="{X(30) - X(0)}" height="6" rx="3" fill="{c}" fill-opacity="0.35"/>')
        d.o.append(f'<circle cx="{X(3)}" cy="{cy}" r="7" fill="{ACC}"/>')
        d.t(X(3) + 12, cy - 12, "변경을 밀어 받음 · 바로 앎", 12, ACC, KR, "start", 600)

d.t(20, 394, "회색 점 · API 서버로 가는 폴링 요청 · 간격을 줄일수록 반응은 빨라지고 부하는 커진다", 13, MUTED, KR, "start")
d.t(20, 416, "간격 10초 · 2초와 변경 시각은 예시 값", 12, SOFT, KR, "start")

d.legend(430, [("모르는 구간 · 10초", BAD), ("모르는 구간 · 2초", WARN), ("watch 연결", INFO), ("바로 아는 자리", ACC)])
d.save("06-01.poll-vs-watch.svg")
