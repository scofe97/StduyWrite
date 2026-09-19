# 01-01 §4 — 목적지 주소의 종류와 스위치 설정이 프레임을 어느 포트까지 복사하는가.
# 타입 스펙: type-architecture — 구성요소(보낸 프레임 · 스위치 · 포트 셋)와 연결. 흐름은 왼쪽 → 오른쪽 하나로 잡는다.
#           축약: 같은 토폴로지를 경우마다 한 줄씩 세로로 쌓는다(컷을 세로로 쌓는 관례). 스위치는 모든 줄을
#           관통하는 세로 기둥 하나이고, 기둥에서 나온 버스가 복사된 포트에만 수직으로 떨어진다 — 버스가 지나가도
#           떨어지지 않은 칸은 그 포트로 안 간 것이다. 멀티캐스트는 스누핑 유무와 224.0.0.x 예외로 세 줄로 가른다.
#           focal 은 01-02 실습에서 실제로 잡힌 자리(스누핑을 켜도 퍼지는 224.0.0.251 이 내 포트에 도착) 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 592
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 01-01 §4",
      "주소 종류가 정하는 도착 범위",
      "같은 스위치에 붙은 장비 B · 나(분석기) · 그룹 가입자 C 에게 프레임이 복사되는 범위. 유니캐스트는 목적지 포트로만, 브로드캐스트는 모든 포트로 간다. 멀티캐스트는 IGMP 스누핑이 없으면 모든 포트로, 있으면 가입 포트로만 가되 224.0.0.x 대역은 모든 포트로 간다.",
      "가운데 열이 분석기 자리입니다 — 남의 유니캐스트는 오지 않고, 그룹 주소는 대개 옵니다")

def kr(s): return KR if any("가" <= c <= "힣" for c in s) else MONO

LX = 40                                    # 목적지 칸 글자 x
SW_X, SW_W = 304, 160                      # 스위치 기둥
PORTS = [(540, "장비 B", "유니캐스트 목적지"), (660, "나", "분석기 자리"), (780, "그룹 가입자 C", "멀티캐스트 가입")]
PW, PH = 80, 36                            # 포트 칸 — 줄 위에서 28 아래
Y0, RS = 164, 72                           # 첫 줄 위 · 줄 stride
ROWS = [  # (이름, IPv4, MAC, 스위치 판단, 도착한 포트 인덱스)
    ("유니캐스트",              "192.168.0.20",                "B 의 MAC · IG 0",           "B 의 포트로만",        {0}),
    ("브로드캐스트",            "255.255.255.255",             "ff:ff:ff:ff:ff:ff · IG 1",  "모든 포트로",          {0, 1, 2}),
    ("멀티캐스트 · 스누핑 없음", "224.0.0.0 ~ 239.255.255.255", "01:00:5e:… · IG 1",         "가입자 모름 · 모든 포트", {0, 1, 2}),
    ("멀티캐스트 · 스누핑 켬",   "239.x.x.x 그룹",              "01:00:5e:… · IG 1",         "가입 포트로만",        {2}),
    ("멀티캐스트 · 스누핑 켬",   "224.0.0.251 (mDNS)",          "01:00:5e:00:00:fb · IG 1",  "224.0.0.x 는 모든 포트", {0, 1, 2}),
]
FOCAL = (4, 1)

# 열 머리
d.t(LX, 124, "목적지 주소", 13, INK, KR, "start", 600)
d.t(LX, 142, "IPv4 · MAC · IG 비트", 12, MUTED, KR, "start")
d.t(SW_X + SW_W / 2, 124, "스위치", 13, INK, KR, "middle", 600)
d.t(SW_X + SW_W / 2, 142, "복사할 포트 판단", 12, MUTED, KR, "middle")
for cx, name, sub in PORTS:
    d.t(cx, 124, name, 13, INK, KR, "middle", 600)
    d.t(cx, 142, sub, 12, MUTED, KR, "middle")
d.line(24, 152, 856, 152, RULE, 0.8)

# 스위치 기둥 — 모든 줄을 관통한다
top, bottom = Y0, Y0 + len(ROWS) * RS - 8
d.box(SW_X, top, SW_W, bottom - top, PAPER2, RULE, 1.0, 8)

for i, (name, ip, mac, rule, hit) in enumerate(ROWS):
    y = Y0 + i * RS
    if i:
        d.line(24, y - 4, SW_X - 16, y - 4, RULE, 0.6)
    mid = y + 36
    # 목적지 칸
    d.t(LX, y + 18, name, 13, INK, KR, "start", 600)
    d.t(LX, y + 38, ip, 12, MUTED, kr(ip), "start")
    d.t(LX, y + 56, mac, 12, MUTED, kr(mac), "start")
    # 연결선 먼저 — 들어오는 화살표, 버스, 떨어지는 화살표
    d.arrow([(264, mid), (SW_X - 4, mid)], MUTED, "ar", 1.2)
    bus_y = y + 8
    last = max(PORTS[j][0] for j in hit)
    d.path(f"M {SW_X + SW_W} {mid} H {SW_X + SW_W + 20} V {bus_y} H {last}", MUTED, 1.2)
    for j in hit:
        d.arrow([(PORTS[j][0], bus_y), (PORTS[j][0], y + 28 - 4)], MUTED, "ar", 1.2)
    d.t(SW_X + SW_W / 2, mid + 5, rule, 12, INK, KR, "middle")
    # 포트 칸
    for j, (cx, _, _) in enumerate(PORTS):
        x, cy = cx - PW / 2, y + 28
        if (i, j) == FOCAL:
            d.o.append(f'<rect x="{x}" y="{cy}" width="{PW}" height="{PH}" rx="6" '
                       f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
            d.t(cx, cy + 23, "도착", 13, ACC, KR, "middle", 600)
        elif j in hit:
            d.tone(x, cy, PW, PH, INFO, 6)
            d.t(cx, cy + 23, "도착", 13, INFO, KR, "middle", 600)
        else:
            d.o.append(f'<rect x="{x}" y="{cy}" width="{PW}" height="{PH}" rx="6" fill="{PAPER}" '
                       f'stroke="{SOFT}" stroke-width="1.0" stroke-dasharray="4,3"/>')
            d.t(cx, cy + 23, "안 옴", 13, SOFT, KR, "middle")

d.legend(Y0 + len(ROWS) * RS + 20, [("01-02 실습에서 잡힌 자리", ACC), ("포트에 도착", INFO), ("오지 않음", SOFT)])
d.save("01-01.address-reach.svg")
