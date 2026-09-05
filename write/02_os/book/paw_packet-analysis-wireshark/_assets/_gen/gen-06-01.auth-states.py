# 06-01 §3 — STA 가 AP 에 붙기까지 지나는 상태. 원문의 인증 절차 서술을 상태 전이로 세운다.
# 타입 스펙: type-state — 주체 하나(STA)의 상태 전이. 전이 라벨은 오가는 프레임 이름이고,
#           focal 은 데이터를 주고받을 수 있게 되는 상태 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 456
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 06-01 §3",
      "STA 가 AP 에 붙기까지",
      "원문이 서술하는 인증·결합 절차를 상태로 세운 것. 프레임 이름이 곧 전이 조건이고, 결합이 끝나야 데이터 프레임이 오간다. WPA 환경에서는 그 뒤 EAPOL 네 메시지가 더 붙는다.",
      "deauthentication 프레임 하나면 어느 상태에서든 처음으로 돌아갑니다")

X = [40, 280, 520, 760]
SW, SH, Y = 200, 56, 168

def state(i, name, sub, c=None, focal=False):
    x = X[i]
    if focal:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{SW}" height="{SH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif c: d.tone(x, Y, SW, SH, c, 8)
    else: d.box(x, Y, SW, SH, PAPER2, RULE, 1.0, 8)
    col = ACC if focal else (c if c else INK)
    d.t(x + SW / 2, Y + 24, name, 12, col, KR, "middle", 600)
    d.t(x + SW / 2, Y + 42, sub, 11, MUTED, MONO)

for i in range(3):
    d.arrow([(X[i] + SW, Y + SH / 2), (X[i + 1] - 4, Y + SH / 2)], MUTED, "ar", 1.4)
labels = [("probe request / response", "0x04 · 0x05"),
          ("authentication", "0x0b"),
          ("association request / response", "0x00 · 0x01")]
for i, (lab, sub) in enumerate(labels):
    mx = (X[i] + SW + X[i + 1]) / 2
    d.t(mx, Y - 16, lab, 11, MUTED, MONO)
    d.t(mx, Y + SH + 24, sub, 10, SOFT, MONO)

state(0, "채널을 훑는 중", "미인증 · 미결합")
state(1, "AP 를 찾음", "beacon 0x08 로 확인")
state(2, "인증됨", "미결합")
state(3, "결합됨", "데이터 프레임 가능", focal=True)

# deauthentication 은 어느 상태에서든 처음으로 — 스펙의 "from any state" 관례대로 주석 하나
d.path(f"M {X[3] + SW / 2} {Y + SH} V 300 H {X[0] + SW / 2} V {Y + SH + 4}", WARN, 1.4, m="warn")
d.t((X[0] + X[3]) / 2 + SW / 2, 292, "deauthentication 0x0c · 어느 상태에서든 처음으로", 11, WARN, KR)

d.t(40, 340, "WPA 라면 결합 뒤에 EAPOL 네 메시지가 이어집니다 — 필터는 eapol 이고, 802.11 복호화에 이 네 개가 필요합니다",
     11, MUTED, KR, "start")

d.legend(H - 60, [("데이터가 오갈 수 있는 상태", ACC), ("처음으로 되돌리는 프레임", WARN)])
d.save("06-01.auth-states.svg")
