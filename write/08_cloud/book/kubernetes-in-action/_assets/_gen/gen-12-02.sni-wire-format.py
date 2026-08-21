# 12-02 §2 — 껍질 셋이 벗겨지며 바이트로 펴진다
# 중첩과 선형 배치를 한 장에 나란히 둔다. 길이가 앞에 붙는다는 사실이 "암호를 풀지 않아도
# 셀 수 있다"의 근거라, 바이트 줄에서 길이 칸을 따로 표시한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 620, "KUBERNETES IN ACTION · 12-02",
      "길이가 앞에 붙어 있어 세면 된다",
      "server_name 한 줄이 껍질 셋에 싸여 실린다. 껍질마다 길이를 앞에 다는 형식이라, "
      "암호를 풀지 않아도 어디부터 어디까지가 호스트명인지 셀 수 있다.",
      "Extension → ServerNameList → ServerName → host_name")

ddx.band(d, 100, 396, "중첩 — 바깥부터 안으로", x=24, w=560)
# 부제를 제목 아래에 두면 한 겹 안쪽 상자가 그 줄을 덮는다 — 같은 줄 오른쪽 끝에 붙인다
SHELL = [("Extension", "type=0x0000", 56, 148, 496, 216),
         ("ServerNameList", "이름을 여럿 담게", 88, 180, 432, 152),
         ("ServerName", "type=0", 120, 212, 368, 88)]
for t, sub, x, y, w, h in SHELL:
    d.box(x, y, w, h, PAPER, RULE, 1.0, 6)
    d.t(x + 16, y + 22, t, 12, SOFT, MONO, "start", 600)
    d.t(x + w - 16, y + 22, sub, 10, SOFT, MONO, "end")
d.o.append(f'<rect x="152" y="244" width="304" height="44" rx="5" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(304, 272, "api.example.com", 13, ACC, MONO)
d.t(304, 384, "실제로는 host_name 하나만 쓰인다", 11, MUTED, KR)

ddx.band(d, 100, 396, "바이트로 펴면", x=604, w=572)
CELL = [("00 00", "확장 타입", 78, SOFT), ("00 14", "길이", 60, INFO),
        ("00 12", "리스트 길이", 78, INFO), ("00", "이름 타입", 48, SOFT),
        ("00 0F", "이름 길이", 66, INFO), ("api.example.com", "값", 148, ACC)]
x = 632
for v, lab, w, c in CELL:
    d.box(x, 216, w, 56, PAPER2, c, 1.1, 5)
    d.t(x + w / 2, 240, v, 10, c, MONO)
    d.t(x + w / 2, 258, lab, 9, MUTED, KR)
    x += w + 8
d.t(890, 306, "파란 칸이 길이다 — 이 셋만 읽으면", 11, INFO, KR)
d.t(890, 328, "호스트명이 어디서 끝나는지 안다", 11, INFO, KR)
d.t(890, 366, "프록시가 하는 일이 정확히 이것이다", 11, SOFT, KR)

d.t(24, 440, "중첩이 셋인 이유는 이름을 여럿 담을 수 있게 설계했기 때문이다. ServerNameList 라는 이름이 그 흔적인데, "
             "쓰지 않는 유연성 때문에 껍질이 한 겹 더 있는 셈이다.", 11, MUTED, KR, "start")
d.t(24, 462, "명세가 IP 주소를 금하고 DNS 호스트명만 허용하므로, IP 로 직접 접속하면 SNI 자리가 아예 빈다.",
     11, MUTED, KR, "start")
d.legend(498, [("길이 칸", INFO), ("호스트명", ACC)])
d.save("12-02-sni-wire-format.svg")
print("ok")
