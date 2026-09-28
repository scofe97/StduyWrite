# 04-04 B7 — 키 로그 한 줄의 첫 값이 ClientHello 난수와 짝을 이뤄 그 연결만 연다. 값은 문서처럼 줄여 적는다.
# 타입 스펙: type-flowchart — 난수 일치 여부로 갈리는 판단. B6 과 같은 좌표 틀. focal 은 옛 캡처(A1)가 비는 끝.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _tls_lab import W, EYEBROW, Flow, text_w, ACC, OK, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO
H = 552
d = Flow(W, H, EYEBROW + "B7", "B7 · 키 로그 한 줄이 여는 연결",
         "SSLKEYLOGFILE 이 남긴 한 줄은 CLIENT_RANDOM 라벨, ClientHello 난수, master secret 으로 이뤄진다. 캡처의 ClientHello 난수와 같은 줄이 있을 때만 그 연결이 열린다.",
         "첫 값이 색인이라, 기록되지 않은 연결에는 쓸 줄이 없습니다")
CX, RX = 300, 700
# 키 로그 한 줄 — 세 칸
d.box(24, 104, 552, 100, PAPER2, RULE, 1.0, 6)
d.t(40, 124, "b7-keys.log 한 줄", 11, SOFT, KR, "start", 600)
cells = [("CLIENT_RANDOM", "라벨", MUTED), ("4f87d368843b…", "ClientHello 난수 · 색인", INFO), ("9a2c31e0bb7d…", "master secret", MUTED)]
x = 40
for v, lab, c in cells:
    w = max(text_w(v, 12), text_w(lab, 11)) + 24
    d.o.append(f'<rect x="{x:.1f}" y="136" width="{w:.1f}" height="28" rx="4" fill="{PAPER}" stroke="{c}" stroke-width="1"/>')
    d.t(x + w / 2, 155, v, 12, c if c != MUTED else INK, MONO, "middle", 600)
    d.t(x + w / 2, 186, lab, 11, MUTED, KR if any("가" <= ch <= "힣" for ch in lab) else MONO)
    x += w + 12
d.arrow([(CX, 204), (CX, 228)], MUTED, "ar", 1.4)
d.diamond(CX, 232, 124, 40, "난수가 같은 줄?")
# 오른쪽 — b7 캡처
d.arrow([(CX + 124, 272), (RX - 144, 272)], MUTED, "ar", 1.4)
d.t(CX + 136, 260, "있음 · b7 캡처", 11, MUTED, KR, "start", 600)
d.step(RX, 236, 280, 72, "세션 키 계산", "ECDHE 인데도 복호화")
d.arrow([(RX, 308), (RX, 412)], MUTED, "ar", 1.4)
d.oval(RX, 416, 280, 40, "평문 스트림", OK)
# 아래 — A1 옛 캡처
d.arrow([(CX, 312), (CX, 412)], MUTED, "ar", 1.4)
d.t(CX + 12, 360, "없음 · A1 캡처", 11, MUTED, KR, "start", 600)
d.oval(CX, 416, 280, 40, "다시 비어 있음", focal=True)
d.legend(H - 56, [("기록 밖 연결은 안 열림", ACC), ("기록된 연결", OK), ("색인 값", INFO)])
d.save("04-04.b7-keylog-index.svg")
