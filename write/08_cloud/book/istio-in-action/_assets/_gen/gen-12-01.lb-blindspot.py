# 12-01 §8 클러스터 경계를 넘는 순간 분산이 균등하지 않아진다 — 원문 12.3.7 의 NOTE.
# 본문(원문 12.3.7 NOTE): 교차 클러스터 트래픽은 상대 클러스터의 동서 게이트웨이를 지나며 SNI 패스스루로
#       다뤄진다. 이 호출은 SNI/TCP 연결이고 게이트웨이가 TLS 연결을 종료하지 않으므로, 게이트웨이는 연결을
#       있는 그대로 백엔드 서비스로 넘기는 것밖에 할 수 없다. 이것은 동서 게이트웨이에서 백엔드 서비스로
#       연결 하나를 여는 것이고 요청 수준 로드밸런싱 능력이 없다. 그래서 페일오버나 클러스터 간 분산에서
#       부하는 클라이언트 관점에서만 나뉘고 원격 클러스터의 모든 인스턴스에 고르게 나뉜다고 보장되지 않는다.
# 타입 스펙: type-swimlane — 같은 요청을 두 구간이 나눠 맡고 각 구간의 분산 단위가 다른 것이 논점이다.
#           레인마다 왼쪽 여백에 mono eyebrow, 레인 구분선 1px, accent 는 보장이 끊기는 칸 하나에.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1240, 540
d = D(W, H, "ISTIO IN ACTION · 12-01 §8",
      "클라이언트까지는 요청 단위, 그 뒤는 연결 단위",
      "클라이언트 쪽 프록시는 요청마다 목적지를 고르지만, 동서 게이트웨이는 TLS 를 풀지 않아 연결을 그대로 "
      "넘길 뿐이다. 색이 붙은 칸에서 요청 단위 분산이 끊기고 그 뒤는 보장되지 않는다.",
      "저자가 추가 설정 없이 그대로 작동한다고 적은 주장이 여기서 한 번 물러섭니다")

LANE_H, LANE_Y0 = 108, 108
lanes = [("CLIENT SIDE", "요청 단위로 고른다"),
         ("REMOTE SIDE", "연결 단위로 넘긴다")]
for k, (name, sub) in enumerate(lanes):
    top = LANE_Y0 + k * LANE_H
    d.line(0, top, W, top, RULE, 0.8)
    d.t(20, top + 48, name, 9, SOFT, MONO, "start", 600)
    d.t(20, top + 66, sub, 11, MUTED, KR, "start")
d.line(0, LANE_Y0 + 2 * LANE_H, W, LANE_Y0 + 2 * LANE_H, RULE, 0.8)
d.line(200, LANE_Y0, 200, LANE_Y0 + 2 * LANE_H, RULE, 1.0)

SW, SH = 216, 64
def sx(j): return 244 + j * 248
def sy(k): return LANE_Y0 + k * LANE_H + 22
def cell(k, j, label, sub, focal=False):
    x, y = sx(j), sy(k)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, SW, SH, PAPER2, RULE, 1.0, 6)
    d.t(x + SW / 2, y + 26, label, 12, ACC if focal else INK, KR, "middle", 600)
    d.t(x + SW / 2, y + 46, sub, 9, MUTED, KR, "middle")

for j in range(3):
    c = ACC if j == 2 else MUTED
    m = "acc" if j == 2 else "ar"
    d.arrow([(sx(j) + SW, sy(0) + SH / 2), (sx(j + 1) - 2, sy(0) + SH / 2)], c, m, 1.5 if j == 2 else 1.4)
for j in range(1, 3):
    d.arrow([(sx(j) + SW, sy(1) + SH / 2), (sx(j + 1) - 2, sy(1) + SH / 2)], MUTED, "ar", 1.4)

cell(0, 0, "webapp", "요청을 낸다")
cell(0, 1, "사이드카", "우선순위로 고른다")
cell(0, 2, "원격 게이트웨이", "TLS 를 풀지 않는다")
cell(0, 3, "여기서 끊긴다", "요청 단위 판단의 끝", focal=True)
cell(1, 1, "SNI 로 목적지 확인", "연결 하나를 연다")
cell(1, 2, "백엔드 서비스", "그 연결이 붙은 곳")
cell(1, 3, "나머지 인스턴스", "고르게 간다는 보장 없음")

d.t(32, 400, "클라이언트가 보기에는 페일오버도 분산도 제대로 일어난다 — 갈리는 것은 원격 클러스터 안이다", 11, SOFT, KR, "start")
d.t(32, 424, "인가 정책은 이 예외에 걸리지 않는다 — 상호 인증이 유지되므로 신원으로 거르는 일은 그대로 작동한다", 11, MUTED, KR, "start")
d.legend(452, [("요청 단위 판단이 끝나는 칸", ACC), ("그 뒤의 연결 단위 구간", MUTED)])
d.save("12-01.lb-blindspot.svg")
