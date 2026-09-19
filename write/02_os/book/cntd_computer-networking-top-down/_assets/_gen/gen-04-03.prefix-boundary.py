# 타입 스펙: type-comparison — 같은 주소 공간을 두 프리픽스로 갈랐을 때 경계가 어디로 옮겨 가는가.
# 출처: RFC 1812 §4.2.2.11 (호스트 자리 전부 0/1 금지) + 이 기계 en0 실측 (회사망 172.16.1.240/23, 2026-09-18)
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, BAD, OK, KR, MONO

W, H = 940, 560
d = D(W, H, "RFC 1812 · PREFIX BOUNDARY",
      "프리픽스가 바뀌면 예약된 두 자리도 옮겨 갑니다",
      "같은 주소 172.16.0.255 와 172.16.1.0 을 /24 와 /23 두 기준으로 나란히 판정한 그림. "
      "/24 에서는 브로드캐스트와 네트워크 주소라 못 쓰는 자리인데, /23 에서는 호스트 비트가 전부 0 도 전부 1 도 아니라 "
      "평범한 호스트 주소가 된다. 예약 여부를 옥텟 값으로 외우면 프리픽스가 달라질 때 틀린다.",
      "예약 기준은 옥텟 값이 아니라 호스트 비트가 전부 0 이냐 전부 1 이냐입니다")

# ── 두 기준 패널 ──────────────────────────────────────────────
PW, PH = 420, 250
PX = [40, 490]
PY = 104

def panel(x, title, mask, hostbits, rows, note):
    d.box(x, PY, PW, PH, PAPER2, RULE, 1.0, 8)
    d.t(x + 18, PY + 28, title, 14, INK, MONO, "start", 600)
    d.t(x + PW - 18, PY + 28, mask, 11, MUTED, MONO, "end")
    d.t(x + 18, PY + 48, hostbits, 11, MUTED, KR, "start")
    d.line(x + 16, PY + 60, x + PW - 16, PY + 60, RULE, 0.8)
    iy = PY + 72
    for addr, bits, label, mark in rows:
        c = {"bad": BAD, "ok": OK, "": MUTED}[mark]
        d.box(x + 18, iy, PW - 36, 34, PAPER, f"{c}55", 1.3 if mark else 0.9, 5)
        d.t(x + 30, iy + 15, addr, 12, c if mark else INK, MONO, "start", 600)
        d.t(x + 30, iy + 29, bits, 9.5, SOFT, MONO, "start")
        d.t(x + PW - 30, iy + 22, label, 10.5, c, KR, "end")
        iy += 40
    d.t(x + 18, PY + PH - 14, note, 10.5, MUTED, KR, "start")

# 호스트 비트 표기: 세 번째 옥텟 마지막 1비트 | 네 번째 옥텟 8비트
panel(PX[0], "172.16.0.0/24", "255.255.255.0", "호스트 자리 8비트 — 네 번째 옥텟만", [
    ("172.16.0.0",   "호스트 = 00000000",   "네트워크 주소",   "bad"),
    ("172.16.0.1",   "호스트 = 00000001",   "첫 호스트",       ""),
    ("172.16.0.255", "호스트 = 11111111",   "브로드캐스트",    "bad"),
    ("172.16.1.0",   "다른 서브넷",          "경계 밖",         ""),
], "호스트 254개 · 2^8 − 2")

panel(PX[1], "172.16.0.0/23", "255.255.254.0", "호스트 자리 9비트 — 세 번째 옥텟 1비트 + 네 번째 8비트", [
    ("172.16.0.0",   "호스트 = 0 00000000", "네트워크 주소",   "bad"),
    ("172.16.0.255", "호스트 = 0 11111111", "평범한 호스트",   "ok"),
    ("172.16.1.0",   "호스트 = 1 00000000", "평범한 호스트",   "ok"),
    ("172.16.1.255", "호스트 = 1 11111111", "브로드캐스트",    "bad"),
], "호스트 510개 · 2^9 − 2")

# ── 같은 주소가 판정이 뒤집히는 자리 ──────────────────────────
d.tone(40, PY + PH + 26, 870, 84, ACC, 8, "10", 1.2)
d.t(58, PY + PH + 50, "같은 주소, 뒤집힌 판정", 12, ACC, KR, "start", 600)
d.t(58, PY + PH + 72, "172.16.0.255 — /24 에서는 브로드캐스트라 못 쓰고, /23 에서는 호스트 비트에 0 이 섞여 있어 쓸 수 있습니다.",
    11, INK, KR, "start")
d.t(58, PY + PH + 92, "172.16.1.0 — /24 에서는 아예 다른 서브넷이고, /23 에서는 같은 서브넷 안의 호스트입니다.",
    11, INK, KR, "start")

# ── 실측 근거 ────────────────────────────────────────────────
d.t(40, 480, "확인 — ifconfig 의 broadcast 필드가 계산 결과를 직접 알려 줍니다",
    11, MUTED, KR, "start")
d.box(40, 490, 870, 30, PAPER2, RULE, 0.9, 5)
d.t(56, 509, "$ ifconfig en0 | grep 'inet '     →     inet 172.16.1.240  netmask 0xfffffe00  broadcast 172.16.1.255",
    11, INK, MONO, "start")

d.legend(532, [("RFC 1812 가 금지하는 자리", BAD), ("붙일 수 있는 호스트 주소", OK), ("판정이 뒤집히는 주소", ACC)])
d.t(900, 554, "EN0 MEASURED 2026-09-18", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "04-03.prefix-boundary.svg"
d.save(out)
print("→", out)
