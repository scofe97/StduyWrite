# 타입 스펙: type-flowchart — cancelFunc(err) 첫 호출 원인이 보존되고 추가 호출은 무시되는 판단 흐름
# 본문 요구(14-02 §2 「원인을 넘기고 Cause 로 꺼냅니다」):
#           WithCancelCause 로 만든 context 는 첫 cancelFunc(err) 호출의 오류만 기록한다.
#           두 번째 호출은 덮어쓰지 않고 무시되며, Cause 는 첫 원인을 돌려주고 Err 는 context.Canceled 다.
# 사실 출처: Learning Go 2판 14장 「Cancellation」 cancel_error_http, first·second 실측
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 530
CX, RX = 360, 740
DW, DH = 260, 60
START_Y = 108
Q_Y = 224
P_Y = 318
RES_Y = 412
LEGEND_Y = 484


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "FLOWCHART · 14-02 §2",
      "취소 원인은 처음 전달된 오류 하나만 유지됩니다",
      "WithCancelCause 의 동작 흐름. 첫 cancelFunc 호출 시 전달된 오류가 Cause 에 저장되고, 이후의 추가 호출은 원인을 덮어쓰지 않고 무시된다.",
      lead="두 번째 이후의 취소 호출은 무시되며 처음 등록된 원인과 Canceled 에러가 유지됩니다.")

# 시작 타원
d.o.append(f'<rect x="{CX - 130}" y="{START_Y}" width="260" height="40" rx="20" fill="{PAPER2}" stroke="{RULE}" stroke-width="0.9"/>')
d.t(CX, START_Y + 25, "cancelFunc(err) 호출", 13, INK, KR, "middle", 600)

# 시작 -> 판단 화살표
d.arrow([(CX, START_Y + 40), (CX, Q_Y - DH // 2)], SOFT, "soft", 1.2)

# 판단 마름모
pts = f"{CX},{Q_Y - DH // 2} {CX + DW // 2},{Q_Y} {CX},{Q_Y + DH // 2} {CX - DW // 2},{Q_Y}"
d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{RULE}" stroke-width="0.9"/>')
d.t(CX, Q_Y + 5, "ctx.Err() != nil ?", 12, INK, MONO, "middle", 600)

# 아니오 분기 (아래로: 첫 번째 취소 — FOCAL)
d.arrow([(CX, Q_Y + DH // 2), (CX, P_Y - 4)], ACC, "acc", 1.4)
d.t(CX - 12, Q_Y + DH // 2 + 22, "아니오 (첫 호출)", 11, ACC, KR, "end", 600)

d.tone(CX - 160, P_Y, 320, 56, ACC, 6, "14", 1.4)
d.t(CX, P_Y + 24, "첫 취소 원인 저장 (focal)", 13, ACC, KR, "middle", 600)
d.t(CX, P_Y + 44, "Cause(ctx) = first · Err() = context.Canceled", 11, MUTED, MONO, "middle")

# 예 분기 (오른쪽으로: 추가 취소 호출)
d.arrow([(CX + DW // 2, Q_Y), (RX, Q_Y), (RX, P_Y - 4)], SOFT, "soft", 1.2)
d.t(CX + DW // 2 + 36, Q_Y - 8, "예 (추가 호출)", 11, MUTED, KR, "start", 600)

d.box(RX - 130, P_Y, 260, 56, PAPER2, RULE, 1.0, 6)
d.t(RX, P_Y + 24, "원인 덮어쓰기 무시", 13, INK, KR, "middle", 600)
d.t(RX, P_Y + 44, "second 원인 버림 · 기존 유지", 11, MUTED, KR, "middle")

# 합류 지점 및 결과 상자
# Node 1 아래 화살표
d.line(CX, P_Y + 56, CX, RES_Y - 20, ACC, 1.2)
# Node 2 아래 연결선 (ㄷ자 우회)
d.line(RX, P_Y + 56, RX, RES_Y - 20, SOFT, 1.2)
d.line(RX, RES_Y - 20, CX, RES_Y - 20, SOFT, 1.2)

# 합류점 원
d.o.append(f'<circle cx="{CX}" cy="{RES_Y - 20}" r="3" fill="{INK}"/>')

# 결과 상자로 들어가는 화살표
d.arrow([(CX, RES_Y - 20), (CX, RES_Y - 4)], OK, "ok", 1.4)

# 결과 상자
d.tone(CX - 220, RES_Y, 440, 48, OK, 6, "14", 1.2)
d.t(CX, RES_Y + 20, "최종 반환 값: 처음 넘긴 원인 유지", 13, OK, KR, "middle", 600)
d.t(CX, RES_Y + 38, "context.Cause(ctx) == first · ctx.Err() == context.Canceled", 11, MUTED, MONO, "middle")

# 범례
d.legend(LEGEND_Y, [("첫 취소 원인 저장 (focal)", ACC), ("추가 취소 무시", SOFT), ("최종 반환 값", OK)])

d.save("14-02.cause-vs-err.svg")
print("ok 14-02 cause-vs-err")
