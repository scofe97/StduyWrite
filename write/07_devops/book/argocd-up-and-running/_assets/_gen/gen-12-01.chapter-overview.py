# 12-01.chapter-overview — 키워드를 노드로, 앞 키워드에서 뒤 키워드로 넘어가는 관계를 화살표 라벨로 이은 편 전체 지도
# 행 하나가 본문 `##` 하나다. 왼쪽 칩은 절 번호, 노드는 그 절의 핵심 키워드와 실제 값, 화살표 라벨은 두 키워드 사이의 관계다.
# 노드 근거: 1행은 §1 요약과 실측 표(실측 최장 288초, 120초 + jitter 60초, 30초 + jitter 0), 2행은 §2 요약과 §1 캐시 설명(Webhook 은 캐시를 건너뜀, 새로 고침만 일으킴),
#           3행은 §3 요약과 핵심 요약(검증 전 배포, 프로젝트 역할 토큰, app sync --revision), 4행은 §4 요약과 Pipeline 절(runAfter, 린트 실패 시 뒤 Task 중단, lint · sync Succeeded),
#           5행은 §5 요약과 EventListener 절(after 를 revision 으로, 인증 없는 POST 도 접수). 값은 모두 본문에 적힌 것이다.
# 타입 스펙: type-process — 행마다 같은 의미 슬롯(문제 · 중간 · 대응)이 같은 자리에 반복된다("Stage framework with semantic slots").
#           화살표는 읽는 순서이고 라벨은 관계다. 형제 편 gen-45-02.chapter-overview.py 와 같은 열 간격을 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, OK, INFO, KR, MONO

W, H = 1000, 608
COL_X, STRIDE, NW, NH = 64, 344, 200, 64
ROW_Y, ROW_STRIDE = 104, 92

d = D(W, H, "CHAPTER MAP · 12-01",
      "Argo CD 는 주기로 변경을 알아채고 CI 는 검증 뒤 리비전을 지정한다",
      "12-01 편의 전체 지도. 첫 행은 풀 방식의 감지 지연과 조정 주기 줄이기, "
      "둘째 행은 Webhook 이 새로 고침만 재촉하는 것, "
      "셋째 행은 검증 전에 배포되는 문제를 프로젝트 역할 토큰으로 부르는 app sync --revision 이 푸는 것, "
      "넷째 행은 Tekton 의 Task 와 Pipeline 이 린트 뒤에 동기화를 잇는 것, "
      "다섯째 행은 push 이벤트가 EventListener 를 거쳐 PipelineRun 이 되는 흐름과 인증 없는 접수를 보인다.",
      lead="행은 본문 절, 화살표 라벨은 앞 키워드에서 뒤 키워드로 넘어가는 관계")


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


def node(i, j, title, sub, c=None):
    x, y = nx(j), ny(i)
    if c:
        d.tone(x, y, NW, NH, c, 6, "14", 1.4 if c == ACC else 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW / 2, y + 27, title, 14, c or INK, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 49, sub, 12, MUTED, kr(sub), "middle")


def harrow(i, j, label):
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    d.arrow([(x1 + 2, y), (x2 - 4, y)], MUTED, "ar", 1.4)
    d.t((x1 + x2) / 2, y - 10, label, 12, MUTED, kr(label), "middle", 600)


for i in range(5):
    d.chip(34, ny(i) + NH / 2 - 4, f"§{i + 1}", MUTED, 11, 4)

# §1 변경을 알아채는 주기와 지연
node(0, 0, "풀 방식의 감지 지연", "실측 최장 288초", INFO)
node(0, 1, "조정 주기", "120초 + jitter 60초", None)
node(0, 2, "주기 단축", "30초 + jitter 0", OK)
harrow(0, 0, "주기마다 끌어옴")
harrow(0, 1, "값을 줄이면")

# §2 Webhook 으로 새로 고침 재촉
node(1, 0, "push 뒤 대기", "캐시 만료 전엔 안 보임", INFO)
node(1, 1, "Webhook", "/api/webhook", None)
node(1, 2, "새로 고침만 일으킴", "동기화는 자동 동기화 몫", OK)
harrow(1, 0, "push 때 재촉")
harrow(1, 1, "받으면")

# §3 파이프라인이 Argo CD 를 부르는 길
node(2, 0, "검증 전 배포", "Webhook 은 검증을 건너뜀", INFO)
node(2, 1, "프로젝트 역할 토큰", "get · sync 두 줄 정책", None)
node(2, 2, "app sync --revision", "자동 동기화는 꺼 둠", ACC)
harrow(2, 0, "순서를 뒤집어")
harrow(2, 1, "토큰으로 호출")

# §4 Tekton Pipelines 로 린트 뒤 동기화
node(3, 0, "린트 통과 조건", "실패하면 뒤 Task 중단", INFO)
node(3, 1, "Task · Pipeline", "정의와 기록을 분리", None)
node(3, 2, "PipelineRun", "lint · sync Succeeded", OK)
harrow(3, 0, "runAfter 로 순서")
harrow(3, 1, "한 번 실행")

# §5 Triggers 로 PipelineRun 시작
node(4, 0, "push 로 파이프라인 시작", "본문의 after", INFO)
node(4, 1, "EventListener", "인증 없는 POST 도 접수", None)
node(4, 2, "PipelineRun 시작", "after 가 revision 으로", OK)
harrow(4, 0, "POST 로 도착")
harrow(4, 1, "바인딩과 템플릿")

d.legend(ny(4) + NH + 24, [("문제", INFO), ("이 편의 한 줄", ACC), ("대응", OK)])
d.save("12-01.chapter-overview.svg")
