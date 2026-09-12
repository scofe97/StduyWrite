# 2026-09-07 D1 — 패킷이 앱에 닿기까지 지나는 층과, 층마다 넘쳐서 버리는 자리.
# 회차에서 학습자가 "저장 공간이 차면 DROP 된다"까지 스스로 세웠으나 그 공간의 이름과
# 읽는 명령을 몰라 막혔다. 층·이름·명령을 한 줄로 짝지어 남긴다.
# 타입 스펙: type-layers — 바깥에서 안쪽으로 내려오는 통과 순서. 각 층은 넘쳤을 때
#           세는 카운터와 그것을 읽는 명령을 함께 싣는다. accent 는 이 문항의 답 한 층.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, BAD, PAPER2, RULE, KR, MONO

W, H = 836, 592
X0, RW, RH, GAP, Y0 = 176, 624, 64, 12, 120

ROWS = [
    ("NIC 링 버퍼", "ethtool -S · rx_missed_errors", "물리 NIC 에만 있습니다", None),
    ("커널 백로그 큐", "/proc/net/softnet_stat · 2열", "CPU 마다 따로 셉니다", None),
    ("conntrack 테이블", "conntrack -C · nf_conntrack_max", "연결을 기억하는 자리입니다", None),
    ("소켓 accept 큐", "nstat · TcpExtListenOverflows", "앱이 못 받아가면 여기가 찹니다", ACC),
    ("애플리케이션", "앱 로그", "여기가 조용하면 위에서 사라진 것입니다", BAD),
]

d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-07 D1",
      "패킷이 사라질 수 있는 층",
      "패킷이 NIC 에서 애플리케이션까지 올라오며 지나는 다섯 층. 층마다 넘치면 버리고, "
      "버릴 때마다 커널이 숫자를 세어 둔다. 어느 층의 숫자가 늘고 있는지가 곧 어디서 사라졌는지다.",
      lead="층마다 세는 카운터가 따로 있습니다. 아래에서 위로 올라가며 하나씩 읽습니다.")

for i, (name, cmd, note, c) in enumerate(ROWS):
    y = Y0 + i * (RH + GAP)
    if c:
        d.tone(X0, y, RW, RH, c, 6)
    else:
        d.box(X0, y, RW, RH, PAPER2, RULE, 1.0, 6)
    d.t(X0 + 16, y + 26, name, 13, c if c else INK, KR, "start", 600)
    d.t(X0 + 16, y + 48, cmd, 11, MUTED, MONO, "start")
    d.t(X0 + RW - 16, y + 38, note, 11, SOFT, KR, "end")

BOT = Y0 + len(ROWS) * (RH + GAP) - GAP
d.arrow([(144, Y0 + 8), (144, BOT - 4)], SOFT, "soft", 1.2)
d.t(128, Y0 + 20, "패킷 도착", 11, MUTED, KR, "end")
d.t(128, BOT - 8, "앱 도달", 11, MUTED, KR, "end")

d.t(24, Y0 + 150, "총량이 아니라", 11, SOFT, KR, "start")
d.t(24, Y0 + 166, "증가분을 봅니다", 11, SOFT, KR, "start")
d.t(24, Y0 + 190, "카운터는 부팅", 11, SOFT, KR, "start")
d.t(24, Y0 + 206, "이후 누적이라", 11, SOFT, KR, "start")
d.t(24, Y0 + 96, "총량만 보면", 11, SOFT, KR, "start")
d.t(24, Y0 + 112, "정상 오차를", 11, SOFT, KR, "start")
d.t(24, Y0 + 128, "문제로 읽습니다", 11, SOFT, KR, "start")

d.t(X0, BOT + 32, "DROP 은 조용합니다. REJECT 라야 즉시 거부가 돌아오고, 버려진 패킷은 타임아웃으로만 드러납니다.",
    12, MUTED, KR, "start")

d.legend(H - 56, [("이 문항의 답이 있던 층", ACC), ("로그가 비어 배제된 층", BAD)])
d.save("2026-09-07.drop-layers.svg")
print("ok drop-layers")
