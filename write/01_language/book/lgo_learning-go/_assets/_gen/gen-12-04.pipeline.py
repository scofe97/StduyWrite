# 12-04.pipeline — GatherAndProcess 는 A·B 를 동시에 부르고 둘이 모이면 C 를 부르며, 모두 50ms 제한 context 안에서 돈다
# 본문 요구(12-04 §1 「cProcessor」 끝 도식 문단): 흐름을 시간 순서로 보인다. start 가 A·B 고루틴을 띄우고, wait 가 outA·outB 를
#           select 로 둘 다 받은 뒤 C 를 띄우고 outC 를 받는다. errs 나 ctx.Done() 이 먼저 오면 그 자리에서 돌아간다.
# 타입 스펙: type-sequence — 레인 넷(GatherAndProcess · A 고루틴 · B 고루틴 · C 고루틴), 시간은 위→아래.
#           상태는 레인 옆 칩, focal 은 50ms 제한 칩 하나.
# 사실 출처: Learning Go 2판 12장 「Put Your Concurrent Tools Together」, 원서 예제 저장소 ch12 sample_code/pipeline 을 go1.25.1 로
#           A 지연·B 오류를 넣어 실행 — 80ms 지연은 context deadline exceeded, B 오류는 B failed (2026-09-28).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 590
d = Seq(W, H, "SEQUENCE · 12-04 §1",
        "A·B 는 동시에, C 는 둘이 모인 뒤에, 모두 50밀리초 안에",
        "GatherAndProcess 는 50밀리초에 시간이 넘는 context 를 만들고 abProcessor.start 로 A 와 B 를 부르는 고루틴 둘을 띄운다. "
        "abProcessor.wait 는 select 로 outA 와 outB 를 둘 다 받을 때까지 기다리고, errs 나 ctx.Done() 이 먼저 오면 바로 돌아간다. "
        "둘이 모이면 cProcessor.start 로 C 를 부르는 고루틴을 띄우고 wait 로 outC 를 받아 돌려준다.",
        lead="위에서 아래로 시간이 흐릅니다. 채널은 모두 버퍼가 있어 고루틴이 쓰고 바로 끝납니다.")
d.lanes([("GatherAndProcess", "ctx 50ms"), ("A 고루틴", "getResultA"), ("B 고루틴", "getResultB"), ("C 고루틴", "getResultC")], y0=96, lane_w=180)
d.rails(480)

d.state("GatherAndProcess", "WithTimeout 50ms", 176, ACC)
d.msg("GatherAndProcess", "A 고루틴", "start", 214)
d.msg("GatherAndProcess", "B 고루틴", "start", 250)
d.msg("B 고루틴", "GatherAndProcess", "outB", 290, SOFT, "soft", dash="5 4")
d.msg("A 고루틴", "GatherAndProcess", "outA", 326, SOFT, "soft", dash="5 4")
d.state("GatherAndProcess", "wait · 둘 다 모임", 362, INFO)
d.msg("GatherAndProcess", "C 고루틴", "start(cIn)", 398)
d.msg("C 고루틴", "GatherAndProcess", "outC", 434, SOFT, "soft", dash="5 4")
d.state("GatherAndProcess", "return COut", 470, OK)
d.t(24, 506, "errs · ctx.Done() 가 먼저 오면 wait 는 그 자리에서 반환", 11, WARN, KR, "start", 600)

d.legend(530, [("시간 제한", ACC), ("select 로 기다림", INFO), ("정상 반환", OK), ("조기 반환", WARN)])
d.save("12-04.pipeline.svg")
print("ok 12-04 pipeline")
