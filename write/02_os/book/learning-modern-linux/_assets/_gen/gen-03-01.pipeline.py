# 03-01 §2 「파이프라인이 실제로 이어지는 방식」 — 10 GB 로그에서 ERROR 5줄을 뽑는 동작 흐름.
# 사실 출처:
# 1. pipe(7): "Since Linux 2.6.11, the pipe capacity is 16 pages (i.e., 65,536 bytes in a system with a page size of 4096 bytes)",
#    "If the pipe is full, then a write(2) will block",
#    "If all file descriptors referring to the read end of a pipe have been closed, then a write(2) will cause a SIGPIPE signal".
# 2. signal(7): SIGPIPE 는 13번, 기본 동작 Term. bash(1): 시그널 n 으로 죽으면 128+n → 141.
# 3. 실측(학습 세션, OrbStack Ubuntu 26.04.1 · bash 5.3.9, 10 GB 대신 300 MB 파일):
#    모든 줄이 ERROR 이면 PIPESTATUS=141 141 0, 앞 5줄만 ERROR 이면 0 0 0 (끝까지 읽음, real 0.087s).
#    재측정(2026-11-11, 같은 환경 · GNU grep 3.12, 300 MB): 모든 줄 ERROR 141 141 0 (3회),
#    ERROR 5줄이 맨 앞 0 0 0 (3회), ERROR 5줄이 맨 끝 0 0 0 (3회).
# 4. GNU grep: 출력이 파이프일 때 블록 버퍼링을 적용하므로 출력이 다음 단계에 즉시 전달되지 않고 모아서 전달된다.
# 타입 스펙: type-sequence — 레인 다섯(cat · 파이프 1 · grep · 파이프 2 · head), 시간은 위→아래.
# 강조(ACC 상자)는 head 종료 뒤 역방향으로 번지는 시그널 도미노 한 곳. 독자에게 보이는 글자에는 강조 표시를 쓰지 않는다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, PAPER2, RULE, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, size=13):
        x1, x2 = s.LX[a], s.LX[b]
        dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 10, label, size, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 18, sub, 12, MUTED, _kr(sub), "middle")


W, H = 960, 1000
d = SeqKR(W, H, "LEARNING MODERN LINUX · 03-01 §2",
          "cat | grep | head 파이프라인의 내부 동작 흐름",
          "10 GB 로그에서 ERROR 5줄을 뽑는 cat, 파이프 1, grep, 파이프 2, head 5개 레인의 시퀀스. "
          "셋이 동시에 시작하고 64 KiB 파이프 버퍼를 사이에 두고 흐르며, head 가 끝나면 다음 write 마다 SIGPIPE 가 역방향으로 번져 141 141 0 으로 끝난다.",
          "프로세스는 동시에 뜨고, 버퍼가 속도를 조절하며, 종료 시그널은 역방향 도미노로 전파됩니다")

# 레인 배치: stride 188px, 폭 144px, 좌우 여백 균등 (모두 4의 배수)
LANES = [
    ("cat", "big.log (10 GB)"),
    ("파이프 1", "커널 버퍼 (64 KiB)"),
    ("grep", "ERROR 검색"),
    ("파이프 2", "커널 버퍼 (64 KiB)"),
    ("head", "-5 (5줄 요구)")
]
d.LX = {"cat": 104, "파이프 1": 292, "grep": 480, "파이프 2": 668, "head": 856}
LANE_W = 144
Y_LANE = 104

for nm, sub in LANES:
    x = d.LX[nm]
    d.box(x - LANE_W // 2, Y_LANE, LANE_W, 48, PAPER2, RULE, 1.0, 6)
    title_text = "grep ERROR" if nm == "grep" else ("head -5" if nm == "head" else nm)
    d.t(x, Y_LANE + 20, title_text, 13, INK, _kr(title_text), "middle", 600)
    d.t(x, Y_LANE + 38, sub, 12, MUTED, _kr(sub), "middle")

d.lane_top = Y_LANE + 48
d.rails(800)

# 1. 셋 동시 시작 (좌우 분할 선으로 중앙 칩과 충돌 방지)
d.line(104, 176, 416, 176, RULE, 1.0, "4 4")
d.line(544, 176, 856, 176, RULE, 1.0, "4 4")
d.chip(480, 176, "셋 동시 시작", MUTED, 13, 10)
d.t(104, 204, "로그 읽기 시작", 13, SOFT, KR)
d.t(480, 204, "필터링 대기", 13, SOFT, KR)
d.t(856, 204, "5줄 수신 대기", 13, SOFT, KR)

# 2. 정상 스트리밍과 버퍼 용량 제한
d.msg("cat", "파이프 1", "write (청크 단위)", 240, OK, "ok")
d.msg("파이프 1", "grep", "read (스트림)", 272, OK, "ok")
d.msg("grep", "파이프 2", "write (ERROR 선별)", 304, OK, "ok", sub="블록 버퍼링 후 쓰기")
d.msg("파이프 2", "head", "read (5줄까지)", 348, OK, "ok")
d.chip(480, 376, "파이프마다 64 KiB 까지만 · 10 GB 를 한 번에 올리지 않음", MUTED, 13, 10)

# 3. 파이프 1 가득 참과 쓰기 대기 (Backpressure)
d.chip(292, 412, "파이프 1 가득 참 (64 KiB)", WARN, 13, 8)
d.tone(99, 404, 10, 56, WARN, 2, op="33", sw=1.2)
d.t(118, 446, "cat 만 write 대기", 13, WARN, KR, "start")
d.path("M 302 456 L 468 456", OK, 1.4, m="ok")
d.t(386, 446, "grep 이 읽어 자리 확보", 13, OK, KR, "middle")
d.t(480, 488, "cat 만 대기 · grep·head 는 계속 실행", 13, MUTED, KR, "middle")

# 4. 강조: 역방향 시그널 도미노 (head 종료 → 다음 write 마다 SIGPIPE)
d.tone(24, 508, 912, 300, ACC, 8, op="0c", sw=1.4)
d.t(36, 528, "head 종료에서 시작하는 역방향 도미노", 13, ACC, KR, "start", 600)

# (1) head 5줄 수신 완료 후 종료
d.chip(856, 556, "종료 (0)", OK, 13, 8)
d.t(856, 582, "5줄 받음", 12, MUTED, KR)

# (2) head 가 끝나 파이프 2 읽는 끝이 닫힘
d.path("M 846 612 L 678 612", MUTED, 1.4, m="ar")
d.t(762, 602, "읽는 끝 닫힘", 13, MUTED, KR)

# (3) grep 이 다음에 쓸 때 SIGPIPE 를 받고 종료
d.path("M 658 644 L 490 644", BAD, 1.5, m="bad")
d.t(574, 634, "write 시 SIGPIPE (13)", 13, BAD, KR)
d.chip(480, 670, "종료 (141)", BAD, 13, 8)
d.t(480, 696, "128 + 13", 11, MUTED, MONO)

# (4) grep 이 끝나 파이프 1 읽는 끝이 닫힘
d.path("M 470 724 L 302 724", MUTED, 1.4, m="ar")
d.t(386, 714, "읽는 끝 닫힘", 13, MUTED, KR)

# (5) cat 이 다음에 쓸 때 SIGPIPE 를 받고 종료
d.path("M 282 756 L 114 756", BAD, 1.5, m="bad")
d.t(198, 746, "write 시 SIGPIPE (13)", 13, BAD, KR)
d.chip(104, 782, "종료 (141)", BAD, 13, 8)

# 5. PIPESTATUS 결과
d.t(104, 836, "141", 13, BAD, MONO, "middle", 600)
d.t(480, 836, "141", 13, BAD, MONO, "middle", 600)
d.t(856, 836, "0", 13, OK, MONO, "middle", 600)
d.chip(480, 864, "PIPESTATUS = 141 141 0", ACC, 13, 12)

# 6. 곁가지 (회색 상자)
d.box(160, 892, 640, 32, PAPER2, RULE, 0.8, 4)
d.t(480, 912, "ERROR 가 5줄뿐 → grep 끝까지 읽음 → 0 0 0", 13, SOFT, KR, "middle")

# 범례
d.legend(952, [("정상 스트림", OK), ("버퍼 가득 참 대기", WARN), ("SIGPIPE 종료", BAD), ("역방향 도미노", ACC)])

d.save("03-01.pipeline.svg")
print("ok 03-01.pipeline")
