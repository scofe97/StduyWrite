# 13-04 개요 — end-to-end 인수(§1), 적시성과 무결성(§2), 분산 트랜잭션 없는 무결성(§3), 느슨한 제약(§4), 코디네이션 회피(§5), 신뢰하되 검증하기(§6), 13장 종합(§7) 전체 지도.
# 사실 출처: 13-04 본문 서두(L13~L16), §1(L22~L30), §2(L32~L42), §3(L44~L55), §4(L57~L67), §5(L69~L80), §6(L82~L92), §7(L94~L109), DDIA 2판 Ch.13 (PDF p.31~56). 칸 라벨은 본문 낱말.
# 타입 스펙: type-architecture
# 2026-10-31 검증: 배너 중립색, 칸 라벨을 본문 낱말로(비분산→분산 트랜잭션 없는, 순서 보장·HDFS/S3 표기·3대 제거), 범례를 칸 뜻에 맞춤
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
Y1 = 156
H1 = 176
Y2 = Y1 + H1 + 20
H2 = 176
Y3 = Y2 + H2 + 18
H3 = 76
LEG = Y3 + H3 + 26
H = LEG + 48

d = D(W, H, "13-04 · CHAPTER OVERVIEW", "정확성과 신뢰·13장 종합 전체 지도",
      "end-to-end 인수(§1), 적시성과 무결성(§2), 분산 트랜잭션 없는 무결성(§3), 느슨한 제약(§4), 코디네이션 회피(§5), 신뢰하되 검증하기(§6), 13장 종합(§7)으로 이어지는 체계를 조망한다.",
      "end-to-end 중복 제거 · 적시성과 무결성 분리 · 최초 이벤트 기록의 원자성 · 사후 보정 · 멀티 리더 비동기 · 지속 검증 · 13장 철학 수렴")

# 상단 공통 전제 배너
d.box(28, BANNER_Y, W - 56, BANNER_H, PAPER2, RULE, 0.9, 4)
d.t(W / 2, BANNER_Y + 23, "강한 일관성 없이 무결성 달성 = end-to-end 관점 · 멱등성 · 비동기 제약 검사 · 신뢰하되 검증", 12, INK, KR, "middle", 600)

CW = 264
GAP = 16
X0 = 28

# Row 1 카드 3개 (§1, §2, §3)
cards_r1 = [
    ("§1", "End-to-End 인수", "양 끝의 지식과 도움",
     [("TCP 중복 제거", "연결 범위 안에서만"),
      ("요청 ID (UUID)", "클라이언트 생성 · end-to-end 전달"),
      ("유니크 제약", "DB에서 중복 차단 · 감사 로그")],
     OK),
    ("§2", "적시성 vs 무결성", "두 가지 별개의 요구",
     [("적시성 (Timeliness)", "최신 상태 관측 · 기다리면 해결"),
      ("무결성 (Integrity)", "손실·모순 없음 · 명시적 수리 필요"),
      ("무결성 > 적시성", "적시성 포기 · 무결성 유연하게 달성")],
     WARN),
    ("§3", "분산 트랜잭션 없는 무결성", "이벤트 로그 · 요청 ID · 재처리",
     [("단일 메시지 기록", "하나의 이벤트 기록 = 원자적 액션"),
      ("결정론적 파생 · 재처리", "불변 메시지로 파생 상태 복구"),
      ("멀티 샤드 거래", "원자성 = 최초 이벤트 기록")],
     OK),
]

for i, (sec, title, sub, items, c) in enumerate(cards_r1):
    x = X0 + i * (CW + GAP)
    d.box(x, Y1, CW, H1, PAPER2, c, 1.2)
    d.chip(x + 24, Y1 + 18, sec, c, 11)
    d.t(x + CW / 2 + 10, Y1 + 22, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, Y1 + 40, sub, 11, MUTED, KR, "middle")
    d.line(x + 8, Y1 + 48, x + CW - 8, Y1 + 48, RULE, 0.8)

    for j, (h_txt, d_txt) in enumerate(items):
        iy = Y1 + 54 + j * 38
        d.box(x + 6, iy, CW - 12, 34, PAPER, RULE, 0.8)
        d.t(x + 12, iy + 14, h_txt, 11.5, c, KR, "start", 600)
        d.t(x + 12, iy + 27, d_txt, 11, MUTED, KR, "start")

    if i < len(cards_r1) - 1:
        arr_x = x + CW + 1
        arr_y = Y1 + H1 / 2
        d.arrow([(arr_x, arr_y), (arr_x + GAP - 2, arr_y)], MUTED, "ar", 1.4)

# Row 2 카드 3개 (§4, §5, §6)
cards_r2 = [
    ("§4", "느슨한 제약", "사전 강제 대신 사후 보정",
     [("유니크 제약 = 합의", "동기 코디네이션 수반"),
      ("보정 비용 < 방지 비용", "초과 판매 · 오버부킹 · 초과 인출"),
      ("사후 보정 거래", "낙관적 쓰기 후 비동기 검사")],
     WARN),
    ("§5", "코디네이션 회피", "약한 적시성 · 강한 무결성",
     [("두 관찰 결합", "파생 무결성 유지 + 사후 보정 허용"),
      ("멀티 리더 구성", "데이터센터별 독립 운영 · 비동기 복제"),
      ("필요한 곳만 코디네이션", "되돌리기 어려운 액션 이전")],
     INFO),
    ("§6", "신뢰하되 검증", "지속적 무결성 검사",
     [("가정은 확률의 문제", "디스크 손상 · 소프트 에러 · 비트 뒤집힘"),
      ("백그라운드 검사", "HDFS·S3 복제본 비교 · 백업 복원"),
      ("이벤트 소싱 감사", "같은 코드로 재실행 · Merkle 트리")],
     INFO),
]

for i, (sec, title, sub, items, c) in enumerate(cards_r2):
    x = X0 + i * (CW + GAP)
    d.box(x, Y2, CW, H2, PAPER2, c, 1.2)
    d.chip(x + 24, Y2 + 18, sec, c, 11)
    d.t(x + CW / 2 + 10, Y2 + 22, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, Y2 + 40, sub, 11, MUTED, KR, "middle")
    d.line(x + 8, Y2 + 48, x + CW - 8, Y2 + 48, RULE, 0.8)

    for j, (h_txt, d_txt) in enumerate(items):
        iy = Y2 + 54 + j * 38
        d.box(x + 6, iy, CW - 12, 34, PAPER, RULE, 0.8)
        d.t(x + 12, iy + 14, h_txt, 11.5, c, KR, "start", 600)
        d.t(x + 12, iy + 27, d_txt, 11, MUTED, KR, "start")

    if i < len(cards_r2) - 1:
        arr_x = x + CW + 1
        arr_y = Y2 + H2 / 2
        d.arrow([(arr_x, arr_y), (arr_x + GAP - 2, arr_y)], MUTED, "ar", 1.4)

# Row 1 -> Row 2 수직 연결 화살표
d.arrow([(W / 2, Y1 + H1), (W / 2, Y2)], MUTED, "ar", 1.4)

# Row 3 카드 (§7 전체 종합)
d.box(X0, Y3, W - 56, H3, PAPER2, ACC, 1.2)
d.chip(X0 + 26, Y3 + 20, "§7", ACC, 11)
d.t(X0 + 64, Y3 + 24, "13장 종합: 스트리밍 시스템의 철학", 13, INK, KR, "start", 600)
d.line(X0 + 8, Y3 + 36, X0 + W - 56 - 8, Y3 + 36, RULE, 0.8)

# §7 내용 2개 박스
PW = (W - 56 - 16) / 2
d.box(X0 + 6, Y3 + 42, PW - 3, 28, PAPER, RULE, 0.8)
d.t(X0 + 14, Y3 + 60, "전문 시스템 조합", 11.5, ACC, KR, "start", 600)
d.t(X0 + PW - 10, Y3 + 60, "단일 도구 대신 이벤트 로그로 전문 시스템 조합", 11.5, INK, KR, "end")

d.box(X0 + PW + 10, Y3 + 42, PW - 3, 28, PAPER, RULE, 0.8)
d.t(X0 + PW + 18, Y3 + 60, "세 목표 수렴", 11.5, ACC, KR, "start", 600)
d.t(X0 + W - 56 - 14, Y3 + 60, "신뢰성(로그) · 확장성(회피) · 유지보수성(재처리)", 11.5, INK, KR, "end")

# Row 2 -> Row 3 수직 연결 화살표
d.arrow([(W / 2, Y2 + H2), (W / 2, Y3)], MUTED, "ar", 1.4)

d.legend(LEG, [
    ("무결성 장치 (§1·§3)", OK),
    ("적시성 양보 (§2·§4)", WARN),
    ("회피·검증 (§5·§6)", INFO),
    ("13장 종합 (§7)", ACC)
])

d.save("13-04.chapter-overview.svg")
