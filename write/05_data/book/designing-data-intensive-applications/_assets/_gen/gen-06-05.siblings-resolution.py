# 06-05 §2 — 동시 쓰기 발생 시 형제 값(siblings) 보존과 수동 해소(API 변경·삭제 부활) 대 자동 해소(strong eventual consistency) 분기.
# 사실 출처: 06-05 §2(L41~L47), DDIA 2판 6장 "Manual conflict resolution" 및 "Automatic conflict resolution" (PDF p.23~24).
# 타입 스펙: type-flowchart
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
LEG = 594
H = LEG + 56

d = D(W, H, "06-05 · SIBLINGS & RESOLUTION FLOW", "형제 값 보관과 수동·자동 충돌 해소 흐름",
      "동시 쓰기 발생 시 형제 값(siblings)을 보관한 뒤 애플리케이션의 수동 병합과 데이터 타입별 자동 수렴으로 나뉘는 해소 흐름을 보인다.",
      "동시 값 형제 보관 · 수동 병합과 삭제 부활 위험 · strong eventual consistency 자동 수렴")

# 1. 루트: 동시 쓰기 충돌 발생
d.box(280, 104, 320, 44, PAPER2, INFO, 1.1, r=6)
d.t(440, 122, "동시 쓰기 충돌 발생", 12, INK, KR, "middle", 600)
d.t(440, 138, "사용자 1: title = 'B'  ·  사용자 2: title = 'C'", 11, MUTED, KR, "middle")

d.arrow([(440, 148), (440, 172)], MUTED, "ar", 1.2)

# 2. 형제 값 동시 보관
d.box(260, 172, 360, 46, PAPER2, RULE, 1.0, r=6)
d.chip(440, 184, "형제 값(siblings) 동시 보관", INFO, 11)
d.t(440, 206, "단일 덮어쓰기 대신 충돌 값 보존: {title: ['B', 'C']}", 11, INK, KR, "middle", 600)

d.arrow([(440, 218), (440, 240)], MUTED, "ar", 1.2)

# 3. 분기 다이아몬드 (마름모 결정 노드)
d.o.append(f'<polygon points="440,240 536,262 440,284 344,262" fill="{PAPER2}" stroke="{INFO}" stroke-width="1.1"/>')
d.t(440, 266, "해소 전략 선택", 12, INK, KR, "middle", 600)

# 좌측 화살표 (수동 해소)
d.path("M 344 262 L 220 262 L 220 294", c=WARN, sw=1.3, m="warn")
d.t(276, 254, "수동 해소 (앱·사용자)", 11, WARN, KR, "middle", 600)

# 우측 화살표 (자동 해소)
d.path("M 536 262 L 660 262 L 660 294", c=ACC, sw=1.5, m="acc")
d.t(604, 254, "자동 해소 (수렴)", 11, ACC, KR, "middle", 600)

# 좌측 경로: 수동 해소 (Manual Resolution)
d.box(40, 296, 360, 52, PAPER, WARN, 0.9, r=6)
d.t(220, 316, "클라이언트 조회 시 siblings 집합 반환", 12, INK, KR, "middle", 600)
d.t(220, 334, "DB API 변경: 단일 문자열 → 문자열 집합", 11, MUTED, KR, "middle")

d.arrow([(220, 348), (220, 372)], WARN, "warn", 1.2)

d.box(40, 372, 360, 52, PAPER, WARN, 0.9, r=6)
d.t(220, 392, "애플리케이션 코드 또는 사용자 수동 병합", 12, INK, KR, "middle", 600)
d.t(220, 410, "문자열 연결('B/C') 또는 사용자 UI 선택 위임", 11, MUTED, KR, "middle")

d.arrow([(220, 424), (220, 448)], WARN, "warn", 1.2)

d.tone(40, 448, 360, 62, WARN, 6, "14", 1.2)
d.t(220, 470, "단순 합집합 병합 시 삭제 항목 부활 함정", 12, WARN, KR, "middle", 600)
d.t(220, 488, "Amazon 장바구니 사례: 삭제한 Book·DVD 재출현", 11, MUTED, KR, "middle")
d.t(220, 502, "동시 수동 해소 간 2차 충돌 및 불일치 위험", 11, MUTED, KR, "middle")

# 우측 경로: 자동 해소 (Automatic Resolution - Strong Eventual Consistency)
d.box(480, 296, 360, 52, PAPER, ACC, 1.2, r=6)
d.t(660, 316, "strong eventual consistency 수렴 보장", 12, INK, KR, "middle", 600)
d.t(660, 334, "도착 순서 무관하게 동일 쓰기 처리 시 동일 상태 수렴", 11, ACC, KR, "middle")

d.arrow([(660, 348), (660, 372)], ACC, "acc", 1.4)

d.box(480, 372, 360, 138, PAPER2, ACC, 1.4, r=6)
d.chip(660, 386, "데이터 타입별 의도 보존 병합 알고리즘", ACC, 11)

# 타입별 서브 박스 3개
d.box(492, 404, 336, 28, PAPER, RULE, 0.7, r=4)
d.t(504, 422, "텍스트", 11, OK, KR, "start", 600)
d.t(550, 422, "삽입·삭제 추적하여 모든 편집 의도 보존", 11, INK, KR, "start")

d.box(492, 438, 336, 28, PAPER, RULE, 0.7, r=4)
d.t(504, 456, "컬렉션", 11, OK, KR, "start", 600)
d.t(550, 456, "삭제 사실 추적해 부활 차단", 11, INK, KR, "start")

d.box(492, 472, 336, 28, PAPER, RULE, 0.7, r=4)
d.t(504, 490, "카운터", 11, OK, KR, "start", 600)
d.t(550, 490, "증감 연산 합산하여 이중 계산·누락 방지", 11, INK, KR, "start")

# 하단 요약 배너
d.tone(24, 532, W - 48, 36, OK, 4, "14", 1.0)
d.t(W / 2, 554, "결론: 수동 해소는 앱 부담과 부활 위험 수반 · 자동 해소는 의도 보존과 손실 최소화", 12, INK, KR, "middle", 600)

d.legend(LEG, [("형제 값 보존", INFO), ("수동 해소 및 부활 함정", WARN), ("자동 수렴 보장 (focal)", ACC), ("일관 수렴 상태", OK)])
d.save("06-05.siblings-resolution.svg")
