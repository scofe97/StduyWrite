# 03-04 §3 — 문서 모델의 연속 저장 locality 와 소규모 필드 갱신 시 전체 재작성 데이터 흐름.
# 사실 출처: 03-04 본문 §3(L83~L95) — 연속 문자열 저장, 웹 페이지 렌더링 전체 로드, 갱신 시 전체 재작성, Spanner interleave.
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY = 96
LEG = 454
H = LEG + 56

d = D(W, H, "03-04 · DATA LOCALITY", "문서 저장 locality와 부분 갱신의 전체 재작성",
      "문서는 연속 바이트열로 저장되어 전체 로드 시 locality 이점이 있지만, 일부 필드만 수정해도 문서 전체를 디스크에 다시 써야 한다.",
      "전체 읽기(연속 저장 로드) vs 부분 갱신(전체 로드 → 메모리 수정 → 전체 재작성)")

# 상단 레인: 전체 문서 읽기 (성능 이점)
Y_READ = PY + 8
H_READ = 120
d.box(24, Y_READ, 832, H_READ, PAPER, RULE, 0.9)
d.t(40, Y_READ + 24, "전체 문서 읽기 — 웹 페이지 렌더링", 13, INK, KR, "start", 600)
d.chip(360, Y_READ + 22, "연속 저장 locality 이점", OK, 11)

# 상단 3단계
XS_READ = [40, 310, 580]
W_READ = 240
# 1. 클라이언트 조회
d.box(XS_READ[0], Y_READ + 44, W_READ, 60, PAPER2, INFO, 1.1)
d.t(XS_READ[0] + W_READ / 2, Y_READ + 68, "프로필 조회 요청", 12, INK, KR, "middle", 600)
d.t(XS_READ[0] + W_READ / 2, Y_READ + 88, "user_id 251 전체 데이터 필요", 11, MUTED, KR, "middle")

# 2. 디스크 연속 읽기
d.box(XS_READ[1], Y_READ + 44, W_READ, 60, PAPER2, INFO, 1.1)
d.t(XS_READ[1] + W_READ / 2, Y_READ + 68, "디스크 연속 읽기", 12, INK, KR, "middle", 600)
d.t(XS_READ[1] + W_READ / 2, Y_READ + 88, "연속 바이트열(BSON) 로드", 11, MUTED, MONO, "middle")

# 3. 로드 완료
d.tone(XS_READ[2], Y_READ + 44, W_READ, 60, OK, 6, "16", 1.2)
d.t(XS_READ[2] + W_READ / 2, Y_READ + 68, "단일 문서 로드 완료", 12, OK, KR, "middle", 600)
d.t(XS_READ[2] + W_READ / 2, Y_READ + 88, "다중 인덱스 탐색 회피", 11, MUTED, KR, "middle")

d.arrow([(XS_READ[0] + W_READ + 4, Y_READ + 74), (XS_READ[1] - 6, Y_READ + 74)], MUTED, "ar", 1.2)
d.arrow([(XS_READ[1] + W_READ + 4, Y_READ + 74), (XS_READ[2] - 6, Y_READ + 74)], OK, "ok", 1.2)


# 하단 레인: 소규모 필드 갱신 (전체 재작성)
Y_WRITE = Y_READ + H_READ + 18
H_WRITE = 138
d.box(24, Y_WRITE, 832, H_WRITE, PAPER, RULE, 0.9)
d.t(40, Y_WRITE + 24, "소규모 필드 갱신 — 전체 재작성 오버헤드", 13, INK, KR, "start", 600)
d.chip(400, Y_WRITE + 22, "작은 갱신에도 전체 재작성", ACC, 11)

# 하단 4단계
XS_WRITE = [40, 246, 452, 658]
W_WRITE = 190

# 1. 갱신 요청
d.box(XS_WRITE[0], Y_WRITE + 44, W_WRITE, 74, PAPER2, INFO, 1.1)
d.t(XS_WRITE[0] + W_WRITE / 2, Y_WRITE + 68, "일부 필드 갱신 요청", 12, INK, KR, "middle", 600)
d.t(XS_WRITE[0] + W_WRITE / 2, Y_WRITE + 88, "first_name 변경 요청", 11, MUTED, KR, "middle")
d.t(XS_WRITE[0] + W_WRITE / 2, Y_WRITE + 104, "단일 속성만 대상", 11, SOFT, KR, "middle")

# 2. 전체 로드
d.box(XS_WRITE[1], Y_WRITE + 44, W_WRITE, 74, PAPER2, WARN, 1.1)
d.t(XS_WRITE[1] + W_WRITE / 2, Y_WRITE + 68, "디스크 전체 로드", 12, WARN, KR, "middle", 600)
d.t(XS_WRITE[1] + W_WRITE / 2, Y_WRITE + 88, "문서 전체를 메모리로 로드", 11, MUTED, KR, "middle")
d.t(XS_WRITE[1] + W_WRITE / 2, Y_WRITE + 104, "불필요한 필드 포함", 11, SOFT, KR, "middle")

# 3. 메모리 수정
d.box(XS_WRITE[2], Y_WRITE + 44, W_WRITE, 74, PAPER2, INFO, 1.1)
d.t(XS_WRITE[2] + W_WRITE / 2, Y_WRITE + 68, "메모리 내 필드 수정", 12, INK, KR, "middle", 600)
d.t(XS_WRITE[2] + W_WRITE / 2, Y_WRITE + 88, "버퍼 내 값 교체", 11, MUTED, KR, "middle")
d.t(XS_WRITE[2] + W_WRITE / 2, Y_WRITE + 104, "작은 일부만 바뀜", 11, SOFT, KR, "middle")

# 4. 전체 재작성 (focal)
d.tone(XS_WRITE[3], Y_WRITE + 44, W_WRITE, 74, ACC, 6, "16", 1.4)
d.t(XS_WRITE[3] + W_WRITE / 2, Y_WRITE + 68, "디스크 전체 재작성", 12, ACC, KR, "middle", 600)
d.t(XS_WRITE[3] + W_WRITE / 2, Y_WRITE + 88, "문서 전체를 다시 기록", 11, ACC, KR, "middle")
d.t(XS_WRITE[3] + W_WRITE / 2, Y_WRITE + 104, "잦은 소규모 갱신 회피 권고", 11, MUTED, KR, "middle")

d.arrow([(XS_WRITE[0] + W_WRITE + 4, Y_WRITE + 81), (XS_WRITE[1] - 6, Y_WRITE + 81)], MUTED, "ar", 1.2)
d.arrow([(XS_WRITE[1] + W_WRITE + 4, Y_WRITE + 81), (XS_WRITE[2] - 6, Y_WRITE + 81)], WARN, "warn", 1.2)
d.arrow([(XS_WRITE[2] + W_WRITE + 4, Y_WRITE + 81), (XS_WRITE[3] - 6, Y_WRITE + 81)], ACC, "acc", 1.4)

# 하단 관계형 대안 스트립
Y_ALT = Y_WRITE + H_WRITE + 14
d.box(24, Y_ALT, 832, 34, PAPER2, RULE, 0.8)
d.t(36, Y_ALT + 22, "관계형 locality 대안", 11, SOFT, KR, "start", 600)
d.t(190, Y_ALT + 22, "Google Spanner 부모-자식 행 interleave  ·  Oracle 다중 테이블 클러스터  ·  Bigtable 컬럼 패밀리", 11, MUTED, KR, "start")

d.legend(LEG, [("전체 로드 이점", OK), ("전체 재작성 오버헤드", ACC), ("비효율 로드 단계", WARN), ("일반 단계", INFO)])
d.save("03-04.document-locality.svg")
