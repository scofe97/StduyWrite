# 타입 스펙: type-dp-security-matrix — 읽기 전략 두 행 × 다섯 순서 칸의 비교 행렬(격자 문법). 윗줄과 아랫줄이 같은 모양으로 이어지고 칸마다 실행 주체가 색으로 갈린다. 초점 칸 하나는 두 전략이 갈리는 자리.
# 사실 출처: 추출본 v1.txt 1747~1788행과 PDF 쪽 73 그림(Cache Aside 는 앱이 miss 뒤 DB 를 읽고 캐시를 채움, Read Through 는 캐시가 miss 뒤 DB 를 읽고 채움, 단계 1~5 순서),
#   Azure Architecture Center Cache-Aside 문서(앱이 요청 시 캐시에 적재), Hazelcast MapStore 문서(MapLoader 가 miss 시 외부 저장소에서 읽는 read-through).
#   user:42 · Kim · id=42 는 이 편이 정한 예시 값이다.
# Layout conventions: _cc_02_01_paths.py 의 §2 공식 값(left_pad 12, comp_col_w 176, role_col_w 128, gap 12, header_h 36, row_h 48, stride 56). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _cc_02_01_paths import build

rows = [
    ("캐시 어사이드", "채우는 쪽 앱", [
        ("앱", "GET user:42"), ("캐시", "miss"), ("앱", "SELECT id=42"), ("DB", "Kim"), ("앱", "SET user:42=Kim"),
    ]),
    ("읽기 관통", "채우는 쪽 캐시", [
        ("앱", "GET user:42"), ("캐시", "miss"), ("캐시", "SELECT id=42"), ("DB", "Kim"), ("캐시", "SET user:42=Kim"),
    ]),
]
build("BYTEBYTEGO · 02-01 §1", "읽기 전략은 miss 뒤 누가 DB 를 읽는지가 갈린다",
      "3단계 SELECT 와 5단계 SET 을 앱이 하느냐 캐시가 하느냐만 다릅니다",
      rows, (1, 2), "두 전략이 갈리는 칸", "02-01.read-paths.svg")
