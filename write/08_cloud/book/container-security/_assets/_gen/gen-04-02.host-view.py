# 타입 스펙: type-nested — 호스트 PID namespace 안에 컨테이너 PID namespace 가 들어 있고, 그 안의 프로세스 하나가 안에서는 PID 10, 밖에서는 PID 30591 로 보인다. focal 은 호스트에서 본 PID 30591.
# 사실 출처: 노트 L159~L165(호스트 프로세스·커널 공유), L169~L180(sleep 1000 · ps -C sleep · 30591 과 10), L184(가상머신과의 차이·모든 컨테이너 관찰).
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, INFO, KR, MONO, PAPER

W, H = 984, 552


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "NESTED · 04-02 §4",
      "같은 sleep 프로세스가 안에서는 PID 10, 호스트에서는 PID 30591 로 보입니다",
      "호스트 PID namespace 안에 컨테이너 PID namespace 가 들어 있다. 컨테이너 안에서 ps 로 보면 sleep 1000 은 PID 10 이고, 호스트에서 ps -C sleep 으로 보면 같은 프로세스가 PID 30591 이다. "
      "프로세스는 하나이고 번호만 둘이며, 호스트 접근 권한이 있으면 모든 컨테이너를 관찰하고 영향을 줄 수 있다.",
      lead="프로세스는 하나이고 번호만 둘입니다. 그래서 호스트에서 컨테이너가 그대로 보입니다.")


def ring(x, y, w, h, label, c, fill):
    d.box(x, y, w, h, fill, c, 1.2, 8)
    d.t(x + 20, y + 28, label, 13, c, KR, "start", 600)


# 링: 호스트 > 컨테이너
ring(36, 112, 912, 332, "호스트 · 기본 PID namespace", MUTED, "#ffffff06")
ring(84, 160, 336, 244, "컨테이너 · 자기 PID namespace", INFO, "#6A95D810")

# 연결선·화살표(상자보다 먼저)
d.arrow([(540, 244), (388, 244)], ACC, "acc", 1.6, "5 4")
d.t(464, 232, "같은 프로세스", 12, ACC, KR, "middle", 600)
d.arrow([(252, 296), (252, 324)], SOFT, "soft", 1.3)
d.arrow([(726, 296), (726, 324)], SOFT, "soft", 1.3)

# 프로세스 상자(컨테이너 안)
d.box(120, 200, 264, 96)
d.t(252, 234, "sleep 1000", 14, INK, MONO, "middle", 600)
d.t(252, 260, "컨테이너화된 프로세스 하나", 12, MUTED, KR, "middle")
d.t(252, 282, "docker run --rm -it ubuntu bash", 12, SOFT, MONO, "middle")

# 컨테이너 안 시점
d.t(120, 348, "컨테이너 안 ps", 12, MUTED, KR, "start")
d.t(120, 380, "PID 10", 22, INK, MONO, "start", 600)

# 호스트 시점(focal)
d.tone(540, 200, 372, 96, ACC, 6, "14", 1.4)
d.t(560, 226, "호스트에서", 12, MUTED, KR, "start")
d.t(892, 226, "ps -C sleep", 12, INFO, MONO, "end")
d.t(560, 274, "PID 30591", 22, ACC, MONO, "start", 600)
d.t(892, 274, "훨씬 큰 번호", 12, MUTED, KR, "end")

# 결과 패널
d.tone(540, 324, 372, 80, BAD, 6, "14", 1.1)
d.t(560, 352, "가상머신과 갈리는 지점", 13, BAD, KR, "start", 600)
fit("호스트 접근 = 모든 컨테이너를 관찰·영향", 12, 340)
d.t(560, 380, "호스트 접근 = 모든 컨테이너를 관찰·영향", 12, MUTED, KR, "start")

# 호스트 커널 공유 칩(호스트 링 아래 테두리)
d.t(492, 432, "호스트 커널 공유", 12, MUTED, KR, "middle")

d.legend(488, [("호스트 시점", ACC), ("컨테이너 namespace", INFO), ("위험", BAD)])
d.save(str(ASSETS / "04-02.host-view.svg"))
print("ok 04-02 host-view")
