# 02-01 편 전체 — 개발자가 쥐는 결정이 어디까지인지를 한 장으로.
# 본문이 이 그림의 구획을 직접 적어 둔다: "이 편의 절반은 무엇을 고를 수 있나이고
# 나머지 절반은 고른 것을 코드로 어떻게 만지나입니다." 그 두 띠를 그대로 위아래로 놓고,
# 그 아래에 소켓 경계선을 그어 "고를 수 없는 것"을 갈랐다.
# 타입 스펙: type-process — 칸마다 절 번호·이름·요약이 같은 자리에 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 정본은 주체(actor)를 전제하는데 편 전체 지도에는 주체가 없다.
#           visual-diagram-selection.md 의 「알려진 공백」 표가 지시한 대체다 — actor 슬롯을 절 번호로 대신했다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 1000, 632
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 02-01",
      "개발자가 쥐는 결정은 소켓 위쪽뿐입니다",
      "일곱 절을 고르는 자리와 만지는 자리로 나누고, 그 아래에 소켓 경계선을 그어 고를 수 없는 것을 갈랐다.",
      "위 두 띠가 이 편이고, 경계선 아래는 이 편이 다루지 않는 자리입니다")

# ── 띠 A: 무엇을 고르나 (§1~§4)
d.t(24, 106, "무엇을 고르나", 13, INK, KR, "start", 600)
d.t(126, 106, "§1 ~ §4", 11, SOFT, MONO, "start")

AW, AGAP, AY, AH = 224, 20, 118, 84
ROW_A = [("§1", "두 구조", "클라이언트-서버냐 P2P 냐"),
         ("§2", "프로세스와 소켓", "문이 놓이는 자리"),
         ("§3", "TCP 냐 UDP 냐", "요구는 넷, 받는 건 둘"),
         ("§4", "앱 프로토콜", "애플리케이션의 한 조각")]
ax = []
for i, (num, name, sub) in enumerate(ROW_A):
    x = 24 + i * (AW + AGAP)
    ax.append(x)
    d.box(x, AY, AW, AH, PAPER2, RULE, 0.9)
    d.t(x + 16, AY + 26, num, 11, INFO, MONO, "start", 600)
    d.t(x + AW / 2, AY + 48, name, 13, INK, KR)
    d.t(x + AW / 2, AY + 68, sub, 11, MUTED, KR)
for i in range(3):
    d.path(f"M {ax[i] + AW + 3} {AY + AH / 2} L {ax[i + 1] - 7} {AY + AH / 2}", MUTED, 1.2, m="ar")

# ── 띠 B: 코드로 만진다 (§5~§7)
# 띠 A 의 마지막 칸에서 띠 B 의 첫 칸으로. 왼쪽 여백을 타고 내려가 띠 라벨을 비껴간다.
d.path(f"M {ax[3] + AW / 2} {AY + AH + 4} L {ax[3] + AW / 2} 224 L 10 224 L 10 300 L 18 300",
       MUTED, 1.2, m="ar")
d.t(24, 246, "고른 것을 코드로 만진다", 13, INK, KR, "start", 600)
d.t(184, 246, "§5 ~ §7", 11, SOFT, MONO, "start")

BW, BGAP, BY, BH = 304, 20, 258, 84
ROW_B = [("§5", "UDP 소켓", "편지마다 주소를 붙입니다"),
         ("§6", "TCP 소켓", "서버의 문이 둘입니다"),
         ("§7", "QUIC API", "악수가 하나로 합쳐집니다")]
bx = []
for i, (num, name, sub) in enumerate(ROW_B):
    x = 24 + i * (BW + BGAP)
    bx.append(x)
    d.box(x, BY, BW, BH, PAPER2, RULE, 0.9)
    d.t(x + 16, BY + 26, num, 11, INFO, MONO, "start", 600)
    d.t(x + BW / 2, BY + 48, name, 13, INK, KR)
    d.t(x + BW / 2, BY + 68, sub, 11, MUTED, KR)
for i in range(2):
    d.path(f"M {bx[i] + BW + 3} {BY + BH / 2} L {bx[i + 1] - 7} {BY + BH / 2}", MUTED, 1.2, m="ar")

# ── 경계선 (이 그림의 강조점)
d.tone(24, 376, 952, 60, ACC, 6, "12", 1.4)
d.t(44, 402, "소켓", 14, ACC, KR, "start", 600)
d.t(96, 402, "애플리케이션 층과 트랜스포트 층 사이의 인터페이스입니다", 12, INK, KR, "start")
d.t(44, 424, "위쪽은 전부 통제합니다. 아래쪽에 남는 것은 프로토콜 하나를 고르는 일과 파라미터 몇 개뿐입니다.",
    11, MUTED, KR, "start")

# ── 띠 C: 고를 수 없는 것
d.t(24, 470, "소켓 아래 — 개발자가 만지지 않는 것", 13, INK, KR, "start", 600)
CW, CGAP, CY, CH = 226, 16, 482, 44
for i, lab in enumerate(["3-way 핸드셰이크", "재전송과 순서 복원", "혼잡 제어 알고리즘", "코어 장비의 소프트웨어"]):
    x = 24 + i * (CW + CGAP)
    d.box(x, CY, CW, CH, PAPER2, RULE, 0.9)
    d.t(x + CW / 2, CY + 27, lab, 11, MUTED, KR)

d.t(24, 556, "그리고 아무도 주지 않는 것 — 처리량 보장과 타이밍 보장은 오늘날 어느 트랜스포트 프로토콜에도 없습니다.",
    11, MUTED, KR, "start")

d.legend(H - 52, [("이 편의 경계선", ACC), ("절 번호", INFO), ("이 편이 다루는 단계", MUTED)])
d.save("02-01.chapter-overview.svg")
print("ok chapter-overview")
