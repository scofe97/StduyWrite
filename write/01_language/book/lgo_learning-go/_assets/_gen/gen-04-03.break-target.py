# 04-03.break-target — switch 안의 break 는 switch 만 빠져나가고, 라벨을 달아야 for 를 빠져나간다
# 본문 요구(04-03 §2 「for 안의 switch 에서 break」): 예제 4-20 은 case 7 의 break 가 case 만 끝내 8·9 가 계속 찍히고,
#           for 에 loop 라벨을 달고 break loop 로 바꾸면 루프가 끝난다. 두 블록이 겹친 포함 관계와 두 break 의 착지점이 논지다.
# 타입 스펙: type-nested — 바깥 for 블록 안에 switch 블록. 두 break 는 같은 case 에서 출발해 서로 다른 겹 밖으로
#           직각으로 나간다(dd-lint 대각선 금지). 좌우 두 열로 같은 구조를 나란히 두고 break 줄만 바꾼다.
#           stride: 열 폭 448, 열 간격 40, 겹 여백 24. focal 은 의도대로 루프를 끝내는 오른쪽 열의 착지점 하나.
# 사실 출처: Learning Go 2판 4장 예제 4-20·labeledBreak, go1.25.1 실행(2026-09-27) — 라벨 없이 break 하면 7 뒤에도
#           8 is boring·9 is boring 이 찍히고, break loop 는 exit the loop! 뒤에서 멈춘다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, WARN, INFO, PAPER2, KR, MONO

W, H = 984, 540
COLW, GAP = 448, 40
XS = (24, 24 + COLW + GAP)


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def block(x, y, w, h, label, c="rgba(191,192,192,0.30)", fill="#161B22"):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{c}" stroke-width="0.9"/>')
    d.t(x + 16, y + 24, label, 13, MUTED, MONO, "start", 600)


d = D(W, H, "NESTED · 04-03 §2",
      "switch 안의 break 가 빠져나가는 곳",
      "for 블록 안에 switch 블록이 든 예제 4-20 을 두 열로 나란히 그린 그림. 왼쪽은 case 7 의 break 가 switch 만 빠져나가 "
      "다음 i 로 이어지므로 8·9 가 계속 찍힌다. 오른쪽은 for 에 loop 라벨을 달고 break loop 로 바꿔, 같은 자리에서 for 블록 밖으로 "
      "빠져나가 루프가 끝난다.",
      lead="같은 case 7 에서 출발한 break 가 어느 상자 밖으로 나가는지 봅니다.")

titles = [("break", "switch 만 끝남"), ("break loop", "for 까지 끝남")]
for k, x in enumerate(XS):
    label = "for i := 0; i < 10; i++" if k == 0 else "loop: for i := 0; i < 10; i++"
    block(x, 104, COLW, 336, label, fill="#0D1117")
    block(x + 24, 144, COLW - 48, 176, "switch i")
    # case 7 칸
    cx, cy = x + 48, 184
    d.tone(cx, cy, COLW - 96, 96, BAD if k == 0 else ACC, 6, "12", 1.2)
    d.t(cx + 16, cy + 26, "case 7:", 14, INK, MONO, "start", 600)
    d.t(cx + 16, cy + 50, 'fmt.Println("exit the loop!")', 13, MUTED, MONO, "start")
    d.t(cx + 16, cy + 76, titles[k][0], 14, BAD if k == 0 else ACC, MONO, "start", 600)
    ax = cx + COLW - 96 - 24
    if k == 0:
        # switch 블록 아래로 — 루프 안에 남음
        d.arrow([(ax, cy + 96), (ax, 344)], BAD, "bad", 1.6)
        d.t(x + 40, 372, "다음 i 로 → 8 is boring · 9 is boring", 13, BAD, KR, "start")
        d.t(x + 40, 400, "switch 만 끝남", 13, BAD, KR, "start", 600)
    else:
        # for 블록 밖으로
        d.arrow([(ax, cy + 96), (ax, 456)], ACC, "acc", 1.6)
        d.t(x + 40, 372, "루프 끝 · exit the loop! 뒤 출력 없음", 13, ACC, KR, "start")
        d.t(x + 40, 400, "for 까지 끝남", 13, ACC, KR, "start", 600)
    d.t(x + COLW // 2, 476, "for 블록 밖", 12, SOFT, KR, "middle")

d.legend(496, [("의도와 다른 착지점", BAD), ("의도한 착지점", ACC)])
d.save("04-03.break-target.svg")
print("ok 04-03 break-target")
