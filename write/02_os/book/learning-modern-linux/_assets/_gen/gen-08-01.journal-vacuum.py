# 08-01 §4 「줄일 때는 vacuum, 지우면 안 되는 이유」 — 저널 디렉터리 안의 파일이 rotate 와 vacuum 으로
#           어떻게 바뀌는지를 실제 출력 값으로 보인다.
# 실측(본문 출력 블록, 컨테이너): journalctl --disk-usage → "Archived and active journals take up 36.7M",
#   journalctl --rotate → journalctl --vacuum-size=16M 이
#   "Deleted archived journal /var/log/journal/f6c1e3bd.../system@...-....journal (21.6M)" 와
#   "freed 21.6M of archived journals" 를 남김 → --disk-usage 15.1M. 36.7 − 21.6 = 15.1.
# 1차 자료: journalctl(1) --disk-usage(보관과 활성을 합친 값)·--rotate(활성 → 보관, 새 활성)·
#   --vacuum-size(보관 파일만, 오래된 것부터).
# 구조: 막대 하나가 /var/log/journal/f6c1e3bd.../ 안 파일의 합이다. 막대 아래쪽을 오래된 파일로 두어,
#   vacuum 이 맨 아래 보관 파일 21.6M 을 지우고 나머지가 내려앉는 모습으로 그린다.
# 축약: rotate 직후의 합계와 새 활성 파일의 크기는 출력에 없다. 그래서 둘째 막대는 앞 값 높이에 두고
#   새 활성 파일은 크기 없는 점선 칸으로만 그렸다. 36.7M 이 보관 몇 개와 활성 하나로 어떻게 나뉘는지도
#   출력에 없어 첫 막대는 쪼개지 않았다. (이전 판의 "처음 8.0M" 막대는 이 출력 블록에 없는 값이라 뺐다.)
# 타입 스펙: type-waterfall — 시작 합계가 삭제 한 번을 거쳐 끝 합계가 된다. 세로축은 MB 선형 눈금,
#           16M 목표선은 점선. accent 는 vacuum 이 지운 보관 파일 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 556
d = D(W, H, "LEARNING MODERN LINUX · 08-01 §4",
      "저널 사용량은 rotate 뒤 vacuum 으로 줄어든다",
      "컨테이너의 /var/log/journal/f6c1e3bd.../ 안 파일 합계가 --disk-usage, --rotate, --vacuum-size=16M, "
      "--disk-usage 를 차례로 지나며 바뀌는 모습. rotate 가 활성 파일을 보관으로 넘기고, vacuum 이 가장 오래된 "
      "보관 파일 system@….journal 21.6M 을 지워 36.7M 이 15.1M 이 된다.",
      "vacuum 은 보관 파일만, 오래된 것부터 지운다 — 21.6M 하나로 16M 아래가 됐다")

BASE, TOP, MAXM = 420, 160, 40
SC = (BASE - TOP) / MAXM


def y(mb):
    return BASE - mb * SC


d.t(24, 124, "/var/log/journal/f6c1e3bd.../", 13, INK, MONO, "start", 600)
d.t(272, 124, "안 파일의 합계", 12, MUTED, KR, "start")

AXX = 96
d.line(AXX, TOP, AXX, BASE, RULE, 1.0)
d.line(AXX, BASE, 840, BASE, RULE, 1.0)
for mb in (0, 10, 20, 30, 40):
    d.line(AXX - 4, y(mb), AXX, y(mb), RULE, 1.0)
    d.t(AXX - 8, y(mb) + 4, f"{mb}M", 11, SOFT, MONO, "end")

d.line(AXX, y(16), 840, y(16), SOFT, 1.0, "6 4")
d.t(844, y(16) + 4, "16M", 11, SOFT, MONO, "start")

BW, X0, STRIDE = 128, 136, 184
X = [X0 + i * STRIDE for i in range(4)]

# 막대 사이 높이 잇기
d.line(X[0] + BW, y(36.7), X[1], y(36.7), MUTED, 1.0, "3 4")
d.line(X[1] + BW, y(36.7), X[2], y(36.7), MUTED, 1.0, "3 4")

# 1 — --disk-usage 36.7M
d.tone(X[0], y(36.7), BW, y(0) - y(36.7), INFO, 4, "22", 1.2)
d.t(X[0] + BW / 2, y(36.7) - 8, "36.7M", 13, INFO, MONO, "middle", 600)
d.t(X[0] + BW / 2, y(27), "보관 + 활성", 12, INK, KR)

# 2 — --rotate: 전부 보관 + 새 활성(크기 출력 없음)
d.tone(X[1], y(36.7), BW, y(0) - y(36.7), MUTED, 4, "22", 1.2)
d.t(X[1] + BW / 2, y(27), "전부 보관", 12, INK, KR)
d.t(X[1] + BW / 2, y(27) + 18, "옛 활성 포함", 11, MUTED, KR)
NA = 14
d.o.append(f'<rect x="{X[1]}" y="{y(36.7) - NA - 2}" width="{BW}" height="{NA}" rx="3" '
           f'fill="none" stroke="{OK}" stroke-width="1.1" stroke-dasharray="4 3"/>')
d.t(X[1] + BW / 2, y(36.7) - NA - 10, "새 system.journal", 12, OK, MONO, "middle", 600)

# 3 — --vacuum-size=16M: 맨 아래(가장 오래된) 보관 파일 21.6M 삭제
d.o.append(f'<rect x="{X[2]}" y="{y(21.6)}" width="{BW}" height="{y(0) - y(21.6)}" rx="4" '
           f'fill="{ACC}1A" stroke="{ACC}" stroke-width="1.4" stroke-dasharray="6 4"/>')
d.t(X[2] + BW / 2, y(10.8) - 6, "system@….journal", 12, ACC, MONO, "middle", 600)
d.t(X[2] + BW / 2, y(10.8) + 14, "21.6M 삭제", 13, ACC, KR, "middle", 600)
d.tone(X[2], y(36.7), BW, y(21.6) - y(36.7), MUTED, 4, "22", 1.2)
d.t(X[2] + BW / 2, (y(36.7) + y(21.6)) / 2 + 5, "남는 15.1M", 12, INK, KR)
d.t(X[2] + BW / 2, y(36.7) - 8, "가장 오래된 것부터", 12, MUTED, KR)

# 4 — --disk-usage 15.1M (남은 파일이 바닥으로)
d.arrow([(X[2] + BW + 4, (y(36.7) + y(21.6)) / 2), (X[3] + BW / 2, (y(36.7) + y(21.6)) / 2),
         (X[3] + BW / 2, y(16) - 28)], MUTED, "ar", 1.1)
d.tone(X[3], y(15.1), BW, y(0) - y(15.1), OK, 4, "22", 1.2)
d.t(X[3] + BW / 2, y(16) - 8, "15.1M", 13, OK, MONO, "middle", 600)
d.t(X[3] + BW / 2, y(7.5) + 5, "보관 + 활성", 12, INK, KR)

for x, cmd, sub in ((X[0], "--disk-usage", "채운 뒤"), (X[1], "--rotate", "활성 → 보관"),
                    (X[2], "--vacuum-size=16M", "보관 파일만"), (X[3], "--disk-usage", "정리 뒤")):
    d.t(x + BW / 2, BASE + 22, cmd, 12, MUTED, MONO)
    d.t(x + BW / 2, BASE + 40, sub, 12, SOFT, KR)

NY = BASE + 72
d.t(24, NY, "36.7 − 21.6 = 15.1 · 막대 아래가 오래된 파일 · rotate 직후 합계와 새 활성 크기는 출력에 없음",
    11, SOFT, KR, "start")
d.legend(NY + 16, [("vacuum 이 지운 보관 파일", ACC), ("보관 + 활성 합계", INFO),
                   ("보관 파일", MUTED), ("새 활성 · 정리 뒤", OK)])
d.save("08-01.journal-vacuum.svg")
print("ok 08-01.journal-vacuum")
