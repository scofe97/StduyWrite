# 타입 스펙: type-layers — 위에서 아래로 쌓인 계층. 세 장비가 어디까지 올라가는지를 같은 축에 나란히 둔다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.4.3 Figure 6.24 와 Table 6.1
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 940, 496
d = D(W, H, "SECTION 6.4.3 · HOW FAR UP EACH DEVICE READS",
      "어디까지 올라가 읽느냐가 둘을 가릅니다",
      "스위치는 2 계층까지만 읽고 라우터는 3 계층까지 읽는다. 처리 속도와 플러그 앤 플레이 여부가 이 차이에서 갈린다.",
      "계층 도달 범위는 원문 Figure 6.24 그대로입니다")

LAYERS = ["애플리케이션", "트랜스포트", "네트워크", "링크", "물리"]
LX, LW, LH = 24, 200, 52
DEVICES = [(268, "스위치", 3, OK), (508, "라우터", 2, INFO), (748, "호스트", 0, MUTED)]

d.t(LX, 104, "프로토콜 스택", 11, SOFT, KR, "start", 600)
for i, name in enumerate(LAYERS):
    y = 116 + i * (LH + 6)
    d.box(LX, y, LW, LH, PAPER2, RULE, 0.9)
    d.t(LX + LW / 2, y + 31, name, 12, INK, KR, "middle", 600)

for x, dev, top_idx, c in DEVICES:
    d.t(x + 84, 104, dev, 11, c, KR, "middle", 600)
    for i in range(len(LAYERS)):
        y = 116 + i * (LH + 6)
        if i >= top_idx:
            d.tone(x, y, 168, LH, c, 6, "14", 1.2)
            d.t(x + 84, y + 31, "읽습니다", 11, c, KR)
        else:
            d.box(x, y, 168, LH, PAPER, RULE, 0.6)
            d.t(x + 84, y + 31, "안 봅니다", 11, SOFT, KR)

d.line(24, 416, W - 48, 416, RULE, 0.8)
d.t(24, 438, "스위치는 프레임을 2 계층까지만 처리하므로 필터링·포워딩 속도가 상대적으로 높습니다. "
             "대신 브로드캐스트 순환을 막으려 활성 토폴로지가 신장 트리로 제한됩니다.", 11, MUTED, KR, "start")

d.legend(456, [("2 계층까지 — 스위치", OK), ("3 계층까지 — 라우터", INFO), ("끝까지 — 호스트", MUTED)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-04.processing-depth.svg"
d.save(out)
print("→", out)
