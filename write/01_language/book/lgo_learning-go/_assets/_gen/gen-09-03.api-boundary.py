# 09-03.api-boundary — 서드파티용 라이브러리의 공개 함수가 recover 로 panic 을 붙잡아 error 로 바꿔 돌려주는 구조
# 본문 요구(09-03 §2 「recover 는 서드파티용 API 경계에서 씁니다」): 원문이 recover 를 권하는 유일한 상황은 panic 이 공개 API 경계를
#           넘어 새어 나가지 않게 공개 함수가 recover 로 panic 을 오류로 바꿔 돌려주고, 호출하는 코드가 어떻게 할지 정하게 하는 것이다.
# 타입 스펙: type-architecture — 왼쪽 호출 코드, 가운데 점선 경계, 존(라이브러리) 안에 공개 함수와 내부 코드. 직교 화살표만.
#           위 줄은 호출(→), 아래 줄은 되돌아오는 panic·error(←). focal 은 공개 함수 안의 recover 칩 하나.
# 사실 출처: Learning Go 2판 9장 「panic and recover」 마지막 문단.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER2, KR, MONO

W, H = 984, 404
BY, BH, BW = 168, 128, 256
X_CALL, X_PUB, X_INT = 36, 400, 700
ZX, ZY, ZW, ZH = 376, 132, 592, 196


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "ARCHITECTURE · 09-03 §2",
      "panic 은 공개 API 경계 안에서 오류가 됩니다",
      "서드파티용 라이브러리를 만들 때의 구조. 호출 코드가 공개 함수를 부르고 공개 함수가 내부 코드를 부른다. 내부에서 panic 이 나면 "
      "공개 함수에 defer 로 둔 recover 가 붙잡아 error 로 바꾸고, 호출 코드는 panic 이 아니라 오류를 받아 어떻게 할지 정한다.",
      lead="점선 안이 라이브러리입니다. panic 이 점선 밖으로 새어 나가지 않게 합니다.")

d.o.append(f'<rect x="{ZX}" y="{ZY}" width="{ZW}" height="{ZH}" rx="10" fill="none" stroke="{SOFT}" stroke-width="1" stroke-dasharray="5 5"/>')
d.t(ZX + 16, ZY + 20, "라이브러리 · 공개 API 경계", 12, MUTED, KR, "start", 600)

d.box(X_CALL, BY, BW, BH, r=8)
d.t(X_CALL + BW // 2, BY + 32, "호출 코드", 14, INK, KR, "middle", 600)
d.t(X_CALL + BW // 2, BY + 52, "서드파티 사용자", 12, MUTED, KR, "middle")

d.box(X_PUB, BY, BW, BH, r=8)
d.t(X_PUB + BW // 2, BY + 32, "공개 함수", 14, INK, KR, "middle", 600)
d.t(X_PUB + BW // 2, BY + 52, "(…, error) 를 돌려줌", 12, MUTED, KR, "middle")
d.tone(X_PUB + 24, BY + 72, BW - 48, 32, ACC, 4, "22", 1.4)
d.t(X_PUB + BW // 2, BY + 93, "defer … recover()", 12, ACC, MONO, "middle", 600)

d.box(X_INT, BY, BW - 16, BH, r=8)
d.t(X_INT + (BW - 16) // 2, BY + 32, "내부 코드", 14, INK, KR, "middle", 600)
d.t(X_INT + (BW - 16) // 2, BY + 52, "여기서 panic", 12, MUTED, KR, "middle")

TOP, BOT = BY + 76, BY + 104
d.arrow([(X_CALL + BW + 2, TOP), (X_PUB - 4, TOP)], SOFT, "soft", 1.3)
d.t((X_CALL + BW + X_PUB) // 2, TOP - 8, "호출", 12, MUTED, KR, "middle", 600)
d.arrow([(X_PUB + BW + 2, TOP), (X_INT - 4, TOP)], SOFT, "soft", 1.3)
d.t((X_PUB + BW + X_INT) // 2, TOP - 8, "호출", 12, MUTED, KR, "middle", 600)
d.arrow([(X_INT - 2, BOT), (X_PUB + BW + 4, BOT)], BAD, "bad", 1.3)
d.t((X_PUB + BW + X_INT) // 2, BOT + 20, "panic", 12, BAD, MONO, "middle", 600)
d.arrow([(X_PUB - 2, BOT), (X_CALL + BW + 4, BOT)], OK, "ok", 1.3)
d.t((X_CALL + BW + X_PUB) // 2, BOT + 20, "error", 12, OK, MONO, "middle", 600)

d.legend(348, [("panic", BAD), ("recover 로 붙잡음", ACC), ("오류로 전달", OK)])
d.save("09-03.api-boundary.svg")
print("ok 09-03 api-boundary")
