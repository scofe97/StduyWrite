# 04-01 개념도 — 직접 실행이 낳는 두 문제(위험한 일, 통제권 되찾기)가 갈라지고, 문제마다 짝지은 장치가 같은 trap table 을 거쳐 커널에 들어간다.
# 본문 요구(04-01 「학습 목표」 개념도 문단): 왼쪽 출발 직접 실행(§1), 가운데 두 문제(§1), 오른쪽 제한된 직접 실행 틀 안의 대응 —
#           위 갈래 사용자·커널 모드(§2)·시스템 콜과 trap(§2), 아래 갈래 타이머 인터럽트(§3)·문맥 교환(§4), 둘이 함께 쓰는 trap table(§2),
#           곁가지 인터럽트 중첩·비용 측정(§5), 위쪽 gVisor 가 받는 쪽을 바꾼 사례(§6).
# 값 근거: 개념도라 값은 없다.
# 공식 근거: OSTEP 6장 §6.1~§6.5, gVisor 플랫폼 문서(systrap·KVM).
# 타입 스펙: type-architecture — 구성요소를 존으로 묶고 라벨 붙은 화살표로 잇는 노드 그래프. 고른 이유: 이 장의 줄기가
#             「하나(직접 실행)에서 두 문제로 갈라지고 문제마다 장치가 짝지어지되 두 갈래가 같은 trap table 로 모인다」는 갈래·합류라
#             절 순서의 격자로는 짝과 합류가 안 보인다. 존(제한된 직접 실행 틀)과 라벨 화살표를 그릴 수 있는 가장 가까운 타입이라 골랐다.
#             스펙에 갈래 전용 공식은 없어 좌표는 4 의 배수 stride 로 직접 잡았다.
#             (옛 판의 7행 × 3열 격자 공식 열 x = 60 + j·340 은 쓰지 않는다.)
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 984, 796


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "ARCHITECTURE · 04-01 OVERVIEW",
      "직접 실행이 낳는 두 문제를 모드·trap 과 타이머·문맥 교환이 나눠 푼다",
      "04-01 의 키워드 개념도. 왼쪽 직접 실행은 빠르지만 그동안 운영체제 코드가 돌지 않아 통제를 잃는다. 여기서 두 문제가 갈라진다. "
      "위 갈래는 프로그램이 위험한 일을 하는 문제이고 사용자 모드와 시스템 콜 trap 이 막는다. 아래 갈래는 CPU 를 쥔 프로그램에게서 제어를 되찾는 문제이고 "
      "타이머 인터럽트로 되찾은 뒤 문맥 교환으로 프로세스를 바꾼다. 책의 모델에서 두 갈래는 부팅 때 깔아 둔 같은 trap table 을 거쳐 커널에 들어간다. "
      "주황 틀이 속도는 직접 실행으로 얻고 통제는 미리 깔아 둔 길로 지키는 제한된 직접 실행이다. 위쪽의 gVisor 는 시스템 콜을 받는 쪽을 Sentry 로 바꾸고, "
      "아래쪽은 인터럽트 중첩과 비용 측정이라는 곁가지다.",
      lead="화살표 위 글자는 두 요소의 관계, 칩은 그 요소를 다루는 절, 왼쪽에서 오른쪽으로 읽습니다.")


def node(x, y, w, h, title, sub, c, sec, sub2=None):
    d.tone(x, y, w, h, c, 6, "14", 1.1)
    d.chip(x + 24, y + 14, sec, c, 11)
    d.t(x + w / 2, y + 40, title, 14, c, kr(title), "middle", 600)
    d.t(x + w / 2, y + 58, sub, 13, MUTED, kr(sub), "middle")
    if sub2:
        d.t(x + w / 2, y + 74, sub2, 13, MUTED, kr(sub2), "middle")


NH = 68
TOP_Y, BOT_Y, MID_Y = 288, 524, 408

# 왼쪽 구역 머리
for x, x2, cap in ((24, 164, "출발"), (288, 428, "두 문제")):
    d.t(x, 262, cap, 13, MUTED, KR, "start", 600)
    d.line(x, 270, x2, 270, RULE, 0.8)

# 출발 — 직접 실행
node(24, 398, 140, 84, "직접 실행", "CPU 에서 그대로", INFO, "§1", "빠르지만 통제를 잃음")

# 두 문제
node(288, TOP_Y, 140, NH, "위험한 일", "하지 못하게 막기", INFO, "§1")
node(288, BOT_Y, 140, NH, "제어 되찾기", "쥔 프로그램에게서", INFO, "§1")
d.arrow([(166, 440), (176, 440), (176, TOP_Y + 34), (286, TOP_Y + 34)], INFO, "info", 1.5)
d.t(231, TOP_Y + 24, "제한이 없으면", 13, MUTED, KR, "middle", 600)
d.arrow([(176, 440), (176, BOT_Y + 34), (286, BOT_Y + 34)], INFO, "info", 1.5)
d.t(231, BOT_Y + 24, "실행되지 않으면", 13, MUTED, KR, "middle", 600)

# 제한된 직접 실행 틀
FX, FY, FW, FH = 544, 224, 424, 384
d.tone(FX, FY, FW, FH, ACC, 8, "10", 1.4)
d.t(FX + 16, FY + 28, "제한된 직접 실행", 17, ACC, KR, "start", 700)
d.t(FX + 16, FY + 48, "속도는 직접 실행, 통제는 깔아 둔 길", 13, MUTED, KR, "start")
d.chip(FX + FW - 28, FY + 24, "§1", ACC, 11)

AX, AW, BX, BW = 560, 148, 808, 144
node(AX, TOP_Y, AW, NH, "사용자 · 커널 모드", "제한된 연산 보호", OK, "§2")
node(BX, TOP_Y, BW, NH, "시스템 콜 · trap", "커널에 들어감", OK, "§2")
node(AX, BOT_Y, AW, NH, "타이머 인터럽트", "하드웨어가 강제로", OK, "§3")
node(BX, BOT_Y, BW, NH, "문맥 교환", "swtch() · 레지스터", OK, "§4")

# 두 갈래가 함께 쓰는 trap table
node(AX, MID_Y, 392, 64, "trap table", "책의 모델에서 부팅 때 깔아 둔 행선지", OK, "§2")

# 문제 → 대응
d.arrow([(430, TOP_Y + 34), (558, TOP_Y + 34)], INFO, "info", 1.5)
d.t(493, TOP_Y + 24, "모드로 막고", 13, MUTED, KR, "middle", 600)
d.arrow([(430, BOT_Y + 34), (558, BOT_Y + 34)], INFO, "info", 1.5)
d.t(493, BOT_Y + 24, "타이머로 되찾고", 13, MUTED, KR, "middle", 600)

# 대응 안의 흐름
d.arrow([(AX + AW + 2, TOP_Y + 34), (BX - 2, TOP_Y + 34)], OK, "ok", 1.4)
d.t((AX + AW + BX) / 2, TOP_Y + 24, "시스템 콜로", 13, MUTED, KR, "middle", 600)
d.arrow([(AX + AW + 2, BOT_Y + 34), (BX - 2, BOT_Y + 34)], OK, "ok", 1.4)
d.t((AX + AW + BX) / 2, BOT_Y + 24, "바꾸기로 하면", 13, MUTED, KR, "middle", 600)

# 두 갈래가 trap table 로 모인다
d.arrow([(880, TOP_Y + NH + 2), (880, MID_Y - 4)], OK, "ok", 1.4)
d.t(868, 388, "행선지를 정함", 13, MUTED, KR, "end", 600)
d.arrow([(634, BOT_Y - 2), (634, MID_Y + 64 + 4)], OK, "ok", 1.4)
d.t(646, 504, "같은 표에 등록", 13, MUTED, KR, "start", 600)

# 곁가지 — 받는 쪽을 바꾼 gVisor, 인터럽트 중첩과 비용 측정
node(760, 104, 208, NH, "gVisor", "Sentry 가 시스템 콜을 처리", MUTED, "§6")
d.arrow([(880, TOP_Y - 2), (880, 104 + NH + 4)], SOFT, "soft", 1.3, "4 3")
d.t(868, 206, "받는 쪽을 바꾸면", 13, MUTED, KR, "end", 600)

node(560, 648, 260, NH, "인터럽트 중첩 · 비용 측정", "남긴 질문 · 비용 재는 법", MUTED, "§5")
d.arrow([(634, BOT_Y + NH + 2), (634, 644)], SOFT, "soft", 1.3, "4 3")
d.t(646, 632, "다른 인터럽트가 오면", 13, MUTED, KR, "start", 600)

d.legend(H - 40, [("전제 · 문제", INFO), ("대응", OK), ("이 편의 핵심", ACC), ("곁가지 · 예고", MUTED)])
d.save("04-01.chapter-overview.svg")
print("ok 04-01 overview")
