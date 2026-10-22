# 타입 스펙: type-architecture — 두 갈래 흐름(루트 파일시스템 · 설정 정보)이 이미지에서 번들로 풀려 runc 로 모이는 4단 구성. 오른쪽에 실행 시점 덮어쓰기 입력 하나. focal 은 umoci unpack.
# 사실 출처: 노트 L53~L54(Dockerfile 명령과 두 부분), L56(docker inspect), L60~L72(docker run -e · Pod env · config.json), L84~L95(런타임 번들 · rootfs · config.json · cgroup · namespace).
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, INFO, KR, MONO, PAPER

W, H = 984, 668
NW, NH = 232, 64
XL, XR, XO = 120, 432, 736          # 왼쪽 갈래 · 오른쪽 갈래 · 덮어쓰기 입력
ROW_Y = [112, 240, 368, 496]        # 명령 · 이미지 · 번들 · 런타임


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "CONTAINER SECURITY · 06-01 §1~2",
      "런타임은 이미지를 그대로 쓰지 못하고 rootfs 와 config.json 번들로 풉니다",
      "Dockerfile 의 FROM·ADD·COPY·RUN 은 루트 파일시스템을, USER·EXPOSE·ENV 는 설정 정보를 바꾼다. "
      "두 부분이 나란히 저장된 이미지를 umoci unpack 으로 풀면 rootfs 디렉토리와 config.json 파일의 번들이 되고, runc 가 그 번들로 컨테이너를 만든다. "
      "실행 시점의 docker run -e 나 Pod 의 env 값은 config.json 에 들어간다.",
      lead="왼쪽 칩은 단계, 파랑은 루트 파일시스템 갈래, 노랑은 실행 시점에 덮어쓸 수 있는 설정 갈래입니다.")


def node(x, y, title, sub, c=None, w=NW):
    fit(title, 13, w - 16)
    fit(sub, 12, w - 16)
    if c:
        d.tone(x, y, w, NH, c, 6, "14", 1.4 if c == ACC else 1.1)
    else:
        d.box(x, y, w, NH)
    d.t(x + w / 2, y + 27, title, 13, c or INK, kr(title), "middle", 600)
    d.t(x + w / 2, y + 48, sub, 12, MUTED, kr(sub), "middle")


def down(x, y1, y2, label, c=SOFT, m="soft"):
    d.arrow([(x, y1 + 2), (x, y2 - 4)], c, m, 1.3)
    if label:
        d.t(x + 12, (y1 + y2) / 2 + 4, label, 12, MUTED, kr(label), "start", 600)


for y, s in zip(ROW_Y, ("명령", "이미지", "번들", "런타임")):
    d.chip(60, y + NH / 2, s, MUTED, 12, 8)

# 1단 — Dockerfile 명령
node(XL, ROW_Y[0], "FROM·ADD·COPY·RUN", "루트 파일시스템을 바꿈", INFO)
node(XR, ROW_Y[0], "USER·EXPOSE·ENV", "설정 정보에 영향", WARN)
# 2단 — OCI 이미지의 두 부분
node(XL, ROW_Y[1], "루트 파일시스템", "alpine 과 같은 디렉토리 구조", INFO)
node(XR, ROW_Y[1], "설정 정보", "docker inspect 로 확인", WARN)
down(XL + NW / 2, ROW_Y[0] + NH, ROW_Y[1], "내용 저장")
down(XR + NW / 2, ROW_Y[0] + NH, ROW_Y[1], "나란히 저장")
# 3단 — 풀린 번들
node(XL, ROW_Y[2], "rootfs/", "배포판 내용", INFO)
node(XR, ROW_Y[2], "config.json", "cgroup 자원 · namespace 목록", WARN)
down(XL + NW / 2, ROW_Y[1] + NH, ROW_Y[2], "")
down(XR + NW / 2, ROW_Y[1] + NH, ROW_Y[2], "")
# 두 화살표 사이에 놓은 focal 단계
cx, cy = (XL + NW + XR) / 2, (ROW_Y[1] + NH + ROW_Y[2]) / 2
d.tone(cx - 56, cy - 14, 112, 28, ACC, 6, "14", 1.4)
d.t(cx, cy + 5, "umoci unpack", 12, ACC, MONO, "middle", 600)
d.line(XL + NW / 2, cy, cx - 56, cy, ACC, 1.0, "3 4")
d.line(cx + 56, cy, XR + NW / 2, cy, ACC, 1.0, "3 4")

# 실행 시점 덮어쓰기 — config.json 으로 들어간다
node(XO, ROW_Y[2], "Pod env · docker run -e", "값이 config.json 에 들어감")
d.arrow([(XO - 2, ROW_Y[2] + NH / 2), (XR + NW + 4, ROW_Y[2] + NH / 2)], WARN, "warn", 1.4)
d.t((XR + NW + XO) / 2, ROW_Y[2] + NH / 2 - 9, "값 교체", 12, WARN, KR, "middle", 600)

# 4단 — runc
rx = XL + (XR + NW - XL) / 2 - NW / 2   # 두 갈래의 가운데
node(rx, ROW_Y[3], "runc", "번들로 컨테이너 인스턴스화", OK)
ytop, ymid = ROW_Y[3], ROW_Y[2] + NH + (ROW_Y[3] - ROW_Y[2] - NH) / 2
d.arrow([(XL + NW / 2, ROW_Y[2] + NH + 2), (XL + NW / 2, ymid), (rx + 56, ymid), (rx + 56, ytop - 4)], SOFT, "soft", 1.3)
d.arrow([(XR + NW / 2, ROW_Y[2] + NH + 2), (XR + NW / 2, ymid), (rx + NW - 56, ymid), (rx + NW - 56, ytop - 4)], SOFT, "soft", 1.3)

d.legend(612, [("루트 파일시스템", INFO), ("설정 정보", WARN), ("런타임", OK), ("핵심 접점", ACC)])
d.save(str(ASSETS / "06-01.image-anatomy.svg"))
print("ok 06-01 image-anatomy")
