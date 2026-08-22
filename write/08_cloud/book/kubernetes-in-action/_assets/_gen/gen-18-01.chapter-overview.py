# 18-01 전체 지도 — 끝나야 완료되는 워크로드
# 본문이 층 구조를 지정한다 — "위층은 Job 상태가 생성에서 완료까지 가로로, 가운데는 그 아래에서
# 실제로 도는 파드, 아래층은 끝난 뒤의 정리". 그 세 층을 그대로 세운다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 700, "KUBERNETES IN ACTION · 18-01",
      "끝나야 완료되는 워크로드",
      "Deployment 는 계속 도는 것이 정상이지만 Job 은 끝나야 정상이다. 그래서 상태·제어·정리가 "
      "모두 '언제 끝나는가'를 축으로 놓인다.",
      "§1 전제 · §2 작성 · §3·§4 관찰 · §5 제어 · §6·§7 정리")

ddx.band(d, 100, 268, "Job 오브젝트의 상태 — 생성에서 완료까지", x=24, w=1192)
ST = [("생성", "§2 매니페스트"), ("실행 중", "§3·§4 관찰"),
      ("일시 정지", "§5 suspend"), ("완료", "성공 횟수를 채웠다")]
BW, GP = 240, 48
X0 = (1240 - (4 * BW + 3 * GP)) // 2
CX = [X0 + BW // 2 + i * (BW + GP) for i in range(4)]
for cx, (t, s) in zip(CX, ST):
    d.box(cx - BW // 2, 168, BW, 72, PAPER2, INFO, 1.1, 6)
    d.t(cx, 196, t, 13, INFO, KR, "middle", 600)
    d.t(cx, 220, s, 10, MUTED, KR)
for a, b in zip(CX, CX[1:]):
    d.path(f"M {a+BW//2+5} 204 L {b-BW//2-9} 204", MUTED, 1.4, m="ar")

ddx.band(d, 292, 436, "그 아래에서 실제로 도는 파드", x=24, w=1192)
d.t(620, 320, "Job 이 만들고, 끝나면 남는다", 11, SOFT, KR)
for i, cx in enumerate(CX):
    if i == 2:
        ddx.tag(d, cx, 380, "새로 만들지 않는다", WARN, 220)
    elif i == 3:
        ddx.tag(d, cx, 380, "Completed 로 남는다", ACC, 220)
    else:
        ddx.tag(d, cx, 380, "파드가 돈다", OK, 220)
    d.line(cx, 244, cx, 356, RULE, 0.8, "3 5")

ddx.band(d, 460, 596, "끝난 뒤의 정리", x=24, w=1192, focal=True)
for i, (t, s) in enumerate((("§6 직접 지운다", "가비지 컬렉터가 파드까지"),
                            ("cascade orphan", "파드를 독립시킨다"),
                            ("§7 TTL 컨트롤러", "완료 후 자동으로"))):
    cx = 320 + i * 300
    d.box(cx - 140, 500, 280, 72, PAPER2, ACC, 1.1, 6)
    d.t(cx, 528, t, 12, ACC, KR, "middle", 600)
    d.t(cx, 552, s, 10, MUTED, KR)

d.t(24, 612, "정리를 안 하면 완료된 파드가 쌓인다. 컨트롤 플레인이 결국 회수하지만 그 사이에 쌓인 파드가 "
             "클러스터 성능을 떨어뜨릴 수 있다.", 11, MUTED, KR, "start")
# WARN 은 일시 정지 칸("새로 만들지 않는다")에만 쓰이는데 범례에 없어 해독할 수 없었다.
d.legend(644, [("Job 상태", INFO), ("도는 파드", OK), ("멈춘 동안", WARN), ("정리", ACC)])
d.save("18-01.chapter-overview.svg")
print("ok")
