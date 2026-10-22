# 타입 스펙: type-architecture — 키워드 개념도. 이미지 두 부분과 덮어쓰기, OCI 번들, 데몬 빌드, 지운 파일이 남는 층, 다이제스트와 태그를 잇는 5행 × 3열 노드 격자. focal 은 docker save 로 꺼낸 layer.tar.
# 사실 출처: 노트 L21~L23(핵심 요약), L47~L72(두 부분·Dockerfile 명령·덮어쓰기), L84~L95(OCI 번들), L103~L121(소켓·데몬·대안 도구), L137~L181(층·docker save), L197~L214(blob·매니페스트·다이제스트·태그).
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 764


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "CONTAINER SECURITY · 06-01 OVERVIEW",
      "층에 넣은 것은 지워도 남고, 다이제스트만 내용에 묶입니다",
      "06-01 의 키워드 개념도. 첫 줄은 이미지의 루트 파일시스템과 설정 정보, 그리고 실행 시점의 덮어쓰기다. "
      "둘째 줄은 OCI 이미지를 umoci 로 풀어 rootfs 와 config.json 번들로 만드는 흐름이다. "
      "셋째 줄은 docker build 가 소켓으로 root 데몬에 닿는 위험과 데몬 없는 빌드 도구다. "
      "넷째 줄은 RUN rm 으로 지운 password.txt 가 docker save 로 꺼내면 layer.tar 에 남는 흐름이다. "
      "다섯째 줄은 층 blob 에서 매니페스트와 다이제스트가 나오고 태그는 사람이 읽는 이름으로 옮겨 다니는 흐름이다.",
      lead="화살표 위 글자는 두 키워드의 관계, 왼쪽 칩은 그 줄을 다루는 절입니다.")


def node(i, j, title, sub, c=None):
    x, y = nx(j), ny(i)
    fit(title, 13, NW - 16)
    fit(sub, 12, NW - 16)
    if c:
        d.tone(x, y, NW, NH, c, 6, "14", 1.4 if c == ACC else 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW / 2, y + 27, title, 13, c or INK, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 48, sub, 12, MUTED, kr(sub), "middle")


def harrow(i, j, label):
    fit(label, 12, STRIDE - NW - 12)
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)
    d.t((x1 + x2) / 2, y - 9, label, 12, MUTED, kr(label), "middle", 600)


def wrap(i, label):
    # 오른쪽 끝 노드 아래에서 내려와 왼쪽 끝 노드 위로 들어가는 줄 바꿈 화살표
    xa, xb = nx(2) + NW / 2, nx(0) + NW / 2
    y1, y2 = ny(i) + NH, ny(i + 1)
    ym = y1 + 32
    d.arrow([(xa, y1 + 2), (xa, ym), (xb, ym), (xb, y2 - 4)], SOFT, "soft", 1.3)
    d.t((xa + xb) / 2, ym - 7, label, 12, MUTED, kr(label), "middle", 600)


for i, sec in enumerate(("§1", "§2", "§3", "§4", "§5")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, "루트 파일시스템", "FROM·ADD·COPY·RUN", INFO)
node(0, 1, "설정 정보", "USER·EXPOSE·ENV", INFO)
node(0, 2, "docker run -e", "실행 시점에 덮어쓰기")
harrow(0, 0, "나란히 저장")
harrow(0, 1, "값 교체")
wrap(0, "런타임이 쓰려면")

node(1, 0, "OCI 이미지", "skopeo copy ... oci:")
node(1, 1, "umoci unpack", "런타임 파일시스템 번들")
node(1, 2, "rootfs/ + config.json", "runc 가 읽는 번들", INFO)
harrow(1, 0, "그대로는 못 씀")
harrow(1, 1, "풀면")
wrap(1, "이미지를 만드는 도구")

node(2, 0, "docker build", "CLI → Docker 소켓")
node(2, 1, "Docker 데몬", "root · 빌드 이상의 능력", BAD)
node(2, 2, "BuildKit · Kaniko", "데몬 없이 빌드", OK)
harrow(2, 0, "API 요청")
harrow(2, 1, "대안")
wrap(2, "빌드가 만든 층")

node(3, 0, "echo > /password.txt", "RUN 한 줄 = 층 하나")
node(3, 1, "RUN rm /password.txt", "위층의 삭제 표시일 뿐", WARN)
node(3, 2, "docker save", "55*/layer.tar 에 남음", ACC)
harrow(3, 0, "다음 줄에서")
harrow(3, 1, "꺼내 보면")
wrap(3, "층을 저장하면")

node(4, 0, "이미지 매니페스트", "층 blob 의 집합")
node(4, 1, "다이제스트", "내용에 묶인 식별자", OK)
node(4, 2, "태그", "옮겨 다니는 라벨", WARN)
harrow(4, 0, "해시를 취하면")
harrow(4, 1, "다른 참조 방식")

d.legend(704, [("구조", INFO), ("위험", BAD), ("조건부", WARN), ("안전·대안", OK), ("핵심 접점", ACC)])
d.save(str(ASSETS / "06-01.chapter-overview.svg"))
print("ok 06-01 overview")
