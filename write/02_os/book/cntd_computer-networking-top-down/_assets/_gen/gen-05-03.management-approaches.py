# 타입 스펙: type-quadrant — 관리 방식 셋을 두 축에 놓으면 무엇이 비어 있는지가 보인다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.7.1 (CLI · SNMP/MIB · NETCONF/YANG 의 성격)
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, WARN, KR, MONO

W, H = 1000, 640
d = D(W, H, "SECTION 5.7 · THREE WAYS TO MANAGE",
      "조회는 오래 됐고 설정이 늦었습니다",
      "망을 관리하는 세 방식을 대상 범위와 주된 쓰임 두 축에 놓은 그림. 장비를 하나씩 다루는 방식이 오래 쓰였고, 망 전체를 한 번에 설정하는 방식이 가장 늦게 왔다.",
      "RFC 3535 이 지적한 빈자리가 NETCONF 를 낳았습니다")

X0, Y0, SZ = 240, 120, 380
d.box(X0, Y0, SZ, SZ, f"{INK}04", RULE, 1.0, 10)
d.line(X0 + SZ / 2, Y0, X0 + SZ / 2, Y0 + SZ, RULE, 1.0)
d.line(X0, Y0 + SZ / 2, X0 + SZ, Y0 + SZ / 2, RULE, 1.0)

d.t(X0 + SZ / 2, Y0 - 14, "주로 조회에 씁니다", 11, SOFT, KR)
d.t(X0 + SZ / 2, Y0 + SZ + 26, "주로 설정에 씁니다", 11, SOFT, KR)
d.t(X0 - 16, Y0 + SZ / 2 - 8, "장비를", 11, SOFT, KR, "end")
d.t(X0 - 16, Y0 + SZ / 2 + 10, "하나씩", 11, SOFT, KR, "end")
d.t(X0 + SZ + 16, Y0 + SZ / 2 - 8, "망 전체를", 11, SOFT, KR, "start")
d.t(X0 + SZ + 16, Y0 + SZ / 2 + 10, "한 번에", 11, SOFT, KR, "start")

ITEMS = [("SNMP / MIB", "1980년대 후반부터", X0 + 96, Y0 + 96, INFO,
          "MIB 객체를 읽고 씁니다"),
         ("CLI", "사람이 직접 또는 스크립트로", X0 + 96, Y0 + 292, WARN,
          "공급자마다 달라 자동화가 어렵습니다"),
         ("NETCONF / YANG", "RFC 6241 · RFC 6020", X0 + 288, Y0 + 292, ACC,
          "여러 장비에 원자적으로 적용합니다")]
for name, when, cx, cy, c, sub in ITEMS:
    d.tone(cx - 88, cy - 34, 176, 68, c, 8, "16", 1.5)
    d.t(cx, cy - 10, name, 12, c, KR, "middle", 600)
    d.t(cx, cy + 10, when, 11, MUTED, KR)
    d.t(cx, cy + 52, sub, 11, SOFT, KR)

d.t(X0 + 288, Y0 + 96, "여기는 비어 있습니다", 11, MUTED, KR)

d.t(30, 552, "RFC 3535 의 2002년 워크숍은 SNMP/MIB 가 장비 감시에는 값어치가 있지만 설정과 규모에서는 모자란다고 짚었습니다.", 11, MUTED, KR, "start")
d.t(30, 572, "\"운영자가 개별 장비가 아니라 망 전체의 설정에 집중하게 하라\"는 요구가 NETCONF 를 낳았습니다.", 11, ACC, KR, "start")

d.legend(596, [("설정 중심", ACC), ("조회 중심", INFO), ("사람 손", WARN)])

out = pathlib.Path(__file__).resolve().parent.parent / "05-03.management-approaches.svg"
d.save(out)
print("→", out)
