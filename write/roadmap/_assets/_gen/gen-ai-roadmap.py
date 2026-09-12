# write/roadmap/ai-roadmap.md §학습 순서 — AI 로드맵(DevOps 축).
#
# 축이 다른 편과 다르다 — 모델을 만드는 쪽이 아니라 부리고 운영하는 쪽만 담는다.
#   사전학습·파인튜닝·데이터셋 구축·모델 아키텍처는 이 로드맵의 대상이 아니다.
#   판단 기준은 "이 지식이 배포 파이프라인이나 클러스터 운영에 닿는가" 하나다.
# 절단선은 4단계 뒤에 긋는다 — 1~4 가 모델을 프로그램으로 부리는 일,
#   5 부터가 그것을 개발 환경과 배포 파이프라인에 앉히는 일이다.
#
# 판형은 roadmap.sh 계열이다 — 세로 척추에 단계를 걸고 개념을 좌우로 뻗되,
#   노드마다 우선순위 점을 찍는다.
# 노드의 주인공은 개념이고 책은 그 개념을 다루는 자리다. 책 줄이 비면 아직 자료가 없다는 뜻이다.
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
    ("1 · 모델을 도구로 쓰기", "스크립트에 물릴 수 있는 상태로",
     [("모델 종류와 선택 기준", "AI Engineering 1장", "필수"),
      ("추론 노력과 사고 깊이 조절", "", "필수"),
      ("구조화 출력 — JSON Schema", "", "필수")],
     [("토큰 넷 — 입력 · 출력 · 추론 · 캐시", "AI Engineering 1장", "필수"),
      ("비용과 지연의 셈법", "", "필수"),
      ("모델 교체와 거부 · 폴백", "", "추천")]),

    ("2 · 프롬프트와 컨텍스트", "모델이 보는 세계를 짜는 일",
     [("지시 3계층 — 시스템 · 개발자 · 사용자", "AI Engineering 5장", "필수"),
      ("출력 형식과 예시 설계", "AI Engineering 5장", "필수"),
      ("컨텍스트 윈도우 구성", "", "필수"),
      ("압축 · 우선순위 · 축출", "", "필수")],
     [("프롬프트 캐싱과 접두 일치", "", "필수"),
      ("컨텍스트 격리와 토큰 예산", "", "추천"),
      ("RAG — 런북과 매니페스트를 근거로", "AI Engineering 6장", "추천"),
      ("컨텍스트 부패 · 롱컨텍스트 한계", "", "추천")]),

    ("3 · 도구 연결과 MCP", "모델에 손발을 달되 권한을 가른다",
     [("도구 호출과 스키마", "AI Agents 4장", "필수"),
      ("도구 표면 설계 — 범용 셸 대 전용", "AI Agents 4장", "필수"),
      ("결과 압축과 오류 · 재시도", "", "필수"),
      ("JSON-RPC 와 도구 스키마", "Claude Code 7장", "추천")],
     [("MCP 삼자 — 호스트 · 서버", "Claude Code 7장", "필수"),
      ("Tools · Resources · Prompts", "Claude Code 7장", "필수"),
      ("전송 방식과 인증", "", "추천"),
      ("읽기 전용과 쓰기의 분리", "Claude Code 5장", "필수")]),

    ("4 · 하네스와 에이전트", "모델 바깥 전부가 하네스다",
     [("에이전트 루프의 뼈대", "AI Agents 2장", "필수"),
      ("워크플로우로 고정할 자리", "AI Agents 2장", "필수"),
      ("상태 · 메모리 · 재개", "AI Agents 6장", "필수")],
     [("오케스트레이션 패턴", "AI Agents 5장", "필수"),
      ("하나에서 여럿으로 — 서브에이전트", "AI Agents 8장", "추천"),
      ("사람이 끼는 지점", "AI Agents 13장", "필수"),
      ("완료 검증과 루브릭", "AI Agents 9장", "필수")]),

    ("5 · AI 개발 환경", "에이전트를 실제 저장소에 붙인다",
     [("에이전틱 개발이 바꾼 것", "Claude Code 1장", "필수"),
      ("행동 규칙 · 스킬 · 훅", "Claude Code 6장", "필수"),
      ("권한과 신뢰 경계", "Claude Code 5장", "필수"),
      ("분위기 코딩이 막히는 자리", "Claude Code 4장", "추천")],
     [("워크트리로 작업 공간 가르기", "", "추천"),
      ("여러 에이전트 동시 운전", "", "추천"),
      ("이슈에서 PR 까지 한 줄기", "", "추천"),
      ("거짓 성공과 개입 신호", "", "필수")]),

    ("6 · GitAIOps — 인프라를 AI 와 짓기", "여기가 DevOps 직무의 정중앙",
     [("GitOps 선언과 드리프트", "AI 인프라 1장", "필수"),
      ("ArgoCD Application 과 롤백", "AI 인프라 3장", "필수"),
      ("CI 연결과 무한 루프 방어", "AI 인프라 3장", "필수"),
      ("관측을 한 번에 세우기", "AI 인프라 4장", "필수")],
     [("배포 전략 — 롤링 · 블루그린 · 카나리", "AI 인프라 5·6장", "필수"),
      ("멀티 노드풀과 멀티테넌시", "AI 인프라 7장", "추천"),
      ("행동 규칙 · 메모리 · 결정 기록", "AI 인프라 3~6장", "필수"),
      ("위험 명령 가드레일", "AI 인프라 8장", "필수")]),

    ("7 · 평가와 가드레일", "비결정적인 것을 채점하고 가둔다",
     [("골든 데이터셋과 회귀 시험", "AI Engineering 3장", "필수"),
      ("무엇을 잴 것인가", "AI Engineering 4장", "필수"),
      ("심판 모델과 그 한계", "AI Agents 9장", "추천"),
      ("CI 게이트로 굳히기", "", "필수")],
     [("주입 3종 — 프롬프트 · 도구 · 유출", "AI Agents 12장", "필수"),
      ("샌드박스와 최소 권한", "AI Agents 12장", "필수"),
      ("시크릿 가리기와 개인정보", "", "필수"),
      ("예산 한도와 속도 제한", "", "추천")]),

    ("8 · 운영", "에이전트도 운영 대상 시스템이다",
     [("에이전트 지표와 감사 로그", "AI Agents 10장", "필수"),
      ("과업당 비용과 병목", "AI Agents 10장", "필수"),
      ("개선 루프", "AI Agents 11장", "추천")],
     [("프로덕션 준비와 배포", "Introducing MLOps 5·6장", "추천"),
      ("모니터링과 되먹임", "Introducing MLOps 7장", "추천"),
      ("모델 거버넌스", "Introducing MLOps 8장", "추천"),
      ("추론 서빙 비용", "AI Engineering 9장", "선택")]),
]

CUT_AFTER = 3          # 4단계 뒤에 "모델을 부리기" ↔ "파이프라인에 앉히기" 절단선
NOTES = {
    3: "1~4단계는 모델을 프로그램으로 부리는 일이고 5단계부터는 그것을 저장소와 클러스터에 앉히는 일이다.",
    5: "6단계가 이 로드맵의 무게중심이다. 앞 다섯 단계는 여기에 도달하기 위한 준비다.",
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

d = D(W, H, "WRITE · AI ROADMAP (DEVOPS)",
      "AI 학습 로드맵 — DevOps 축",
      "모델을 만드는 쪽이 아니라 부리고 운영하는 쪽만 담았다. 스크립트에 물릴 수 있는 모델 사용법에서 "
      "시작해 도구·하네스를 지나 개발 환경과 GitAIOps 배포 파이프라인, 평가와 운영으로 간다. 척추에 "
      "단계 여덟을 걸고 개념을 좌우로 뻗었다. 점 색이 우선순위이고, 책 줄이 비면 자료가 없는 자리다.",
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
        ("모델을 만드는 쪽", "사전학습 · 파인튜닝 · 데이터셋 구축"),
        ("k8s-roadmap", "쿠버네티스 오브젝트와 내부 구조 자체"),
        ("observability-roadmap", "지표 · 로그 · 트레이스의 일반 이론"),
        ("제품 UX", "에이전트 화면 설계와 사용자 경험")]):
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
        d.o.append(f'<rect x="{SX - 255}" y="{y}" width="510" height="22" rx="4" fill="{PAPER}"/>')
        d.t(SX, y + 17, "1~4단계는 모델을 부리기 · 5단계부터는 파이프라인에 앉히기", 13, WARN, KR)
        y += 56

d.legend(H - 60, [("필수", INFO), ("추천", OK), ("선택", SOFT), ("대체 선택지", ACC),
                  ("부리기와 앉히기의 경계", WARN)])
d.save("ai-roadmap.svg")
