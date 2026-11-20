# 10-01.chapter-overview — 키워드를 노드로, 앞 키워드에서 뒤 키워드로 넘어가는 관계를 화살표 라벨로 이은 편 전체 지도
# 행 하나가 본문 `##` 하나다. 왼쪽 칩은 절 번호, 노드는 그 절의 핵심 키워드와 실제 값, 화살표 라벨은 두 키워드 사이의 관계다.
# 노드 근거: §1 은 「Application 사이 순서와 헬스 판정」(Application 은 서로 기다리지 않고 wave 는 한 Application 안만 정렬,
#            Application 의 헬스는 직계 자식 리소스 중 가장 나쁜 헬스, readinessProbe 가 없으면 Healthy 로 일찍 보임),
#            §2 는 「헬스 체크가 만드는 wave 간 대기」(헬스 체크가 없으면 wave 사이 기본 지연 2초, 체크를 더하면 database 에서 backend 까지 약 27초,
#            backend 에서 frontend 까지 약 16초),
#            §3 은 「ApplicationSet 과 단계별 sync」(순서는 정하지 않음, steps·matchExpressions)와 「켜기 전후의 동작과 한계」
#            (켠 뒤 api-1 은 약 26초 뒤, api-2 는 그 약 17초 뒤, frontend 는 다시 약 17초 뒤에 sync)다. 값은 모두 본문에 있는 것이다.
#            focal 은 핵심 요약 첫 문장(순서는 Application 위의 한 층이고 그 층이 기다릴 수 있는 이유는 Application 의 헬스)에 맞춰 §1 가운데 노드에 둔다.
# 타입 스펙: type-process — 행마다 같은 의미 슬롯(문제 · 중간 · 대응)이 같은 자리에 반복된다("Stage framework with semantic slots").
#           화살표는 읽는 순서이고 라벨은 관계다. 색은 문제 INFO, 대응 OK, 이 편의 한 줄 ACC 다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, OK, INFO, KR, MONO

W, H = 1000, 424
COL_X, STRIDE, NW, NH = 64, 344, 200, 64
ROW_Y, ROW_STRIDE = 104, 92

d = D(W, H, "CHAPTER MAP · 10-01",
      "Application 의 순서는 한 층 위에서 헬스를 기다리며 만든다",
      "10-01 편의 전체 지도. 첫 행은 Application 끼리 기다리지 않아 wave 가 한 Application 안만 정렬하므로 "
      "Application 의 헬스를 기준으로 위의 한 층이 아래쪽 헬스를 기다리는 흐름, "
      "둘째 행은 App-of-Apps 에서 헬스 체크가 없으면 wave 사이가 2초뿐이어서 argocd-cm 에 헬스 체크를 더해 앞 자식의 Healthy 를 기다리는 흐름, "
      "셋째 행은 ApplicationSet 이 순서 없이 Application 을 만든 뒤 RollingSync 의 단계마다 Healthy 를 기다리며 sync 하는 흐름을 보인다.",
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


for i in range(3):
    d.chip(34, ny(i) + NH / 2 - 4, f"§{i + 1}", MUTED, 11, 4)

# §1 Application 의 순서와 헬스
node(0, 0, "서로 안 기다림", "wave 는 앱 안만 정렬", INFO)
node(0, 1, "Application 헬스", "가장 나쁜 자식 헬스", ACC)
node(0, 2, "아래쪽 헬스 기다림", "readinessProbe 필요", OK)
harrow(0, 0, "기준은 헬스")
harrow(0, 1, "층이 기다림")

# §2 App-of-Apps 와 sync wave
node(1, 0, "wave 사이 2초", "App-of-Apps 의 기본", INFO)
node(1, 1, "헬스 체크 추가", "argocd-cm 에 키", None)
node(1, 2, "앞 자식 Healthy", "27초 · 16초 간격", OK)
harrow(1, 0, "그래서 추가")
harrow(1, 1, "대기가 작동")

# §3 ApplicationSet 과 RollingSync
node(2, 0, "순서 없는 생성", "ApplicationSet 이 한꺼번에", INFO)
node(2, 1, "RollingSync", "steps · matchExpressions", None)
node(2, 2, "단계마다 Healthy", "26초 · 17초 · 17초 간격", OK)
harrow(2, 0, "단계를 나눔")
harrow(2, 1, "기능을 켜면")

d.legend(ny(2) + NH + 24, [("문제", INFO), ("이 편의 한 줄", ACC), ("대응", OK)])
d.save("10-01.chapter-overview.svg")
