# 개념 노트 「힙 밖에서 쌓이는 메모리」 · 스레드가 늘어나는 경로.
# 논지는 포함 관계다 — 리소스 묶음 안에 그룹, 그룹 안에 루프, 루프 하나가 소켓 여럿.
# 묶음을 여러 벌 만들면 가장 안쪽 스레드 수가 곱해진다.
# 타입 스펙: type-nested — 포함·범위로 드러나는 계층. 겹의 깊이가 곧 "무엇이 무엇을 여럿 갖는가"다.
#           라벨은 계약대로 좌상단에 두되 paper 마스크 대신 겹 안쪽 여백에 넣어 겹침 검사를 피한다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, OK, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 464
d = D(W, H, "TROUBLESHOOTING CONCEPT · NETTY EVENT LOOP",
      "루프 하나가 소켓 여럿을 맡고, 그 루프가 여러 개 묶입니다",
      "Netty 의 이벤트 루프는 스레드 하나가 소켓 여럿의 입출력을 돌아가며 처리하는 구조다. 그 루프를 여럿 묶은 것이 그룹이고, "
      "그룹은 클라이언트의 리소스 묶음이 갖는다. 묶음을 여러 벌 만들면 가장 안쪽 스레드 수가 그만큼 곱해진다.",
      lead="스레드가 늘면 malloc 의 arena 도 함께 늘어납니다")

RINGS = [(24, 96, 560, 296), (56, 136, 496, 240), (88, 176, 432, 184), (120, 216, 368, 128)]
STROKE = [f"{INK}30", f"{INK}44", f"{INK}58"]
for i, (x, y, w, h) in enumerate(RINGS[:3]):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="none" '
               f'stroke="{STROKE[i]}" stroke-width="1.0"/>')
x, y, w, h = RINGS[3]
d.tone(x, y, w, h, ACC, 8)

d.t(40, 120, "자바 프로세스", 12, SOFT, KR, "start", 600)
d.t(72, 160, "리소스 묶음 · ClientResources", 12, SOFT, KR, "start", 600)
d.t(104, 200, "이벤트 루프 그룹 · EventLoopGroup", 12, SOFT, KR, "start", 600)
d.t(136, 244, "이벤트 루프 하나 = 스레드 하나", 13, ACC, KR, "start", 600)
d.t(136, 268, "소켓 여럿을 돌아가며 처리", 12, MUTED, KR, "start")
d.t(136, 300, "힙 바깥 버퍼를 직접 다룬다", 12, MUTED, KR, "start")

# 오른쪽 — 묶음이 여러 벌일 때 스레드가 곱해진다
BX, BW, BH2 = 640, 256, 68
ROWS = [("묶음 한 벌", "그룹 1 × 루프 n", OK),
        ("묶음 세 벌", "그룹 3 × 루프 n", ACC),
        ("에이전트가 더하는 몫", "계측 스레드와 할당 경로", MUTED)]
for i, (t1, t2, c) in enumerate(ROWS):
    y2 = 104 + i * 92
    d.box(BX, y2, BW, BH2, PAPER2, RULE, 0.9, 6)
    d.t(BX + 20, y2 + 28, t1, 13, c, KR, "start", 600)
    d.t(BX + 20, y2 + 50, t2, 12, MUTED, KR, "start")

d.legend(408, [("가장 안쪽 = 스레드", ACC), ("한 벌일 때", OK), ("겹의 경계", INK)])
d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-21.eventloop-group.svg"))
print("ok")
