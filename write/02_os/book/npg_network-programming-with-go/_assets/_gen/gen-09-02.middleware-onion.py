# 09-02.middleware-onion — A(B(h)): 바깥부터 요청을 받고, 막히면 안쪽은 불리지 않는다
# 본문 요구(09-02 §1 실행 순서 문단): 바깥 미들웨어 A 가 먼저 불리고, 그다음 안쪽 B, 마지막에 핸들러 h.
#           비밀번호 헤더가 없으면 A 가 401 을 쓰고 돌아가 안쪽은 불리지 않는다. B 는 핸들러가 돌아온 뒤 경과 시간을 남긴다.
# 타입 스펙: type-nested — 바깥에서 안쪽으로 A ⊃ B ⊃ h. 한 겹당 안쪽 여백 28.
#           왼쪽에서 들어오는 요청 화살표 하나와 바깥 겹 아래쪽에서 되돌아 나가는 401 화살표 하나, 둘은 교차하지 않는다. focal 은 401 경로.
# 사실 출처: 09-02 §1 실행 순서 문단 — A·B·C 입구·출구 로그를 go1.25.1 에서 돌린 결과(A 가 막으면 A 입구만 남음, 2026-11-02).
#           도식은 겹 둘(A ⊃ B ⊃ h)로 줄여 그렸고 본문의 C 는 B 와 같은 안쪽 겹으로 본다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 540
d = D(W, H, "NESTED · 09-02 §1",
      "바깥 미들웨어부터 요청을 받고, 핸들러가 돌아오면 안쪽부터 정리합니다",
      "A(B(h)) 로 감싼 겹. 요청은 바깥의 A 가 먼저 받아 비밀번호 헤더를 검사하고, "
      "없으면 401 을 쓰고 돌아가 안쪽은 불리지 않는다. 있으면 B 가 시작 시각을 적고 h 를 부르며, "
      "h 가 응답을 쓰고 돌아오면 B 가 걸린 시간을 남긴다.",
      lead="바깥 겹이 먼저 받고, 안쪽 겹이 먼저 끝납니다.")


def layer(x, y, w, h, title, sub, c):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{c}0d" stroke="{c}" stroke-width="1.2"/>')
    d.t(x + 20, y + 28, title, 13, c, MONO, "start", 600)
    d.t(x + 20, y + 48, sub, 11, MUTED, KR, "start")


layer(200, 100, 736, 360, "A", "비밀번호 헤더 검사 · 없으면 401 쓰고 반환", INFO)
layer(228, 170, 680, 262, "B", "start := time.Now() · 돌아오면 걸린 시간 기록", INFO)
layer(256, 240, 624, 164, "h", "", OK)
d.t(568, 322, "응답 작성", 14, OK, KR, "middle", 600)

# 요청 들어옴
d.arrow([(24, 300), (196, 300)], SOFT, "soft", 1.4)
d.t(30, 290, "요청", 12, MUTED, KR, "start", 600)
# 401 되돌아 나감
d.arrow([(198, 420), (30, 420)], ACC, "acc", 1.6)
d.t(30, 410, "401 · 비밀번호 헤더 없음", 12, ACC, KR, "start", 600)
d.t(568, 348, "200 · 응답", 12, MUTED, KR, "middle", 600)

d.legend(480, [("미들웨어 겹", INFO), ("실제 핸들러", OK), ("안쪽을 부르지 않고 반환", ACC)])
d.save("09-02.middleware-onion.svg")
print("ok 09-02 onion")
