# 09-01.error-choice — 어떤 오류를 만들까: 문자열 · 사용자 정의 타입 · 기존 센티널 · 새 센티널
# 본문 요구(09-01 §3 「센티널 오류는 공개 API 에 대한 약속입니다」): 원문은 단순한 오류는 errors.New·fmt.Errorf 로,
#           조건 정보가 필요하면 오류 타입으로, 표준 라이브러리의 기존 센티널이 있으면 재사용하고, 더 처리할 수 없는 상태이면서
#           추가 정보가 필요 없을 때만 새 센티널을 정의하라고 권한다. 이 권고들을 위에서 아래 판단 순서로 엮은 것은 노트의 풀이다.
# 타입 스펙: type-flowchart — 02-02.declare-choice 와 같은 골격(시작 타원, 판단 마름모, 결과 사각, 끝 타원).
#           예는 오른쪽 결과로, 아니오는 아래로. stride 세로 96, 판단 열 중심 x 256, 결과 열 x 536.
#           coral 은 마지막에 남는 "새 센티널" 끝 하나(공개 API 약속이라 가장 신중해야 하는 선택).
# 사실 출처: Learning Go 2판 9장 「Use Strings for Simple Errors」·「Sentinel Errors」·「Errors Are Values」.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 984, 596
CX, RX, RW, RH = 256, 536, 400, 48
DW, DH = 344, 60
START_Y, STRIDE = 112, 96
Q_Y = [START_Y + 88 + i * STRIDE for i in range(3)]     # 200 296 392
END_Y = Q_Y[-1] + DH // 2 + 48


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def diamond(cx, cy, text):
    pts = f"{cx},{cy - DH // 2} {cx + DW // 2},{cy} {cx},{cy + DH // 2} {cx - DW // 2},{cy}"
    d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="rgba(191,192,192,0.22)" stroke-width="0.9"/>')
    d.t(cx, cy + 5, text, 13, INK, kr(text), "middle", 600)


def result(y, main, sub, c):
    d.tone(RX, y - RH // 2, RW, RH, c, 6, "10", 1.0)
    d.t(RX + 16, y - 2, main, 14, c, kr(main), "start", 600)
    d.t(RX + 16, y + 16, sub, 12, MUTED, kr(sub), "start")


d = D(W, H, "FLOWCHART · 09-01 §3",
      "어떤 오류를 만들까",
      "원문의 권고를 판단 순서로 엮은 흐름도. 호출자가 오류를 골라 처리할 필요가 없으면 errors.New 나 fmt.Errorf 의 문자열 오류로 충분하다. "
      "원인을 설명할 정보가 더 필요하면 사용자 정의 오류 타입을 만든다. 표준 라이브러리에 같은 뜻의 센티널이 있으면 재사용한다. "
      "그 어느 것도 아니고 더 처리할 수 없는 상태를 알려야 할 때만 새 센티널을 정의하며, 이것은 공개 API 에 대한 약속이 된다.",
      lead="판단 순서는 노트가 원문 권고를 엮은 것입니다. 예는 오른쪽, 아니오는 아래로 갑니다.")

d.o.append(f'<rect x="{CX - 96}" y="{START_Y}" width="192" height="40" rx="20" fill="{PAPER2}" stroke="rgba(191,192,192,0.22)" stroke-width="0.9"/>')
d.t(CX, START_Y + 25, "오류를 만들 때", 14, INK, KR, "middle", 600)
d.arrow([(CX, START_Y + 40), (CX, Q_Y[0] - DH // 2)], SOFT, "soft", 1.2)

qs = [("호출자가 골라 처리할 필요 없음?", ("errors.New · fmt.Errorf", "문자열 오류로 충분", INFO)),
      ("원인 설명에 정보가 더 필요?", ("사용자 정의 오류 타입", "StatusErr · 반환 타입은 error", OK)),
      ("표준 라이브러리에 같은 센티널?", ("기존 센티널 재사용", "io.EOF · zip.ErrFormat", WARN))]
for i, (q, (m, s, c)) in enumerate(qs):
    y = Q_Y[i]
    diamond(CX, y, q)
    d.arrow([(CX + DW // 2, y), (RX, y)], SOFT, "soft", 1.2)
    d.t(CX + DW // 2 + 32, y - 8, "예", 12, MUTED, KR, "middle")
    result(y, m, s, c)
    nxt = Q_Y[i + 1] - DH // 2 if i < 2 else END_Y
    d.arrow([(CX, y + DH // 2), (CX, nxt)], SOFT, "soft", 1.2)
    d.t(CX + 12, y + DH // 2 + 22, "아니오", 12, MUTED, KR, "start")

d.o.append(f'<rect x="{CX - 132}" y="{END_Y}" width="264" height="44" rx="20" fill="{ACC}14" stroke="{ACC}" stroke-width="1.4"/>')
d.t(CX, END_Y + 28, "새 센티널 오류", 15, ACC, KR, "middle", 600)
d.t(CX + 148, END_Y + 20, "var ErrX = errors.New(...)", 12, MUTED, MONO, "start")
d.t(CX + 148, END_Y + 38, "공개 API 약속 · == 로 확인", 12, MUTED, KR, "start")

d.legend(540, [("문자열 오류", INFO), ("사용자 정의 타입", OK), ("기존 센티널", WARN), ("새 센티널", ACC)])
d.save("09-01.error-choice.svg")
print("ok 09-01 error-choice")
