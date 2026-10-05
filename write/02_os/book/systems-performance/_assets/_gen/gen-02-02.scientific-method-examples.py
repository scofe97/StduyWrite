# 02-02 §2 — 과학적 방법 다섯 단계를 원서 예시 셋에 채운 표.
# 타입 스펙: type-process — Stage framework with semantic slots. 단계 다섯이 칸으로 반복되고 행마다 예시 하나.
#           축약: 주체(lane)가 없는 대조라 lanes·§2 공식 대신 카드 stride 로 놓는다(selection §알려진 공백).
#           원서 2.5.6(p.28–29)의 Example 셋. 칸의 말은 원서 문장을 줄인 것이다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, OK, BAD, PAPER2, RULE, KR, MONO

W, H = 928, 500
LX, X0, CW, GAP = 24, 136, 148, 6
Y0, RH, RG = 120, 84, 12
STAGES = ["질문", "가설", "예측", "검증", "분석"]
ROWS = [
    ("관측", "가설 기각", BAD, [("느린 DB 쿼리의", "원인은?"), ("이웃 테넌트의", "디스크 I/O 경합"),
                              ("FS 지연이 쿼리", "지연을 설명"), ("쿼리 중 FS 대기", "5% 미만"), ("FS·디스크 배제", "→ 새 가설로")]),
    ("실험", "가설 일치", OK, [("A→C 가 B→C 보다", "느린 이유는?"), ("A·B 가 다른", "데이터센터"),
                              ("A 를 옮기면", "해결"), ("A 이전 후", "측정"), ("해결 —", "가설과 일치")]),
    ("부정 검증", "가설 일치", OK, [("캐시가 클수록", "FS 가 느린 이유?"), ("레코드가 많으면", "관리 연산 증가"),
                                 ("레코드를 줄이면", "점점 악화"), ("레코드 크기를", "단계별 축소"), ("예측과 일치", "→ 드릴다운")]),
]

d = DK(W, H, "SYSTEMS PERFORMANCE · 02-02 §2",
       "같은 다섯 칸, 갈리는 결론",
       "원서 2.5.6 의 예시 셋을 질문·가설·예측·검증·분석 칸에 채웠다. 마지막 칸의 색이 가설의 운명이다.",
       "원서 2.5.6 의 Example 셋")

for j, st in enumerate(STAGES):
    x = X0 + j * (CW + GAP)
    d.box(x, Y0, CW, 32, PAPER2, RULE, 1.0, 4)
    d.t(x + CW / 2, Y0 + 21, f"{j + 1} {st}", 13, INK, KR, "middle", 600)

for i, (kind, verdict, vc, cells) in enumerate(ROWS):
    y = Y0 + 44 + i * (RH + RG)
    focal = kind == "부정 검증"
    d.t(LX, y + 36, kind, 13, ACC if focal else INK, KR, "start", 600)
    d.t(LX, y + 56, verdict, 12, vc, KR, "start")
    for j, (a, b) in enumerate(cells):
        x = X0 + j * (CW + GAP)
        if j == 4: d.tone(x, y, CW, RH, vc, 6)
        elif focal and j == 3: d.tone(x, y, CW, RH, ACC, 6)
        else: d.box(x, y, CW, RH, PAPER2, RULE, 1.0, 6)
        d.t(x + CW / 2, y + 36, a, 13, INK, KR, "middle")
        d.t(x + CW / 2, y + 56, b, 13, INK, KR, "middle")

yl = Y0 + 44 + 3 * (RH + RG) + 8
d.legend(yl, [("가설 기각", BAD), ("가설 일치", OK), ("일부러 성능을 해치는 검증", ACC)])
d.save("02-02.scientific-method-examples.svg")
