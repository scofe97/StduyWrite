# 타입 스펙: type-sequence
# 2절 슬롯 점유와 Channel 원격 호출 흐름 — Executor 슬롯 점유 후 CPS VM 스레드가 Channel.call 로 프로세스를 띄우고 감시 스케줄러가 결과 파일을 점검하는 왕복
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import (Seq, PAPER2, INK, MUTED, RULE, ACC,  # noqa: E402
                OK, INFO, KR, MONO)


def _kr(txt):
    """한글이 섞이면 한글 스택으로. Seq 프리미티브가 MONO 를 하드코딩하는 자리를 덮는다."""
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=164):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 48, PAPER2, RULE, 1.0)
            s.t(x, y0 + 21, nm, 14, INK, _kr(nm), "middle", 600)
            sub_sz = 12 if _kr(sub) == MONO and len(str(sub)) > 16 else 13
            s.t(x, y0 + 40, sub, sub_sz, MUTED, _kr(sub))
        s.lane_top = y0 + 48
        return s.LX

    def act(s, a, y1, y2):
        x = s.LX[a]
        s.o.append(f'<rect x="{x - 4}" y="{y1}" width="8" height="{y2 - y1}" '
                   f'fill="{INK}10" stroke="{MUTED}" stroke-width="0.8"/>')

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 10, label, 13, c, _kr(label), "middle", 600)
        if sub:
            sub_sz = 12 if _kr(sub) == MONO and len(str(sub)) > 15 else 13
            s.t(mx, y + 20, sub, sub_sz, MUTED, _kr(sub))

    def state(s, a, txt, y, c):
        x = s.LX[a]
        han = sum(1 for ch in str(txt) if "가" <= ch <= "힣")
        w = han * 13.0 + (len(txt) - han) * 7.8 + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" '
                   f'fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 5, txt, 13, c, _kr(txt))


W, H = 960, 824

d = SeqKR(
    W, H,
    "JENKINS · STEP ROUNDTRIP OVER CHANNEL",
    "슬롯 배정에서 빌드 프로세스 회신까지의 왕복",
    "Queue 가 Executor 슬롯에 PlaceholderTask 를 배정하고 스레드를 놓은 뒤 Controller 의 CPS VM 스레드가 Channel.call 로 Agent 에 프로세스를 띄우고 감시 스케줄러가 결과 파일을 점검하는 순서",
    lead="슬롯 점유 뒤 CPS VM 스레드가 프로세스를 띄우고 감시 스케줄러가 결과 파일을 점검하는 왕복"
)

d.lanes([
    ("Queue", "대기열"),
    ("Executor 슬롯", "Controller JVM"),
    ("Controller 스레드", "CPS VM · 감시 스케줄러"),
    ("Agent JVM", "remoting.jar"),
    ("빌드 프로세스", "sh · OS 자식"),
], y0=104, lane_w=164)

d.rails(740)
# Executor 슬롯이 스레드를 놓은 뒤 완료 콜백까지 점유 상태를 유지함을 활성화 막대로 표시
d.act("Executor 슬롯", 332, 660)

y = 184
d.msg("Queue", "Executor 슬롯", "슬롯 배정", y, INFO, "info", sub="PlaceholderTask")

y = 228
d.state("Executor 슬롯", "1. RemoteLauncher", y, INFO)

y = 264
d.state("Executor 슬롯", "2. ws 임대", y, INFO)

y = 320
d.msg("Executor 슬롯", "Controller 스레드", "2. 본문 위임", y, INFO, "info", sub="스레드 반환 · 슬롯 유지")

y = 372
d.state("Controller 스레드", "3. RemoteLaunchCallable", y, INFO)

y = 428
d.msg("Controller 스레드", "Agent JVM", "4. Channel.call", y, ACC, "acc", sub="CPS VM 스레드 · Callable 전송")

y = 488
d.msg("Agent JVM", "빌드 프로세스", "4. 프로세스 시작", y, INFO, "info", sub="LocalLauncher")

y = 548
d.msg("빌드 프로세스", "Agent JVM", "5. 결과 파일 기록", y, OK, "ok", dash="5 4", sub="jenkins-result.txt")

y = 608
d.msg("Agent JVM", "Controller 스레드", "5. 결과 전달", y, OK, "ok", dash="5 4", sub="감시 스케줄러 · watch · 폴링")

y = 668
d.msg("Controller 스레드", "Executor 슬롯", "슬롯 해제", y, OK, "ok", dash="5 4", sub="Callback.finished")

y = 716
d.state("Executor 슬롯", "슬롯 반납", y, OK)

d.legend(768, [
    ("Controller · 시작", INFO),
    ("원격 Callable 전송", ACC),
    ("종료 코드 · 회신", OK),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "01-03.step-roundtrip.svg")
d.save(out_path)
print(f"saved: {out_path}")
