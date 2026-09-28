# 10-04.chapter-overview — 저장소에 올려 게시하고, 태그로 버전을 매기며, replace·exclude 는 의존성을, retract 는 내 버전을 다루고, 워크스페이스가 로컬 소스를 잇고, 프록시와 체크섬 DB 가 받기를 지킨다
# 본문 요구(10-04 「학습 목표」 개념도 문단): 첫 줄 게시와 라이선스(§1), 둘째 줄 버전 태그와 /v2(§2), 셋째 줄 replace·exclude·retract(§3), 넷째 줄 워크스페이스(§4), 다섯째 줄 프록시와 체크섬 DB(§5).
# 타입 스펙: type-architecture — 키워드 개념도. 5행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 10장 「Publishing Your Module」부터 장 끝까지, go1.25.1 로컬 실행(2026-09-27).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 808


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, 'ARCHITECTURE · 10-04 OVERVIEW',
      '게시는 저장소와 태그로, 받기는 프록시와 체크섬으로',
      '10-04 의 키워드 개념도. 첫 줄은 모듈을 저장소에 올리는 것만으로 게시하고, 오픈 소스면 루트에 LICENSE 를 두며 Go 커뮤니티는 허용적 라이선스를 선호한다는 것이다. 둘째 줄은 프리릴리스 태그는 자동으로 골라지지 않고, 호환이 깨지면 /v2 경로와 v2.0.0 태그를 쓴다는 것이다. 셋째 줄은 replace 와 exclude 가 내가 쓰는 의존성을 바꾸거나 막고, retract 는 내 모듈을 쓰는 쪽에 특정 버전을 쓰지 말라고 알린다는 것이다. 넷째 줄은 go.work 가 게시하지 않은 모듈을 로컬 소스로 이어 준다는 것이다. 다섯째 줄은 go get 이 프록시에서 받고 체크섬 데이터베이스로 바뀐 버전을 거부한다는 것이다.',
      lead='화살표 위 글자는 두 키워드의 관계, 왼쪽 칩은 그 줄을 다루는 절입니다.')


def node(i, j, title, sub, c=None):
    x, y = nx(j), ny(i)
    if c:
        d.tone(x, y, NW, NH, c, 6, "14", 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW / 2, y + 27, title, 14, c or INK, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 48, sub, 11, MUTED, kr(sub), "middle")


def harrow(i, j, label, c=SOFT, m="soft"):
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    d.arrow([(x1 + 2, y), (x2 - 4, y)], c, m, 1.3)
    d.t((x1 + x2) / 2, y - 9, label, 11, c if c != SOFT else MUTED, kr(label), "middle", 600)


def varrow(i, j, label):
    x = nx(j) + NW / 2
    y1, y2 = ny(i) + NH, ny(i + 1)
    d.arrow([(x, y1 + 2), (x, y2 - 4)], SOFT, "soft", 1.3)
    d.t(x + 10, (y1 + y2) / 2 + 4, label, 11, MUTED, kr(label), "start", 600)




for i, sec in enumerate(('§1', '§2', '§3', '§4', '§5')):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, '저장소에 올림', '중앙 업로드 없음')
node(0, 1, 'LICENSE', '저장소 루트', INFO)
node(0, 2, 'BSD · MIT · Apache', '허용적 라이선스', OK)
harrow(0, 0, '오픈 소스면')
harrow(0, 1, 'Go 커뮤니티는')

node(1, 0, 'v1.4.0-rc2', '프리릴리스 태그')
node(1, 1, '자동 선택 안 됨', '버전을 명시해야 받음', INFO)
node(1, 2, '/v2 · v2.0.0', '하위 디렉터리나 브랜치', OK)
harrow(1, 0, 'go get 은')
harrow(1, 1, '호환이 깨지면')

node(2, 0, '의존 모듈', '버그 · 관리 중단')
node(2, 1, '내 go.mod', 'replace · exclude · retract', INFO)
node(2, 2, '내 모듈 사용자', '철회된 버전으로 안 올림', ACC)
harrow(2, 0, '포크로 · 버전 막기')
harrow(2, 1, 'retract', ACC, 'acc')

node(3, 0, 'workspace_lib', '아직 게시 안 함')
node(3, 1, 'go.work', '로컬 소스로 풂 · 커밋 안 함', INFO)
node(3, 2, 'workspace_app', '로컬 변경이 보임', OK)
harrow(3, 0, 'go work use')
harrow(3, 1, '빌드하면')

node(4, 0, 'go get', '모듈 요청')
node(4, 1, 'proxy.golang.org', '캐시 · 사라짐 방지', INFO)
node(4, 2, '체크섬 데이터베이스', '바뀐 버전 거부', OK)
harrow(4, 0, 'GOPROXY')
harrow(4, 1, '해시 비교')


d.legend(712, [("장치", INFO), ("결과", OK), ("남에게 알림", ACC)])
d.save('10-04.chapter-overview.svg')
print('ok', '10-04')
