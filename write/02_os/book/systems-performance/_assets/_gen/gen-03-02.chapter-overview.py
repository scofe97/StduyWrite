# 03-02 전체 지도 — 커널이 나누는 자원별 절과, 주제마다 깊어지는 장.
# 타입 스펙: type-layers — 일곱 절이 자원 다섯(메모리·CPU·저장장치 경로·캐시·네트워크와 장치) 위에
#           주체가 늘 때의 장치 둘(여러 CPU·자원 제어)을 쌓은 지도다.
#           축약: 인덱스 태그를 절 번호로, 오른쪽 메모를 깊어지는 장 번호로 채운다(폴더 개요 관례).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 928, 660
BX, BW, BH, Y0, STRIDE = 96, 736, 56, 108, 64

d = DK(W, H, "SYSTEMS PERFORMANCE · 03-02",
       "커널이 나누는 자원과 깊어지는 장",
       "03-02 의 일곱 절. 메모리·CPU 시간·저장장치(경로와 캐시)·네트워크와 장치를 차례로 보고, 나누는 주체가 여럿일 때 필요한 멀티프로세서·선점과 자원 제어로 끝난다. 행 끝의 장 번호가 그 주제를 깊게 다루는 곳이다.",
       "주제마다 한 장씩 깊어지므로 여기서는 멘탈 모델까지만 세웁니다")

BANDS = [
    ("§1", "가상 메모리", "사적 주소 공간 · 처음 쓸 때 매핑 · 페이징", "7장", INFO),
    ("§2", "스케줄러", "CPU 시간 · 우선순위 · 런큐", "6장", INFO),
    ("§3", "파일시스템", "전역 네임스페이스 · VFS · I/O 스택", "8 · 9장", INFO),
    ("§4", "캐싱", "열다섯 층 · 위에서 적중하면 멈춤", "8장", INFO),
    ("§5", "네트워킹과 디바이스 드라이버", "TCP/IP 스택 · 소켓 · character · block", "10장", INFO),
    ("§6", "멀티프로세서 · IPI · 선점", "SMP · NUMA · 세 가지 선점 설정", "6 · 7장", None),
    ("§7", "자원 관리와 관측성", "nice · ulimit · cgroups · 관측 도구", "11 · 4장", None),
]
for i, (tag, name, sub, ch, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 24, y + 34, tag, 13, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 24, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 44, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 34, ch, 13, c if c else SOFT, KR, "end")

d.legend(Y0 + 7 * STRIDE + 24, [("자원 하나씩", INFO), ("나누는 주체가 늘 때", MUTED)])
d.save("03-02.chapter-overview.svg")
