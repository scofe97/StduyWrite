# 04-04.readiness-timeline — readiness 를 잃고 되찾는 데 걸린 시간
# 본문 요구: `## readiness 를 잃을 때 사라지는 줄` 의 확인된 것 — 프로브 주기 5초 · failureThreshold 2 · successThreshold 1 이라
#           낙하는 5~10초 범위(관찰 8초 · 재실행 9.9초), 복귀는 한 번의 성공으로 뒤집혀 더 짧다(관찰 1초·4초 · 재실행 3.3초).
# 타입 스펙: type-timeline — 사건이 시간 축 위에 놓인다. 같은 0~10초 축에 두 줄(낙하·복귀), 이론 범위는 띠, 잰 값은 점.
#           빈 점은 2026-09 관찰, 찬 점은 2026-11-08 재실행. coral focal 은 낙하보다 짧은 복귀 띠 하나.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 590
X0, X1 = 240, 940
SEC = (X1 - X0) / 10.0


def sx(s):
    return X0 + s * SEC


d = D(W, H, "TIMELINE · 04-04 READINESS",
      "복귀는 낙하보다 짧습니다",
      "readiness 프로브가 주기 5초, failureThreshold 2, successThreshold 1 일 때 Pod 가 서비스 명단에서 빠지고 돌아오는 시간. "
      "낙하는 5초에서 10초 사이이고 2026-09 에는 8초, 2026-11-08 에는 9.9초였다. "
      "복귀는 성공 한 번으로 뒤집혀 2026-09 에 1초와 4초, 2026-11-08 에 3.3초였다.",
      lead="띠는 설정에서 나오는 범위, 빈 점은 2026-09 관찰, 찬 점은 2026-11-08 재실행입니다")

LANES = [
    # 제목, 부제, y, 띠 시작, 띠 끝, 띠 설명, 색, 점(초, 라벨, 찬 점 여부)
    ("낙하", "rm /tmp/ready", 190, 5, 10, "5~10초 = 첫 검사 0~5 + 한 번 더 5", INFO,
     [(8.0, "8초", False), (9.9, "9.9초", True)]),
    ("복귀", "touch /tmp/ready", 350, 0, 5, "0~5초 = 첫 성공 한 번", ACC,
     [(1.0, "1초", False), (4.0, "4초", False), (3.3, "3.3초", True)]),
]

AXY = 450
for s in range(0, 11):
    x = sx(s)
    d.line(x, 118, x, AXY, RULE, 0.6, "2 4")
    d.line(x, AXY, x, AXY + 6, MUTED, 1.0)
    d.t(x, AXY + 22, str(s), 12, MUTED, MONO, "middle")
d.line(X0, AXY, X1, AXY, MUTED, 1.2)
d.t(X1, AXY + 44, "초 (rm 또는 touch 를 친 시점부터)", 12, MUTED, KR, "end")

for title, sub, y, a, b, note, c, pts in LANES:
    d.t(24, y - 2, title, 14, c if c == ACC else INK, KR, "start", 600)
    d.t(24, y + 20, sub, 12, MUTED, MONO, "start")
    d.line(X0, y, X1, y, SOFT, 1.0)
    d.tone(sx(a), y - 15, (b - a) * SEC, 30, c, 6, "1F" if c == ACC else "14", 1.5 if c == ACC else 1.1)
    d.t((sx(a) + sx(b)) / 2, y - 26, ddx.fit(note, 12, (b - a) * SEC + 60, note), 12, c, KR, "middle", 600)
    for s, lab, filled in pts:
        x = sx(s)
        if filled:
            d.o.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{INK}" stroke="{INK}" stroke-width="1.4"/>')
            d.t(x, y + 36, lab, 12, INK, KR, "middle", 600)
        else:
            d.o.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>')
            d.t(x, y + 36, lab, 12, MUTED, KR, "middle")

d.t(24, 268, "낙하 뒤 재시작 0 · 나가는 길은 열림 · 서비스 체인에서만 빠짐", 12, MUTED, KR, "start")
d.t(24, 288, "빠진 Pod 의 엔드포인트 체인 미생성 · 서비스 체인에 확률 0.50000000000 한 줄", 12, MUTED, KR, "start")

d.legend(528, [("설정에서 나오는 범위", INFO), ("낙하보다 짧은 복귀", ACC)])
d.save("04-04.readiness-timeline.svg")
print("ok readiness-timeline")
