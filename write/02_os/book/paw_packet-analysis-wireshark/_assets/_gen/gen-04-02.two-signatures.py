# 04-02 §1 「두 서명이 가르는 것」 — 같은 핸드셰이크에 나오는 서명 둘을 나란히 세워 가른다.
# 본문 요구: 표가 여섯 축(있는 곳·주체·보증 대상·시점·검증 키·복사 가능)을 세지만,
#            "왜 하나는 복사되고 하나는 안 되는가"가 표로는 안 선다.
#            만들어지는 시점을 축으로 두 줄을 그려, 발급 때 한 번 굳는 값과
#            연결마다 새로 나는 값이 다르다는 것을 보인다.
# 타입 스펙: type-sequence — 서명이 만들어지는 시간순 흐름. 발급 시점과 연결 시점을 구분선으로
#           나눠 쌓고, 같은 자리를 두 번 그려 무엇이 굳고 무엇이 매번 나는지 대조한다.
#           focal 은 소유 증명을 지는 서버 서명 하나다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 600
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-02 §1",
      "CA 서명과 서버 서명 — 보증 대상과 수명",
      "인증서 안의 CA 서명은 발급 때 한 번 만들어져 인증서에 굳는다. 그래서 인증서를 통째로 베끼면 "
      "이 서명도 따라간다. ServerKeyExchange 의 서버 서명은 이번 연결의 공개값에 대해 그때 만들어지므로 "
      "베낄 대상이 없다. 소유 증명이 인증서 밖에 있는 이유가 이 시점 차이다.",
      "TLS 1.2 ECDHE 기준입니다. 정적 RSA 는 서버 서명 자리가 비고 Finished 가 그 역할을 대신합니다")

LX, RX = 300, 660
BW, BH = 240, 62

# ── 시간축 ────────────────────────────────────────────────
d.t(24, 156, "발급 때", 12, SOFT, KR, "start", 600)
d.t(24, 174, "한 번", 12, SOFT, KR, "start", 600)
d.t(24, 358, "연결마다", 12, SOFT, KR, "start", 600)
d.t(24, 376, "새로", 12, SOFT, KR, "start", 600)

# ── A · CA 서명 (발급 시점) ───────────────────────────────
d.box(LX - BW / 2, 128, BW, BH, PAPER2, RULE, 1.0, 8)
d.t(LX, 154, "CA 개인키", 13, INK, KR, "middle", 600)
d.t(LX, 174, "ca.key", 12, MUTED, MONO, "middle")

d.arrow([(LX + BW / 2, 159), (RX - BW / 2 - 6, 159)], INFO, "info", 1.4)
d.t((LX + RX) / 2, 148, "서명", 12, INFO, KR, "middle", 600)

d.tone(RX - BW / 2, 128, BW, BH, INFO, 8)
d.t(RX, 154, "인증서 안의 CA 서명", 13, INFO, KR, "middle", 600)
d.t(RX, 174, "a.test.crt", 12, MUTED, MONO, "middle")

d.t(RX + BW / 2 + 16, 159, "주인 보증", 12, SOFT, KR, "start")

# 굳는다 — 발급 이후 값이 고정됨을 아래 화살표로
d.arrow([(RX, 190), (RX, 236)], MUTED, "ar", 1.2)
d.t(RX + 14, 216, "값이 굳음", 11, MUTED, KR, "start")

d.box(RX - BW / 2, 236, BW, 40, PAPER, RULE, 1.0, 6)
d.t(RX, 261, "연결마다 같은 값", 12, MUTED, KR, "middle")

# ── 구분선 ────────────────────────────────────────────────
d.line(24, 300, W - 24, 300, RULE, 0.8, "4 6")

# ── B · 서버 서명 (연결 시점) ─────────────────────────────
d.box(LX - BW / 2, 330, BW, BH, PAPER2, RULE, 1.0, 8)
d.t(LX, 356, "서버 개인키", 13, INK, KR, "middle", 600)
d.t(LX, 376, "a.test.key", 12, MUTED, MONO, "middle")

d.arrow([(LX + BW / 2, 361), (RX - BW / 2 - 6, 361)], ACC, "acc", 1.6)
d.t((LX + RX) / 2, 350, "서명", 12, ACC, KR, "middle", 600)

d.o.append(f'<rect x="{RX - BW / 2}" y="330" width="{BW}" height="{BH}" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(RX, 356, "ServerKeyExchange 의 서명", 12, ACC, KR, "middle", 600)
d.t(RX, 376, "x25519 공개값 32B + 서명 256B", 11, MUTED, MONO, "middle")

d.t(RX + BW / 2 + 16, 361, "소유 증명", 12, SOFT, KR, "start")

d.arrow([(RX, 392), (RX, 424)], MUTED, "ar", 1.2)
d.box(RX - BW / 2, 424, BW, 40, PAPER, RULE, 1.0, 6)
d.t(RX, 449, "연결마다 다른 값", 12, MUTED, KR, "middle")

# ── 결론 축 ───────────────────────────────────────────────
d.line(24, 490, W - 24, 490, RULE, 0.8)
d.t(24, 512, "베낀 인증서는 CA 서명까지 따라오지만, 이번 연결의 공개값에 붙일 서명은 만들지 못함",
     13, INK, KR, "start", 600)

d.legend(H - 40, [("주인 보증 · 복사 가능", INFO), ("소유 증명 · 복사 불가", ACC)])
d.save("04-02.two-signatures.svg")
