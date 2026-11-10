# 05-01 §7 — cat /proc/... 호출 시 디스크 블록 없이 커널이 내용을 동적으로 직렬화하는 흐름.
# 타입 스펙: type-process — 프로세스 요청 → VFS → 커널 RAM 자료구조 참조 → 텍스트 직렬화 → 사용자 반환 흐름.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 580
d = D(W, H, "LEARNING MODERN LINUX · 05-01 §7",
      "가짜 파일시스템의 동적 내용 생성 흐름",
      "cat /proc/cpuinfo 실행 시 디스크 블록 I/O 없이 커널 RAM 상태를 "
      "그 시점에 직렬화해 돌려주는 온디맨드 읽기 과정.",
      "디스크 블록이 없다는 것이 가짜 파일시스템의 본질")

CW = 158
CH = 220
GAP = 14
X0 = 20
Y0 = 120

steps = [
    ("1. openat 호출", "fd 할당", INK, [
        ("명령", "cat /proc/cpuinfo", MONO, INK),
        ("시스템 콜", "openat(O_RDONLY)", MONO, INFO),
        ("반환", "fd = 3", MONO, OK),
        ("VFS 상태", "가상 dentry 연결", KR, SOFT),
    ]),
    ("2. read 진입", "VFS 라우팅", INFO, [
        ("시스템 콜", "read(3, buf, 131072)", MONO, INFO),
        ("핸들러", "proc_reg_read_iter()", MONO, INK),
        ("인터페이스", "seq_file 기반 순회", KR, MUTED),
        ("특징", "디스크 요청 전무", KR, ACC),
    ]),
    ("3. RAM 상태 조회", "자료구조 탐색", WARN, [
        ("대상", "CPU별 정보 구조체", KR, WARN),
        ("위치", "커널 주기억장치(RAM)", KR, INK),
        ("수집 정보", "프로세서별 항목", KR, MUTED),
        ("성격", "실시간 커널 변수", KR, SOFT),
    ]),
    ("4. 텍스트 직렬화", "온디맨드 렌더링", ACC, [
        ("함수", "seq_printf() 포맷", MONO, ACC),
        ("출력 크기", "2664바이트 생성", MONO, INK),
        ("복사", "커널 → 유저 버퍼", KR, MUTED),
        ("핵심", "읽는 순간 바이트 생성", KR, ACC),
    ]),
    ("5. stdout 출력", "사용자 화면 전달", OK, [
        ("시스템 콜", "write(1, buf, 2664)", MONO, OK),
        ("결과", "터미널 텍스트 표시", KR, INK),
        ("디스크 I/O", "0회 (물리 블록 없음)", KR, ACC),
        ("공간 점유", "디스크 용량 0 바이트", KR, MUTED),
    ]),
]

for i, (title, sub, col, items) in enumerate(steps):
    x = X0 + i * (CW + GAP)
    focal = (i == 3)
    if focal:
        d.o.append(f'<rect x="{x}" y="{Y0}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.5"/>')
    else:
        d.box(x, Y0, CW, CH, PAPER2, col, 1.1, 8)

    d.t(x + CW / 2, Y0 + 24, title, 13, col, KR, "middle", 600)
    d.t(x + CW / 2, Y0 + 44, sub, 11, SOFT, MONO, "middle")
    d.line(x + 10, Y0 + 54, x + CW - 10, Y0 + 54, RULE, 0.8)

    for j, (k, v, fam, c) in enumerate(items):
        iy = Y0 + 74 + j * 36
        d.box(x + 8, iy, CW - 16, 30, PAPER, RULE, 0.6, 4)
        d.t(x + 14, iy + 12, k, 11, SOFT, KR, "start")
        d.t(x + 14, iy + 26, v, 11, c, fam, "start", 600 if c == ACC else 400)

    if i < len(steps) - 1:
        nx = x + CW
        d.arrow([(nx, Y0 + CH / 2), (nx + GAP - 2, Y0 + CH / 2)], MUTED, "ar", 1.4)

# 하단 일반 파일시스템 vs 가짜 파일시스템 비교 카드
BY = 368
BW = W - 40
BH = 130
d.box(X0, BY, BW, BH, PAPER2, RULE, 1.0, 8)
d.t(X0 + 20, BY + 26, "물리 블록 기반 파일시스템 vs 가짜 파일시스템 비교", 13.5, INK, KR, "start", 600)

comp_boxes = [
    ("일반 파일시스템 (ext4 / XFS)", "물리 매체 블록 I/O", "du -sh 로 실제 크기 확인", OK),
    ("procfs (/proc)", "커널 자료구조를 텍스트로", "du -sh /proc 결과 0 · 읽을 때 생성", ACC),
    ("sysfs (/sys)", "장치 모델 계층", "block · bus · class 트리", INFO),
    ("devtmpfs (/dev)", "커널이 만드는 장치 노드", "udev 가 권한·링크 보조", WARN),
]

for k, (hdr, sub1, sub2, c) in enumerate(comp_boxes):
    bx = X0 + 16 + k * 206
    d.box(bx, BY + 40, 196, 76, PAPER, c, 1.0, 6)
    d.t(bx + 10, BY + 58, hdr, 11, c, MONO if k == 0 else KR, "start", 600)
    d.t(bx + 10, BY + 78, sub1, 11, INK, KR, "start")
    d.t(bx + 10, BY + 98, sub2, 11, MUTED, KR, "start")

d.legend(524, [("시스템 콜 호출", INK), ("VFS 인터페이스", INFO),
               ("커널 RAM 상태", WARN), ("온디맨드 직렬화 (핵심)", ACC)])
d.save("05-01.pseudo-fs.svg")
print("ok 05-01.pseudo-fs")
