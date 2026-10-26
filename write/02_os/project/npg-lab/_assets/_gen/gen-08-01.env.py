# 08-01-env — 8장 리버스 프록시 진단 리허설 환경 구성도
# 본문 요구(08-01 리허설 환경): 부하 발생기, 프록시, 백엔드, 관측 도구와 장애 주입 경로의 연결 관계를 보인다.
# 타입 스펙: type-architecture
# 사실 출처: 08-01.기본값 리버스 프록시가 겪는 장애 - 느린 검색·포트 고갈·POST 502·회복 지연·중복 등록.md:36-49·53, cmd/npgwatch/main.go:161-164
import sys
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, RULE, PAPER2, ACC, INFO, KR, MONO

W = 960
H = 512

d = D(
    W,
    H,
    "ARCHITECTURE · CH08 REHEARSAL ENVIRONMENT",
    "리버스 프록시 진단 리허설 환경",
    "npgload 부하 발생기, npgproxy v0 기본 리버스 프록시, fakeinv 백엔드, npgwatch 관측 화면 및 장애 주입 구성",
    lead="부하 생성부터 프록시·백엔드 전달 경로와 지표 수집, 숨겨진 장애 주입 구조"
)

# 1. 상단 장애 주입 (focal 1곳: fakeinv 위에 독립 배치, 학습자에게 원인 숨김)
d.tone(680, 104, 240, 52, ACC, r=6, op="14", sw=1.6)
d.t(800, 125, "/_faults", 14, ACC, MONO, "middle", 600)
d.t(800, 144, "장애 주입 · 원인 숨김", 13, ACC, KR, "middle")

# 장애 주입 화살표 (/_faults -> fakeinv)
d.arrow([(800, 156), (800, 196)], c=ACC, m="acc", sw=1.4)
d.t(808, 180, "장애 주입", 13, ACC, KR, "start", 600)

# 2. 주 요청 경로 노드 3개 (왼쪽 -> 오른쪽)
# (1) npgload (부하 발생기)
d.box(40, 196, 240, 104, PAPER2, RULE, 0.9, 6)
d.t(160, 226, "npgload", 14, INK, MONO, "middle", 600)
d.t(160, 254, "get 50/s · search 5/s", 12, MUTED, MONO, "middle")
d.t(160, 280, "poisson 분포 부하", 13, MUTED, KR, "middle")

# 요청 전달 화살표 (npgload -> npgproxy)
d.arrow([(280, 248), (360, 248)], c=MUTED, m="ar", sw=1.4)
d.t(320, 236, "HTTP 요청", 13, INK, KR, "middle", 600)

# (2) npgproxy v0 (리버스 프록시)
d.box(360, 196, 240, 104, PAPER2, RULE, 0.9, 6)
d.t(480, 226, "npgproxy v0", 14, INK, MONO, "middle", 600)
d.t(480, 254, ":18080 · 기본 Transport", 13, INK, KR, "middle")
d.t(480, 280, ":18081 /debug/vars", 12, MUTED, MONO, "middle")

# 프록시 전달 화살표 (npgproxy -> fakeinv)
d.arrow([(600, 248), (680, 248)], c=MUTED, m="ar", sw=1.4)
d.t(640, 236, "프록시 전달", 13, INK, KR, "middle", 600)

# (3) fakeinv (백엔드)
d.box(680, 196, 240, 104, PAPER2, RULE, 0.9, 6)
d.t(800, 226, "fakeinv", 14, INK, MONO, "middle", 600)
d.t(800, 254, ":9090 · 창구 workers", 13, INK, KR, "middle")
d.t(800, 280, "/_stats 내부 지표", 13, MUTED, KR, "middle")

# 3. 하단 관측 화면 (npgwatch)
d.tone(520, 356, 240, 68, INFO, r=6, op="12", sw=1.1)
d.t(640, 382, "npgwatch", 14, INFO, MONO, "middle", 600)
d.t(640, 406, ":8090 · 관측 화면", 13, MUTED, KR, "middle")

# 4. 관측 스크랩 직교 경로 (점선, 1초마다)
# npgwatch -> npgproxy 관리 포트 (:18081 /debug/vars)
d.path("M 520 390 H 448 Q 440 390 440 382 V 300", c=INFO, sw=1.2, m="info", dash="4 3")
d.t(430, 346, "1초마다 수집", 13, INFO, KR, "end", 600)

# npgwatch -> fakeinv 통계 경로 (/_stats)
d.path("M 760 390 H 832 Q 840 390 840 382 V 300", c=INFO, sw=1.2, m="info", dash="4 3")
d.t(850, 346, "1초마다 수집", 13, INFO, KR, "start", 600)

# 5. 범례 (margin 36px 확보)
d.legend(452, [
    ("장애 주입", ACC),
    ("관측 지표 스크랩", INFO),
])

d.save("08-01-env.svg")
print("saved 08-01-env.svg")
