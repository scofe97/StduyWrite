# 타입 스펙: type-flowchart — 이상 동작 탐지 뒤 "막을 수 있는가"로 갈라진다. 예는 예방(focal)으로 끝나고, 아니오는 경보 수신 뒤 다섯 처리 선택으로 퍼지는데 선택마다 대가라는 막다른 길이 붙고, 세 번째(재생성)는 탐지로 되돌아오는 악순환 고리다.
# 사실 출처: 노트 L148~L152(막을 것인가 알릴 것인가 · 예방 · 경보만 띄우는 모드), L154~L162(다섯 딜레마 표), L164(컨테이너가 뜬다 → 탐지 → 종료 → 오케스트레이터 재생성 악순환), L166~L170(정답 없음 · 예방이 낫다 · 프로파일 밖 실행 불가 · 막으면서 경보·로그).
# Layout conventions: 다이아몬드 w=200 h=80, 다섯 열 w=172 stride 184(x=24부터), 단계 간 간격 28~36. 모든 좌표 4의 배수(열 중심 x+86 제외).
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, INFO, KR, MONO, RULE

W, H = 960, 684


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "CONTAINER SECURITY · 13-01 §3",
      "막지 못하는 도구의 경보는 다섯 처리 방식 모두 대가를 치릅니다",
      "이상 동작을 탐지하면 막을 수 있는지 먼저 가른다. 막을 수 있으면 실행 자체가 일어나지 않지만, 막지 못하면 경보를 받아 처리 방식을 골라야 한다. "
      "컨테이너 삭제, 프로세스 종료, 재생성, 롤백, 사람의 조사 각각에 대가가 따르고 재생성은 악순환으로 이어진다.",
      "그래서 저자는 치료보다 예방이 낫다고 결론짓습니다.")

# 1행 — 탐지와 분기
d.arrow([(200, 154), (228, 154)], INFO, "info", 1.4)
d.arrow([(432, 154), (476, 154)], ACC, "acc", 1.6)
d.arrow([(332, 196), (332, 232)], WARN, "warn", 1.4)

d.tone(24, 130, 176, 48, INFO, 24, "14", 1.2)
d.t(112, 159, "이상 동작 탐지", 14, INK, KR, "middle", 600)

d.o.append(f'<polygon points="232,154 332,114 432,154 332,194" fill="{INFO}14" stroke="{INFO}" stroke-width="1.2"/>')
d.t(332, 159, "막을 수 있는가?", 13, INK, KR, "middle", 600)
d.t(454, 144, "예", 12, ACC, KR, "middle", 600)
d.t(344, 220, "아니오", 12, WARN, KR, "start", 600)

# 예방 박스 (focal)
d.tone(480, 104, 452, 100, ACC, 6, "1F", 1.4)
d.t(496, 130, "예방", 14, ACC, KR, "start", 600)
for i, t in enumerate(("프로파일 밖 실행 파일 → 실행 불가", "좋은 프로세스는 평소처럼 동작", "막으면서 경보 · 로그도 남김 (최선)")):
    fit(t, 12, 452 - 32)
    d.t(496, 154 + 20 * i, t, 12, INK if i == 0 else MUTED, KR, "start", 600 if i == 0 else 400)

# 경보 수신 띠
d.tone(24, 236, 908, 40, WARN, 6, "12", 1.1)
d.t(478, 261, "경보 수신 · 처리 방식 선택", 14, WARN, KR, "middle", 600)

CX = [24 + 184 * i for i in range(5)]
CW = 172
OPTS = [
    ("컨테이너 자동 삭제", ("사용자 서비스 영향", "포렌식 증거 삭제")),
    ("문제 프로세스 종료", ("인젝션에 조종된", "'좋은' 프로세스")),
    ("오케스트레이터 재생성", ("같은 공격 재수신", "→ 악순환")),
    ("이전 버전 롤백", ("새 버전의", "롤백 가능 여부")),
    ("사람이 조사", ("반응까지 지연", "유출 · 피해 시간")),
]
OY, OH = 308, 48
PY, PH = 384, 72
for i, (opt, (p1, p2)) in enumerate(OPTS):
    x = CX[i]
    cx = x + CW // 2
    fit(opt, 13, CW - 24)
    fit(p1, 12, CW - 24)
    fit(p2, 12, CW - 24)
    loop = i == 2
    d.arrow([(cx, 278), (cx, OY - 4)], WARN, "warn", 1.4)
    d.tone(x, OY, CW, OH, WARN, 6, "14", 1.2)
    d.t(cx, OY + 29, opt, 13, INK, KR, "middle", 600)
    d.arrow([(cx, OY + OH + 2), (cx, PY - 4)], BAD, "bad", 1.4)
    d.tone(x, PY, CW, PH, BAD, 6, "14" if not loop else "1F", 1.1 if not loop else 1.8)
    d.t(cx, PY + 30, p1, 12, INK, kr(p1), "middle", 600)
    d.t(cx, PY + 52, p2, 12, BAD if loop else MUTED, kr(p2), "middle", 600 if loop else 400)

# 악순환 고리 — 세 번째 열에서 내려온다
SY, SH = 488, 112
d.arrow([(CX[2] + CW // 2, PY + PH + 2), (CX[2] + CW // 2, SY - 4)], BAD, "bad", 1.4)
d.tone(24, SY, 908, SH, BAD, 6, "0C", 1.4)
d.t(40, SY + 22, "악순환", 12, BAD, KR, "start", 600)
LOOP = ["컨테이너 기동", "나쁜 동작 탐지", "보안 도구가 종료", "오케스트레이터 재생성"]
NX = [48 + 228 * i for i in range(4)]
NW, NY, NH = 176, 528, 40
for i, t in enumerate(LOOP):
    fit(t, 13, NW - 20)
    d.tone(NX[i], NY, NW, NH, BAD, 6, "14", 1.1)
    d.t(NX[i] + NW // 2, NY + 25, t, 13, INK, KR, "middle", 600)
    if i < 3:
        d.arrow([(NX[i] + NW + 2, NY + 20), (NX[i + 1] - 4, NY + 20)], BAD, "bad", 1.4)
d.arrow([(NX[3] + NW // 2, NY + NH + 2), (NX[3] + NW // 2, 588), (NX[0] + NW // 2, 588), (NX[0] + NW // 2, NY + NH + 4)], BAD, "bad", 1.4)

d.legend(624, [("탐지 · 분기", INFO), ("예방", ACC), ("처리 선택", WARN), ("대가", BAD)])
d.save(str(ASSETS / "13-01.prevent-vs-alert.svg"))
print("ok 13-01 prevent-vs-alert")
