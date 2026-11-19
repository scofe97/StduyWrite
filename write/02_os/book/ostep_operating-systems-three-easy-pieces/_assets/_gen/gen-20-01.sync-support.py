# 20-01 「원자성을 얻는 길」 — 모든 갱신을 한 명령으로 만들 수는 없으므로 하드웨어의 소수 명령과 운영체제 지원으로 동기화 기본 요소를 만든다.
# 본문 근거: 이 노트 「5. 임계 구역과 동기화 지원」.
# 값 근거: 개념 도식이라 값은 없다.
# 공식 근거: OSTEP 26장 §26.5 — memory-add 같은 원자 명령이 있으면 끝나지만 일반적으로는 없다(동시 B-tree 의 원자 갱신 명령은 비현실적). 대신 하드웨어의 유용한 명령 몇 개와 운영체제 도움으로 동기화 기본 요소를 만든다. §26.6 — 다른 스레드를 기다리는 일이 둘째 문제다.
# 타입 스펙: type-flowchart — 위에서 아래로 흐르는 결정 분기. 마름모 하나(원자 명령으로 되는가)에서 예·아니오로 갈라지고, 아니오 쪽이 책의 CRUX 로 이어진다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, PAPER2, ACC, OK, WARN, INFO, KR, MONO

W, H = 920, 680
d = D(W, H, "FLOWCHART · 20-01 §5",
      "원자 명령이 있으면 끝나지만 일반적으로는 없어서 동기화 기본 요소를 만든다",
      "임계 구역을 한 번에 실행하려 할 때 그 갱신을 하나의 원자 명령으로 만들 수 있으면 인터럽트가 끼어들 틈이 없어 끝난다. "
      "그러나 일반적으로는 그런 명령이 없으므로 하드웨어에서 유용한 명령 몇 개를 받고 운영체제 도움을 더해 동기화 기본 요소를 만들며, "
      "이것이 상호 배제를 얻는 길이다. 다른 스레드를 기다리는 문제는 조건 변수가 따로 맡는다.",
      lead="핵심 질문은 아래 갈림길의 오른쪽 길 하나입니다.")


def pill(cx, y, w, h, t1, t2, c):
    d.tone(cx - w / 2, y, w, h, c, 6, "18", 1.3 if c == ACC else 1.1)
    d.t(cx, y + (24 if t2 else h / 2 + 5), t1, 14, c, KR if any("가" <= ch <= "힣" for ch in t1) else MONO, "middle", 600)
    if t2:
        d.t(cx, y + 44, t2, 12, MUTED, KR, "middle")


CX = 460
pill(CX, 100, 400, 56, "임계 구역을 원자적으로 실행하고 싶다", None, INFO)
d.arrow([(CX, 156), (CX, 188)], SOFT, "soft", 1.3)

# 마름모
dy = 192
pts = f"{CX},{dy} {CX + 180},{dy + 56} {CX},{dy + 112} {CX - 180},{dy + 56}"
d.o.append(f'<polygon points="{pts}" fill="{WARN}18" stroke="{WARN}" stroke-width="1.3"/>')
d.t(CX, dy + 52, "갱신을 명령 하나로", 14, WARN, KR, "middle", 600)
d.t(CX, dy + 72, "만들 수 있는가", 14, WARN, KR, "middle", 600)

# 예(왼쪽)
d.arrow([(CX - 180, dy + 56), (200, dy + 56), (200, 340)], OK, "ok", 1.3)
d.t(CX - 188, dy + 44, "예", 13, OK, KR, "end", 600)
pill(200, 344, 340, 72, "memory-add 같은 원자 명령", "중간 상태가 보이지 않아 끝", OK)
d.t(200, 452, "일반적으로는 이런 명령이 없음", 12, MUTED, KR, "middle")

# 아니오(오른쪽)
d.arrow([(CX + 180, dy + 56), (680, dy + 56), (680, 340)], ACC, "acc", 1.3)
d.t(CX + 188, dy + 44, "아니오", 13, ACC, KR, "start", 600)
pill(680, 344, 340, 72, "하드웨어의 유용한 명령 몇 개", "동시 B-tree 갱신 명령까진 비현실적", ACC)
d.arrow([(680, 416), (680, 448)], SOFT, "soft", 1.3)
pill(680, 452, 340, 72, "운영체제의 도움을 더함", "둘로 동기화 기본 요소를 만듦", INFO)
d.arrow([(680, 524), (680, 556)], SOFT, "soft", 1.3)
pill(680, 560, 340, 48, "임계 구역에 상호 배제", None, OK)

d.t(200, 560, "다른 스레드를 기다리는 문제는", 13, MUTED, KR, "middle")
d.t(200, 580, "조건 변수가 따로 맡음", 13, MUTED, KR, "middle", 600)

d.legend(H - 40, [("시작·동작", INFO), ("결과", OK), ("갈림길", WARN), ("핵심 질문", ACC)])
d.save("20-01.sync-support.svg")
print("ok 20-01 sync-support")
