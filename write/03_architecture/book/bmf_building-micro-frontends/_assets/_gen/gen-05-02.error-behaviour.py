# 05-02 §4 — 조각 서비스가 실패했을 때 무엇을 할지. 저자의 analyseMFEresponse 코드가 갈리는 그대로다.
# 플레이스홀더에 적힌 errorbehaviour 값이 그 판단을 정한다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단. 모양이 종류를 나르고 색은 한 갈래에만 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, WARN, KR, MONO

W = 1300
LEGEND_Y = 522
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 05-02 §4",
      "실패한 조각을 어떻게 다룰 것인가",
      "플레이스홀더에 적어 둔 errorbehaviour 가 컴포저의 판단을 정한다. 색이 붙은 갈래가 페이지 전체를 살리는 쪽이다.",
      "마름모가 판단이고 사각형이 그 결과입니다")

# 연결선 먼저
d.arrow([(620, 156), (620, 170)], MUTED, "ar", 1.4)
d.arrow([(490, 216), (250, 216), (250, 312)], MUTED, "ar", 1.4)
d.arrow([(750, 216), (880, 216), (880, 284)], MUTED, "ar", 1.4)
d.arrow([(790, 330), (670, 330), (670, 440)], MUTED, "ar", 1.4)
d.arrow([(970, 330), (1070, 330), (1070, 440)], ACC, "acc", 1.5)

d.box(620 - 200, 104, 400, 52, PAPER2, RULE, 1.0, 6)
d.t(620, 128, "조각 서비스의 응답이 돌아왔다", 12.5, INK, KR, "middle", 600)
d.t(620, 145, "Promise.allSettled 결과 하나", 9, MUTED, MONO)

d.o.append(f'<polygon points="620,170 750,216 620,262 490,216" fill="{PAPER2}" stroke="{MUTED}" stroke-width="1.2"/>')
d.t(620, 221, "status 가 fulfilled 인가", 11.5, INK, KR, "middle", 600)
d.t(264, 262, "그렇다", 9.5, MUTED, MONO, "start")
d.t(894, 262, "아니다", 9.5, MUTED, MONO, "start")

d.box(250 - 165, 312, 330, 52, f"{INK}08", MUTED, 0.8, 6)
d.t(250, 336, "받은 HTML 을 그대로 끼운다", 12, INK, KR, "middle", 600)
d.t(250, 353, "컴포저는 내용을 해석하지 않는다", 9.5, MUTED, KR)

d.o.append(f'<polygon points="880,284 970,330 880,376 790,330" fill="{PAPER2}" stroke="{MUTED}" stroke-width="1.2"/>')
d.t(880, 334, "errorbehaviour", 10.5, INK, MONO, "middle", 600)

d.box(670 - 165, 440, 330, 52, PAPER2, RULE, 1.0, 6)
d.t(670, 464, "error · 예외를 던진다", 12, INK, KR, "middle", 600)
d.t(670, 481, "그 조각 없이는 페이지가 의미 없을 때", 9.5, WARN, KR)

d.tone(1070 - 165, 440, 330, 52, ACC, 6, "14", 1.3)
d.t(1070, 464, "hide · 그 자리를 비운다", 12, ACC, KR, "middle", 600)
d.t(1070, 481, "나머지 페이지는 그대로 뜬다", 9.5, ACC, KR)

d.t(658, 400, "error", 9, MUTED, MONO, "end")
d.t(1086, 400, "hide · 기본값", 9, ACC, MONO, "start")

d.legend(LEGEND_Y, [("페이지 전체를 살리는 갈래", ACC), ("페이지를 함께 실패시키는 갈래", WARN)])
d.save("05-02.error-behaviour.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
