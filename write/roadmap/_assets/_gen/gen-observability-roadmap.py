# write/roadmap/observability-roadmap.md §학습 순서 — 관측 가능성 학습 로드맵.
#
# 자료 규칙이 다른 편과 다르다 — 정독 노트 50편과 소장 책 여섯 권, 그리고 공식 문서만 쓴다.
#   06_observability 의 자체 노트(01_Foundations·02_LGTMStack·03_Project·05_SpringActuator)는
#   프로젝트 기록이라 순서를 정하는 근거로 삼지 않는다. book/ 아래 정독 노트만 건다.
# 절단선은 4단계 뒤에 긋는다 — 1~4 가 신호를 만들고 읽는 일, 5 부터가 운영으로 잇는 일이다.
#
# 판형은 roadmap.sh 계열이다 — 세로 척추에 단계를 걸고 개념을 좌우로 뻗되,
#   노드마다 우선순위 점을 찍는다. 단계에만 배지를 달던 앞 판은 한 단계 안에서
#   무엇이 뼈대이고 무엇이 곁가지인지 말하지 못했다.
#
# 노드의 주인공은 개념이고 책은 그 개념을 다루는 자리다. 책 줄이 비면 아직 자료가 없다는 뜻이고,
#   소장 목록이 늘면 그 줄만 채운다. 정독 노트 편수는 도식에 적지 않는다 —
#   "어디를 펴야 하는가"에 답하지 않는 정보다. 노트 링크는 본문 단계 표가 맡는다.
#
# 대체(ACC)는 같은 자리를 두 자료가 대신 채우는 경우다. 둘 다 읽으라는 뜻이 아니다.
# 타입 스펙: type-tree — 부모(단계)에서 자식(개념)으로 갈라지는 계층.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

SX = 500
W = 1000
NODE_W, NODE_H = 320, 52
CH_W, CH_H, CH_GAP = 268, 46, 10
BUS, ROW_GAP, PHASE_GAP = 184, 44, 40
NOTE_H = 76
ELBOW = 14

MARK = {"필수": INFO, "추천": OK, "선택": SOFT, "대체": ACC}

# (단계 제목, 단계 부제, [왼쪽], [오른쪽])
#   개념 노드 = (개념, 책 챕터 — 없으면 빈 문자열, 우선순위)
stages = [
    ("1 · 관측 가능성의 자리", "무엇을 모르는지 물을 수 있는가",
     [("모니터링과 관측 가능성의 차이", "Observability Engineering 1장", "필수"),
      ("세 신호 — 지표 · 로그 · 트레이스", "Mastering Prometheus 1장", "필수"),
      ("구조화 이벤트가 기본 단위", "Observability Engineering 5·6장", "필수"),
      ("고카디널리티와 질문 중심 사고", "Observability Engineering 8장", "추천")],
     [("Grafana 스택과 페르소나 · LGTM", "Observability with Grafana 1장", "추천"),
      ("SRE 가 보는 관측과 모니터링", "SRE 2판 8장", "추천"),
      ("관측 가능성의 기원", "Observability Engineering 3장", "선택")]),

    ("2 · 계측", "무엇을 어떤 모양으로 내보내는가",
     [("로그 형식 · 구조화 필드", "Observability with Grafana 2장", "필수"),
      ("메트릭 타입 넷 — counter · gauge", "Prometheus Up and Running 3장", "필수"),
      ("exposition · exporter · 클라이언트", "Prometheus Up and Running 4장", "필수"),
      ("라벨 설계와 카디널리티 한계", "Prometheus Up and Running 5장", "필수")],
     [("OpenTelemetry 로 계측하기", "Observability Engineering 7장", "필수"),
      ("트레이싱 프로토콜 · 컨텍스트 전파", "Distributed Tracing 2·3장", "필수"),
      ("계측 모범 사례", "Distributed Tracing 4장", "추천"),
      ("인프라 계측 표준", "Observability with Grafana 2장", "추천")]),

    ("3 · 지표와 PromQL", "숫자를 저장하고 묻는 법",
     [("Prometheus 데이터 모델", "Mastering Prometheus 3장", "필수"),
      ("TSDB 쓰기 경로와 저장 구조", "Mastering Prometheus 3장", "필수"),
      ("PromQL 기초 · 집계 연산자", "Prometheus Up and Running 13·14장", "필수"),
      ("range query · step · 시간 창", "Prometheus Up and Running 13장", "추천"),
      ("이항 연산자 · 함수 · 레코딩 룰", "Prometheus Up and Running 15~17장", "추천")],
     [("서비스 디스커버리와 relabeling", "Mastering Prometheus 4장", "필수"),
      ("컨테이너와 Kubernetes 지표", "Prometheus Up and Running 9장", "필수"),
      ("Node Exporter 해부와 collector", "Mastering Prometheus 8장", "추천"),
      ("Prometheus 배포와 Operator", "Mastering Prometheus 2장", "추천")]),

    ("4 · 로그와 트레이스", "숫자가 못 말하는 것을 읽는 법",
     [("Loki 와 LogQL · 파이프라인", "Observability with Grafana 4장", "필수"),
      ("라벨과 검색 빈도의 균형", "Observability with Grafana 4장", "필수"),
      ("로그 검색 백엔드 — 색인과 매핑", "OpenSearch 4·5장", "선택"),
      ("로그 분석과 시각화", "OpenSearch 7장", "선택")],
     [("Tempo 와 TraceQL · 구조 연산자", "Observability with Grafana 6장", "필수"),
      ("트레이싱 배포 · 오버헤드 · 샘플링", "Distributed Tracing 5·6장", "필수"),
      ("exemplar 로 지표에서 트레이스로", "Mastering Prometheus 15장", "추천"),
      ("기준 성능 개선과 복구", "Distributed Tracing 8·9장", "추천")]),

    ("5 · 알림과 SLO", "언제 사람을 깨울 것인가",
     [("Alertmanager — 라우팅 · 억제", "Mastering Prometheus 5장", "필수"),
      ("견고한 알림과 룰 단위 테스트", "Mastering Prometheus 5장", "필수"),
      ("알림 피로와 침묵 규칙", "Prometheus Up and Running 18·19장", "추천")],
     [("SLI · SLO · 에러 버짓", "SRE 2판 7장", "필수"),
      ("SLO 를 Prometheus 로 정의하기", "Mastering Prometheus 13장", "필수"),
      ("사고 관리 · 온콜 · 지휘 체계", "SRE 2판 9장", "추천"),
      ("사고에서 배우기 · 포스트모템", "SRE 2판 10장", "추천"),
      ("근거의 출처를 함께 남기기", "", "추천")]),

    ("6 · 확장과 운영", "지표가 한 대에 안 들어갈 때",
     [("샤딩 · 페더레이션 · 고가용성", "Mastering Prometheus 6장", "필수"),
      ("최적화와 디버깅", "Mastering Prometheus 7장", "필수"),
      ("remote write · remote read", "Mastering Prometheus 9장", "추천")],
     [("Thanos 저장 경로와 쿼리 경로", "Mastering Prometheus 10장", "추천"),
      ("VictoriaMetrics · Grafana Mimir", "Mastering Prometheus 9장", "추천"),
      ("Prometheus 와 OpenTelemetry 통합", "Mastering Prometheus 14장", "추천"),
      ("서버 측 보안", "Prometheus Up and Running 20장", "선택")]),

    ("7 · 플랫폼", "한 팀이 아니라 조직이 쓰게 만들기",
     [("대시보드 — 목적과 인지 부하", "Observability with Grafana 8장", "필수"),
      ("Jsonnet 과 모니터링 믹스인", "Mastering Prometheus 11장", "추천"),
      ("CI 로 규칙 검증 — promtool · Pint", "Mastering Prometheus 12장", "추천"),
      ("코드형 인프라 · Helm · Terraform", "Observability with Grafana 10장", "추천")],
     [("플랫폼 데이터 아키텍처 · RBAC", "Observability with Grafana 11장", "추천"),
      ("인프라 관측 — K8s 와 클라우드 3사", "Observability with Grafana 7장", "추천"),
      ("RUM · Faro · Web Vitals", "Observability with Grafana 12장", "선택"),
      ("관측 가능성 주도 개발", "Observability Engineering 9장", "선택"),
      ("AI 에이전트의 자리", "Observability Engineering 10장", "선택")]),
]

CUT_AFTER = 3          # 4단계 뒤에 "신호를 만들고 읽기" ↔ "운영으로 잇기" 절단선
NOTES = {
    3: "1~4단계는 신호를 만들고 읽는 일이고 5단계부터는 그것을 운영 판단으로 잇는 일이다.",
    6: "자체 프로젝트 노트는 순서의 근거로 쓰지 않는다. 정독 노트 50편과 소장 책 여섯, 공식 문서만 건다.",
}


def row_h(left, right):
    n = max(len(left), len(right))
    return max(NODE_H, n * CH_H + (n - 1) * CH_GAP) + 28


ROOT_Y = 116 + 190
y = ROOT_Y + 52 + PHASE_GAP
for i, (_t, _s, left, right) in enumerate(stages):
    y += row_h(left, right) + ROW_GAP
    if i in NOTES:
        y += NOTE_H
    if i == CUT_AFTER:
        y += 56
H = y + 84

d = D(W, H, "WRITE · OBSERVABILITY ROADMAP",
      "관측 가능성 학습 로드맵",
      "무엇을 모르는지 묻는 관점에서 시작해 계측·지표·로그·트레이스를 지나 알림과 SLO, 확장과 "
      "플랫폼으로 간다. 척추에 단계 일곱을 걸고 개념을 좌우로 뻗었다. 노드의 주인공은 개념이고 "
      "아래 줄은 그 개념을 다루는 책의 장이다. 점 색이 우선순위이고, 책 줄이 비면 자료가 없는 자리다.",
      "노드는 개념, 아래 줄은 그 개념을 다루는 책의 장입니다")

LX, LY, LW, LH = 40, 96, 380, 190
d.box(LX, LY, LW, LH, PAPER2, RULE, 1.0)
d.t(LX + 16, LY + 24, "읽는 법", 13, INK, KR, "start", 600)
for i, (lab, txt) in enumerate([("필수", "빼면 뒤가 막힙니다"),
                                ("추천", "빼도 되지만 손해가 큽니다"),
                                ("선택", "목표가 생겼을 때만"),
                                ("대체", "같은 자리 — 하나만 고릅니다")]):
    cy = LY + 54 + i * 26
    c = MARK[lab]
    d.o.append(f'<circle cx="{LX + 24}" cy="{cy}" r="5" fill="{c}"/>')
    d.t(LX + 40, cy + 4, lab, 12, c, KR, "start", 600)
    d.t(LX + 78, cy + 4, txt, 12, MUTED, KR, "start")
d.t(LX + 16, LY + 172, "책 줄이 비면 아직 자료가 없는 자리 — 개념이 먼저입니다", 12, SOFT, KR, "start")

RX, RY, RW, RH = 580, 96, 380, 190
d.box(RX, RY, RW, RH, PAPER, RULE, 0.9)
d.o.append(f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="6" fill="none" '
           f'stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 4"/>')
d.t(RX + 16, RY + 24, "여기서 다루지 않는 것", 13, INK, KR, "start", 600)
for i, (who, what) in enumerate([
        ("os-roadmap", "perf · Ftrace · eBPF 의 커널 관측"),
        ("k8s-roadmap", "이벤트 · kubectl 로 좁히는 오브젝트 진단"),
        ("network-roadmap", "패킷 캡처와 Hubble 의 흐름 관측"),
        ("06_observability 프로젝트 노트", "LGTM 스택 구축 기록 — 순서가 아니라 사례")]):
    cy = RY + 56 + i * 33
    d.t(RX + 16, cy, who, 13, MUTED, KR, "start", 600)
    d.t(RX + 16, cy + 16, what, 12, SOFT, KR, "start")

d.box(SX - 130, ROOT_Y, 260, 52, PAPER2, RULE, 1.0)
d.t(SX, ROOT_Y + 32, "여기서 시작합니다", 14, INK, KR, "middle", 600)
d.line(SX, ROOT_Y + 52, SX, H - 120, RULE, 1.4)


def draw_stage(title, sub, left, right, y):
    h = row_h(left, right)
    mid = y + h / 2
    for side, items in (("left", left), ("right", right)):
        sign = -1 if side == "left" else 1
        bus = SX + sign * BUS
        top = mid - (len(items) * CH_H + (len(items) - 1) * CH_GAP) / 2
        d.line(SX + sign * (NODE_W / 2), mid, bus, mid, RULE, 1.0)
        for i, (concept, book, mark) in enumerate(items):
            cy = top + i * (CH_H + CH_GAP) + CH_H / 2
            bx = bus + (sign * ELBOW) - (CH_W if side == "left" else 0)
            c = MARK[mark]
            d.line(bus, mid, bus, cy, RULE, 1.0)
            d.line(bus, cy, bus + sign * ELBOW, cy, RULE, 1.0)
            d.box(bx, cy - CH_H / 2, CH_W, CH_H, PAPER2, RULE, 0.9)
            d.o.append(f'<circle cx="{bx + 15}" cy="{cy - 8}" r="4.5" fill="{c}"/>')
            d.t(bx + 28, cy - 4, concept, 12, INK, KR, "start")
            d.t(bx + 28, cy + 14, book if book else "책 없음 — 채울 자리", 10,
                SOFT if book else MARK["선택"], MONO, "start")
    d.box(SX - NODE_W / 2, mid - NODE_H / 2, NODE_W, NODE_H, PAPER, INFO, 1.2)
    d.t(SX, mid - 4, title, 14, INK, KR, "middle", 600)
    d.t(SX, mid + 16, sub, 11, SOFT, KR)
    return h


def draw_note(text, y):
    d.o.append(f'<rect x="110" y="{y}" width="780" height="{NOTE_H - 12}" rx="6" '
               f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="2 4"/>')
    d.t(130, y + 26, "메모", 11, SOFT, MONO, "start")
    d.t(130, y + 46, text, 13, MUTED, KR, "start")
    return NOTE_H


y = ROOT_Y + 52 + PHASE_GAP
for i, (title, sub, left, right) in enumerate(stages):
    y += draw_stage(title, sub, left, right, y) + ROW_GAP
    if i in NOTES:
        y += draw_note(NOTES[i], y)
    if i == CUT_AFTER:
        d.line(40, y + 12, W - 40, y + 12, WARN, 1.4, "6 5")
        d.o.append(f'<rect x="{SX - 235}" y="{y}" width="470" height="22" rx="4" fill="{PAPER}"/>')
        d.t(SX, y + 17, "1~4단계는 신호를 만들고 읽기 · 5단계부터는 운영으로 잇기", 13, WARN, KR)
        y += 56

d.legend(H - 60, [("필수", INFO), ("추천", OK), ("선택", SOFT), ("대체 선택지", ACC),
                  ("신호와 운영의 경계", WARN)])
d.save("observability-roadmap.svg")
