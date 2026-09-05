# 07-01 §4 — 원문이 나열한 완화책이 각각 어느 층에 서는가. 바깥일수록 안쪽이 보는 양이 줄어든다.
# 타입 스펙: type-layers — 위에서 아래로 바깥에서 안쪽. 각 층은 무엇을 걸 수 있는지와
#           원문이 그 층에 적어 둔 실제 손잡이를 함께 싣는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, BAD, PAPER2, RULE, KR, MONO

W, H = 976, 544
X0, RW, RH, GAP, Y0 = 232, 688, 60, 12, 116

d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 07-01 §4",
      "완화가 설 수 있는 층",
      "원문이 SYN·ICMP 홍수 완화책으로 나열한 항목들을 층으로 갈라 놓은 것. 같은 공격을 어느 층에서 끊느냐에 따라 아래 층이 처리해야 할 양이 달라진다.",
      "원문의 구체적인 손잡이는 거의 전부 커널 층에 있습니다")

ROWS = [
    ("데이터센터 엣지 · 라우터", "네트워크 ACL · rate limit · DoS 보호 장비", "여기서 끊으면 안쪽은 아무것도 못 봅니다", None),
    ("로드밸런서", "연결을 대신 받아 냅니다", "공격은 LB 에서 끝나고 VM 은 남습니다", None),
    ("호스트 방화벽 · netfilter", "iptables -A INPUT ... -j DROP", "Wireshark 의 Firewall ACL Rules 가 만들어 줍니다", None),
    ("커널 TCP/IP 스택 · sysctl", "tcp_syncookies · tcp_synack_retries · icmp_echo_ignore_all", "원문의 손잡이가 모여 있는 층입니다", ACC),
    ("애플리케이션", "타임아웃 · 동시 접속 상한", "여기까지 왔다면 이미 늦습니다", BAD),
]

for i, (name, knob, note, c) in enumerate(ROWS):
    y = Y0 + i * (RH + GAP)
    if c: d.tone(X0, y, RW, RH, c, 6)
    else: d.box(X0, y, RW, RH, PAPER2, RULE, 1.0, 6)
    d.t(X0 + 16, y + 24, name, 12, c if c else INK, KR, "start", 600)
    d.t(X0 + 16, y + 45, knob, 11, MUTED, MONO, "start")
    d.t(X0 + RW - 16, y + 37, note, 11, SOFT, KR, "end")

BOT = Y0 + len(ROWS) * (RH + GAP) - GAP
d.arrow([(196, Y0 + 8), (196, BOT - 4)], SOFT, "soft", 1.2)
d.t(180, Y0 + 20, "바깥", 11, MUTED, KR, "end")
d.t(180, BOT - 8, "안쪽", 11, MUTED, KR, "end")
d.t(24, (Y0 + BOT) / 2, "막는 자리가", 11, SOFT, KR, "start")
d.t(24, (Y0 + BOT) / 2 + 16, "아래로 갈수록", 11, SOFT, KR, "start")
d.t(24, (Y0 + BOT) / 2 + 32, "쓰는 자원이 늡니다", 11, SOFT, KR, "start")

d.legend(H - 60, [("원문의 손잡이가 있는 층", ACC), ("이미 늦은 층", BAD)])
d.save("07-01.mitigation-layers.svg")
