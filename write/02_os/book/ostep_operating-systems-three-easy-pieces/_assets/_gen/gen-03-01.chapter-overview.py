# 03-01 개념도 — 부모 줄과 자식 줄이 나란히 흐르고, fork 와 exec 사이의 틈에서 자식이 열어 둔 파일을 바꿔 프로그램을 고치지 않고 리다이렉션이 된다.
# 본문 요구(03-01 「학습 목표」 개념도 문단): 위 부모 줄(fork §1 → wait §2), 아래 자식 줄(자식 §1 → 틈 §4 → exec §3 → 새 프로그램 §3),
#           틈에서 내려오는 이점(리다이렉션·파이프 §4)과 합친 호출의 한계(§4), 줄 바깥에서 들어오는 시그널(§5).
# 값 근거: 개념도라 값은 없다.
# 공식 근거: OSTEP 5장 §5.1~§5.4, 5.6.
# 타입 스펙: type-architecture — 구성요소를 줄(존)로 묶고 라벨 붙은 화살표로 잇는 노드 그래프. 고른 이유: 이 편의 줄기가
#             「두 프로세스의 시간 흐름 사이에서 한 구간이 일을 한다」는 두 줄의 병행이라 절 격자로는 틈이 보이지 않는다.
#             시간축 순서표(Seq)는 같은 노트의 shell-line 도식이 이미 쓰므로 피하고, 줄 두 개와 틈 하나를 노드로 그렸다.
#             스펙에 두 줄 전용 공식은 없어 좌표는 4 의 배수 stride 로 직접 잡았다. (옛 판의 5행 × 3열 격자 공식은 쓰지 않는다.)
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 984, 640


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "ARCHITECTURE · 03-01 OVERVIEW",
      "fork 와 exec 사이의 틈에서 프로그램을 고치지 않고 환경을 바꾼다",
      "03-01 의 키워드 개념도. 위쪽 부모 줄은 셸이 fork 로 복제한 뒤 wait 로 자식이 끝나기를 기다리는 흐름이다. "
      "아래쪽 자식 줄은 부모의 복제본으로 시작해 틈을 지나 exec 으로 다른 프로그램을 덮어쓰고 실행하는 흐름이다. "
      "틈은 아직 셸의 코드가 도는 구간이라 열어 둔 파일을 바꿀 수 있고, 그래서 리다이렉션과 파이프가 프로그램을 고치지 않고 된다. "
      "생성과 실행을 합친 호출은 정해진 목록만 바꾼다. 시그널은 두 줄 바깥에서 이미 도는 프로세스로 들어온다.",
      lead="화살표 위 글자는 두 요소의 관계, 칩은 그 요소를 다루는 절, 줄마다 왼쪽에서 오른쪽으로 읽습니다.")


def node(x, y, w, h, title, sub, c, sec, sub2=None):
    d.tone(x, y, w, h, c, 6, "14", 1.1)
    d.chip(x + 24, y + 14, sec, c, 11)
    d.t(x + w / 2, y + 40, title, 14, c, kr(title), "middle", 600)
    d.t(x + w / 2, y + 58, sub, 13, MUTED, kr(sub), "middle")
    if sub2:
        d.t(x + w / 2, y + 74, sub2, 13, MUTED, kr(sub2), "middle")


def harrow(x1, x2, y, label, c=SOFT, m="soft", lw=1.3):
    d.arrow([(x1 + 2, y), (x2 - 2, y)], c, m, lw)
    d.t((x1 + x2) / 2, y - 9, label, 13, MUTED, kr(label), "middle", 600)


# 줄 머리
d.t(24, 116, "부모 줄 · 셸", 13, MUTED, KR, "start", 600)
d.t(24, 272, "자식 줄", 13, MUTED, KR, "start", 600)

# 부모 줄
PY = 132
node(24, PY, 140, 64, "fork()", "명령을 받아 복제", INFO, "§1")
node(244, PY, 700, 64, "wait()", "자식이 끝날 때까지 부모를 막아 두고 끝나면 돌아옴", INFO, "§2")
harrow(164, 244, PY + 32, "복제 뒤")

# 자식 줄
CY = 330
node(24, CY, 140, 64, "자식 프로세스", "부모의 복제본", INFO, "§1")
node(594, CY, 150, 64, "exec()", "프로그램을 덮어씀", INFO, "§3")
node(814, CY, 130, 64, "새 프로그램", "실행 뒤 종료", INFO, "§3")

# 틈 — 이 도식에서 가장 크게
GX, GY, GW, GH = 244, 300, 280, 124
d.tone(GX, GY, GW, GH, ACC, 8, "1e", 1.6)
d.chip(GX + GW - 28, GY + 24, "§4", ACC, 11)
d.t(GX + GW / 2, GY + 52, "fork 와 exec 사이의 틈", 16, ACC, KR, "middle", 700)
d.t(GX + GW / 2, GY + 80, "셸 코드가 자식 안에서 돎", 13, MUTED, KR, "middle")
d.t(GX + GW / 2, GY + 100, "열어 둔 파일을 바꿈", 13, MUTED, KR, "middle")

harrow(164, 244, CY + 32, "exec 전")
harrow(526, 594, CY + 32, "바꾼 뒤", ACC, "acc", 1.5)
harrow(744, 814, CY + 32, "성공하면")

# 부모의 fork 가 자식을 만든다
d.arrow([(124, PY + 64 + 3), (124, CY - 3)], SOFT, "soft", 1.3)
d.t(136, 270, "복제해", 13, MUTED, KR, "start", 600)

# 자식이 끝나면 부모가 돌아온다
d.arrow([(900, CY - 3), (900, PY + 64 + 3)], SOFT, "soft", 1.3)
d.t(888, 270, "끝나면 돌아옴", 13, MUTED, KR, "end", 600)

# 아래 — 틈이 만드는 이점과 합친 호출의 한계
BY = 490
node(24, BY, 140, 64, "합친 호출", "정해진 것만 바꿈", INFO, "§4")
node(244, BY, 280, 64, "리다이렉션 · 파이프", "프로그램을 고치지 않음", OK, "§4")
harrow(164, 244, BY + 32, "목록으로만", OK, "ok", 1.4)
d.arrow([(GX + GW / 2, GY + GH + 3), (GX + GW / 2, BY - 3)], ACC, "acc", 1.5)
d.t(GX + GW / 2 + 12, 462, "그 틈에서 바꿔", 13, MUTED, KR, "start", 600)

# 곁가지 — 시그널
SX, SY, SW, SH = 754, 490, 190, 84
node(SX, SY, SW, SH, "kill() 과 시그널", "이미 도는 프로세스 제어", MUTED, "§5", "대상은 사용자 개념이 정함")
d.arrow([(850, SY - 3), (850, CY + 64 + 3)], SOFT, "soft", 1.3, "4 3")
d.t(838, 450, "이미 도는 프로세스로", 13, MUTED, KR, "end", 600)

d.legend(H - 40, [("호출 · 전제", INFO), ("이점", OK), ("핵심", ACC), ("곁가지", MUTED)])
d.save("03-01.chapter-overview.svg")
print("ok 03-01 overview")
