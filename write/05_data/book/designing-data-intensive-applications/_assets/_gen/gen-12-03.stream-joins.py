# 12-03 세부 도식 — 스트림 조인 세 가지 유형과 상태 관리 구조
# 사실 출처: 12-03 본문 §4(L67~L84), 원서 Ch. 12 Stream Joins (p.46~50: p.47 user ID·network round trip·overloading, p.49 posts.sender_id·follows.followee_id)
# 원서: DDIA 2nd Edition Ch. 12 "Stream-stream join", "Stream-table join", "Table-table join", "Time dependence of joins"
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
H = 600

d = D(W, H, "12-03 · SECTION 4", "스트림 조인 세 가지 유형과 상태 관리 구조",
      "입력 스트림의 성격(이벤트 vs 변경로그)에 따른 내부 로컬 상태 유지 및 파생 출력 생성 아키텍처",
      "스트림-스트림 윈도우 조인 · 스트림-테이블 캐시 강화 · 테이블-테이블 구체화 뷰 · SCD 시간 의존성")

ROWS = [
    ("스트림-스트림 조인 (윈도우 조인)", ACC, 112,
     [("검색 이벤트", "session_id · query"),
      ("클릭 이벤트", "session_id · url")],
     ("스트림 프로세서 (1시간 세션 윈도우)",
      "세션 ID 기준 양방향 이벤트 인덱스 버퍼 유지",
      "새 이벤트 도착 시 상대 인덱스 매칭 즉시 조회",
      "1시간 만료 시 미매칭(클릭 없음) 이벤트 방출"),
     ("조인 결과 파생 스트림",
      "검색-클릭 매칭 이벤트 방출",
      "1시간 만료 미매칭 이벤트 방출")),

    ("스트림-테이블 조인 (스트림 강화)", INFO, 232,
     [("사용자 활동 이벤트", "user_id · action"),
      ("프로필 CDC 변경로그", "user_id · profile")],
     ("스트림 프로세서 (로컬 해시 테이블)",
      "사용자 프로필 DB 복사본을 로컬 메모리에 로드",
      "CDC 스트림 구독으로 로컬 캐시 사본 최신 유지",
      "네트워크 왕복 없이 로컬에서 조회"),
     ("프로필 강화 활동 스트림",
      "사용자 프로필 속성 결합 이벤트",
      "원격 DB 질의의 지연·과부하 회피")),

    ("테이블-테이블 조인 (구체화 뷰 유지)", OK, 352,
     [("게시물 CDC 변경로그", "posts: post_id · sender_id"),
      ("팔로우 CDC 변경로그", "follows: follower · followee")],
     ("스트림 프로세서 (타임라인 캐시 뷰)",
      "사용자별 팔로워 목록 DB + 게시물 캐시 유지",
      "새 게시물 발행 시 팔로워 홈 타임라인에 삽입",
      "팔로우·언팔로우 발생 시 타임라인 증분 갱신"),
     ("홈 타임라인 구체화 뷰",
      "홈 타임라인 캐시 단일 키 조회",
      "팔로우 변경 시 타임라인 갱신")),
]

LX = 24
LW = 204
CX = 260
CW = 312
RX = 604
RW = 248

for title, c, ry, inputs, proc, output in ROWS:
    is_focal = (c == ACC)

    # 행 배경 외곽 박스
    if is_focal:
        d.box(LX - 4, ry - 4, W - 40, 116, PAPER2, ACC, 1.2)
    else:
        d.box(LX - 4, ry - 4, W - 40, 116, PAPER, RULE, 0.7)

    # 행 타이틀 (d.t 사용으로 center 좌표 계산 및 overflow 원천 배제)
    d.t(LX + 12, ry + 16, title, 12, c, KR, "start", 600)

    # 좌측 입력 스트림 2개
    in1, in2 = inputs
    d.box(LX + 4, ry + 28, LW - 8, 34, PAPER2, c, 0.8)
    d.t(LX + 12, ry + 42, in1[0], 11, INK, KR, "start", 600)
    d.t(LX + 12, ry + 56, in1[1], 10, MUTED, MONO, "start")

    d.box(LX + 4, ry + 68, LW - 8, 34, PAPER2, c, 0.8)
    d.t(LX + 12, ry + 82, in2[0], 11, INK, KR, "start", 600)
    d.t(LX + 12, ry + 96, in2[1], 10, MUTED, MONO, "start")

    # 입력 -> 중앙 화살표
    d.arrow([(LX + LW, ry + 65), (CX - 4, ry + 65)], SOFT, "soft", 1.2)

    # 중앙 프로세서 & 상태 박스
    proc_title, p1, p2, p3 = proc
    d.tone(CX, ry + 12, CW, 92, c, 4, "14" if is_focal else "08", 1.0)
    d.t(CX + 12, ry + 28, proc_title, 12, c, KR, "start", 600)
    d.t(CX + 12, ry + 48, f"• {p1}", 11, INK, KR, "start")
    d.t(CX + 12, ry + 66, f"• {p2}", 11, INK, KR, "start")
    d.t(CX + 12, ry + 84, f"• {p3}", 11, MUTED, KR, "start")

    # 중앙 -> 우측 화살표
    d.arrow([(CX + CW + 4, ry + 65), (RX - 4, ry + 65)], SOFT, "soft", 1.2)

    # 우측 출력 박스
    out_title, o1, o2 = output
    d.box(RX, ry + 12, RW, 92, PAPER2, c, 0.8)
    d.t(RX + 12, ry + 30, out_title, 12, c, KR, "start", 600)
    d.t(RX + 12, ry + 52, f"• {o1}", 11, INK, KR, "start")
    d.t(RX + 12, ry + 72, f"• {o2}", 11, MUTED, KR, "start")

# 하단 시간 의존성 & SCD 패널
PANEL_Y = 476
d.tone(LX - 4, PANEL_Y, W - 40, 50, WARN, 4, "12", 1.0)
d.t(LX + 12, PANEL_Y + 18, "조인의 시간 의존성과 SCD 패턴 (DDIA p.50)", 12, WARN, KR, "start", 600)
d.t(LX + 12, PANEL_Y + 38, "상태 변경 시점 대조 문제: 판매 시점 세금율 등 특정 레코드 버전에 고유 ID를 부여하여 결정론적 조인 재처리 보장", 11, INK, KR, "start")

# 범례
LEG = 538
legend_items = [
    ("스트림-스트림 (윈도우, focal)", ACC),
    ("스트림-테이블 (로컬 캐시)", INFO),
    ("테이블-테이블 (구체화 뷰)", OK),
    ("SCD (시간 의존성)", WARN),
]
d.line(24, LEG, W - 24, LEG, RULE, 0.8)
d.t(24, LEG + 22, "LEGEND", 8, SOFT, MONO, "start")
lx = 80
for lab, c in legend_items:
    d.o.append(f'<rect x="{lx}" y="{LEG + 12}" width="14" height="12" rx="2" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
    d.t(lx + 20, LEG + 22, lab, 11, MUTED, KR, "start")
    w_text = sum(11 if "가" <= ch <= "힣" else 7 for ch in lab)
    lx += 26 + w_text + 16

d.save("12-03.stream-joins.svg")
