# 05-04 §3 — 로컬 함수 호출과 네트워크 RPC 사이의 다섯 가지 근본적인 동작 차이 비교.
# 사실 출처: 05-04 §3(L61~L67), 원서 The problems with remote procedure calls (PDF p.23~24). 원서는 여섯 항목, 본문은 인자 인코딩과 언어 간 타입을 합쳐 다섯.
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
H = 604
LEG = H - 56

d = D(W, H, "05-04 · RPC LOCATION TRANSPARENCY", "로컬 함수 호출 대 네트워크 RPC 비교",
      "로컬 함수 호출과 네트워크 RPC 사이의 다섯 가지 차이와 location transparency 의 한계를 견준다.",
      "예측 가능성 · 타임아웃 · 재시도 중복 · 가변 지연 · 인자 인코딩")

COL_SIDE_W = 340
COL_MID_W = 128
X_LEFT = 24
X_MID = 376
X_RIGHT = 516
Y0 = 104

# 3열 헤더 박스
d.box(X_LEFT, Y0, COL_SIDE_W, 36, PAPER2, OK, 1.2)
d.t(X_LEFT + COL_SIDE_W / 2, Y0 + 23, "로컬 함수 호출 (Local Call)", 13, OK, KR, "middle", 600)

d.box(X_MID, Y0, COL_MID_W, 36, PAPER2, RULE, 1.0)
d.t(X_MID + COL_MID_W / 2, Y0 + 23, "비교 기준", 13, INK, KR, "middle", 600)

d.box(X_RIGHT, Y0, COL_SIDE_W, 36, PAPER2, WARN, 1.2)
d.t(X_RIGHT + COL_SIDE_W / 2, Y0 + 23, "네트워크 RPC (Remote Call)", 13, WARN, KR, "middle", 600)

# 5가지 비교 항목
rows = [
    ("예측 가능성",
     "제어 가능한 성공·실패", "매개변수와 로컬 상태에 종속",
     "통제 밖 결함 노출", "요청·응답 손실 · 원격 머신 느림·불가용"),
    ("타임아웃",
     "명확한 반환 상태", "결과 반환 · 예외 · 안 돌아옴",
     "도달 여부 판단 불가", "타임아웃 시 요청 도착 여부 확인 불가"),
    ("재시도 중복",
     "중복 실행 위험 없음", "네트워크 재시도가 없음",
     "중복 실행 부작용", "응답 유실 시 재시도 → 멱등성 메커니즘 필수"),
    ("가변 지연",
     "대체로 일정한 시간", "네트워크 요청보다 훨씬 빠름",
     "가변적 지연 변동", "1ms 미만 ~ 혼잡·과부하 시 수 초"),
    ("인자 인코딩",
     "포인터 직접 전달", "로컬 메모리 객체 참조를 넘김",
     "바이트 인코딩 필수", "모든 인자를 바이트로 · 언어 간 타입 번역"),
]

ROW_H = 58
GAP_Y = 10

for idx, (dim, l_title, l_sub, r_title, r_sub) in enumerate(rows):
    y = 152 + idx * (ROW_H + GAP_Y)

    # 좌측: 로컬 호출 카드
    d.box(X_LEFT, y, COL_SIDE_W, ROW_H, PAPER, RULE, 0.8)
    d.t(X_LEFT + 16, y + 23, l_title, 12, OK, KR, "start", 600)
    d.t(X_LEFT + 16, y + 43, l_sub, 12, MUTED, KR, "start")

    # 중앙: 비교 기준
    d.box(X_MID, y, COL_MID_W, ROW_H, PAPER2, RULE, 0.8)
    d.t(X_MID + COL_MID_W / 2, y + 34, dim, 12, INK, KR, "middle", 600)

    # 우측: 네트워크 RPC 카드
    d.box(X_RIGHT, y, COL_SIDE_W, ROW_H, PAPER, WARN, 0.9)
    d.t(X_RIGHT + 16, y + 23, r_title, 12, WARN, KR, "start", 600)
    d.t(X_RIGHT + 16, y + 43, r_sub, 12, BAD if "중복" in r_title or "불가" in r_title else MUTED, KR, "start")

# 하단 결론 박스
Y_BOT = 152 + 5 * (ROW_H + GAP_Y) + 6
d.box(X_LEFT, Y_BOT, W - 48, 38, PAPER2, INFO, 1.2)
d.t(W / 2, Y_BOT + 24, "location transparency 한계 · 네트워크 호출과 로컬 함수의 근본적 괴리", 12, INFO, KR, "middle", 600)

d.legend(LEG, [("로컬 메모리 호출", OK), ("원격 네트워크 RPC", WARN), ("중복·통제 밖 결함", BAD), ("설계 원칙", INFO)])
d.save("05-04.rpc-vs-local.svg")
