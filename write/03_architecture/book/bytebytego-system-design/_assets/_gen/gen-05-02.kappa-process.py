# 타입 스펙: type-process — 같은 구성요소(로그·작업 v1·작업 v2·앱 읽기)를 네 단계에 걸쳐 같은 자리에 되풀이해 그린다. 칸 사이를 건너가는 것은 로그를 읽는 위치(오프셋) 하나이고, 그 위치가 단계마다 움직인다.
# 표기: v1 은 옛 작업, v2 는 새 작업. Kreps 글의 "beginning of the retained data" 를 「보관된 처음」 으로 옮겼다.
# 사실 출처: Jay Kreps, "Questioning the Lambda Architecture"(O'Reilly Radar, 2014-07-02) — 재처리하려는 기간만큼 Kafka 보관 기간을 늘리고(예: 30일), 처리 코드가 바뀌면 같은 작업의 두 번째 인스턴스를 로그 처음부터 돌려 새 출력 테이블에 쓰고, 따라잡으면 앱이 새 테이블을 읽게 바꾸고, 옛 작업을 멈추고 옛 테이블을 지운다. 오프셋 4,200·4,230·4,260·4,290 은 설명용 예시 값이다.
# Layout conventions: 행 라벨 열 x=24 w=140, 단계 열 4개 x=180·364·548·732 w=160(stride 184), 행 y=148·216·284·352 h=52(stride 68), 단계 머리 y=100 h=32. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 480
d = D(W, H, "BYTEBYTEGO · 05-02 §5",
      "카파 구조의 재처리 네 단계",
      "로그를 오래 보관한 채 새 작업을 처음부터 돌려 새 테이블을 채우고 앱이 그 테이블로 옮겨 가는 흐름입니다",
      "같은 로그의 읽는 위치가 단계마다 움직입니다. 값은 예시입니다")

X0, STRIDE, CW = 180, 184, 160
HEAD_Y, ROW_Y0, ROW_STRIDE, RH = 100, 148, 68, 52
STAGES = ["1 평상시", "2 v2 시작", "3 따라잡음", "4 정리"]
ROWS = ["로그", "작업 v1", "작업 v2", "앱 읽기"]

# (문구, 상태색, 점선 여부)
CELLS = [
    [("보관 30일 · 끝 4,200", INFO, False), ("끝 4,230", INFO, False), ("끝 4,260", INFO, False), ("끝 4,290", INFO, False)],
    [("위치 4,200", OK, False), ("위치 4,230", OK, False), ("위치 4,260", OK, False), ("중지 · 테이블 삭제", BAD, False)],
    [("없음", SOFT, True), ("보관된 처음에서 시작", WARN, False), ("위치 4,260", OK, False), ("위치 4,290", OK, False)],
    [("v1 테이블", OK, False), ("v1 테이블", OK, False), ("v2 테이블로 전환", ACC, False), ("v2 테이블", OK, False)],
]


def fam(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


# 단계 머리와 사이 화살표
for k, name in enumerate(STAGES):
    x = X0 + k * STRIDE
    d.box(x, HEAD_Y, CW, 32, PAPER2, RULE, 0.9, 6)
    d.t(x + CW / 2, HEAD_Y + 21, name, 13, INK, KR, "middle", 600)
    if k < len(STAGES) - 1:
        d.arrow([(x + CW + 2, HEAD_Y + 16), (x + STRIDE - 4, HEAD_Y + 16)], MUTED, "ar", 1.4)

# 행 라벨과 칸
for r, rname in enumerate(ROWS):
    y = ROW_Y0 + r * ROW_STRIDE
    d.t(24, y + 30, rname, 13, INK, fam(rname), "start", 600)
    for k, (txt, c, dashed) in enumerate(CELLS[r]):
        x = X0 + k * STRIDE
        if dashed:
            d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{RH}" rx="6" fill="none" stroke="{SOFT}" stroke-width="1" stroke-dasharray="4 4"/>')
            d.t(x + CW / 2, y + 31, txt, 13, SOFT, fam(txt), "middle")
        elif c == ACC:
            d.tone(x, y, CW, RH, ACC, 6, "14", 1.4)
            d.t(x + CW / 2, y + 31, txt, 13, ACC, fam(txt), "middle", 600)
        else:
            d.tone(x, y, CW, RH, c, 6, "14", 1.0)
            d.t(x + CW / 2, y + 31, txt, 13, INK, fam(txt), "middle")

d.legend(H - 44, [("진행", OK), ("로그 끝", INFO), ("새로 시작", WARN), ("멈춤·삭제", BAD), ("앱이 옮겨 가는 순간", ACC)])
d.save("05-02.kappa-process.svg")
