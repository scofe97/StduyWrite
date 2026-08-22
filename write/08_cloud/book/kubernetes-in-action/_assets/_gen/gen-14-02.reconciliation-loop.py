# 14-02 §1 — 기억하지 않고 매번 지금만 본다
# 본문이 루프 그림 뒤에 두 사실을 더 붙인다 — 폴링이 아니라 watch + resync 이중이고,
# 루프가 무슨 일이 있었는지 기억하지 않는다(level-triggered). 고리만 그리면 그 둘이 빠진다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 640, "KUBERNETES IN ACTION · 14-02",
      "무슨 일이 있었는지는 묻지 않는다",
      "컨트롤러는 원하는 상태와 실제 상태를 견줘 다르면 조정한다. 이 순환이 기억을 갖지 않아서, "
      "알림을 몇 개 놓쳐도 다음 관찰에서 같은 결론에 이른다.",
      "ReplicaSet 컨트롤러 · ReplicaSet 과 Pod 를 본다")

ddx.band(d, 100, 452, "reconciliation control loop", x=24, w=680)
STEP = [("관찰한다", "ReplicaSet · Pod", 200, 200),
        ("비교한다", "원하는 수 ↔ 실제 수", 520, 276),
        ("조정한다", "만들거나 지운다", 200, 352)]
for t, s, cx, cy in STEP:
    ddx.node(d, cx, cy, t, s, 250, 80, INFO)
d.path("M 326 216 L 360 216 L 360 250 L 396 250", INFO, 1.5, m="info")
d.path("M 456 316 L 456 344 L 326 344", INFO, 1.5, m="info")
# 되돌아가는 선은 박스 바깥으로 돌린다 — 조정 박스가 x 75~325 라 그 안을 지나면 관통한다
d.path("M 71 352 L 52 352 L 52 200 L 71 200", INFO, 1.5, m="info")
d.t(364, 414, "같으면 아무것도 하지 않는다", 11, SOFT, KR)

ddx.band(d, 100, 452, "그래서 생기는 성질", x=728, w=468)
d.o.append(f'<rect x="768" y="164" width="388" height="96" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(962, 196, "level-triggered", 13, ACC, MONO, "middle", 600)
d.t(962, 220, "사건이 아니라 지금 상태를 본다", 11, MUTED, KR)
d.t(962, 242, "알림을 놓쳐도 결론이 같다", 11, ACC, KR)
for i, (t, s) in enumerate((("watch", "변화 알림을 받아 즉시 반응 — 폴링이 아니다"),
                            ("resync", "주기적으로 전체를 다시 훑어 놓친 것을 쓸어 담는다"))):
    d.box(768, 276 + i * 76, 388, 64, PAPER2, RULE, 1.1, 6)
    d.t(788, 302 + i * 76, t, 12, INK, MONO, "start", 600)
    d.t(788, 322 + i * 76, ddx.fit(s, 10, 352, s), 10, MUTED, KR, "start")
d.t(962, 434, "즉시성은 watch, 최종 정합성은 resync", 11, SOFT, KR)

d.t(24, 504, "파드를 지우자마자 대체 파드가 뜨는 것이 폴링이 아니라는 근거다. 폴링이었다면 최대 주기만큼 지연이 보여야 한다.",
     11, MUTED, KR, "start")
d.t(24, 526, "이벤트를 순서대로 재생해야 맞아떨어지는 설계였다면 놓친 알림 하나가 영구적인 어긋남이 됐을 것이다.",
     11, MUTED, KR, "start")
d.legend(556, [("루프의 세 걸음", INFO), ("기억을 갖지 않는다", ACC)])
d.save("14-02-reconciliation-loop.svg")
print("ok")
