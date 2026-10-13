# 타입 스펙: type-dp-security-matrix — 쓰기 전략 세 행 × 다섯 순서 칸의 비교 행렬(격자 문법). 행마다 칸 수가 다르다는 것 자체가 논지(관통 둘·지연 넷·우회 셋). 초점 칸 하나는 쓰기 지연에서 DB 가 받는 유일한 쓰기.
# 사실 출처: 추출본 v1.txt 1747~1788행과 PDF 쪽 73 그림(Write Through: 캐시에 쓰고 DB 에 바로 쓴다 · Write Back: 캐시에 계속 쓰고 DB 에는 가끔 한 번 · Write Around: DB 에 쓰고 읽을 때 캐시를 먼저 봄 — 이 도식은 캐시에 옛 값이 남아 있는 갈래, miss 갈래는 읽기 도식과 같음),
#   Hazelcast MapStore 설정 문서(write-delay-seconds 가 0 이면 write-through, 0 보다 크면 write-behind, write-coalescing 이 true 면 지연 시간 안의 같은 키는 마지막 쓰기만 DB 로 간다).
#   views:42 의 101→102→103, name=Lee, user:42 는 이 편이 정한 예시 값이다.
# Layout conventions: _cc_02_01_paths.py 의 §2 공식 값(left_pad 12, comp_col_w 176, role_col_w 128, gap 12, header_h 36, row_h 48, stride 56). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _cc_02_01_paths import build

rows = [
    ("쓰기 관통", "캐시와 DB 에 바로", [
        ("앱", "SET user:42=Lee"), ("캐시", "UPDATE name=Lee"), None, None, None,
    ]),
    ("쓰기 지연", "DB 는 나중에 한 번", [
        ("앱", "SET views:42=101"), ("앱", "SET views:42=102"), ("앱", "SET views:42=103"), ("캐시", "UPDATE views=103"), None,
    ]),
    ("쓰기 우회", "쓰기는 DB 에만", [
        ("앱", "UPDATE name=Lee"), ("앱", "GET user:42"), ("캐시", "Kim"), None, None,
    ]),
]
build("BYTEBYTEGO · 02-01 §1", "쓰기 전략은 DB 가 언제 값을 받는지가 갈린다",
      "관통은 곧바로, 지연은 모아서 한 번, 우회는 DB 에만 씁니다",
      rows, (1, 3), "DB 가 받는 유일한 쓰기", "02-01.write-paths.svg")
