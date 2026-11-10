# 09-01 §5 「pam_limits — 로그인할 때 거는 자원 한도」 — limits 파일을 읽는 순서와 이기는 줄.
# 1차 자료 pam_limits(8): limits.conf 다음 limits.d/*.conf 를 "C" 로케일 순서로 읽고, 효과는 그 순서로 이어 붙인 것과 같다.
#       limits.conf(5): "In general, individual limits have priority over group limits" ·
#       "group and wildcard limits are not applied to the root user" · "all limit settings are set per login".
# 실측(debian:12, libpam-modules 1.5.2): 10-a.conf "alice soft nofile 2048" + 20-b.conf "* soft nofile 4096"
#       → su alice -c 'ulimit -Sn' = 2048. 파일을 바꾸기 전에 띄운 alice 의 sleep 은 /proc/PID/limits 1024 그대로.
# 주의: Debian 12 기본 limits.conf 는 전부 주석이고 limits.d 는 비어 있다. 01 띠는 그 상태를 적었다.
# 타입 스펙: type-layers — 읽는 순서로 쌓인 띠 다섯(CSS cascade 와 같은 겹침), 왼쪽 인덱스, 오른쪽 sublabel, focal 띠 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 508
d = D(W, H, "LEARNING MODERN LINUX · 09-01 §5",
      "같은 nofile 을 두 파일이 말하면 사용자 줄이 이긴다",
      "limits.conf 와 limits.d 를 이름순으로 이어 붙인 뒤 이기는 줄을 고르는 실측. 이 결정은 로그인할 때 "
      "한 번 일어나고, 이미 돌던 프로세스에는 닿지 않는다.",
      "나중에 읽힌 * 줄도 alice 를 지목한 줄을 못 이깁니다")

BX, BW, BH, Y0 = 112, 744, 64, 108
bands = [
    ("01", "/etc/security/limits.conf", "Debian 12 기본, 전부 주석", False),
    ("02", "limits.d/10-a.conf   alice  soft  nofile  2048", "사용자 줄", False),
    ("03", "limits.d/20-b.conf   *  soft  nofile  4096", "와일드카드 줄, 나중에 읽힘", False),
    ("04", "→ alice  soft  nofile  2048", "사용자 줄 > @그룹·*, 같은 순위면 나중 줄", True),
    ("05", "su alice -c 'ulimit -Sn'   2048", "로그인 때만, 돌던 프로세스는 1024 그대로", False),
]
for i, (idx, name, sub, focal) in enumerate(bands):
    y = Y0 + i * BH
    if focal:
        d.tone(BX, y, BW, BH, ACC, 0, "14", 1.4)
    else:
        d.box(BX, y, BW, BH, PAPER if i % 2 else PAPER2, RULE, 1.0, 0)
    d.t(BX + 16, y + BH / 2 + 4, idx, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(BX + 56, y + BH / 2 + 5, name, 13, ACC if focal else INK, MONO, "start", 600)
    d.t(BX + BW - 16, y + BH / 2 + 5, sub, 12, ACC if focal else MUTED, KR, "end")
d.o.append(f'<rect x="{BX}" y="{Y0}" width="{BW}" height="{BH * 5}" fill="none" stroke="{MUTED}" stroke-width="1"/>')

# 왼쪽 방향 표시
d.t(64, Y0 - 8, "읽는 순서", 12, MUTED, KR)
d.arrow([(64, Y0 + 8), (64, Y0 + BH * 3 - 8)], MUTED, "ar", 1.3)
d.t(64, Y0 + BH * 3 + 30, "고르기", 12, MUTED, KR)
d.t(64, Y0 + BH * 4 + 38, "적용", 12, MUTED, KR)

d.t(BX, Y0 + BH * 5 + 24, "root 예외:  * - nofile 5000 → root 1024 그대로   ·   root - nofile 6000 → root 6000",
    12, SOFT, KR, "start")
d.legend(464, [("pam_limits 가 고른 줄", ACC)])
d.save("09-01.pam-limits.svg")
print("ok 09-01.pam-limits")
