# 13-01.chapter-overview — 키워드를 노드로, 앞 키워드에서 뒤 키워드로 넘어가는 관계를 화살표 라벨로 이은 편 전체 지도
# 행 하나가 본문 `##` 하나다. 왼쪽 칩은 절 번호, 노드는 그 절의 핵심 키워드와 실제 값, 화살표 라벨은 두 키워드 사이의 관계다.
# 노드 근거: 1행은 §1 요약과 구성요소별 포트 표(8082 · 8083 · 8084), ServiceMonitor 절, 2행은 §2 요약과 핵심 요약(ConfigMap 이 비어 있음, service · template · trigger, annotation 구독),
#           3행은 §3 요약과 복제 수 표(server 2 · repo-server 2), Redis 는 버려도 되는 캐시, 4행은 §4 요약과 처리기 수 표(status 20 · operation 10), 핵심 요약의 샤딩 설정(복제 수와 같은 수의 환경 변수).
#           값은 모두 본문에 적힌 것이다.
# 타입 스펙: type-process — 행마다 같은 의미 슬롯(문제 · 중간 · 대응)이 같은 자리에 반복된다("Stage framework with semantic slots").
#           화살표는 읽는 순서이고 라벨은 관계다. 형제 편 gen-45-02.chapter-overview.py 와 같은 열 간격을 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, OK, INFO, KR, MONO

W, H = 1000, 516
COL_X, STRIDE, NW, NH = 64, 344, 200, 64
ROW_Y, ROW_STRIDE = 104, 92

d = D(W, H, "CHAPTER MAP · 13-01",
      "상태는 메트릭과 알림으로 보고 부하는 복제와 샤딩으로 견딘다",
      "13-01 편의 전체 지도. 첫 행은 구성요소마다 다른 포트의 메트릭을 ServiceMonitor 가 골라 Grafana 대시보드로 보는 길, "
      "둘째 행은 비어 있는 ConfigMap 에 service 와 template 과 trigger 를 적고 annotation 으로 구독하는 알림, "
      "셋째 행은 고가용성 매니페스트가 정한 복제 수와 버려도 되는 Redis 캐시, "
      "넷째 행은 느려지는 원인에 따라 처리기 수를 올리고 클러스터가 많으면 복제 수와 샤딩 설정을 함께 적는 것을 보인다.",
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


for i in range(4):
    d.chip(34, ny(i) + NH / 2 - 4, f"§{i + 1}", MUTED, 11, 4)

# §1 메트릭과 대시보드
node(0, 0, "구성요소마다 포트", "8082 · 8083 · 8084", INFO)
node(0, 1, "ServiceMonitor", "복제마다 수집", None)
node(0, 2, "Grafana 대시보드", "Prometheus 데이터 소스", OK)
harrow(0, 0, "Service 를 고름")
harrow(0, 1, "Prometheus 가 저장")

# §2 알림 컨트롤러 설정과 구독
node(1, 0, "설치만으로는 무발송", "ConfigMap 이 비어 있음", INFO)
node(1, 1, "세 조각", "어디로 · 무엇을 · 언제", None)
node(1, 2, "annotation 구독", "조건이 참이면 발송", OK)
harrow(1, 0, "ConfigMap 에 적음")
harrow(1, 1, "앱이 구독")

# §3 고가용성
node(2, 0, "ha/install.yaml", "서로 다른 노드 세 개")
node(2, 1, "복제 수", "server 2 · repo-server 2", None)
node(2, 2, "Redis 는 캐시", "버려도 다시 채워짐", OK)
harrow(2, 0, "구성요소마다 정함")
harrow(2, 1, "상태를 안 둠")

# §4 성능 확장과 샤딩
node(3, 0, "느려지는 원인", "앱 수 · 클러스터 수", INFO)
node(3, 1, "처리기 수", "status 20 · operation 10", None)
node(3, 2, "복제 수와 샤딩 설정", "replicas · 환경 변수 같은 수", ACC)
harrow(3, 0, "앱이 많으면")
harrow(3, 1, "또는 클러스터가 많으면")

d.legend(ny(3) + NH + 24, [("문제", INFO), ("이 편의 한 줄", ACC), ("대응", OK)])
d.save("13-01.chapter-overview.svg")
