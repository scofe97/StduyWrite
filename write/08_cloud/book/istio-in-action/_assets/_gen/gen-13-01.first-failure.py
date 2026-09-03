# 13-01 §8 클러스터에서 VM 서비스를 처음 부를 때 운영자가 지나는 다섯 마디 — 원문 13.3.5.
# 본문(원문 13.3.5): 라벨 셀렉터로 워크로드 엔트리를 고르는 쿠버네티스 서비스를 만들고 요청을 걸면
#       HTTP/1.1 500 이 돌아온다. 저자는 "요청이 실패했다. 우리가 뭔가 잘못했다는 뜻인가? 원인을 찾기
#       전에는 알 수 없다" 고 적고, 이 훈련의 목적이 계획대로 되지 않았을 때를 위한 연습이라고 밝힌다.
#       추적은 오류를 돌려준 webapp 의 액세스 로그에서 시작한다 — UH 는 "No healthy upstream" 이고
#       클러스터에 건강한 엔드포인트가 하나도 없을 때만 나온다. istioctl proxy-config endpoints 로
#       확인하면 비어 있고, WorkloadEntry 의 status.conditions 가 Healthy False 에 connection refused 다.
#       원인은 VM 에서 애플리케이션을 아직 시작하지 않은 것이고, 그 단서는 13.2.2 의 nmap 출력이 이미
#       포트 8080 을 closed 로 보여 준 데 있었다. 앱을 켜면 몇 초 뒤 True 로 바뀌고 200 이 온다.
# 타입 스펙: type-journey — 한 사람이 여러 마디를 지나며 그때마다 어떻게 느끼는지가 논점이고,
#           감정 곡선이 이 타입을 지탱한다. 마디 5(최대 6) · 내용 행 3 · 통증 표시는 골짜기에만 최대 2.
#           감정 곡선은 데이터 곡선이라 직각 엘보 규칙의 예외다(스펙이 명시한 면제).
#           축약: 스펙은 범례에 곡선 · 골짜기 · 통증 태그 셋을 요구하지만, 프리미티브의 범례
#           스와치가 실선 사각형 하나뿐이라 점선 태그를 색으로만 구분하면 골짜기 키와 겹친다.
#           통증 태그는 골짜기 칸 안에만 나타나므로 골짜기 키가 그것을 함께 가리키게 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

COL_W, GUT, X0 = 200, 24, 76
W, H = 1208, 632
d = D(W, H, "ISTIO IN ACTION · 13-01 §8",
      "저자는 500 을 고치지 않고 훈련으로 남겼다",
      "메시 운영자가 클러스터에서 VM 서비스를 처음 부를 때 지나는 다섯 마디. 색이 붙은 자리가 골짜기이고, "
      "그 아래 두 표시가 그때 운영자가 실제로 겪는 것이다.",
      "단서는 이미 앞 절의 nmap 출력에 closed 로 찍혀 있었습니다")

def cx(i): return X0 + i * (COL_W + GUT) + COL_W / 2
def colx(i): return X0 + i * (COL_W + GUT)
PLOT_R = colx(4) + COL_W

stages = [
    ("서비스를 만든다", 2, ["라벨로 forum 을 고르는", "서비스를 적용한다"],
     "kubectl apply", "80 -> 8080"),
    ("첫 요청", 4, ["/api/users 를 부르면", "500 이 돌아온다"],
     "curl -is | grep HTTP", "HTTP/1.1 500"),
    ("로그를 본다", 3, ["액세스 로그에 UH", "엔드포인트가 비었다"],
     "kubectl logs · proxy-config", "UH · <empty>"),
    ("상태를 편다", 1, ["조건이 Healthy False", "연결이 거부됐다"],
     "kubectl get workloadentry", "connection refused"),
    ("앱을 켠다", 0, ["앱을 켜자 엔드포인트가", "생기고 200 이 온다"],
     "./forum", "HTTP/1.1 200"),
]
TROUGH = 1
LEVEL_Y = [160, 196, 232, 268, 304]

for i, (name, _, _, _, _) in enumerate(stages):
    d.t(cx(i), 112, f"STAGE {i + 1}", 8, SOFT, MONO, "middle", 600)
    d.t(cx(i), 134, name, 12, ACC if i == TROUGH else INK, KR, "middle", 600)

for lab, y in (("HIGH", 160), ("NEUTRAL", 232), ("LOW", 304)):
    d.line(X0, y, PLOT_R, y, INK, 0.8)
    d.o[-1] = d.o[-1].replace('stroke-width="0.8"', 'stroke-width="0.8" opacity="0.10"')
    d.t(X0 - 12, y + 3, lab, 8, MUTED, MONO, "end")

pts = [(cx(i), LEVEL_Y[s[1]]) for i, s in enumerate(stages)]
for i in range(len(pts) - 1):
    (x1, y1), (x2, y2) = pts[i], pts[i + 1]
    mx = (x1 + x2) / 2
    focal = (i + 1 == TROUGH)
    d.path(f"M {x1} {y1} C {mx} {y1} {mx} {y2} {x2} {y2}",
           ACC if focal else MUTED, 1.5)
for i, (x, y) in enumerate(pts):
    c = ACC if i == TROUGH else MUTED
    d.o.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{c}"/>')

ROWS = [(324, 444, "ACTIONS"), (444, 492, "TOUCHPOINTS"), (492, 540, "SIGNAL")]
for top, bot, lab in ROWS:
    d.line(X0, top, PLOT_R, top, RULE, 0.8)
    d.t(X0 - 12, top + 26, lab, 8, SOFT, MONO, "end", 600)
d.line(X0, 540, PLOT_R, 540, RULE, 0.8)

for i, (name, lvl, actions, touch, signal) in enumerate(stages):
    for j, ln in enumerate(actions):
        d.t(cx(i), 350 + j * 20, ln, 12, ACC if i == TROUGH else INK, KR, "middle",
            600 if i == TROUGH else 400)
    d.t(cx(i), 472, touch, 9, MUTED, MONO)
    d.t(cx(i), 520, signal, 9, MUTED, MONO)

pains = ["무엇을 볼지 모른다", "단서를 이미 지나쳤다"]
for j, p in enumerate(pains):
    py = 396 + j * 24
    pw = len(p) * 9.4 + 16
    d.o.append(f'<rect x="{cx(TROUGH) - pw / 2:.2f}" y="{py}" width="{pw:.2f}" height="18" rx="2" '
               f'fill="{ACC}0A" stroke="{ACC}80" stroke-width="1" stroke-dasharray="3 3"/>')
    d.t(cx(TROUGH), py + 13, p, 11, ACC, KR, "middle")

d.t(24, 566, "저자가 이 실패에서 뽑아 내는 것은 고치는 방법이 아니라 Istio 가 준비되지 않은 워크로드를 다루는 방식이다", 11, SOFT, KR, "start")
d.legend(584, [("골짜기 — 원인을 모른 채 실패한 자리", ACC), ("운영자가 느끼는 흐름", MUTED)])
d.save("13-01.first-failure.svg")
