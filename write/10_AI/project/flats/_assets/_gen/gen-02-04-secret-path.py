# 사실 출처: internal/core/secrets.go:18-20,24-48,57,63,103-105,109-115,127-157,171-185,190-204 · internal/core/env.go:14-33,78-117 · internal/store/store.go:290 · internal/runtime/protocol.go:50-51,59 · docs/design.md 「Secrets」
# 타입 스펙: type-data-flow
import os
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 520
d = D(
    W, H,
    "SECRETS LIFECYCLE · STORAGE & INJECTION FLOW",
    "비밀(secret) 암호화 저장 및 워커 주입 데이터 흐름",
    "운영자 설정에서 AES-256-GCM 봉인, flats.db 보관, 스냅샷 복호화 및 워커 전달 파이프라인",
    lead="비밀값은 OS 환경변수나 인자로 노출되지 않고 오직 표준 입력(stdin)의 JSON 명세로만 안전하게 전달됩니다"
)

# 4개 열 헤더
COL_W = 190
C1_X = 24
C2_X = 264
C3_X = 504
C4_X = 744

headers = [
    (C1_X, "1. 운영자 입력 및 검증", "CLI · 콘솔 루프백 전용"),
    (C2_X, "2. 호스트 키 봉인", "AES-256-GCM 암호화"),
    (C3_X, "3. 활성화 시점 복호화", "captureEnvironment 스냅샷"),
    (C4_X, "4. 워커 격리 주입", "stdin JSON 스트림 주입")
]

for x, title, sub in headers:
    d.t(x + COL_W / 2, 114, title, 12, INK, KR, "middle", 600)
    d.t(x + COL_W / 2, 132, sub, 10, MUTED, MONO, "middle")

# 1열: 입력원 및 API 접근 제한
d.box(C1_X, 160, COL_W, 220, fill=PAPER2, stroke=INFO, sw=1.2)
d.t(C1_X + COL_W / 2, 186, "SetSecret 권한 통제", 12, INFO, KR, "middle", 600)
d.line(C1_X + 12, 198, C1_X + COL_W - 12, 198, RULE, 0.8)

# 상단: 운영자 쓰기 명령
d.box(C1_X + 10, 206, COL_W - 20, 76, fill=PAPER, stroke=OK, sw=0.9, r=4)
d.t(C1_X + 18, 222, "flats secret set", 10.5, OK, MONO, "start", 600)
d.t(C1_X + 18, 237, "ViaCLI · ViaConsole 만 허용", 9.5, INK, KR, "start")
d.t(C1_X + 18, 251, "헤더 식별 · 로컬 셸 프로세스는 못 막음", 8.2, WARN, KR, "start")
d.t(C1_X + 18, 265, "이름 ≤64자 · 값 ≤64 KiB", 8.5, MUTED, KR, "start")

# 하단: 원격/에이전트 차단
d.box(C1_X + 10, 294, COL_W - 20, 72, fill=PAPER, stroke=WARN, sw=0.9, r=4)
d.t(C1_X + 18, 314, "SecretNames 조회", 11, WARN, MONO, "start", 600)
d.t(C1_X + 18, 332, "API · MCP는 이름만 반환", 10, INK, KR, "start")
d.t(C1_X + 18, 350, "평문 값 원격 유출 차단", 9, MUTED, KR, "start")

# 화살표 1 -> 2
d.arrow([(C1_X + COL_W, 246), (C2_X, 246)], c=INFO, m="info")

# 2열: AES-256-GCM 암호화 및 영속화
d.box(C2_X, 160, COL_W, 220, fill=PAPER2, stroke=ACC, sw=1.4)
d.t(C2_X + COL_W / 2, 186, "호스트 키 봉인", 12, ACC, KR, "middle", 600)
d.line(C2_X + 12, 198, C2_X + COL_W - 12, 198, RULE, 0.8)

# 2열 상단: secret.key
d.box(C2_X + 10, 210, COL_W - 20, 72, fill=PAPER, stroke=ACC, sw=0.9, r=4)
d.t(C2_X + 18, 230, "<data>/secret.key", 11, ACC, MONO, "start", 600)
d.t(C2_X + 18, 248, "권한 0600 · 32바이트", 10, INK, KR, "start")
d.t(C2_X + 18, 264, "분실 시 복구 불가 (백업 필수)", 9, MUTED, KR, "start")

# 2열 하단: flats.db 저장
d.box(C2_X + 10, 294, COL_W - 20, 72, fill=PAPER, stroke=RULE, sw=0.9, r=4)
d.t(C2_X + 18, 314, "flats.db 영속화", 11, INK, KR, "start", 600)
d.t(C2_X + 18, 332, "table: secrets", 10, MUTED, MONO, "start")
d.t(C2_X + 18, 350, "Nonce 12B · AAD=이름", 9, SOFT, MONO, "start")

# 화살표 2 -> 3
d.arrow([(C2_X + COL_W, 246), (C3_X, 246)], c=ACC, m="acc")

# 3열: 활성화 스냅샷 및 복호화
d.box(C3_X, 160, COL_W, 220, fill=PAPER2, stroke=RULE, sw=1.2)
d.t(C3_X + COL_W / 2, 186, "스냅샷 캡처 시점", 12, INK, KR, "middle", 600)
d.line(C3_X + 12, 198, C3_X + COL_W - 12, 198, RULE, 0.8)

# 3열 상단: 캡처 계기
d.box(C3_X + 10, 210, COL_W - 20, 72, fill=PAPER, stroke=OK, sw=0.9, r=4)
d.t(C3_X + 18, 230, "반영 시점 (Activation)", 11, OK, KR, "start", 600)
d.t(C3_X + 18, 248, "배포·재배포·롤백·복원·재시작·미리보기", 8.2, INK, KR, "start")
d.t(C3_X + 18, 264, "실행 중 워커는 즉시 안 바뀜", 9, WARN, KR, "start")

# 3열 하단: decryptSecrets
d.box(C3_X + 10, 294, COL_W - 20, 72, fill=PAPER, stroke=INFO, sw=0.9, r=4)
d.t(C3_X + 18, 314, "decryptSecrets", 11, INFO, MONO, "start", 600)
d.t(C3_X + 18, 332, "메모리 상에서만 일시 복호화", 10, INK, KR, "start")
d.t(C3_X + 18, 350, "newRedactor 로그 마스킹", 9, MUTED, MONO, "start")

# 화살표 3 -> 4
d.arrow([(C3_X + COL_W, 246), (C4_X, 246)], c=OK, m="ok")

# 4열: 워커 격리 주입 및 노출
d.box(C4_X, 160, COL_W, 220, fill=PAPER2, stroke=OK, sw=1.4)
d.t(C4_X + COL_W / 2, 186, "워커 샌드박스 주입", 12, OK, KR, "middle", 600)
d.line(C4_X + 12, 198, C4_X + COL_W - 12, 198, RULE, 0.8)

# 4열 상단: stdin 주입
d.box(C4_X + 10, 210, COL_W - 20, 72, fill=PAPER, stroke=OK, sw=0.8, r=4)
d.t(C4_X + 18, 230, "stdin 1회성 JSON", 11, OK, MONO, "start", 600)
d.t(C4_X + 18, 248, "workerSpec.Env 필드", 10, INK, MONO, "start")
d.t(C4_X + 18, 264, "cmd.Env=[] · ps 노출 차단", 9, MUTED, KR, "start")

# 4열 하단: 런타임 접근
d.box(C4_X + 10, 294, COL_W - 20, 72, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(C4_X + 18, 314, "런타임 코드 접근", 11, INK, KR, "start", 600)
d.t(C4_X + 18, 332, "JS: env.SECRET_NAME", 10, INK, MONO, "start")
d.t(C4_X + 18, 350, "WASI: 게스트 환경변수", 9, MUTED, KR, "start")

# 하단 범례
d.legend(456, [
    ("운영자 쓰기 통제", INFO),
    ("AES-256-GCM 마스터 키 봉인", ACC),
    ("배포 스냅샷 캡처", OK),
    ("조회 제한 및 갱신 지연", WARN)
])

out_path = _HERE.parent / "02-04-secret-path.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
