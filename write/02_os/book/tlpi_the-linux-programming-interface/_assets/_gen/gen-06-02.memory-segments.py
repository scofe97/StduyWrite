# 06-02 §1 프로세스 메모리 배치 — x86-32 가상 메모리 세그먼트와 경계 심볼
# 근거: TLPI 6.3 Figure 6-1, 06.txt 310-335, 367; end(3) man page
# 타입 스펙: type-layers — 가상 주소 공간의 세그먼트들을 수직 띠로 배치하고 경계 주소 및 심볼 표기
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 940, 548
d = D(W, H, "TLPI · 06-02 §1",
      "프로세스 가상 메모리 세그먼트 배치",
      "리눅스 x86-32 환경에서 각 프로세스가 바라보는 4GB 가상 주소 공간의 세그먼트 구조와 경계 심볼",
      "낮은 주소(0x08048000)부터 높은 주소(0xC0000000 이상)까지의 전형적인 배치 · 주소는 커널 설정과 링크 옵션에 따라 다름")

# 좌측 주소 증가 화살표
AX = 26
d.line(AX, 110, AX, 450, MUTED, 1.4)
d.arrow([(AX, 120), (AX, 104)], MUTED, "ar", 1.4)
d.t(AX + 10, 280, "가상 주소 증가", 10, MUTED, KR, "start", 400)

BX = 210
BW = 700

# 박스 배치 정의 (위에서 아래로 높은 주소 -> 낮은 주소)
layers = [
    # (y, h, name, addr_left, desc_right, symbol_right, color, is_focal)
    (110, 42, "커널 공간 (Kernel)", "0xC0000000~", "사용자 접근 차단 · 시스템 콜 실행", "/proc/kallsyms", SOFT, False),
    (156, 36, "인자·환경 변수 (argv, environ)", "0xC0000000 직하", "명령행 인자 문자열 및 환경 목록", "ARG_MAX", PAPER2, False),
    (196, 52, "스택 세그먼트 (Stack)", "고위 주소 → 저위 주소", "함수 프레임 · 지역 변수 · 호출 연결 정보", "ESP 레지스터", ACC, True),
    (252, 40, "미할당 가상 주소 공간", "미매핑 영역", "스택 하향 및 힙 상향 확장 대역", "SIGSEGV 발생", PAPER, False),
    (296, 48, "힙 세그먼트 (Heap)", "저위 주소 → 고위 주소", "동적 메모리 할당 (malloc / brk)", "program break", INFO, False),
    (348, 36, "BSS 세그먼트 (Uninitialized)", "&edata ~ &end", "미초기화 전역·정적 변수 (0 초기화)", "&end", OK, False),
    (388, 36, "초기화된 데이터 세그먼트 (Data)", "&etext ~ &edata", "명시적 초기화된 전역·정적 변수", "&edata", PAPER2, False),
    (428, 40, "텍스트 세그먼트 (Text)", "0x08048000~", "프로그램 기계어 코드 (읽기 전용 · 공유 가능)", "&etext", PAPER2, False),
]

for y, h, name, addr, desc, sym, c, focal in layers:
    if focal:
        d.tone(BX, y, BW, h, c, 4, "1F", 1.5)
        d.t(BX + 18, y + h/2 + 5, name, 13, INK, KR, "start", 600)
    elif c == PAPER:
        d.box(BX, y, BW, h, PAPER, RULE, 1.0, 4)
        d.line(BX, y, BX + BW, y, RULE, 0.8, "3 3")
        d.line(BX, y + h, BX + BW, y + h, RULE, 0.8, "3 3")
        d.t(BX + 18, y + h/2 + 5, name, 12, SOFT, KR, "start", 500)
    elif c == SOFT:
        d.box(BX, y, BW, h, PAPER2, SOFT, 1.0, 4)
        d.t(BX + 18, y + h/2 + 5, name, 13, INK, KR, "start", 600)
    else:
        d.box(BX, y, BW, h, PAPER2, RULE, 1.0, 4)
        d.t(BX + 18, y + h/2 + 5, name, 13, INK, KR, "start", 600)

    # 좌측 주소 범위
    d.t(BX - 14, y + h/2 + 4, addr, 10, MUTED, MONO, "end")
    # 중간 설명
    d.t(BX + 245, y + h/2 + 4, desc, 11, MUTED, KR, "start")
    # 최우측 심볼 / 마커
    d.chip(BX + BW - 65, y + h/2, sym, c if focal or c in (OK, INFO) else MUTED, 10, 6)

# 하단 미매핑 0 주소 표기
d.line(BX, 496, BX + BW, 496, RULE, 0.8, "2 4")
d.t(BX - 14, 500, "0x00000000", 10, SOFT, MONO, "end")
d.t(BX + 18, 487, "미매핑 영역 (NULL 포인터 역참조 방지)", 11, SOFT, KR, "start")

d.legend(516, [("스택 (하향 확장)", ACC), ("힙 (상향 확장)", INFO), ("BSS 세그먼트", OK), ("커널 보호 영역", SOFT)])
d.save("06-02.memory-segments.svg")
print("ok 06-02.memory-segments.svg")
