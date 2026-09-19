# 04-01 §4 「Certificate — 체인째 옵니다」 — 체인이 어디까지 오고 어디부터 이미 갖고 있는가.
# 본문 요구: "서버가 인증서 체인으로 설정돼 있으면 체인 전체가 서버 인증서와 함께 클라이언트에 제시됩니다.
#            클라이언트는 체인의 최상위 인증서를 자기가 저장한 CA 인증서와 대조하며, 현대 브라우저는
#            신뢰할 수 있는 CA 제공자로부터 루트 CA 를 미리 설치해 둡니다."
#            루트는 보통 전송에서 생략하며, 신뢰 저장소까지 검증 경로를 연결한다.
# 타입 스펙: type-dependency — 각 인증서가 상위 발급자의 공개키에 의존해 검증된다. 화살표가 의존 방향이고,
#           세로줄이 그 사슬이다. 왼쪽은 선을 타고 온 것, 오른쪽은 클라이언트가 이미 가진 것으로 가른다.
#           focal 은 사슬이 닫히는 자리 — 여기서 신뢰 저장소와 만나야 검증이 끝난다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 700
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-01 §4",
      "체인은 어디까지 오고 어디부터 이미 갖고 있는가",
      "Certificate 메시지에는 서버 인증서와 필요한 중간 CA 인증서가 실려 온다. 루트 CA는 보통 전송에서 생략한다. "
      "서버 인증서에서 발급자 방향으로 서명을 확인해 클라이언트가 별도로 신뢰하는 루트에 도달해야 한다. "
      "서버가 루트를 함께 보냈다는 사실만으로 신뢰가 생기지는 않는다.",
      "루트는 보통 전송에서 생략합니다. 신뢰 여부는 클라이언트의 신뢰 저장소가 정합니다")

LX, LW = 60, 420          # 선을 타고 온 것
RX, RW = 540, 372         # 이미 갖고 있는 것
CH = 92
Y = [214, 346, 478]       # 서버 인증서 · 중간 CA · 루트 CA

d.t(LX, 178, "Certificate 메시지로 온 것", 12, INFO, KR, "start", 600)
d.t(RX, 178, "클라이언트가 이미 가진 것", 12, OK, KR, "start", 600)
d.line(LX + LW + 30, 196, LX + LW + 30, 586, RULE, 1.0, "4 6")

def cert(x, w, y, title, issuer, inside, c, focal=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.tone(x, y, w, CH, c, 8)
    col = ACC if focal else c
    d.t(x + 18, y + 30, title, 13, col, KR, "start", 600)
    d.t(x + 18, y + 54, issuer, 11, MUTED, KR, "start")
    d.t(x + 18, y + 74, inside, 11, SOFT, KR, "start")

cert(LX, LW, Y[0], "서버 인증서", "발급자 — 중간 CA", "안에 공개키 하나 · 발급자 서명 하나", INFO)
cert(LX, LW, Y[1], "중간 CA 인증서", "발급자 — 루트 CA", "안에 공개키 하나 · 발급자 서명 하나", INFO)
# 루트는 위에 발급자가 없어 자기 개인키로 자기를 서명한다 — 그래서 여기서 사슬이 끝난다
cert(RX, RW, Y[2], "루트 CA 인증서", "신뢰 저장소에 미리 설치됨",
     "자기가 자기를 서명 — 사슬의 끝", OK, focal=True)

# 서버에서 발급자 방향으로 각 서명을 확인한다. 이 도식의 화살표 방향은 위에서 아래다.
d.arrow([(LX + LW + 14, Y[0] + CH / 2), (LX + LW + 14, Y[1] + CH / 2 + 10),
         (LX + LW - 6, Y[1] + CH / 2 + 10)], ACC, "acc", 1.5)
d.t(LX + LW + 22, Y[0] + CH / 2 + 34, "서버 인증서의 서명을 중간 CA 의 공개키로 확인", 11, ACC, KR, "start")
# 대각선은 규약 금지 — 아래로 내린 뒤 가로로 건너간다
d.arrow([(LX + LW / 2, Y[1] + CH), (LX + LW / 2, Y[2] + CH / 2), (RX - 8, Y[2] + CH / 2)], ACC, "acc", 1.5)
d.t(LX + LW / 2 + 12, Y[2] + CH / 2 - 10, "중간 CA 의 서명을 루트 CA 의 공개키로 확인", 11, ACC, KR, "start")

# 사슬이 닫히지 않는 경우
d.line(24, 592, W - 48, 592, RULE, 0.8, "4 6")
d.t(24, 620, "체인 검증 실패의 예", 12, SOFT, KR, "start", 600)
for i, (cond, res) in enumerate((("중간 CA 를 확보하지 못함", "신뢰 루트로 경로 구성 실패"),
                                 ("루트가 저장소에 없음", "검증할 기준이 없음"))):
    x = 260 + i * 360
    d.t(x, 620, cond, 11, INK, KR, "start")
    d.t(x, 640, res, 11, MUTED, KR, "start")
# 가능한 Alert 예시이며 모든 구현이 같은 코드를 보내는 것은 아니다.
d.t(24, 644, "가능한 Alert", 11, MUTED, KR, "start")
d.chip(150, 640, "unknown_ca(48)", BAD, 11)

d.legend(H - 40, [("사슬이 닫히는 자리", ACC), ("선을 타고 온 것", INFO), ("이미 갖고 있는 것", OK)])
d.save("04-01.certificate-chain.svg")
