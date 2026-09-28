# 15-01.test-lifecycle — TestMain 은 패키지에 한 번 불려 m.Run 으로 테스트를 돌리고, 테스트 하나의 Cleanup 은 등록 역순으로 돈다
# 본문 요구(15-01 §2 「TestMain 은 패키지에 한 번 돌고 m.Run 의 결과로 끝납니다」「Cleanup 은 도우미 함수가 정리를 등록하게 합니다」):
#           go test 가 TestMain 을 부르고, TestMain 은 준비 → m.Run → 정리 순서로 돈다. 테스트 하나는 Cleanup 을 등록하고, 본문이 끝나면
#           t.Context 가 취소된 뒤 등록 역순으로 정리 함수가 돈다. TestMain 이 반환하면 Go 1.15 부터 m.Run 의 값으로 os.Exit 가 불린다.
# 타입 스펙: type-sequence — 레인 셋(go test · TestMain · 테스트 하나), 시간은 위→아래, 메시지는 수평 화살표, 상태는 레인 칩.
#           stride: 행 간격 36~46. focal 은 역순으로 도는 정리 칩 하나.
# 사실 출처: Learning Go 2판 15장 「Setting Up and Tearing Down」, Go 1.15·1.24 릴리스 노트, go1.27.1 실행(2026-09-28) —
#           testmain 출력, cleanup 2 → cleanup 1, t.Context Err 는 본문 nil · 정리 안 context canceled.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, PAPER, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 620
d = Seq(W, H, "SEQUENCE · 15-01 §2",
        "TestMain 은 패키지 테스트를 한 번 감싸고 Cleanup 은 테스트마다 거꾸로 돕니다",
        "go test 가 TestMain 을 한 번 부른다. TestMain 은 패키지 변수를 준비한 뒤 m.Run 으로 테스트 함수들을 돌린다. "
        "테스트 하나는 t.Cleanup 으로 정리 함수 둘을 등록하고, 본문이 끝나면 t.Context 가 먼저 취소된 뒤 나중에 등록한 정리부터 거꾸로 돈다. "
        "m.Run 이 종료 코드를 돌려주면 TestMain 이 정리하고 반환하며, Go 1.15 부터는 반환만 해도 그 값으로 os.Exit 가 불린다.",
        lead="위에서 아래로 시간이 흐릅니다. 테스트 함수가 여럿이면 가운데 묶음이 테스트마다 되풀이됩니다.")
d.lanes([("go test", "테스트 바이너리"), ("TestMain", "*testing.M"), ("테스트 하나", "*testing.T")], y0=96, lane_w=210)
d.rails(548)


def state(key, txt, y, c):
    # Seq.state 는 반투명 칩이라 레일이 비치고 한글 폭을 작게 어림한다 — 불투명 바탕과 글자별 폭으로 다시 그린다
    x = d.LX[key]
    w = sum(11.0 if "가" <= ch <= "힣" else 6.9 for ch in txt) + 24
    d.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{PAPER}"/>')
    d.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
    d.t(x, y + 4, txt, 11, c, MONO, "middle", 600)


d.msg("go test", "TestMain", "TestMain(m)", 188)
d.selfmsg("TestMain", "준비", 232, sub="testTime = time.Now()")
d.msg("TestMain", "테스트 하나", "m.Run()", 284)
state("테스트 하나", "t.Cleanup(1) · t.Cleanup(2)", 320, INFO)
state("테스트 하나", "본문 끝 · t.Context 취소", 360, WARN)
state("테스트 하나", "cleanup 2 → cleanup 1", 400, ACC)
d.msg("테스트 하나", "TestMain", "종료 코드 0 · 1", 444, MUTED, "ar", dash="5 4")
d.selfmsg("TestMain", "정리", 484)
d.msg("TestMain", "go test", "반환", 528, OK, "ok", sub="Go 1.15+ 그 값으로 os.Exit")

d.legend(572, [("등록", INFO), ("취소 알림", WARN), ("역순 정리", ACC), ("종료", OK)])
d.save("15-01.test-lifecycle.svg")
print("ok 15-01 lifecycle")
