# 타입 스펙: type-tree
# 03-01 이미지 한 개를 이루는 digest 사슬 (node:20.11.1-alpine, linux/amd64)
# 값은 2026-11-23 docker save --platform linux/amd64 로 만든 tar 에서 직접 잰 것이다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 484

d = D(W, H, "DEVOPS · CONTAINER · 03-01",
      "이미지 한 개를 이루는 digest 사슬",
      "index 가 manifest 를, manifest 가 config 와 layer 넷을 sha256 digest 로 가리키는 구조",
      lead="node:20.11.1-alpine linux/amd64 — digest 는 앞 8자리만 표기")

# 노드 폭은 둘뿐이다: 넓은 것(루트·manifest·diff_ids) 200, 좁은 것(config·layer) 160
WN, WB = 160, 200
H3 = 52
Y1, Y2, Y3, Y4 = 104, 188, 272, 356
H4 = 60

XS = [24, 212, 400, 588, 776]          # 자식 다섯의 왼쪽 x (간격 28)
CX = [x + WN // 2 for x in XS]
ROOT_CX = (XS[0] + XS[-1] + WN) // 2   # 480
BUS_Y = 256

# ── 연결선은 노드보다 먼저 그린다 ──
# 루트 → manifest
d.arrow([(ROOT_CX, Y1 + H3), (ROOT_CX, Y2 - 2)], MUTED, "ar", 1.2)
# manifest → 버스 → 자식 다섯
d.line(ROOT_CX, Y2 + H3, ROOT_CX, BUS_Y, MUTED, 1.2)
d.line(CX[0], BUS_Y, CX[-1], BUS_Y, MUTED, 1.2)
for cx in CX:
    d.arrow([(cx, BUS_Y), (cx, Y3 - 2)], MUTED, "ar", 1.2)
# config → diff_ids
d.arrow([(CX[0], Y3 + H3), (CX[0], Y4 - 2)], MUTED, "ar", 1.2)
# layer 1 → 압축을 풀어 잰 값 (diff_ids 첫 값)
d.arrow([(CX[1], Y3 + H3), (CX[1], Y4 + H4 // 2), (XS[0] + WB + 2, Y4 + H4 // 2)],
        INFO, "info", 1.4, "5 4")
d.t(CX[1] + 16, Y4 - 4, "압축 해제 후 sha256", 13, INFO, KR, "start", 600)


def node(x, y, w, h, name, sub, tone=None):
    if tone:
        d.tone(x, y, w, h, tone, 6, "14", 1.4 if tone == ACC else 1.2)
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    c = tone or INK
    d.t(x + w // 2, y + 22, name, 13, c if tone else INK, KR, "middle", 600)
    d.t(x + w // 2, y + 40, sub, 12, INK if tone else MUTED, MONO, "middle")


# 1단: 루트
node(ROOT_CX - WB // 2, Y1, WB, H3, "index.json", "→ 121edf66")
# 2단: manifest (focal — 이미지 ID 가 되는 digest)
node(ROOT_CX - WB // 2, Y2, WB, H3, "manifest", "121edf66", ACC)
# 3단: config 와 layer 넷
node(XS[0], Y3, WN, H3, "config", "ae7f6c37")
for i, (x, dg) in enumerate(zip(XS[1:], ["4abcf206", "9f16480e", "092226d5", "0493dfb2"]), 1):
    node(x, Y3, WN, H3, f"layer {i} · gzip", dg)
# 4단: diff_ids (config 안의 값)
d.tone(XS[0], Y4, WB, H4, INFO, 6, "12", 1.2)
d.t(XS[0] + WB // 2, Y4 + 20, "diff_ids ×4 · 압축 전", 13, INFO, KR, "middle", 600)
d.t(XS[0] + WB // 2, Y4 + 38, "d4fc045c · f6810059", 12, INK, MONO, "middle")
d.t(XS[0] + WB // 2, Y4 + 54, "b4770ab4 · 468d5814", 12, INK, MONO, "middle")

d.legend(Y4 + H4 + 20, [
    ("이미지 ID 가 되는 manifest", ACC),
    ("digest 로 가리킴", MUTED),
    ("압축을 풀어 잰 digest", INFO),
])

d.save("03-01.digest-chain.svg")
print("ok gen-03-01.digest-chain")
