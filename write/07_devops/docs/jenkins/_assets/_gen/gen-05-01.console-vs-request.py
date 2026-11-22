# 타입 스펙: type-flowchart
# 4절 Script Console 의 권한과 위험 — 웹 UI·REST 요청과 Script Console 경로의 권한 검사 및 실행 범위 비교
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 452

d = D(W, H, "JENKINS · SCRIPT CONSOLE VS REQUEST",
      "웹 UI·REST 요청과 Script Console 경로 비교",
      "웹 UI·REST 의 매 요청 권한 검사와 Script Console 의 1회 진입 후 임의 코드 실행 범위 비교",
      lead="웹 UI·REST: 요청마다 권한 대조 후 정해진 동작 vs Script Console: 진입 후 보안 통제 없이 실물 객체 직접 조작")

# ── 1. 웹 UI · REST 요청 경로 (상단) ───────────────────────────────────
Y1 = 145
d.t(28, 108, "웹 UI · REST 요청 경로 (바깥 문)", 12, INK, KR, "start", 600)

# Col 0: 시작 (Oval rx=20)
d.box(28, 122, 140, 46, PAPER2, RULE, 1.0, 20)
d.t(98, 141, "웹 UI · REST", 13, INK, KR, "middle", 600)
d.t(98, 157, "개별 요청 진입", 12, MUTED, KR, "middle")

d.arrow([(168, Y1), (214, Y1)], SOFT, "soft", 1.2)

# Col 1: 판단 (Diamond dw=128, dh=52)
d.o.append(f'<path d="M 280 119 L 344 {Y1} L 280 171 L 216 {Y1} Z" fill="{PAPER2}" stroke="{RULE}" stroke-width="1.0"/>')
d.t(280, 141, "권한 검사", 13, INK, KR, "middle", 600)
d.t(280, 157, "요청마다 대조", 12, MUTED, KR, "middle")

# Col 1 -> 미승인 (Exit 1: 아래)
d.arrow([(280, 171), (280, 194)], BAD, "bad", 1.2)
d.t(270, 186, "미승인", 12, BAD, KR, "end")
d.box(225, 196, 110, 32, PAPER2, BAD, 1.0, 16)
d.t(280, 216, "요청 차단", 12, BAD, KR, "middle")

# Col 1 -> 승인 (Exit 2: 오른쪽)
d.arrow([(344, Y1), (390, Y1)], OK, "ok", 1.2)
d.t(368, 134, "승인", 12, OK, KR, "middle")

# Col 2: 단계 (Rectangle rx=6)
d.box(392, 122, 180, 46, PAPER2, RULE, 1.0, 6)
d.t(482, 141, "허용된 API 실행", 13, INK, KR, "middle", 600)
d.t(482, 157, "바깥 문 엔드포인트", 12, MUTED, KR, "middle")

d.arrow([(572, Y1), (626, Y1)], OK, "ok", 1.2)
d.t(600, 134, "한정 범위", 12, MUTED, KR, "middle")

# Col 3: 결과 범위 (좁은 범위)
d.tone(628, 122, 304, 46, OK, 6, "12", 1.1)
d.t(780, 141, "허용된 API 호출만 수행", 13, OK, KR, "middle", 600)
d.t(780, 157, "바깥 문 · Controller 객체 보호", 12, MUTED, KR, "middle")


# ── 2. Script Console 경로 (하단) ──────────────────────────────────────
Y2 = 291
d.t(28, 254, "Script Console 경로 (안방)", 12, INK, KR, "start", 600)

# Col 0: 시작 (Oval rx=20)
d.box(28, 268, 140, 46, PAPER2, RULE, 1.0, 20)
d.t(98, 287, "Script Console", 13, INK, MONO, "middle", 600)
d.t(98, 303, "관리자 콘솔 접속", 12, MUTED, KR, "middle")

d.arrow([(168, Y2), (214, Y2)], SOFT, "soft", 1.2)

# Col 1: 판단 (Diamond dw=128, dh=52)
d.o.append(f'<path d="M 280 265 L 344 {Y2} L 280 317 L 216 {Y2} Z" fill="{PAPER2}" stroke="{RULE}" stroke-width="1.0"/>')
d.t(280, 287, "Administer", 13, INK, MONO, "middle", 600)
d.t(280, 303, "최초 1회 검사", 12, MUTED, KR, "middle")

# Col 1 -> 미승인 (Exit 1: 아래)
d.arrow([(280, 317), (280, 340)], BAD, "bad", 1.2)
d.t(270, 332, "미승인", 12, BAD, KR, "end")
d.box(225, 342, 110, 32, PAPER2, BAD, 1.0, 16)
d.t(280, 362, "접근 차단", 12, BAD, KR, "middle")

# Col 1 -> 통과 (Exit 2: 오른쪽)
d.arrow([(344, Y2), (390, Y2)], ACC, "acc", 1.2)
d.t(368, 280, "통과", 12, ACC, KR, "middle")

# Col 2: 단계 (Rectangle rx=6 - Focal 1곳!)
d.tone(392, 268, 180, 46, ACC, 6, "18", 1.4)
d.t(482, 287, "임의 스크립트 실행", 13, ACC, KR, "middle", 600)
d.t(482, 303, "보안 통제 없음", 12, MUTED, KR, "middle")

# Col 3: 결과 범위 (넓은 범위 — 임의 조작 3갈래 확장)
d.arrow([(572, Y2), (600, Y2), (600, 252), (626, 252)], WARN, "warn", 1.2)
d.arrow([(572, Y2), (626, Y2)], WARN, "warn", 1.2)
d.arrow([(572, Y2), (600, Y2), (600, 330), (626, 330)], WARN, "warn", 1.2)

# Card 1: 크레덴셜 복호화
d.tone(628, 236, 304, 32, WARN, 6, "10", 1.0)
d.t(640, 256, "크레덴셜 복호화 API 직접 호출", 12, WARN, KR, "start", 600)

# Card 2: 메모리 실물 객체 수정
d.tone(628, 275, 304, 32, WARN, 6, "10", 1.0)
d.t(640, 295, "JVM 메모리 실물 객체 직접 수정", 12, WARN, KR, "start", 600)

# Card 3: 영속화 및 락 제어
d.tone(628, 314, 304, 32, WARN, 6, "10", 1.0)
d.t(640, 334, "instance.save() · Queue.withLock", 12, WARN, MONO, "start", 600)


# ── 3. 범례 ────────────────────────────────────────────────────────────
d.legend(404, [
    ("정의된 정상 동작", OK),
    ("임의 스크립트 실행", ACC),
    ("통제 우회 · 직접 조작", WARN),
    ("검사 불일치 차단", BAD)
])

d.save("05-01.console-vs-request.svg")
print("ok 05-01.console-vs-request.svg")
