# 09-02 학습 목표 뒤 전체 지도 — 절 다섯과 각 절이 필요해지는 운영 상황. 09-01 지도(gen-09-01.chapter-overview.py)와 한 벌.
# 조건 두 줄은 모두 09-02 본문에서 뽑았다. 책 원문이 아니라 노트가 더한 운영 상황이다.
#   §1 "서비스를 내렸는데 프로세스가 한참 버티다 강제로 죽는 일이 있습니다"(§1 첫 문단, 56줄 근처)
#   §2 "프로세스를 죽이지 않고 진행 상황을 보거나 로그 파일을 다시 열게 하려면"(「USR1 로 쓰는 자리」),
#      "기본 동작이 Core 라도 코어 파일이 항상 생기지는 않습니다"(「코어 덤프와 자원 한도」)
#   §3 "컨테이너나 서비스가 137 이나 143 으로 끝나면 먼저 128 을 빼 봅니다"(「128+n 종료 코드와 systemctl stop」),
#      「kill·pkill·timeout 비교」 절 제목
#   §4 "프로세스가 살아 있으나 CPU 를 쓰지 않고 kill 에 반응이 없으면 ps 의 STAT 열부터 봅니다"(§4 첫 문단)
#   §5 "소스 없이 프로세스가 시그널을 어떻게 다루는지 보려면"(「/proc/PID/status 로 처리 방식 읽기」),
#      "SSH 세션에 남은 프로세스를 정리할 때는"(「loginctl·pkill -t 로 세션 끝내기」, 카드는 줄여 "남은 세션을 정리할 때")
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 언제 필요해지나)이 반복되고 읽는 순서가
#           화살표로 흐른다. 축약: 주체 lane 이 없어 카드 격자 stride 로 놓는다. 09-01 지도와 슬롯·stride·색·글자 크기가 같다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 428
d = D(W, H, "LEARNING MODERN LINUX · 09-02",
      "시그널은 번호 하나만 보내고 끝나는 모양은 처리 방식이 정한다",
      "둘째 편의 절 다섯을 읽는 순서로 이은 지도. 아래 두 줄은 그 절이 필요해지는 운영 상황이다.",
      "137 종료도 시그널로 읽습니다")

CW, CH, GAPX, GAPY, X0, Y0 = 272, 108, 12, 20, 20, 112
cards = [
    ("§1", "시그널의 정체와 기본 동작", "서비스 중지가 한참 버틸 때,", "강제로 죽을 때"),
    ("§2", "USR1 의 쓰임과 자원 한도", "로그를 다시 열게 할 때,", "코어가 안 생길 때"),
    ("§3", "보내는 도구와 종료 코드", "컨테이너가 137·143 일 때,", "시그널 보내는 도구를 고를 때"),
    ("§4", "멈춤과 재개", "살아 있는데 CPU 를 안 쓰고,", "kill 에 반응이 없을 때"),
    ("§5", "처리 방식 읽기와 세션 끝내기", "소스 없이 처리 방식을 읽을 때,", "남은 세션을 정리할 때"),
]
FOCAL = 2


def pos(i):
    return X0 + (i % 3) * (CW + GAPX), Y0 + (i // 3) * (CH + GAPY)


for i in range(len(cards) - 1):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.3)
    else:
        bus = y1 + CH + 10
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} {bus} "
               f"L {x2 + CW / 2} {bus} L {x2 + CW / 2} {y2 - 2}", MUTED, 1.3, m="ar")

for i, (n, title, c1, c2) in enumerate(cards):
    x, y = pos(i)
    focal = (i == FOCAL)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 16, y + 52, title, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, y + 76, c1, 12, MUTED, KR, "start")
    d.t(x + 16, y + 94, c2, 12, MUTED, KR, "start")

d.legend(384, [("운영 알림을 읽는 절", ACC)])
d.save("09-02.chapter-overview.svg")
print("ok 09-02.chapter-overview")
