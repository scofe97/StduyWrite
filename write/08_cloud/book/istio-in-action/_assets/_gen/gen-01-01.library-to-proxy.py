# 01-01 §4 같은 기능이 어디에 사는지가 바뀐다.
# 본문: 해법은 이 관심사들을 인프라로 내리는 것이고, 그러려면 커넥션과 패킷이 아니라 메시지와 요청을
#       이해하는 L7 프록시가 필요하다. Envoy 가 그 자리를 채우며 언어나 프레임워크 의존성 없이 구현한다.
# 왼쪽 레인이 비고 오른쪽 레인이 차는 것이 이 절의 내용이다 — 언어 제약이 사라지는 자리가 accent.
# 타입 스펙: type-swimlane — 같은 일을 두 주체가 나눠 맡고 그 경계가 옮겨 가는 것이 논점이다.
#           레인마다 왼쪽 여백에 mono eyebrow, 레인 구분선 1px, accent 는 옮겨 가서 얻는 것 하나에.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1000, 500
d = D(W, H, "ISTIO IN ACTION · 01-01 §4",
      "같은 기능이 프로세스 밖으로 나간다",
      "재시도·타임아웃·서킷 브레이킹·디스커버리는 그대로 필요하다. 달라지는 것은 그것이 어디 사는가다. "
      "색이 붙은 칸이 옮겨서 얻는 것이고, 그것이 이 장이 라이브러리 방식의 결정적 한계로 지목한 자리다.",
      "전통적 프록시는 커넥션과 패킷을, Envoy 는 메시지와 요청을 이해합니다")

LANE_H, LANE_Y0 = 116, 104
lanes = [("APPLICATION", "우리 프로세스 안"),
         ("SIDECAR PROXY", "프로세스 밖 · Envoy")]
for k, (name, sub) in enumerate(lanes):
    top = LANE_Y0 + k * LANE_H
    d.line(0, top, W, top, RULE, 0.8)
    d.t(20, top + 50, name, 9, SOFT, MONO, "start", 600)
    d.t(20, top + 68, sub, 11, MUTED, KR, "start")
d.line(0, LANE_Y0 + 2 * LANE_H, W, LANE_Y0 + 2 * LANE_H, RULE, 0.8)
d.line(168, LANE_Y0, 168, LANE_Y0 + 2 * LANE_H, RULE, 1.0)

BW, BH = 180, 60
def cell(k, j, label, sub, faint=False, focal=False):
    x = 188 + j * 196; y = LANE_Y0 + k * LANE_H + 28
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif faint:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" fill="{INK}04" '
                   f'stroke="{MUTED}" stroke-width="1" stroke-dasharray="5 5"/>')
    else:
        d.box(x, y, BW, BH, PAPER2, RULE, 1.0, 6)
    d.t(x + BW / 2, y + 26, label, 12, ACC if focal else (SOFT if faint else INK), KR, "middle", 600)
    d.t(x + BW / 2, y + 44, sub, 9, MUTED, MONO)

for j, (lab, sub) in enumerate([("레질리언스", "retry · timeout"),
                                ("로드밸런싱", "client-side LB"),
                                ("디스커버리", "registry"),
                                ("메트릭 수집", "rps · failures")]):
    cell(0, j, lab, sub, faint=True)
    cell(1, j, lab, sub)

# 옮겨 가는 방향
for j in range(4):
    x = 232 + j * 244 + BW / 2
    d.arrow([(x, LANE_Y0 + 28 + BH), (x, LANE_Y0 + LANE_H + 26)], MUTED, "ar", 1.3)

d.t(32, 372, "옮겨서 얻는 것 — 언어와 프레임워크 의존성이 사라지고, 처리가 전부 애플리케이션 프로세스 밖에서 일어난다", 11, ACC, KR, "start", 600)
d.t(32, 400, "덤으로 얻는 것 — 초당 요청 수 · 실패 건수 · 서킷 브레이킹 발생이 자동으로 관측된다", 11, SOFT, KR, "start")
d.t(32, 424, "배포 형태는 사이드카다 — 애플리케이션은 먼저 Envoy 에 요청을 넘기고 그다음은 Envoy 가 처리한다", 11, MUTED, KR, "start")
d.legend(452, [("옮겨서 얻는 것", ACC), ("비워지는 자리", MUTED)])
d.save("01-01.library-to-proxy.svg")
