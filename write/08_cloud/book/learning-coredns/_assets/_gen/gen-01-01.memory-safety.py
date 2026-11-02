# 01-01 §4 — DNS 패킷이 파싱 버퍼 칸을 넘을 때 C 서버와 Go 서버(CoreDNS)의 동작 차이.
# 원문 근거: "Go는 반납된 메모리를 다른 곳이 쓰는 문제(dangling pointer)는 GC로, 칸 밖을 읽고 쓰는 문제(버퍼 오버플로)는 실행 중 범위 검사로 막습니다."
#            "악의를 가진 쪽이 버퍼 오버플로를 악용하면 DNS 서버를 죽이거나 더 나아가 그 밑의 운영체제를 장악할 수도 있습니다."
#            "범위를 벗어난 인덱스에 접근하면 런타임 panic이 일어납니다. CoreDNS 서버는 플러그인에서 발생한 panic을 recover()로 받아 서버 전체가 비정상 종료되지 않도록 살립니다."
# 타입 스펙: type-flowchart
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, BAD, OK, INFO, KR, MONO

W, H = 960, 560
d = D(W, H, "LEARNING COREDNS · 01-01 §4",
      "칸을 넘는 패킷과 두 언어의 갈림",
      "바깥 DNS 패킷의 길이가 버퍼 칸을 넘을 때 C 서버는 인접 메모리를 덮어써 중단이나 OS 장악으로 이어질 수 있지만, "
      "Go 서버(CoreDNS)는 실행 중 범위 검사로 panic을 일으키고 recover()로 수습해 서버를 살린다. "
      "가리키는 곳이 없어진 메모리는 가비지 컬렉터(GC)가 따로 회수한다.",
      "범위 검사가 없는 C는 옆 메모리를 덮고, Go는 범위 검사로 멈추며 CoreDNS가 recover()로 서버를 살립니다")

# 1. 상단 공통 단계 (열 1 ~ 열 3)
d.box(28, 184, 152, 64, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(104, 210, "바깥 DNS 패킷", 14, INK, KR, "middle", 600)
d.t(104, 232, "길이 N+k", 13, MUTED, MONO, "middle")

d.arrow([(180, 216), (208, 216)], MUTED, "ar", 1.4)

d.box(208, 184, 152, 64, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(284, 210, "고정 크기 버퍼", 14, INK, KR, "middle", 600)
d.t(284, 232, "칸 N", 13, MUTED, MONO, "middle")

d.arrow([(360, 216), (388, 216)], MUTED, "ar", 1.4)

d.tone(388, 184, 156, 64, BAD, 6, "12", 1.2)
d.t(466, 210, "버퍼 칸 넘김", 14, BAD, KR, "middle", 600)
d.t(466, 232, "길이 N+k > 칸 N", 13, INK, MONO, "middle")

# 2. 분기 화살표 (열 3 -> 열 4)
d.arrow([(544, 216), (556, 216), (556, 152), (568, 152)], BAD, "bad", 1.4)
d.arrow([(544, 216), (556, 216), (556, 280), (568, 280)], OK, "ok", 1.4)

# 3. C 서버 갈래 (상단 우측)
d.box(560, 96, 376, 112, fill=PAPER2, stroke=BAD, sw=0.8, r=6)
d.t(572, 114, "C 서버 (범위 검사 부재)", 13, BAD, KR, "start", 600)

d.tone(568, 124, 160, 56, BAD, 6, "14", 1.1)
d.t(648, 148, "인접 메모리 침범", 14, BAD, KR, "middle", 600)
d.t(648, 168, "버퍼 오버플로 발생", 13, MUTED, KR, "middle")

d.arrow([(728, 152), (752, 152)], BAD, "bad", 1.4)

d.tone(752, 124, 176, 56, BAD, 6, "20", 1.2)
d.t(840, 148, "서버 중단 · OS 장악", 14, BAD, KR, "middle", 600)
d.t(840, 168, "악용 시 가능한 피해", 13, MUTED, KR, "middle")

# 4. Go 서버 갈래 (하단 우측) — 핵심 안전장치 focal(ACC) 1곳
d.box(560, 224, 376, 112, fill=PAPER2, stroke=OK, sw=0.8, r=6)
d.t(572, 242, "Go 서버 · CoreDNS (실행 중 검사)", 13, OK, KR, "start", 600)

d.tone(568, 252, 160, 56, ACC, 6, "14", 1.4)
d.t(648, 276, "실행 중 범위 검사", 14, ACC, KR, "middle", 600)
d.t(648, 296, "런타임 panic 발생", 13, MUTED, KR, "middle")

d.arrow([(728, 280), (752, 280)], OK, "ok", 1.4)

d.tone(752, 252, 176, 56, OK, 6, "14", 1.2)
d.t(840, 276, "recover() 서버 생존", 14, OK, KR, "middle", 600)
d.t(840, 296, "질의 실패 · 프로세스 유지", 13, MUTED, KR, "middle")

# 5. 하단 별도 띠: 가비지 컬렉터 (GC)
d.box(28, 356, 904, 120, fill=PAPER2, stroke=INFO, sw=0.9, r=6)
d.t(44, 378, "별도 안전장치: 가비지 컬렉터 (GC)", 13, INFO, KR, "start", 600)
d.t(320, 378, "dangling pointer 방지 · 버퍼 범위 검사와 무관한 독립 메모리 회수", 13, MUTED, KR, "start")

d.box(44, 396, 248, 60, fill=PAPER, stroke=RULE, sw=0.9)
d.t(168, 422, "가리키는 곳 없는 메모리 식별", 14, INK, KR, "middle", 600)
d.t(168, 442, "도달 불가능 객체 추적", 13, MUTED, KR, "middle")

d.arrow([(292, 426), (324, 426)], MUTED, "ar", 1.4)

d.box(324, 396, 248, 60, fill=PAPER, stroke=RULE, sw=0.9)
d.t(448, 422, "백그라운드 자동 회수", 14, INK, KR, "middle", 600)
d.t(448, 442, "런타임 힙 메모리 정리", 13, MUTED, KR, "middle")

d.arrow([(572, 426), (604, 426)], INFO, "info", 1.4)

d.tone(604, 396, 312, 60, INFO, 6, "14", 1.2)
d.t(760, 422, "dangling pointer 차단", 14, INFO, KR, "middle", 600)
d.t(760, 442, "해제 메모리 오접근 및 훼손 방지", 13, MUTED, KR, "middle")

# 6. 범례
d.legend(508, [
    ("칸 넘김 위험", BAD),
    ("정상 방어 및 서버 생존", OK),
    ("핵심 안전장치 (focal)", ACC),
    ("독립 회수 장치 (GC)", INFO),
])

d.save("01-01.memory-safety.svg")
