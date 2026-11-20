# 사실 출처: internal/runtime/wasi.go:45,54-59,76-87,89,96-104 · internal/runtime/protocol.go:27,30,31 · README.md:206-211
# 타입 스펙: type-data-flow
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 560
d = D(
    W, H,
    "DATA FLOW · WASI PREVIEW1 I/O PIPELINE",
    "WASI 핸들러 입출력 파이프라인 — stdin JSON 요청과 stdout JSON 응답",
    "호스트는 표준 스트림(fd 0/1)만 연결하고 외부 파일시스템과 임의 모듈 import를 거부합니다",
    lead="요청마다 새 인스턴스를 띄우고(preview1 command) stdin으로 요청을 밀어 넣은 뒤 stdout 응답을 회수합니다"
)

# 구획 (Zone)
def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="4 4"/>')
    d.t(x + 16, y + 20, label, 11, SOFT, KR, "start", 600)

zone(24, 104, 270, 396, "호스트 런타임 (wazero Engine)")
zone(320, 104, 360, 396, "WASI 프리뷰1 인스턴스 (신뢰하지 않는 코드)")
zone(706, 104, 270, 396, "응답 수신 및 결과 반환")

# 1. 호스트 요청 스트림 준비 (좌측)
REQ_X, REQ_Y, REQ_W, REQ_H = 40, 150, 238, 70
d.tone(REQ_X, REQ_Y, REQ_W, REQ_H, INFO, 6, "14", 1.2)
d.t(REQ_X + 14, REQ_Y + 24, "요청 JSON 직렬화", 12, INFO, KR, "start", 600)
d.t(REQ_X + 14, REQ_Y + 46, "bytes.NewReader(req)", 11, INK, MONO, "start")

IMPORT_X, IMPORT_Y, IMPORT_W, IMPORT_H = 40, 260, 238, 120
d.tone(IMPORT_X, IMPORT_Y, IMPORT_W, IMPORT_H, BAD, 6, "12", 1.1)
d.t(IMPORT_X + 14, IMPORT_Y + 26, "모듈 Import 검증", 12, BAD, KR, "start", 600)
d.t(IMPORT_X + 14, IMPORT_Y + 48, "wasi_snapshot_preview1 만 허용", 11, INK, KR, "start")
d.t(IMPORT_X + 14, IMPORT_Y + 70, "다른 모듈 import 발견 시 거부", 10, BAD, KR, "start")
d.t(IMPORT_X + 14, IMPORT_Y + 92, "wasi.go:54-59 에러 반환", 10, MUTED, MONO, "start")

# 2. WASI 인스턴스 내부 (중앙)
STDIN_X, STDIN_Y, STDIN_W, STDIN_H = 340, 150, 320, 70
d.box(STDIN_X, STDIN_Y, STDIN_W, STDIN_H, PAPER2, RULE, 1.0)
d.t(STDIN_X + 14, STDIN_Y + 24, "표준 입력 (fd 0 stdin)", 12, INK, KR, "start", 600)
d.t(STDIN_X + 14, STDIN_Y + 48, "WithStdin(bytes.NewReader(req))", 11, INFO, MONO, "start")

EXEC_X, EXEC_Y, EXEC_W, EXEC_H = 340, 256, 320, 80
d.tone(EXEC_X, EXEC_Y, EXEC_W, EXEC_H, OK, 6, "14", 1.2)
d.t(EXEC_X + 14, EXEC_Y + 24, "_start 진입점 실행", 12, OK, KR, "start", 600)
d.t(EXEC_X + 14, EXEC_Y + 46, "fd_read(0, ...) 로 JSON 디코딩", 11, INK, MONO, "start")
d.t(EXEC_X + 14, EXEC_Y + 66, "DefaultTimeout = 10s 강제", 10, WARN, MONO, "start")

STDOUT_X, STDOUT_Y, STDOUT_W, STDOUT_H = 340, 370, 320, 70
d.box(STDOUT_X, STDOUT_Y, STDOUT_W, STDOUT_H, PAPER2, RULE, 1.0)
d.t(STDOUT_X + 14, STDOUT_Y + 24, "표준 출력 (fd 1 stdout)", 12, INK, KR, "start", 600)
d.t(STDOUT_X + 14, STDOUT_Y + 48, "fd_write(1, ...) 로 응답 JSON 출력", 11, ACC, MONO, "start")

# 3. 응답 버퍼 및 완료 (우측)
RESP_X, RESP_Y, RESP_W, RESP_H = 722, 260, 238, 80
d.tone(RESP_X, RESP_Y, RESP_W, RESP_H, ACC, 6, "14", 1.2)
d.t(RESP_X + 14, RESP_Y + 24, "출력 버퍼링 (capWriter)", 12, ACC, KR, "start", 600)
d.t(RESP_X + 14, RESP_Y + 46, "WithStdout(out)", 11, INK, MONO, "start")
d.t(RESP_X + 14, RESP_Y + 66, "MaxResponseBody = 32 MiB", 10, MUTED, MONO, "start")

DONE_X, DONE_Y, DONE_W, DONE_H = 722, 370, 238, 70
d.box(DONE_X, DONE_Y, DONE_W, DONE_H, PAPER2, RULE, 1.0)
d.t(DONE_X + 14, DONE_Y + 24, "HTTP 응답 반환", 12, INK, KR, "start", 600)
d.t(DONE_X + 14, DONE_Y + 48, "wasiEngine.handle 완료", 11, OK, MONO, "start")

# 화살표 연결
# 1 -> stdin (수평)
d.arrow([(REQ_X + REQ_W, REQ_Y + 35), (STDIN_X, STDIN_Y + 35)], INFO, "info", 1.4)
d.t(309, REQ_Y + 25, "주입", 10, INFO, KR, "middle")

# stdin -> exec (수직)
d.arrow([(STDIN_X + STDIN_W // 2, STDIN_Y + STDIN_H), (STDIN_X + STDIN_W // 2, EXEC_Y)], INFO, "info", 1.4)

# exec -> stdout (수직)
d.arrow([(EXEC_X + EXEC_W // 2, EXEC_Y + EXEC_H), (EXEC_X + EXEC_W // 2, STDOUT_Y)], ACC, "acc", 1.4)

# stdout -> capWriter (직각 꺾은선)
d.arrow([(STDOUT_X + STDOUT_W, STDOUT_Y + 35), (700, STDOUT_Y + 35), (700, RESP_Y + 40), (RESP_X, RESP_Y + 40)], ACC, "acc", 1.4)
d.t(690, STDOUT_Y + 25, "회수", 10, ACC, KR, "middle")

# capWriter -> done (수직)
d.arrow([(RESP_X + RESP_W // 2, RESP_Y + RESP_H), (RESP_X + RESP_W // 2, DONE_Y)], OK, "ok", 1.4)

# stderr 보조 표시
d.t(EXEC_X + EXEC_W // 2, 460, "stderr (fd 2) → lineWriter(level: error)", 10, MUTED, MONO, "middle")

# 범례
d.legend(H - 44, [
    ("요청 스트림 주입", INFO),
    ("격리 인스턴스 실행", OK),
    ("응답 바이트 수신", ACC),
    ("미인가 권한 거부", BAD)
])

out_path = Path(__file__).parent.parent / "02-01-wasi-io.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
