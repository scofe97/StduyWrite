# 05-04 개요 — 데이터가 프로세스 사이를 흐르는 네 가지 경로와 각 절의 주제를 보이는 전체 지도.
# 사실 출처: 05-04 도입(L18~L24), §1(L31~L43), §2(L48~L54), §3(L59~L75), §4(L80~L94)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY, PH = 104, 276
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "05-04 · CHAPTER OVERVIEW", "데이터플로우 전체 지도",
      "DB·서비스를 거치는 데이터플로우, RPC 의 한계, 서비스 인프라 네 절을 잇는다.",
      "저장소 경유 · 서비스 캡슐화 · 네트워크 추상화 한계 · 분산 인프라")

CW = 196
GAP = 16
X0 = 24

cards = [
    ("§1", "DB 데이터플로우", "시간 격차와 저장소",
     [("쓰는 쪽 인코딩", "읽는 쪽 디코딩"),
      ("data outlives code", "5년 전 데이터 잔존"),
      ("지연 마이그레이션", "LSM · NULL 기본값")],
     INFO),
    ("§2", "REST 서비스", "HTTP API 캡슐화",
     [("비즈니스 로직 제약", "임의 쿼리 차단"),
      ("독립 배포와 진화", "버전 간 호환성"),
      ("OpenAPI · gRPC", "IDL 기반 인터페이스")],
     OK),
    ("§3", "RPC의 한계", "투명성 추상화 결함",
     [("로컬 ≠ 네트워크", "통제 밖 결함 노출"),
      ("타임아웃과 재시도", "중복 실행과 멱등성"),
      ("가변 지연 · 인자 인코딩", "포인터 전달 불가")],
     WARN),
    ("§4", "서비스 인프라", "주소 탐색과 분산",
     [("서비스 디스커버리", "etcd · ZooKeeper"),
      ("로드 밸런서", "HW · NGINX · DNS"),
      ("서비스 메시", "Sidecar · TLS 암호화")],
     ACC),
]

FOCAL = 2

for i, (sec, title, role, items, card_c) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    is_focal = (i == FOCAL)

    # 카드 외곽
    if is_focal:
        d.box(x, PY, CW, PH, PAPER2, WARN, 1.3)
    else:
        d.box(x, PY, CW, PH, PAPER2, RULE, 0.9)

    # 절 헤더: 칩(sec) + 제목
    d.chip(x + 28, PY + 22, sec, card_c, 11)
    d.t(x + CW / 2 + 14, PY + 26, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 46, role, 12, SOFT, KR, "middle")
    d.line(x + 12, PY + 56, x + CW - 12, PY + 56, RULE, 0.8)

    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 68 + j * 66

        if is_focal and j == 0:
            d.tone(x + 12, iy, CW - 24, 54, WARN, 6, "1C", 1.2)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, WARN, KR, "middle")
        elif i == 0 and j == 1:
            d.tone(x + 12, iy, CW - 24, 54, INFO, 6, "1C", 1.2)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, MONO if "data" in top_txt else KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, INFO, KR, "middle")
        elif i == 3 and j == 2:
            d.tone(x + 12, iy, CW - 24, 54, ACC, 6, "1C", 1.2)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, ACC, KR, "middle")
        else:
            d.box(x + 12, iy, CW - 24, 54, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, MONO if any(c in top_txt for c in "=_·") and not any('가'<=c<='힣' for c in top_txt) else KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, MUTED, KR, "middle")

# 카드 간 수평 연결 화살표
for i in range(3):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = PY + PH / 2
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)

d.legend(LEG, [("데이터 저장소", INFO), ("서비스 캡슐화", OK), ("추상화 한계·주의", WARN), ("인프라 솔루션", ACC)])
d.save("05-04.chapter-overview.svg")
