# 타입 스펙: type-dp-security-matrix — 격자 문법을 비교 행렬로 쓴다. 행은 비교 축 넷, 열은 관리 방식 셋.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.7.1 · 노트 05-03 §6
# 칸마다 본문 문장이 근거다 — 주로 하는 일(§6 CLI·SNMP 항목의 "조회하고 CLI 로 설정"),
# 다루는 단위("앞의 둘은 장비를 하나씩"), 전송(콘솔·SSH / 대개 UDP·재전송 미규정 / SSH 필수·830),
# 설정·규모(CLI 자동화 어려움 / RFC 3535 의 SNMP 평가 / 여러 장비에 걸친 원자적 연산).
# 좌표는 같은 폴더 gen-02-01.tcp-udp-services.py 의 행 높이 40 · stride 48 을 그대로 쓴다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER2, INK, MUTED, RULE, ACC, OK, WARN, INFO, KR, MONO

W, H = 1000, 428
d = D(W, H, "SECTION 5.7 · THREE WAYS TO MANAGE",
      "장비를 하나씩 다루던 둘, 망 전체를 설정하는 하나",
      "CLI · SNMP/MIB · NETCONF/YANG 을 주로 하는 일, 다루는 단위, 전송, 설정·규모 네 축으로 견준 행렬. 앞의 둘은 장비를 하나씩 다루고, NETCONF 는 여러 장비에 걸친 원자적 연산으로 망 전체의 설정을 다룬다.",
      "RFC 3535 가 짚은 설정·규모의 빈자리를 NETCONF 가 메웁니다")

C0, C0W = 24, 196                      # 비교 축
CW, CG = 240, 12                       # 방식 열 폭 · 간격
CX = [232 + i * (CW + CG) for i in range(3)]   # 232, 484, 736
HY, HH = 108, 52                       # 머리 행
RY0, RH, RS = 168, 40, 48              # 데이터 행 시작 · 높이 · stride


def fam(txt):
    return KR if any("가" <= ch <= "힣" for ch in txt) else MONO


HEAD = [("CLI", "공급자·장비마다 다른 명령"),
        ("SNMP / MIB", "MIB 는 SMI 로 명세"),
        ("NETCONF / YANG", "YANG 이 데이터 모델")]

d.box(C0, HY, C0W, HH, PAPER2, RULE, 0.9)
d.t(C0 + C0W / 2, HY + 32, "비교 축", 13, MUTED, KR)
for x, (name, sub) in zip(CX, HEAD):
    d.box(x, HY, CW, HH, PAPER2, RULE, 0.9)
    d.t(x + CW / 2, HY + 22, name, 14, INK, MONO, "middle", 600)
    d.t(x + CW / 2, HY + 42, sub, 13, MUTED, KR)

# (축, [(값, 색), ...]) — 색은 스타일 계약 상태색: INFO 중립 사실 · WARN 한계 · OK 갖춘 것
ROWS = [("주로 하는 일", [("설정", INFO), ("조회", INFO), ("설정 관리", INFO)]),
        ("다루는 단위", [("장비 하나씩", WARN), ("장비 하나씩", WARN), ("망 전체", OK)]),
        ("전송", [("콘솔 또는 SSH", INFO), ("대개 UDP · 재전송 규정 없음", WARN), ("SSH 필수 · 포트 830", OK)]),
        ("설정·규모", [("자동화·규모 확장 어려움", WARN), ("설정·규모에서 모자람", WARN), ("여러 장비에 걸친 원자적 연산", ACC)])]

for i, (axis, cells) in enumerate(ROWS):
    y = RY0 + i * RS
    d.box(C0, y, C0W, RH, PAPER2, RULE, 0.9)
    d.t(C0 + 16, y + 25, axis, 13, INK, KR, "start")
    for x, (val, c) in zip(CX, cells):
        focal = c == ACC
        d.tone(x, y, CW, RH, c, 6, "12" if focal else "14", 1.4 if focal else 1.1)
        d.t(x + CW / 2, y + 25, val, 13, c, fam(val), "middle", 600 if focal else 400)

d.legend(H - 44, [("중립 사실", INFO), ("장비 하나씩의 한계", WARN), ("망 전체를 다루려고 갖춘 것", OK), ("이 절의 논점", ACC)])

out = pathlib.Path(__file__).resolve().parent.parent / "05-03.management-approaches.svg"
d.save(out)
print("→", out)
