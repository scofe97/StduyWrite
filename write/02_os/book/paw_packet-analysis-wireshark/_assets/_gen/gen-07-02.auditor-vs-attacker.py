# 07-02 §2 — 원문은 스캐닝 절에서 보안 감사자와 공격자를 나란히 적는다. 둘이 쓰는 도구가 같다.
# 타입 스펙: type-venn — 두 집합의 겹침. 겹치는 자리가 이 절의 요점이므로 그 하나만 강조한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, PAPER2, RULE, KR, MONO

W, H = 960, 560
CY, R = 296, 160
AX, BX = 400, 560

d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 07-02 §2",
      "감사자와 공격자가 겹치는 자리",
      "원문 스캐닝 절은 같은 문단에서 보안 감사자와 공격자를 나란히 적는다. 둘의 목적은 반대지만 쓰는 명령과 패킷이 같으므로, 캡처만 보고 어느 쪽인지 가릴 수 없다.",
      "겹치는 부분이 이 절의 요점입니다 — 캡처는 의도를 담지 않습니다")

d.o.append(f'<circle cx="{AX}" cy="{CY}" r="{R}" fill="{OK}0D" stroke="{OK}" stroke-width="1"/>')
d.o.append(f'<circle cx="{BX}" cy="{CY}" r="{R}" fill="{BAD}0D" stroke="{BAD}" stroke-width="1"/>')

d.t(320, 112, "보안 감사자", 14, OK, KR, "middle", 600)
d.t(320, 130, "SECURITY AUDITOR", 9, SOFT, MONO)
d.t(648, 112, "공격자", 14, BAD, KR, "middle", 600)
d.t(648, 130, "ATTACKER", 9, SOFT, MONO)

for i, line in enumerate(["허가를 받고", "약한 스위트를 찾아", "제거하려는 목적"]):
    d.t(320, 268 + i * 26, line, 11, MUTED, KR)
for i, line in enumerate(["허가 없이", "열린 DB 포트를 찾아", "이용하려는 목적"]):
    d.t(648, 268 + i * 26, line, 11, MUTED, KR)

d.t(480, 216, "같은 것", 12, ACC, KR, "middle", 600)
# 교집합 렌즈의 최대 폭은 160px 이다. 한 줄로 두면 165px 라 양쪽 원 둘레를 3~4px 씩
# 넘어 걸친다(2026-09-18 실측). 스크립트 이름을 두 줄로 나눠 렌즈 안에 넣는다.
for i, line in enumerate(["nmap -T4 -A -v", "--script ssl-cert,", "ssl-enum-ciphers",
                          "포트마다 SYN 하나", "Win 값이 뒤섞인 탐침"]):
    d.t(480, 244 + i * 24, line, 11, ACC, KR if any("가" <= c <= "힣" for c in line) else MONO)

d.t(24, 486, "판정 근거는 캡처가 아니라 사전 통보와 작업 창 · 같은 스캔이 감사도 공격도 될 수 있음",
     11, MUTED, KR, "start")

d.legend(H - 60, [("두 쪽이 함께 쓰는 것", ACC), ("감사자 쪽", OK), ("공격자 쪽", BAD)])
d.save("07-02.auditor-vs-attacker.svg")
