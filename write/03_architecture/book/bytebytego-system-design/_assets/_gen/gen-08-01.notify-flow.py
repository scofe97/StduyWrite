# 타입 스펙: type-flowchart — 알림 한 건이 위에서 아래로 음소거·방해 금지·멘션 억제·스레드 구독을 거치며 한 칸이라도 걸리면 안 보냄으로 빠지고, 남으면 기기별 채널 pref 와 전역 pref 값으로 갈리는 판정 순서. 판정 마름모 대신 오른쪽 출구 상자가 분기를 나른다(조건 분기를 열 둘로 편 축약).
# 사실 출처: Slack Engineering, "Reducing Slack's memory footprint"(2017-03-03, 2021-03-23 갱신) 의 알림 판정 흐름도. 질문·값 이름은 그 그림을 직접 읽은 것이고 하위 분기(Mentions 아래 DM?·@here·Highlight word? 등)는 싣지 않았다. 추출본 v1.txt 886~900행, PDF 쪽 33 그림. https://slack.engineering/reducing-slacks-memory-footprint/
# Layout conventions: 질문 상자 폭 330·높이 40·stride 64(y=100+64k), 출구 상자 x=460 폭 300, 값 칩 폭 144·stride 160. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO


def fam(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


W, H = 960, 700
d = D(W, H, "BYTEBYTEGO · 08-01 §3",
      "알림은 음소거부터 기기별 pref 까지 순서대로 걸러진다",
      "음소거·방해 금지·멘션 억제에서 안 보냄으로 빠지고, 남은 건 기기별 pref 값이 가른다",
      "Slack 이 서버에서 판정하는 순서 · 하위 분기는 줄임")

X, QW, QH, S, Y0 = 40, 332, 40, 64, 100
rows = [
    ("채널 음소거?", "예 + 구독한 스레드 아님"),
    ("방해 금지(DnD) 중?", "예 + 덮어쓰기 없음"),
    ("@channel · @everyone · @here?", "예 + 채널 멘션 억제"),
    ("구독한 스레드 · threads_everything?", "채널 pref 가 Nothing"),
]
for k, (q, ex) in enumerate(rows):
    y = Y0 + k * S
    d.box(X, y, QW, QH, PAPER2, RULE, 0.9, 6)
    d.t(X + QW / 2, y + 25, q, 13, INK, fam(q), "middle", 600)
    d.arrow([(X + QW + 2, y + QH / 2), (460, y + QH / 2)], BAD, "bad", 1.4)
    d.tone(464, y, 300, QH, BAD, 6, "14", 1.1)
    d.t(614, y + 25, ex + " → 안 보냄", 13, BAD, KR, "middle")
    d.arrow([(X + QW / 2, y + QH + 2), (X + QW / 2, y + S - 2)], MUTED, "ar", 1.4)

y5 = Y0 + 4 * S
d.arrow([(766, Y0 + 3 * S + QH / 2), (780, Y0 + 3 * S + QH / 2)], OK, "ok", 1.4)
d.tone(784, Y0 + 3 * S, 148, QH, OK, 6, "14", 1.1)
d.t(858, Y0 + 3 * S + 25, "아니면 바로 보냄", 12, OK, KR, "middle")
d.tone(X, y5, QW, QH, ACC, 6, "14", 1.4)
d.t(X + QW / 2, y5 + 25, "이 기기의 채널 pref 는?", 13, ACC, KR, "middle", 600)
CY = y5 + S
chips = [
    ("Nothing", "안 보냄", BAD),
    ("Everything", "스레드면 구독 확인", INFO),
    ("Mentions", "멘션 조건", INFO),
    ("Default", "전역 pref 로", INFO),
]
d.line(X + 72, y5 + QH + 12, X + 3 * 160 + 72, y5 + QH + 12, RULE, 0.8)
d.line(X + QW / 2, y5 + QH + 2, X + QW / 2, y5 + QH + 12, RULE, 0.8)
for k, (v, sub, c) in enumerate(chips):
    x = X + k * 160
    d.tone(x, CY, 144, 56, c, 6, "14", 1.1)
    d.t(x + 72, CY + 24, v, 13, c, MONO, "middle", 600)
    d.t(x + 72, CY + 44, sub, 12, MUTED, KR, "middle")
    d.arrow([(x + 72, y5 + QH + 12), (x + 72, CY - 2)], MUTED, "ar", 1.0)

GY = CY + 88
d.arrow([(X + 3 * 160 + 72, CY + 58), (X + 3 * 160 + 72, GY - 8)], MUTED, "ar", 1.4)
d.line(X + 84, GY - 8, X + 4 * 176 + 84, GY - 8, RULE, 0.8)
vals = [("All", "스레드·구독 확인", INFO), ("Mentions", "멘션 조건", INFO), ("DMs (mobile)", "DM 이면", INFO),
        ("Highlight Words (mobile)", "단어 · @멘션", INFO), ("Never", "안 보냄", BAD)]
for k, (v, sub, c) in enumerate(vals):
    x = X + k * 176
    d.tone(x, GY, 168, 52, c, 6, "14", 1.0)
    d.t(x + 84, GY + 22, v, 11, c, MONO, "middle", 600)
    d.t(x + 84, GY + 42, sub, 12, MUTED, KR, "middle")
    d.arrow([(x + 84, GY - 8), (x + 84, GY - 2)], MUTED, "ar", 1.0)
d.t(X + 3 * 160 + 84, GY - 16, "Default 일 때 이 기기의 전역 pref", 12, SOFT, KR, "start")

MY = GY + 88
for k in (1, 2):
    xx = X + k * 160 + 72
    d.line(xx, CY + 56, xx, CY + 64, OK, 1.0)
d.line(24, CY + 64, X + 2 * 160 + 72, CY + 64, OK, 1.0)
d.arrow([(24, CY + 64), (24, MY + 20), (X - 2, MY + 20)], OK, "ok", 1.4)
for k in range(4):
    xx = X + k * 176 + 84
    d.line(xx, GY + 52, xx, GY + 68, OK, 1.0)
d.line(X + 84, GY + 68, X + 3 * 176 + 84, GY + 68, OK, 1.0)
d.arrow([(X + 84, GY + 68), (X + 84, MY - 2)], OK, "ok", 1.4)
d.tone(X, MY, QW, QH, OK, 6, "14", 1.1)
d.t(X + QW / 2, MY + 25, "통과하면 YES", 13, OK, KR, "middle", 600)
d.arrow([(X + QW + 2, MY + QH / 2), (460, MY + QH / 2)], MUTED, "ar", 1.4)
d.box(464, MY, 300, QH, PAPER2, RULE, 0.9, 6)
d.t(614, MY + 25, "모바일이면 푸시 타이밍 임계값", 13, INK, KR, "middle")

d.legend(H - 52, [("안 보냄", BAD), ("이 편의 초점", ACC), ("pref 값", INFO), ("보냄", OK)])
d.save("08-01.notify-flow.svg")
