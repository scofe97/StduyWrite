# 타입 스펙: type-layers — 위에서 아래로 층 3 · 2 · 1. 같은 층 더미를 두 가지로 읽는다: 위에서 겹쳐 본 실행 결과(파일 없음)와 층 하나씩 꺼낸 결과(top-secret). focal 은 파일이 남은 층 2.
# 사실 출처: 노트 L137~L141(Dockerfile 세 줄), L146~L149(ls 결과), L155~L158(docker save), L174~L179(55*/layer.tar · cat password.txt), L181(어느 층에든 한 번이라도 존재했던 파일은 얻을 수 있다).
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 984, 484
SX, SW = 48, 500                    # 층 더미 x · 폭
LH, STRIDE = 72, 96                 # 층 높이 · stride
LY = [120, 120 + STRIDE, 120 + 2 * STRIDE]   # 층 3 · 2 · 1
RX, RW = 656, 288                   # 오른쪽 결과 상자


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "CONTAINER SECURITY · 06-01 §4",
      "위층에서 지워도 아래층의 password.txt 는 layer.tar 에 그대로 있습니다",
      "Dockerfile 세 줄이 층 세 개가 된다. 층 2 가 password.txt 를 만들고 층 3 이 rm 으로 지우면, 실행한 컨테이너에서는 ls 가 No such file 을 내지만 "
      "docker save 로 꺼낸 55*/layer.tar 에는 top-secret 이 남아 있다.",
      lead="층은 각각 따로 저장되므로 한 층의 삭제 표시가 다른 층의 내용을 지우지 못합니다.")

LAYERS = [
    ("층 3", 'RUN rm /password.txt', "/password.txt 삭제 표시", WARN),
    ("층 2", 'RUN echo "top-secret" > /password.txt', "/password.txt 파일 생성", ACC),
    ("층 1", "FROM alpine", "alpine 루트 파일시스템", None),
]
for (tag, cmd, what, c), y in zip(LAYERS, LY):
    fit(cmd, 13, SW - 32)
    fit(what, 12, SW - 32)
    if c:
        d.tone(SX, y, SW, LH, c, 6, "14", 1.4 if c == ACC else 1.1)
    else:
        d.box(SX, y, SW, LH)
    d.t(SX + 16, y + 20, tag, 11, SOFT, KR, "start", 600)
    d.t(SX + 16, y + 42, cmd, 13, c or INK, MONO, "start", 600)
    d.t(SX + 16, y + 62, what, 12, MUTED, kr(what), "start")


def result(y, title, out, c):
    fit(title, 12, RW - 16)
    fit(out, 12, RW - 16)
    d.tone(RX, y, RW, LH, c, 6, "14", 1.1)
    d.t(RX + 12, y + 28, title, 12, INK, MONO, "start", 600)
    d.t(RX + 12, y + 52, out, 12, c, MONO, "start")


def link(y, label, c, m):
    d.arrow([(SX + SW + 4, y + LH / 2), (RX - 4, y + LH / 2)], c, m, 1.4)
    fit(label, 12, RX - SX - SW - 12)
    d.t((SX + SW + RX) / 2, y + LH / 2 - 9, label, 12, MUTED, KR, "middle", 600)


# 위에서 겹쳐 본 실행 결과 — 층 3 의 삭제 표시에서 끝난다
result(LY[0], "docker run ... ls /password.txt", "No such file or directory", WARN)
link(LY[0], "합쳐 본 결과", WARN, "warn")
# 층 하나씩 꺼낸 결과 — 층 2 의 파일이 그대로 나온다
result(LY[1], "docker save → tar -xf 55*/layer.tar", "cat password.txt → top-secret", BAD)
link(LY[1], "층째로 꺼냄", BAD, "bad")

d.legend(412, [("삭제 표시", WARN), ("파일이 남은 층", ACC), ("꺼낸 결과", BAD)])
d.save(str(ASSETS / "06-01.layer-persistence.svg"))
print("ok 06-01 layer-persistence")
