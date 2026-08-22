# 01-04.twelve-packets — 비율 막대 (개수가 폭으로 보여야 한다)
# 본문: "12개가 나와야 하고, 그 구성은 수립 3개, 서버 ACK 1개, 데이터 2개, 데이터 ACK 2개, 종료 4개"
#        "색이 붙은 한 칸만 데이터입니다. 나머지 네 칸 열 개는 그 두 개를 안전하게 나르기 위해 드는 값입니다."
# 타입 스펙: type-bar.md 관례 — 부분이 전체에서 차지하는 몫이 요점이면 폭을 개수에 비례시킨다.
#           '2 개뿐'이 눈으로 보여야 하므로 칸 폭을 눈대중으로 고르지 않는다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 552
d = D(W, H, "ONE REQUEST · 12 PACKETS",
      "요청 하나가 12패킷 — 그중 실제 데이터는 2개뿐이다",
      "lo0 캡처에서 세는 12개를 시간 순서로 묶은 것. 가운데 한 칸만 데이터이고 나머지 열 개가 신뢰성에 드는 값이다.",
      lead="가운데 한 칸만 데이터이고 나머지 열 개가 신뢰성에 드는 값이다")

SEGS = [("수립", 3, "SYN·SYN-ACK·ACK", "[S] [S.] [.]"),
        ("서버 ACK", 1, "수립 직후", "[.]"),
        ("데이터", 2, "요청 · 응답", "[P.]"),
        ("데이터 ACK", 2, "각각 잘 받았다", "[.]"),
        ("종료", 4, "양쪽이 FIN·ACK", "[F.] [.]")]
TOTAL = sum(s[1] for s in SEGS)                                  # 12
X0, X1, BY, BH = 60, 940, 268, 84
UNIT = (X1 - X0) / TOTAL                                         # 칸 하나의 폭 = 73.33
FOCAL = 2                                                        # 실제로 나른 칸

ddx.band(d, 104, 488, "열 개는 두 개를 안전하게 나르기 위해 드는 값이다")

x = X0
edges = []
for i, (name, n, note, flags) in enumerate(SEGS):
    w = UNIT * n
    edges.append((x, w))
    focal = (i == FOCAL)
    c = ACC if focal else (INFO if i in (0, 4) else MUTED)
    d.o.append(f'<rect x="{x:.1f}" y="{BY}" width="{w:.1f}" height="{BH}" rx="5" '
               f'fill="{c}{"18" if focal else "0E"}" stroke="{c}" stroke-width="{1.6 if focal else 1.1}"/>')
    d.t(x + w / 2, BY + 40, str(n), 22, c, MONO, "middle", 600)
    d.t(x + w / 2, BY + 64, "개", 10, MUTED, KR)
    # 좁은 칸과 focal 칸은 한 줄 올린다 — focal 은 위에 '실어 나른 것' 라벨이 붙으므로
    ny = 216 if (i % 2 == 1 or focal) else 240
    d.t(x + w / 2, ny, ddx.fit(name, 12, w - 6, f"seg{i} name"), 12,
        c, KR, "middle", 600)
    if ny == 216 and not focal: d.line(x + w / 2, 224, x + w / 2, BY - 6, RULE, 0.8, "3 4")
    dy = 380 if i % 2 == 0 else 404
    d.t(x + w / 2, dy, ddx.fit(note, 11, w + 40, f"seg{i} note"), 11, MUTED, KR)
    d.t(x + w / 2, dy + 18, flags, 9, SOFT, MONO)
    x += w

fx, fw = edges[FOCAL]
d.o.append(f'<rect x="{fx-6:.1f}" y="{BY-14}" width="{fw+12:.1f}" height="{BH+28}" rx="8" '
           f'fill="none" stroke="{ACC}" stroke-width="1.4" stroke-dasharray="7 6"/>')
d.t(fx + fw / 2, BY - 24, "실어 나른 것", 11, ACC, KR)

d.t(500, 448, "12 개 중 2 개 — 나머지 열 개는 연결을 세우고 확인하고 닫는 데 든다", 12, MUTED, KR)
d.legend(504, [("연결 관리", INFO), ("실제 데이터", ACC)])
d.save("01-04.twelve-packets.svg")
print("ok twelve-packets")
