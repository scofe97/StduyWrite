# 07-04 §1 — 로컬 보조 인덱스 구조와 읽기 질의의 전 샤드 scatter/gather (fan-out).
# 사실 출처: 07-04 본문 §1(L26, L28~L30), DDIA 2판 Ch.7 Figure 7-9(원서 PDF 23쪽).
#   레코드·인덱스 값은 Figure 7-9 그림 글자 그대로(location 열은 뺐다). 샤드의 기본키 구간은 그림에 없어 적지 않는다.
#   질의는 그림의 "I am looking for a red car" · "Read from all shards" 를 본문 말(빨간 차 전부)로 옮겼다.
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
LEG = 540
H = LEG + 56

d = D(W, H, "07-04 §1 · LOCAL SECONDARY INDEX", "로컬 보조 인덱스와 scatter/gather 질의",
      "샤드별 독립 보조 인덱스와 전 샤드 병렬 질의(scatter/gather) 흐름을 보인다.",
      "샤드 독립 인덱싱과 읽기 fan-out 및 꼬리 지연 증폭")

# 상단: 클라이언트 질의
d.box(290, 88, 300, 44, PAPER2, WARN, 1.2)
d.t(440, 104, "빨간 차 전부 검색 · 모든 샤드로", 11, SOFT, KR, "middle")
d.t(440, 122, "color:red", 12, INK, MONO, "middle", 600)

# 두 샤드 외곽 상자
SW = 404
SH = 244
SY = 168

# Shard 0
d.box(24, SY, SW, SH, PAPER2, RULE, 1.0)
d.tone(24, SY, SW, 28, INFO, 4, "18", 1.0)
d.t(226, SY + 18, "샤드 0", 12, INK, KR, "middle", 600)

# Shard 0 기본키 인덱스
d.box(36, SY + 36, SW - 24, 76, PAPER, RULE, 0.8)
d.t(48, SY + 52, "기본키 인덱스 (Primary Key)", 11, MUTED, KR, "start")
d.t(48, SY + 70, "191 → {color: \"red\", make: \"Honda\"}", 11, INK, MONO, "start")
d.t(48, SY + 88, "214 → {color: \"black\", make: \"Dodge\"}", 11, INK, MONO, "start")
d.t(48, SY + 104, "306 → {color: \"red\", make: \"Ford\"}", 11, INK, MONO, "start")

# Shard 0 로컬 보조 인덱스
d.box(36, SY + 120, SW - 24, 112, PAPER, RULE, 0.8)
d.t(48, SY + 136, "로컬 보조 인덱스 (샤드 독립)", 11, INFO, KR, "start", 600)
d.t(48, SY + 154, "color:black → [214]", 11, INK, MONO, "start")
d.tone(44, SY + 164, SW - 40, 22, ACC, 3, "20", 1.0)
d.t(48, SY + 179, "color:red   → [191, 306]", 11, ACC, MONO, "start", 600)
d.t(48, SY + 204, "make:Honda  → [191]", 11, MUTED, MONO, "start")
d.t(48, SY + 222, "make:Ford   → [306]", 11, MUTED, MONO, "start")

# Shard 1
d.box(452, SY, SW, SH, PAPER2, RULE, 1.0)
d.tone(452, SY, SW, 28, INFO, 4, "18", 1.0)
d.t(654, SY + 18, "샤드 1", 12, INK, KR, "middle", 600)

# Shard 1 기본키 인덱스
d.box(464, SY + 36, SW - 24, 76, PAPER, RULE, 0.8)
d.t(476, SY + 52, "기본키 인덱스 (Primary Key)", 11, MUTED, KR, "start")
d.t(476, SY + 70, "515 → {color: \"silver\", make: \"Ford\"}", 11, INK, MONO, "start")
d.t(476, SY + 88, "768 → {color: \"red\", make: \"Volvo\"}", 11, INK, MONO, "start")
d.t(476, SY + 104, "893 → {color: \"silver\", make: \"Audi\"}", 11, INK, MONO, "start")

# Shard 1 로컬 보조 인덱스
d.box(464, SY + 120, SW - 24, 112, PAPER, RULE, 0.8)
d.t(476, SY + 136, "로컬 보조 인덱스 (샤드 독립)", 11, INFO, KR, "start", 600)
d.t(476, SY + 154, "color:black  → []", 11, SOFT, MONO, "start")
d.tone(472, SY + 164, SW - 40, 22, ACC, 3, "20", 1.0)
d.t(476, SY + 179, "color:red    → [768]", 11, ACC, MONO, "start", 600)
d.t(476, SY + 204, "color:silver → [515, 893]", 11, INK, MONO, "start")
d.t(476, SY + 222, "make:Volvo   → [768]", 11, MUTED, MONO, "start")

# scatter 질의 직각 화살표
d.arrow([(380, 132), (380, 150), (226, 150), (226, SY - 2)], WARN, "warn", 1.4)
d.t(300, 142, "scatter 질의", 11, WARN, KR, "middle")

d.arrow([(500, 132), (500, 150), (654, 150), (654, SY - 2)], WARN, "warn", 1.4)
d.t(580, 142, "scatter 질의", 11, WARN, KR, "middle")

# 하단: gather 병합 상자
GY = 448
d.box(230, GY, 420, 68, PAPER2, WARN, 1.2)
d.t(440, GY + 19, "결과 병합 (gather) 및 꼬리 지연", 12, INK, KR, "middle", 600)
d.t(440, GY + 38, "[191, 306] + [768] → [191, 306, 768]", 12, ACC, MONO, "middle", 600)
d.t(440, GY + 55, "모든 샤드 응답 대기 · tail latency 증폭", 11, MUTED, KR, "middle")

# gather 직각 화살표
d.arrow([(226, SY + SH), (226, 436), (320, 436), (320, GY - 2)], WARN, "warn", 1.4)
d.t(270, 426, "[191, 306]", 11, ACC, MONO, "middle")

d.arrow([(654, SY + SH), (654, 436), (560, 436), (560, GY - 2)], WARN, "warn", 1.4)
d.t(610, 426, "[768]", 11, ACC, MONO, "middle")

d.legend(LEG, [("기본키·로컬 인덱스", INFO), ("검색 일치 (color:red)", ACC), ("scatter/gather 질의·병합", WARN)])
d.save("07-04.secondary-index-sharding.svg")
