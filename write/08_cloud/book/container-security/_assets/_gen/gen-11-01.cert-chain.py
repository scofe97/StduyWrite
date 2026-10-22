# 타입 스펙: type-flowchart — 인증서 체인은 서명자를 따라 올라가다 "서명자 = 주체" 인 자체 서명 인증서에서 끝난다. 아니오 길은 다른 CA 인증서가 이어지는 끝없는 사슬. focal 은 자체 서명 인증서(Carol).
# 사실 출처: 노트 L96~L110(CA 도 인증서, 사슬은 자체 서명에서 끝, Ann·Bob·Carol 예, 신뢰는 선택), L114(루트 CA 미리 설치), L118(사설 시스템은 자체 서명으로 자기 CA)
# Layout conventions: 위 행 y=124(상자 폭 136·높이 84, 간격 52), 마름모 중심 (660,166), 아래 행 y=300 은 아니오 길을 오른쪽에서 왼쪽으로 잇는다. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, KR, MONO


def kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


W, H = 960, 476
d = D(W, H, "FLOWCHART · 11-01 §3",
      "인증서 체인은 서명자가 자기 자신인 인증서에서 끝납니다",
      "Ann 인증서는 Bob 이, Bob 인증서는 Carol 이 서명하고 Carol 인증서는 Carol 자신이 서명한다. 서명자가 주체와 같으면 사슬이 끝나고, 다르면 다른 CA 인증서가 끝없이 이어진다.",
      lead="사슬의 끝에서 신뢰는 검증되는 것이 아니라 선택됩니다")

BW, BH = 136, 84
Y1 = 124
XS = [48, 236, 424]          # Ann, Bob, Carol
CERTS = [("Ann 인증서", "Ann", "Bob"), ("Bob 인증서", "Bob", "Carol"), ("Carol 인증서", "Carol", "Carol")]


def cert(x, y, title, subj, issuer, c=None, focal=False):
    fit(title, 14, BW - 16)
    if focal:
        d.tone(x, y, BW, BH, ACC, 6, "1F", 1.6)
    else:
        d.box(x, y, BW, BH)
    d.t(x + BW / 2, y + 28, title, 14, ACC if focal else INK, KR, "middle", 600)
    d.t(x + BW / 2, y + 52, f"주체 {subj}", 12, INFO, MONO, "middle")
    d.t(x + BW / 2, y + 72, f"서명 {issuer}", 12, ACC if focal else INFO, MONO, "middle")


# 화살표는 상자 아래에 깔리도록 먼저 그린다
CY = Y1 + BH // 2
d.arrow([(XS[0] + BW + 2, CY), (XS[1] - 2, CY)], SOFT, "soft", 1.4)
d.arrow([(XS[1] + BW + 2, CY), (XS[2] - 2, CY)], SOFT, "soft", 1.4)

# 마름모: 서명자 = 주체?
DCX, DCY, DW, DH = 660, CY, 128, 100
d.arrow([(XS[2] + BW + 2, CY), (DCX - DW // 2 - 2, CY)], ACC, "acc", 1.5)
for (x, y), (t, a, b) in zip([(x, Y1) for x in XS], CERTS):
    cert(x, y, t, a, b, focal=(a == b))
pts = f"{DCX},{DCY-DH//2} {DCX+DW//2},{DCY} {DCX},{DCY+DH//2} {DCX-DW//2},{DCY}"
d.o.append(f'<polygon points="{pts}" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.6"/>')
d.t(DCX, DCY - 2, "서명자 =", 13, ACC, KR, "middle", 600)
d.t(DCX, DCY + 18, "주체?", 13, ACC, KR, "middle", 600)

# 예 → 끝
OX, OW = 776, 136
d.arrow([(DCX + DW // 2 + 2, DCY), (OX - 2, DCY)], OK, "ok", 1.5)
d.t((DCX + DW // 2 + OX) / 2, DCY - 12, "예", 12, OK, KR, "middle", 600)
d.tone(OX, DCY - 26, OW, 52, OK, 26, "14", 1.2)
fit("신뢰하기로 선택", 13, OW - 24)
d.t(OX + OW / 2, DCY + 5, "신뢰하기로 선택", 13, OK, KR, "middle", 600)

# 누가 신뢰를 고르는가 (노트 L114·L118)
d.t(OX + OW / 2, 232, "누가 고르나", 12, SOFT, KR, "middle", 600)
for y, t1, t2 in [(248, "공개 · 루트 CA", "브라우저 미리 설치"), (320, "사설 · 자기 CA", "자체 서명으로 생성")]:
    fit(t1, 13, OW - 16); fit(t2, 12, OW - 16)
    d.box(OX, y, OW, 56)
    d.t(OX + OW / 2, y + 24, t1, 13, INK, KR, "middle", 600)
    d.t(OX + OW / 2, y + 44, t2, 12, MUTED, KR, "middle")

# 아니오 → 끝없는 사슬 (오른쪽에서 왼쪽으로)
Y2 = 300
CY2 = Y2 + 36
d.arrow([(DCX, DCY + DH // 2 + 2), (DCX, CY2), (XS[2] + BW + 2, CY2)], BAD, "bad", 1.5, "5 4")
d.t(DCX + 12, 252, "아니오", 12, BAD, KR, "start", 600)
d.arrow([(XS[2] - 2, CY2), (XS[1] + BW + 2, CY2)], BAD, "bad", 1.4, "5 4")
d.arrow([(XS[1] - 2, CY2), (XS[0] + BW + 2, CY2)], BAD, "bad", 1.4, "5 4")
for x, t1, t2 in [(XS[2], "다른 CA 인증서", "서명 또 다른 CA"), (XS[1], "다른 CA 인증서", "서명 또 다른 CA")]:
    fit(t1, 14, BW - 16)
    d.tone(x, Y2, BW, 72, BAD, 6, "0F", 1.0)
    d.t(x + BW / 2, Y2 + 30, t1, 14, BAD, KR, "middle", 600)
    d.t(x + BW / 2, Y2 + 54, t2, 12, MUTED, kr(t2), "middle")
d.tone(XS[0], Y2, BW, 72, BAD, 6, "0F", 1.0)
d.t(XS[0] + BW / 2, Y2 + 30, "끝없는 사슬", 14, BAD, KR, "middle", 600)
d.t(XS[0] + BW / 2, Y2 + 54, "…", 14, MUTED, MONO, "middle")

d.legend(412, [("자체 서명 인증서", ACC), ("서명 필드", INFO), ("사슬 끝", OK), ("끝없는 사슬", BAD)])
d.save(str(ASSETS / "11-01.cert-chain.svg"))
print("ok 11-01 cert-chain")
