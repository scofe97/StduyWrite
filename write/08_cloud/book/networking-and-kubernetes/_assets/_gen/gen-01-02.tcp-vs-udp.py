# 01-02.tcp-vs-udp — 같은 저울의 반대편, 헤더가 능력을 정하고 능력이 값을 부른다
# 본문 요구(01-02 §6): 두 프로토콜을 "같은 자리에서 반대 방향을 고른 둘"로 읽는다. 그래서 표가
#           단순 대조가 아니라 인과의 사슬이다 — 헤더에 무엇을 두느냐 → 그래서 할 수 있는 일 →
#           그래서 치르는 값. 열 사이 화살표가 그 "그래서"다.
#           칸 색이 열마다 고정이 아니라 행마다 뒤집히는 것이 이 장의 요점이다. TCP 는 능력이
#           초록(얻는다)이고 값이 노랑(치른다)인데, UDP 는 능력이 빨강(포기한다)이고 값이
#           초록(치르지 않는다)이다. 같은 열에서 색이 바뀌는 자리가 곧 맞바꿈이다.
# 타입 스펙: type-dp-security-matrix.md — 행은 프로토콜, 열은 세 축. 어느 칸이 이득이고 어느
#           칸이 대가인지를 색이 판정한다.
# 이력: 2026-08-28 신설. 이 장도 dd 프리미티브가 아니라 손으로 쓴 SVG 였다 — defs 에 마커가
#           하나뿐이고 text-anchor 가 없었다. 문구·수치·색 배정을 그대로 두고 배치만 house
#           스타일(표준 헤더·범례 프리미티브)로 다시 세웠다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO

W, H = 938, 424
X0, LW, CW, GAP = 12, 150, 228, 16
HDR_Y, HDR_H, ROW_Y, ROW_H, STRIDE = 88, 44, 152, 92, 104
CX = [X0 + LW + GAP + i * (CW + GAP) for i in range(3)]

d = D(W, H, "COMPARISON MATRIX · 01-02 TRANSPORT",
      "TCP 와 UDP — 같은 저울의 반대편",
      "TCP와 UDP를 헤더 구성·할 수 있는 일·치르는 값 세 축으로 나란히 비교한 행렬. 윗줄과 "
      "아랫줄이 같은 모양으로 이어져, 헤더에 무엇을 두느냐가 능력을 정하고 그 능력이 다시 "
      "비용으로 돌아오는 구조를 보여준다.",
      lead="헤더에 무엇을 두느냐가 할 수 있는 일을 정하고, 그 능력이 다시 값으로 돌아옵니다.")

d.box(X0, HDR_Y, LW, HDR_H, "none", RULE, 0.9)
d.t(X0 + LW / 2, HDR_Y + 27, "프로토콜 vs. 축", 11, SOFT)
for cx, name in zip(CX, ("헤더에 무엇을 두나", "그래서 할 수 있는 일", "그래서 치르는 값")):
    d.box(cx, HDR_Y, CW, HDR_H, PAPER2, RULE, 0.9)
    d.t(cx + CW / 2, HDR_Y + 27, name, 12, INK, KR, "middle", 600)

# (프로토콜, 부제, 행 색, [(윗줄, 아랫줄, 그 칸의 판정색) × 3])
ROWS = [("TCP", "연결 지향 · 기본값", OK,
         [("Seq · Ack · Window · Flags", "10필드 · 최소 20바이트", INFO),
          ("재전송 · 순서 재조립 · 흐름 제어", "유실을 메운다", OK),
          ("핸드셰이크 3 + 종료 4 · 지연", "7패킷을 먼저 지불", WARN)]),
        ("UDP", "비연결 · 명시 지정 필요", ACC,
         [("Src · Dst · Length · Checksum", "4필드 · 최소 8바이트", INFO),
          ("없음 — 보내고 잊는다", "유실을 견뎌야 한다", BAD),
          ("없음 · 지연 없는 전달", "값을 치르지 않는다", OK)])]

for r, (proto, sub, rc, cells) in enumerate(ROWS):
    y = ROW_Y + STRIDE * r
    d.tone(X0, y, LW, ROW_H, rc, 6, "14", 1.2)
    d.t(X0 + LW / 2, y + 42, proto, 20, rc, KR, "middle", 600)
    d.t(X0 + LW / 2, y + 62, sub, 11, MUTED)
    for cx, (top, bot, c) in zip(CX, cells):
        d.box(cx, y, CW, ROW_H, f"{c}12", f"{c}59", 1.0)
        # 가운데 정렬이라 여백은 양쪽으로 갈린다 — 안쪽 4px 씩만 빼고 잰다.
        # fit 의 폭 추정은 일부러 넉넉해서(· 를 전각으로 센다) 16px 을 빼면
        # 실제로는 들어가는 'Src · Dst · Length · Checksum' 이 헛경보로 걸린다.
        d.t(cx + CW / 2, y + 38, ddx.fit(top, 12, CW - 8, top), 12, INK, KR, "middle", 600)
        d.t(cx + CW / 2, y + 62, ddx.fit(bot, 11, CW - 8, bot), 11, c)
    for a, b in zip(CX, CX[1:]):        # "그래서" — 인과가 왼쪽에서 오른쪽으로 흐른다
        d.path(f"M {a+CW+2} {y+ROW_H/2} L {b-2} {y+ROW_H/2}", SOFT, 1.2, m="soft")

d.legend(380, [("헤더 구성", INFO), ("얻는 능력", OK), ("치르는 값", WARN), ("포기한 것", BAD)])
d.save("01-02.tcp-vs-udp.svg")
print("ok tcp-vs-udp")
