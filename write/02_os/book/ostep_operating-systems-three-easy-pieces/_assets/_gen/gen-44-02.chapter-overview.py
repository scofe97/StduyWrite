# 44-02 개념도 — 키 한 점으로 모이는 길 셋과 무작위 키가 가운데 키로 들어가고, 키를 쥔 기계의 한계(못 넘는 선)를 지나, 그래도 OS 가 암호를 쓰는 자리 셋과 서명한 capability 로 퍼진다.
# 본문 요구(44-02 「학습 목표」 개념도 문단): 왼쪽 키가 새거나 약해지는 길(키 유출·줄어든 키 공간·예측되는 시드 §1, 무작위 키 §1),
#           가운데 키(§1)와 못 넘는 선(§2), 오른쪽 암호를 쓰는 자리(비밀번호 해시·네트워크 전송 §2, 저장 데이터 암호화 §3, 서명한 capability §4), 바닥 원칙(§4).
# 값 근거: 본문 「무차별 대입과 키 길이」(32가지, 6번째 시도, 126개 후보), 「무작위 난수로 키 만들기」, 「암호가 쓸모 있는 세 자리」, 「전체 디스크 암호화와 키의 위치」, 「담을 수 있는 정보와 JWT」.
# 타입 스펙: type-architecture — 구성요소를 존으로 묶고 라벨 붙은 화살표로 잇는 노드 그래프. 고른 이유: 이 편의 줄기가 「여러 길이 키 한 점으로 모였다가
#             한계선을 지나 자리 여럿으로 퍼진다」는 모임-퍼짐이라 순서표·격자로는 키가 중심이라는 점이 안 보인다. 스펙에 모임-퍼짐 전용 공식은 없어
#             좌표는 4 의 배수로 직접 잡았다. (옛 판의 4행 × 3열 격자 공식 열 x = 64 + j·344 는 쓰지 않는다.)
import sys; sys.path.insert(0, ".")
from dd import D, MUTED, RULE, ACC, OK, INFO, KR, MONO

W, H = 1000, 780


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "ARCHITECTURE · 44-02 OVERVIEW",
      "암호는 키에서 깨지고 OS 는 키를 숨길 수 없는 선 안에서 암호를 쓴다",
      "44-02 의 키워드 개념도. 왼쪽 세 길은 키가 새거나 후보가 줄거나 시드가 예측되어 키가 깨지는 경로이고 네 번째는 무작위로 키를 만드는 대응이며, 모두 가운데 키로 모인다. "
      "키 아래는 OS 가 키를 쥔 기계에서는 OS 로부터 데이터를 숨길 수 없다는 못 넘는 선이다. "
      "그 선을 지나서도 암호가 쓸모 있는 자리는 비밀번호 해시, 네트워크 전송, 저장 데이터 암호화 셋이다. "
      "키에서는 개인 키로 서명한 capability 가 오른쪽으로 나간다. 바닥은 키를 적은 곳에 짧은 시간만 적은 상대에게 둔다는 원칙이다.",
      lead="화살표에 붙은 글자는 두 요소의 관계, 칩은 그 요소를 다루는 절, 왼쪽에서 가운데를 거쳐 오른쪽으로 읽습니다.")


def node(x, y, w, h, title, sub, c, sec, sub2=None):
    d.tone(x, y, w, h, c, 6, "14", 1.1)
    d.chip(x + 24, y + 14, sec, c, 11)
    d.t(x + w / 2, y + 40, title, 14, c, kr(title), "middle", 600)
    d.t(x + w / 2, y + 58, sub, 13, MUTED, kr(sub), "middle")
    if sub2:
        d.t(x + w / 2, y + 74, sub2, 13, MUTED, kr(sub2), "middle")


# 구역 머리
for x, x2, cap in ((24, 232, "키가 새거나 약해지는 길"), (352, 616, "키의 비밀"), (768, 976, "OS 가 암호를 쓰는 자리")):
    d.t(x, 112, cap, 13, MUTED, KR, "start", 600)
    d.line(x, 120, x2, 120, RULE, 0.8)

# 가운데 — 키 (가장 크게, 주황)
KX, KY, KW, KH = 352, 148, 264, 316
d.tone(KX, KY, KW, KH, ACC, 8, "1e", 1.6)
d.chip(KX + 28, KY + 24, "§1", ACC, 11)
d.t(KX + KW / 2, KY + 168, "키", 36, ACC, KR, "middle", 700)
d.t(KX + KW / 2, KY + 206, "알고리즘이 아니라 키에서 깨짐", 13, MUTED, KR, "middle")
d.t(KX + KW / 2, KY + 228, "이점은 전적으로 키의 비밀에", 13, MUTED, KR, "middle")

# 왼쪽 — 키가 새거나 약해지는 길 (파랑, 전부 키로 모임)
LX, LW = 24, 208
leaks = (("키 유출", "Heartbleed · 공유 개인 키", "키가 알려지면"),
         ("줄어든 키 공간", "32가지 · 6번째 시도", "후보가 줄면"),
         ("예측되는 시드", "시각 시드 · 후보 126개", "방법을 알면"))
for i, (a, b, lab) in enumerate(leaks):
    y = 148 + i * 84
    node(LX, y, LW, 64, a, b, INFO, "§1")
    d.arrow([(LX + LW + 2, y + 32), (KX - 2, y + 32)], INFO, "info", 1.5)
    d.t((LX + LW + KX) / 2, y + 22, lab, 13, MUTED, KR, "middle", 600)

# 왼쪽 아래 — 무작위 키 (초록 대응), 위로 올라가 키 왼쪽으로 들어감
node(LX, 520, LW, 64, "무작위 키", "getrandom · /dev/urandom", OK, "§1")
d.arrow([(LX + LW / 2, 518), (LX + LW / 2, 432), (KX - 2, 432)], OK, "ok", 1.5)
d.t(244, 422, "무작위로 만들면", 13, MUTED, KR, "middle", 600)

# 가운데 아래 — 못 넘는 선
BX, BY, BW, BH = 352, 520, 264, 84
node(BX, BY, BW, BH, "못 넘는 선", "OS 가 키를 쥔 기계에서는", INFO, "§2", "OS 로부터 숨길 수 없음")
d.arrow([(KX + KW / 2, KY + KH + 2), (KX + KW / 2, BY - 2)], INFO, "info", 1.5)
d.t(KX + KW / 2 + 12, 498, "OS 가 키를 쥐면", 13, MUTED, KR, "start", 600)

# 오른쪽 — 서명한 capability (키에서 곧장)
RX, RW = 768, 208
node(RX, 232, RW, 64, "서명한 capability", "개인 키 서명 · exp 만료", OK, "§4")
d.arrow([(KX + KW + 2, 264), (RX - 2, 264)], OK, "ok", 1.5)
d.t((KX + KW + RX) / 2, 254, "개인 키로 서명", 13, MUTED, KR, "middle", 600)

# 오른쪽 — 못 넘는 선의 예외 세 자리
uses = (("비밀번호 해시", "일방향 · 복호 불가", "§2"),
        ("네트워크 전송", "중간 장비가 키를 갖지 않음", "§2"),
        ("저장 데이터 암호화", "장치에 닿는 접근만 막음", "§3"))
for i, (a, b, s) in enumerate(uses):
    node(RX, 348 + i * 84, RW, 64, a, b, OK, s)
TX = 724
d.arrow([(BX + BW + 2, 562), (TX, 562), (TX, 380), (RX - 2, 380)], OK, "ok", 1.5)
d.arrow([(TX, 464), (RX - 2, 464)], OK, "ok", 1.5)
d.arrow([(TX, 548), (RX - 2, 548)], OK, "ok", 1.5)
d.t(670, 550, "예외 세 자리", 13, MUTED, KR, "middle", 600)

# 바닥 — 원칙 한 줄
node(24, 652, 952, 64, "원칙", "키는 적은 곳에, 짧은 시간만, 적은 상대에게", OK, "§4")
d.arrow([(KX + KW / 2, BY + BH + 2), (KX + KW / 2, 650)], OK, "ok", 1.5)
d.t(KX + KW / 2 + 12, 634, "보호가 사라지므로", 13, MUTED, KR, "start", 600)

d.legend(H - 40, [("전제 · 문제", INFO), ("대응", OK), ("이 편의 한 점", ACC)])
d.save("44-02.chapter-overview.svg")
print("ok 44-02 overview")
