# 15-02.parallel-pause — 병렬 하위 테스트는 t.Parallel 에서 멈추고, 부모 테스트 함수가 반환한 뒤에 돌아 그때의 d 를 본다
# 본문 요구(15-02 §2 「Go 1.21 이하 의미에서는 병렬 하위 테스트가 마지막 사례만 봅니다」): t.Run 은 하위 테스트가 t.Parallel 을
#           부르면 돌아오고, 하위 테스트는 PAUSE 한다. 부모 함수가 반환한 뒤(이 예제는 반복문이 함수의 끝이라 d 가 마지막 사례일 때) 셋이 CONT 해 모두 50 60 을 찍는다.
#           go 지시어가 1.22 이상이면 반복마다 새 d 라 10 20 · 30 40 · 50 60 이다.
# 타입 스펙: type-sequence — 레인 넷(부모 함수 · 하위 a · b · c), 시간은 위→아래. t.Run 화살표 라벨은 출발 레인 옆에 둬 다른 레인 레일과
#           겹치지 않게 한다. focal 은 go 1.21 이하 결과 줄 하나.
# 사실 출처: Learning Go 2판 15장 「Running Tests Concurrently」, testing 문서(Run·Parallel), go1.27.1 실행(2026-09-28) —
#           go 1.19 모듈 -v 출력 PAUSE a·b·c 뒤 CONT a·b·c 각 50 60, go 1.25 사본 10 20 · 30 40 · 50 60.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, PAPER, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 640
d = Seq(W, H, "SEQUENCE · 15-02 §2",
        "병렬 하위 테스트는 부모 함수가 끝날 때까지 멈췄다가 그때의 d 를 봅니다",
        "TestParallelTable 의 반복문이 사례마다 t.Run 을 부른다. 하위 테스트는 첫 줄의 t.Parallel 에서 멈추고(PAUSE) t.Run 이 돌아와 반복문이 다음 사례로 간다. "
        "세 사례를 다 돌고 부모 테스트 함수가 반환하면 하위 테스트 셋이 다시 돈다(CONT). 이 예제는 반복문이 함수의 끝이다. go 지시어가 1.21 이하면 변수 d 가 하나라 셋 모두 마지막 사례 50 60 을 보고, "
        "1.22 이상이면 반복마다 새 d 라 각자 제 사례를 본다.",
        lead="위에서 아래로 시간이 흐릅니다. 가로 화살표는 t.Run 호출, 칩은 하위 테스트의 상태입니다.")
d.lanes([("부모 함수", "for _, d := range data"), ("하위 a", "{10, 20}"), ("하위 b", "{30, 40}"), ("하위 c", "{50, 60}")], y0=96, lane_w=180)
d.rails(464)


def state(key, txt, y, c):
    # Seq.state 는 반투명 칩이라 레일이 비치고 한글 폭을 작게 어림한다 — 불투명 바탕과 글자별 폭으로 다시 그린다
    x = d.LX[key]
    w = sum(11.0 if "가" <= ch <= "힣" else 6.9 for ch in txt) + 24
    d.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{PAPER}"/>')
    d.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
    d.t(x, y + 4, txt, 11, c, MONO, "middle", 600)


def run(to, name, y):
    x1, x2 = d.LX["부모 함수"], d.LX[to]
    d.path(f"M {x1+10} {y} L {x2-12} {y}", MUTED, 1.4, m="ar")
    d.t(x1 + 16, y - 9, f"t.Run(\"{name}\")", 11, MUTED, MONO, "start", 600)

run("하위 a", "a", 188); state("하위 a", "PAUSE", 220, WARN)
run("하위 b", "b", 260); state("하위 b", "PAUSE", 292, WARN)
run("하위 c", "c", 332); state("하위 c", "PAUSE", 364, WARN)
state("부모 함수", "반환 · 이때 d = c", 404, INFO)
for k in ("하위 a", "하위 b", "하위 c"):
    state(k, "CONT · d 를 읽음", 444, INFO)
d.line(24, 476, W - 48, 476, RULE, 0.8, "4 4")
d.t(24, 520, "go 1.21 이하", 12, ACC, KR, "start", 600)
d.t(160, 520, "셋 다 50 60 — toTest(50) = 60 이라 PASS 로 가려짐", 12, ACC, KR, "start", 600)
d.t(24, 552, "go 1.22 이상", 12, OK, KR, "start", 600)
d.t(160, 552, "10 20 · 30 40 · 50 60 — 사례마다 새 d", 12, OK, KR, "start", 600)

d.legend(584, [("멈춤", WARN), ("다시 돎", INFO), ("옛 의미의 결과", ACC), ("새 의미의 결과", OK)])
d.save("15-02.parallel-pause.svg")
print("ok 15-02 parallel")
