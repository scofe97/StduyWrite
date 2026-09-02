# 11-01 §4 지연 메트릭 셋이 덮는 구간 — 원문 그림 11.4.
# 본문(원문 11.2.1): (1) pilot_proxy_convergence_time 은 프록시 푸시 요청이 큐에 들어온 때부터 워크로드에
#       배포될 때까지 전 과정을 잰다 (2) pilot_proxy_queue_time 은 푸시 요청이 워커에게 처리될 때까지
#       큐에서 기다린 시간을 잰다 (3) pilot_xds_push_time 은 Envoy 설정을 워크로드로 푸시하는 데 걸린
#       시간을 잰다. 그리고 11.3.4 — 지연 지표는 디바운스 구간을 세지 않는다.
# 타입 스펙: type-gantt — 막대 길이가 곧 구간이고 겹침과 포함이 논점이다. 왼쪽 라벨 열 + 축, 초점 막대 하나.
#           축약: 저자가 구간별 소요 시간을 적지 않아 가로축을 수치 눈금이 아니라 국면 경계로 둔다.
#           막대 길이는 순서 관계만 나타내며 측정값이 아니다. 의존 화살표는 v1 관례대로 그리지 않는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1200, 560
d = D(W, H, "ISTIO IN ACTION · 11-01 §4",
      "지연 하나를 세 구간으로 나눠 잰다",
      "가로축은 국면 경계이고 막대 길이는 순서만 나타낸다. 색이 붙은 막대가 전체를 재는 지표이고, "
      "왼쪽 점선 막대는 어떤 지표도 세지 않는 구간이다.",
      "저자가 구간별 시간을 적지 않아 눈금 대신 경계만 둡니다")

LX, TX, TW = 24, 300, 800
AXIS_Y, ROWH, TOP = 128, 44, 152
marks = [("이벤트 도착", 0.00), ("큐 진입", 0.28), ("워커 착수", 0.56), ("배포 완료", 1.00)]
def X(t): return TX + t * TW
def row_y(i): return TOP + 12 + i * ROWH

for name, t in marks:
    d.line(X(t), AXIS_Y - 6, X(t), TOP + 12 + 4 * ROWH, RULE, 0.8, "3 5")
    d.t(X(t), AXIS_Y - 12, name, 9, SOFT, KR)
d.line(TX, AXIS_Y, TX + TW, AXIS_Y, RULE, 1.0)

def bar(i, name, sub, t0, t1, c=MUTED, focal=False, dashed=False):
    y = row_y(i)
    d.t(LX, y + 21, name, 11, ACC if focal else (c if dashed else INK), MONO, "start", 600)
    d.t(LX, y + 37, sub, 9, MUTED, KR, "start")
    x0, w = X(t0), X(t1) - X(t0)
    if focal:
        d.o.append(f'<rect x="{x0}" y="{y + 4}" width="{w}" height="24" rx="4" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
    elif dashed:
        d.o.append(f'<rect x="{x0}" y="{y + 4}" width="{w}" height="24" rx="4" fill="{c}0C" stroke="{c}" stroke-width="1" stroke-dasharray="4 3"/>')
    else:
        d.o.append(f'<rect x="{x0}" y="{y + 4}" width="{w}" height="24" rx="4" fill="rgba(139,152,169,0.15)" stroke="{MUTED}" stroke-width="1"/>')

bar(0, "(어떤 지표도 없다)", "디바운스 — 이벤트를 묶는 구간", 0.00, 0.28, BAD, dashed=True)
bar(1, "pilot_proxy_convergence_time", "큐 진입부터 배포까지 전 과정", 0.28, 1.00, focal=True)
bar(2, "pilot_proxy_queue_time", "워커가 집을 때까지 기다린 시간", 0.28, 0.56)
bar(3, "pilot_xds_push_time", "설정을 워크로드로 푸시한 시간", 0.56, 1.00)

d.t(32, 392, "큐 대기가 길면 istiod 를 수직으로 키워 동시 처리 능력을 늘린다", 11, SOFT, KR, "start")
d.t(32, 416, "푸시 시간이 길면 대역폭이 눌린 것이다 — Sidecar 로 설정 크기를 줄이는 쪽이 먼저다", 11, MUTED, KR, "start")
d.t(32, 440, "저자가 든 경보 기준 — 10초 넘게 1초를 초과하면 경고, 2초를 초과하면 심각", 11, SOFT, KR, "start")
d.legend(468, [("전체를 재는 지표", ACC), ("구간을 나눠 재는 지표", MUTED), ("아무도 세지 않는 구간", BAD)])
d.save("11-01.latency-spans.svg")
