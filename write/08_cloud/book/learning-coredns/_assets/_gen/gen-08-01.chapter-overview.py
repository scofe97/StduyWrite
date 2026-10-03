# 08-01 학습 목표 뒤 전체 지도 — 도구 여섯이 무엇을 보고, 기본으로 무엇을 남기며, 어디서 값을 깎는가.
# 본문 근거: 이 노트 §1~§7 과 결정 치트시트. 소스 근거: plugin/trace/setup.go(every 기본 1), plugin/dnstap(버퍼 1만),
#            1.7.0 릴리스 노트(카운터 다섯 개명·흡수), log README "JSON Output", errors README(LEVEL·show_first·stacktrace).
# 타입 스펙: type-dp-security-matrix — 도구(행) × 보는 것·기본값·손잡이·원서 이후(열) 격자가 논지다.
#           2026-10-03 절 제목을 이은 노드 사슬에서 실제 값이 든 격자로 다시 그렸다. 옛 범례 "손잡이가 없어 금지" 는
#           본문(금지 이유는 복구를 끄기 때문)과 모순이라 없앴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 630
d = D(W, H, "LEARNING COREDNS · 08-01",
      "도구마다 무엇을 남기고 어디서 깎는가",
      "관측 도구 여섯을 보는 것, 아무것도 적지 않았을 때 남는 것, 값을 깎는 손잡이, 원서 이후 바뀐 것으로 나란히 놓았다. "
      "손잡이 열을 따라 읽으면 도구를 고르는 일이 곧 손잡이를 고르는 일이라는 이 노트의 축이 보인다.",
      "주황 열이 값을 깎는 손잡이입니다")

COLS = [(20, 110, "도구"), (140, 130, "보는 것"), (280, 170, "기본으로 남는 것"),
        (460, 170, "손잡이"), (640, 170, "원서 이후"), (820, 44, "절")]
rows = [
    ("prometheus", ("몇 건 · 얼마나", ""), ("라벨 조합마다", "시계열 하나"), ("CoreDNS 에 없음", "수집 규칙에서 거름"), ("넷 개명 · 하나 흡수", "1.7.0 · view 라벨"), "§1"),
    ("log", ("어느 질의였나", ""), ("질의마다 한 줄", "텍스트"), ("NAMES · class", "형식 문자열"), ("JSON 출력 모드", "time 필드 포함"), "§2·3"),
    ("dnstap", ("응답까지", ""), ("주소 · 시각 · 유형", "버퍼 1만 개"), ("full", "메시지 원문을 실을지"), ("listen · extra", "tls 스킴"), "§4"),
    ("errors", ("처리 중 오류", ""), ("오류마다 한 줄", ""), ("consolidate", "기간 · 정규식"), ("LEVEL · show_first", "stacktrace"), "§5"),
    ("trace", ("어디서 시간을", ""), ("모든 요청 추적", "every 기본 1"), ("every", "표본율"), ("zipkin · datadog 만", ""), "§6"),
    ("debug", ("panic 의 스택", ""), ("복구가 꺼짐", "panic 이 프로세스를 끝냄"), ("없음", "켜고 끄기뿐"), ("errors stacktrace", "복구를 둔 채 스택"), "§7"),
]
Y0, PITCH, RH = 132, 64, 56

for k, (x, w, head) in enumerate(COLS):
    d.t(x + 10, 118, head, 12, ACC if k == 3 else SOFT, KR, "start", 600)

fx, _, _ = COLS[3]
d.tone(fx - 4, Y0 - 4, COLS[3][1] + 8, PITCH * 5 + RH + 8, ACC, 8, "12", 1.4)

for i, (tool, *cells) in enumerate(rows):
    y = Y0 + i * PITCH
    x0, w0, _ = COLS[0]
    d.box(x0, y, w0, RH, PAPER2, RULE, 1.0, 6)
    d.t(x0 + 10, y + 34, tool, 13, INK, MONO, "start", 600)
    for k, cell in enumerate(cells, start=1):
        x, w, _ = COLS[k]
        if k != 3:
            d.box(x, y, w, RH, PAPER2, RULE, 1.0, 6)
        if k == 5:
            d.t(x + w / 2, y + 34, cell, 12, MUTED, KR)
            continue
        main, sub = cell
        col = ACC if k == 3 else INK
        if sub:
            d.t(x + 10, y + 24, main, 13, col, KR, "start", 600)
            d.t(x + 10, y + 44, sub, 12, MUTED, KR, "start")
        else:
            d.t(x + 10, y + 34, main, 13, col, KR, "start", 600)

d.t(20, 540, "1~4절 · 정상 흐름을 보는 도구 · 5~7절 · 잘못됐을 때 쓰는 도구", 13, MUTED, KR, "start")
d.t(20, 564, "debug 금지 이유 · 손잡이가 없어서가 아니라 복구를 끄기 때문", 13, MUTED, KR, "start")

d.legend(584, [("값을 깎는 손잡이", ACC)])
d.save("08-01.chapter-overview.svg")
