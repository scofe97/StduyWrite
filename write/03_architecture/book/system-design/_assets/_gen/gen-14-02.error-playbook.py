# 타입 스펙: type-dp-security-matrix — 격자 문법을 비교 행렬로 쓴다. 행은 장애 위치 열둘(업로드·영상 분할·변환·전처리기·DAG 스케줄러·자원 관리자 큐·작업 서버·API 서버·캐시 서버·DB 주 서버·DB 복제 서버·영상 형식 깨짐), 열은 대응 방식 다섯이고 칸에 실제 대응이 적힌다.
# 사실 출처: 추출본 v2.txt 4276~4304행(복구 가능·복구 불가능 오류와 부품별 대응 목록). 두 대응이 함께 적힌 캐시 서버와 DB 복제 서버는 두 칸에 걸쳐 표시했다.
# Layout conventions: 행 이름 열 x=24 폭 196, 열 다섯 폭 140·stride 148(x=228 부터), 머리 y=96 높이 36, 줄 y=144 부터 stride 44 높이 36. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, INK, PAPER2, RULE, KR, MONO

W, H = 984, 744
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 14-02 §8",
      "장애 위치마다 정해 둔 대응은 다섯 갈래다",
      "같은 일을 다시 하거나 다른 부품이 대신 받거나 다시 만들어 이어가거나 새 서버로 바꾸고, 영상 형식이 깨졌으면 멈추고 오류 코드를 돌려준다.",
      "복구 가능한 오류는 앞의 넷 · 복구 불가능한 오류는 마지막 열")

X0, CW, ST = 228, 140, 148
HY, RY, RS, RH = 96, 144, 44, 36
COLS = ("같은 일 다시", "다른 부품이 대신", "다시 만들어 이어감", "새 서버로 교체", "멈추고 오류 코드")
# (행 이름, {열 번호: 칸 글자})
ROWS = (
    ("업로드", {0: "몇 번 재시도"}),
    ("영상 분할", {1: "서버가 분할"}),
    ("변환", {0: "재시도"}),
    ("전처리기", {2: "DAG 재생성"}),
    ("DAG 스케줄러", {2: "작업 재스케줄"}),
    ("자원 관리자 큐", {1: "복제본 사용"}),
    ("작업 서버", {1: "새 작업자 재시도"}),
    ("API 서버", {1: "다른 API 서버"}),
    ("캐시 서버", {1: "다른 노드 사용", 3: "새 서버로 교체"}),
    ("DB 주 서버", {1: "복제 서버 승격"}),
    ("DB 복제 서버", {1: "다른 복제 서버", 3: "새 서버로 교체"}),
    ("영상 형식 깨짐", {4: "작업 중단"}),
)


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


for i, name in enumerate(COLS):
    x = X0 + ST * i
    d.box(x, HY, CW, 36, PAPER2, RULE, 1.0, 6)
    d.t(x + CW / 2, HY + 23, name, 13, INK, KR, "middle", 600)

for r, (nm, cells) in enumerate(ROWS):
    y = RY + RS * r
    d.t(24, y + 23, nm, 13, INK, KR, "start", 600)
    d.line(24, y + RH + 4, W - 24, y + RH + 4, RULE, 0.6)
    two = len(cells) > 1
    for i, txt in cells.items():
        x = X0 + ST * i
        c = BAD if i == 4 else (WARN if two else OK)
        d.tone(x, y, CW, RH, c, 6, "14", 1.2)
        d.t(x + CW / 2, y + 23, txt, 13, c, KR, "middle", 600)

d.legend(H - 56, [("복구 가능 · 한 가지 대응", OK), ("복구 가능 · 두 대응을 함께", WARN), ("복구 불가능", BAD)])
d.save("14-02.error-playbook.svg")
