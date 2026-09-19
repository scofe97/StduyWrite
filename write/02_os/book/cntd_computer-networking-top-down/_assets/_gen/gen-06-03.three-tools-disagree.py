# 타입 스펙: type-comparison — 같은 대상을 세 도구로 재면 판정이 갈린다. 확정된 것과 확정되지 않은 것을 구분해 보인다.
# 출처: 이 기계 en0 실측 (회사 무선망 172.16.1.240/23, 2026-09-18) — route get · arp -n · traceroute 교차
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, BAD, OK, INFO, WARN, KR, MONO

W, H = 940, 600
d = D(W, H, "MEASURED · NOT CONCLUSIVE",
      "세 도구가 서로 다른 답을 냅니다",
      "같은 주소를 route get · arp · traceroute 로 재면 판정이 갈리는 것을 보인 그림. "
      "route get 은 같은 서브넷이라 하고 traceroute 는 두 홉이라 한다. TTL 뺄셈으로 홉을 세면 틀리는 이유도 함께 적었다. "
      "무엇이 관측됐고 무엇이 확정되지 않았는지를 가르는 것이 이 그림의 목적이다.",
      "관측은 사실이고 구조의 이름은 아직 확정되지 않았습니다")

# ── 세 관측 ──────────────────────────────────────────────────
CW, CH = 288, 110
CY = 104
for i, (tool, cmd, val, read, c) in enumerate([
    ("L3 판정", "route -n get", "gateway 줄 없음", "같은 서브넷이라고 판단", INFO),
    ("L2 주소", "arp -a -n -i en0", "IP 20개가 한 MAC", "게이트웨이와 같은 MAC", WARN),
    ("홉 수",   "traceroute -n",    "2 홉",            "라우터를 지나갑니다",   ACC),
]):
    x = 12 + i * (CW + 14)
    d.box(x, CY, CW, CH, PAPER2, f"{c}44", 1.1, 7)
    d.t(x + 16, CY + 24, tool, 11, c, KR, "start", 600)
    d.t(x + CW - 16, CY + 24, cmd, 10, MUTED, MONO, "end")
    d.line(x + 14, CY + 36, x + CW - 14, CY + 36, RULE, 0.8)
    d.t(x + CW / 2, CY + 66, val, 14, INK, MONO, "middle", 600)
    d.t(x + CW / 2, CY + 92, read, 10.5, MUTED, KR)

# ── 어긋남 ───────────────────────────────────────────────────
GY = CY + CH + 28
d.tone(12, GY, W - 60, 74, BAD, 8, "10", 1.2)
d.t(30, GY + 26, "판정이 갈립니다", 12, BAD, KR, "start", 600)
d.t(30, GY + 50, "route get 은 직접 전달이라 하고, traceroute 는 두 홉을 셉니다. IP 20개가 한 MAC 을 쓰는 것도 "
                 "「라우터는 인터페이스마다 주소를 갖는다」로는 설명되지 않습니다.", 11, INK, KR, "start")

# ── 확정 / 미확정 ────────────────────────────────────────────
SY = GY + 100
BW2 = (W - 60 - 14) / 2
d.box(12, SY, BW2, 132, PAPER2, f"{OK}44", 1.1, 7)
d.t(30, SY + 26, "확정된 것 — 관측 사실", 11, OK, KR, "start", 600)
for j, txt in enumerate(["gateway 줄이 없다", "MAC 을 IP 20개가 공유한다", "traceroute 가 2 홉을 센다"]):
    d.t(30, SY + 52 + j * 24, "· " + txt, 11, INK, KR, "start")

d.box(12 + BW2 + 14, SY, BW2, 132, PAPER2, f"{MUTED}44", 1.1, 7)
d.t(30 + BW2 + 14, SY + 26, "확정되지 않은 것 — 구조의 이름", 11, MUTED, KR, "start", 600)
for j, txt in enumerate(["프록시 ARP 인가", "무선 컨트롤러의 L2 중계인가", "다른 무엇인가 — 장비 설정을 봐야 갈립니다"]):
    d.t(30 + BW2 + 14, SY + 52 + j * 24, "· " + txt, 11, SOFT, KR, "start")

# ── TTL 경고 ─────────────────────────────────────────────────
TY = SY + 156
d.tone(12, TY, W - 60, 76, WARN, 8, "10", 1.2)
d.t(30, TY + 24, "TTL 뺄셈으로 홉을 세지 않습니다", 11, WARN, KR, "start", 600)
d.t(30, TY + 46, "172.16.0.255 도 게이트웨이 172.16.0.1 도 똑같이 ttl=63 인데 traceroute 는 전자를 2 홉이라 답합니다. "
                 "0 홉이어야 할 게이트웨이가 63 이라는 것부터", 10.5, INK, KR, "start")
d.t(30, TY + 64, "초기값이 64 가 아니라는 뜻입니다. 초기값은 응답하는 쪽 OS 가 정합니다 — 8.8.8.8 은 ttl=112, "
                 "1.1.1.1 은 ttl=49 로 서로 다릅니다.", 10.5, INK, KR, "start")

d.t(W - 40, H - 10, "EN0 MEASURED 2026-09-18", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "06-03.three-tools-disagree.svg"
d.save(out)
print("→", out)
