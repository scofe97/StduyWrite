# 16-02 §5 — 되돌린 처방이 정작 고쳐야 할 파드에 닿지 못한다
# 본문이 도식을 직접 가리켜 설명한다 — "3번 상자로 돌아오는 붉은 화살표가 교착 고리",
# "점선으로 표시한 4번이 사람이 개입하는 지점", "그 개입 뒤에야 5번". 번호와 표시를 그대로 지킨다.
# 타입 스펙: type-dependency.md — 3번 상자로 되돌아오는 붉은 화살표가 교착 고리다. type-dependency 정본이
#           말하는 (b) 순환이 바로 이것이고, 순환이 있으면 트리로도 사슬로도 그릴 수 없다.
#           점선으로 표시한 4번(사람의 수동 삭제)이 그 고리를 밖에서 끊는 유일한 손이라,
#           고리와 그 탈출구가 함께 있어야 이 그림이 성립한다.
#           2026-08-29 정정: data-flow 로 적고 '한 줄로 이어지는 인과 파이프라인'이라 썼었다.
#           바로 윗줄 주석이 '교착 고리'라고 적어 둔 것을 읽지 않고 렌더 인상만으로 판단한 결과다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 620, "KUBERNETES IN ACTION · 16-02",
      "고치려고 만든 처방이 그 파드에 닿지 못한다",
      "컨트롤러가 깨진 파드의 Ready 를 계속 기다리느라, 되돌린 템플릿을 적용하는 일 자체를 시작하지 못한다. "
      "공식 문서가 이것을 정책의 설계가 아니라 알려진 이슈로 규정한다.",
      "OrderedReady · readiness probe 가 MongoDB quorum 에 의존")

STEP = [("① 템플릿이 깨져 있다", "readiness 가 MongoDB 에 의존", None),
        ("② quiz-0 이 ready 가 안 된다", "quorum 이 없어 probe 실패", None),
        ("③ 컨트롤러가 기다린다", "첫 파드가 ready 여야 다음을 만든다", BAD),
        ("④ 사람이 수동 삭제한다", "kubectl delete po quiz-0", ACC),
        ("⑤ 새 probe 로 뜬 파드가 ready", "quiz-1 · quiz-2 로 진행", OK)]
BW, GP = 216, 30
X0 = (1240 - (5 * BW + 4 * GP)) // 2
CX = [X0 + BW // 2 + i * (BW + GP) for i in range(5)]
for cx, (t, s, c) in zip(CX, STEP):
    if c is ACC:
        d.o.append(f'<rect x="{cx-BW//2}" y="230" width="{BW}" height="96" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4" stroke-dasharray="7 5"/>'); tc = ACC
    elif c:
        d.box(cx - BW // 2, 230, BW, 96, PAPER2, c, 1.2, 6); tc = c
    else:
        d.box(cx - BW // 2, 230, BW, 96, PAPER2, RULE, 1.1, 6); tc = INK
    d.t(cx, 264, ddx.fit(t, 12, BW - 16, t), 12, tc, KR, "middle", 600)
    d.t(cx, 292, ddx.fit(s, 10, BW - 14, s), 10, MUTED, KR)
for i in range(4):
    a, b = CX[i] + BW // 2, CX[i + 1] - BW // 2
    dash = "5 5" if i == 2 else None
    d.path(f"M {a+5} 278 L {b-9} 278", ACC if i == 2 else MUTED, 1.4,
           m="acc" if i == 2 else "ar", dash=dash)

# 3번 상자로 돌아오는 붉은 고리
d.path(f"M {CX[2]+40} 330 L {CX[2]+40} 384 L {CX[2]-40} 384 L {CX[2]-40} 330", BAD, 1.5, m="bad")
d.t(CX[2], 406, "템플릿을 되돌려도 적용을 시작하지 못한다", 11, BAD, KR)
d.t(CX[3], 358, "여기서만 빠져나온다", 10, ACC, KR)

d.t(24, 470, "컨트롤러는 이 자리에서 스스로 빠져나오지 못한다. 되돌린 템플릿은 다음 파드를 만들 차례가 와야 "
             "적용되는데, 그 차례가 영영 오지 않기 때문이다.", 11, MUTED, KR, "start")
d.t(24, 492, "minReadySeconds 는 Deployment 와 같은 역할이되 업데이트뿐 아니라 스케일에도 적용된다 — "
             "그래서 이 교착이 스케일 과정에서도 생긴다.", 11, MUTED, KR, "start")
d.legend(524, [("교착 고리", BAD), ("사람이 개입하는 지점", ACC), ("풀린 뒤", OK)])
d.save("16-02-forced-rollback.svg")
print("ok")
