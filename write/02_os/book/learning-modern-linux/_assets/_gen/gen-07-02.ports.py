# 07-02 §1 — 포트 65,536개가 세 구간으로 갈린다.
# 원문("Ports"): "A port is a unique 16-bit number identifying a service available at an IP address."
#   Well-known ports (from 0 to 1023): "These are for daemons such as an SSH server or a web server.
#       Using (binding to) one of them requires elevated privileges (root or CAP_NET_BIND_SERVICE
#       capability)."
#   Registered ports (from 1024 to 49151): "These are managed by Internet Assigned Numbers Authority
#       (IANA) through a publicly documented process."
#   Ephemeral ports (from 49152 to 65535): "These cannot be registered. They can be used for automatically
#       allocating a temporary port ... as well as for private (say, company-internal) services."
#   "You can see the ports and mapping in /etc/services."
# 타입 스펙: type-treemap — 전체를 넓이 비율로 쪼개 보이는 형태. 세 구간의 폭이 실제 개수 비율이라
#           잘 알려진 포트가 전체의 1.6% 뿐이라는 사실이 눈에 보인다. accent 는 특권이 필요한 구간.
#           축약: /etc/services 의 개별 항목은 논점이 아니라 예 셋만 칩으로 놓았다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 552
d = D(W, H, "LEARNING MODERN LINUX · 07-02 §1",
      "특권이 필요한 구간은 전체의 1.6% 뿐이다",
      "포트가 16비트라 65,536개다. 그 공간을 저자가 가른 세 구간의 폭을 실제 개수 비율로 그렸다. "
      "낮은 쪽이 좁은데도 이름이 알려진 것은 그 안에 데몬들이 몰려 있기 때문이다.",
      "1024 미만에 바인딩하려면 상승된 특권이 필요합니다")

X0, TOTW, BY, BH = 32, 816, 200, 132
TOTAL = 65536
bands = [
    ("잘 알려진 포트", "0 – 1023", 1024, "root 이거나 CAP_NET_BIND_SERVICE", ACC),
    ("등록된 포트", "1024 – 49151", 48128, "IANA 가 공개 절차로 관리", OK),
    ("임시 포트", "49152 – 65535", 16384, "등록할 수 없다 · 자동 할당과 사설", INFO),
]
x = X0
for name, rng, n, note, col in bands:
    w = TOTW * n / TOTAL
    focal = (col is ACC)
    if focal:
        d.o.append(f'<rect x="{x}" y="{BY}" width="{w}" height="{BH}" rx="6" '
                   f'fill="{ACC}20" stroke="{ACC}" stroke-width="1.6"/>')
    else:
        d.box(x, BY, w, BH, PAPER2, col, 1.2, 6)
    if w > 200:
        d.t(x + w / 2, BY + 34, name, 14, col, KR, "middle", 600)
        d.t(x + w / 2, BY + 58, rng, 12, INK, MONO)
        d.t(x + w / 2, BY + 82, f"{n:,} 개", 11.5, MUTED, MONO)
        d.t(x + w / 2, BY + 108, note, 11, MUTED, KR)
    x += w

# 좁은 첫 구간은 밖에서 라벨
d.path(f"M {X0 + TOTW * 1024 / TOTAL / 2} {BY - 6} L {X0 + TOTW * 1024 / TOTAL / 2} {BY - 44}",
       ACC, 1.4, m="acc")
d.t(X0 + 8, BY - 74, "잘 알려진 포트 — 0 ~ 1023 · 1,024 개", 13, ACC, KR, "start", 600)
d.t(X0 + 8, BY - 54, "SSH 서버나 웹 서버 같은 데몬을 위한 자리", 11.5, MUTED, KR, "start")

d.t(X0, BY + BH + 26, "전체 65,536 개", 12, SOFT, MONO, "start")
d.t(X0 + TOTW, BY + BH + 26, "16비트", 12, SOFT, MONO, "end")

CY = 386
d.o.append(f'<rect x="{X0}" y="{CY}" width="400" height="76" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(X0 + 20, CY + 28, "4장 capability 연계 — 바인딩 권한 분리", 13, ACC, KR, "start", 600)
d.t(X0 + 20, CY + 50, "root 전체 권한 대신 CAP_NET_BIND_SERVICE 부여", 11.5, ACC, KR, "start")
d.t(X0 + 20, CY + 68, "1024 미만 잘 알려진 포트 바인딩 최소 권한 원칙", 11.5, MUTED, KR, "start")

d.tone(X0 + 416, CY, 400, 76, INFO)
d.t(X0 + 436, CY + 28, "리눅스가 고르는 임시 포트", 13, INK, KR, "start", 600)
d.t(X0 + 436, CY + 50, "connect 때 커널이 ip_local_port_range 에서 고름", 11.5, MUTED, KR, "start")
d.t(X0 + 436, CY + 68, "기본 32768 – 60999 · IANA 구간과 다름", 11.5, MUTED, KR, "start")

d.legend(492, [("특권이 필요한 구간", ACC), ("IANA 가 관리하는 구간", OK),
               ("자동으로 할당되는 구간", INFO)])
d.save("07-02.ports.svg")
print("ok 07-02.ports")
