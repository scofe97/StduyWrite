# 01-01 §1 — 원문은 "인터넷이란 무엇인가"에 서술을 둘 준다. 둘이 만나는 자리가 소켓 인터페이스다.
# 타입 스펙: type-venn — 두 집합의 겹침. 겹치는 자리가 이 절의 요점이므로 그 하나만 강조한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER2, RULE, KR, MONO

W, H = 960, 572
CY, R = 300, 160
AX, BX = 400, 560

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 01-01 §1",
      "인터넷을 두 번 소개하는 이유",
      "원문 1.1 은 같은 대상을 부품 목록으로 한 번, 서비스 규약으로 한 번 서술한다. 어느 쪽도 혼자서는 부족하고, 두 서술은 애플리케이션이 인프라에 배달을 요청하는 규칙에서 만난다.",
      "아래쪽은 부품이 맡고 위쪽은 애플리케이션이 맡습니다 — 경계에 규칙이 하나 있습니다")

d.o.append(f'<circle cx="{AX}" cy="{CY}" r="{R}" fill="{INFO}0D" stroke="{INFO}" stroke-width="1"/>')
d.o.append(f'<circle cx="{BX}" cy="{CY}" r="{R}" fill="{OK}0D" stroke="{OK}" stroke-width="1"/>')

d.t(316, 116, "부품 서술", 14, INFO, KR, "middle", 600)
d.t(316, 134, "NUTS AND BOLTS", 9, SOFT, MONO)
d.t(648, 116, "서비스 서술", 14, OK, KR, "middle", 600)
d.t(648, 134, "SERVICES", 9, SOFT, MONO)

for i, line in enumerate(["호스트 190억 대", "링크와 패킷 스위치", "ISP 가 묶습니다", "IP · RFC · IEEE 802"]):
    d.t(316, 258 + i * 26, line, 11, MUTED, KR)
for i, line in enumerate(["분산 애플리케이션", "종단에서만 돕니다", "서비스를 골라 씁니다", "코어는 관심이 없습니다"]):
    d.t(648, 258 + i * 26, line, 11, MUTED, KR)

d.t(480, 224, "소켓 인터페이스", 12, ACC, KR, "middle", 600)
for i, line in enumerate(["배달을 요청하는", "규칙의 집합", "(우표와 봉투와", "주소 쓰는 법)"]):
    d.t(480, 258 + i * 26, line, 11, ACC, KR)

d.t(24, 486, "원문의 우편 비유 — 앨리스는 편지를 창밖으로 던지지 않고 봉투에 넣고 주소를 쓰고 우표를 붙여 우체통에 넣습니다",
     11, MUTED, KR, "start")

d.legend(H - 60, [("두 서술이 만나는 자리", ACC), ("부품 쪽", INFO), ("서비스 쪽", OK)])
d.save("01-01.two-descriptions.svg")
