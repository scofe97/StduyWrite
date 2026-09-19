# 04-01 §3 — cipher suite 이름 하나가 네 조각으로 분해된다.
# 본문 요구: "이 분해가 cipher suite 이름을 읽는 규칙 전부입니다. 다음 편에서 복호화 가능 여부를
#            가를 때 키 교환 방식과 확보한 비밀 정보를 함께 확인합니다."
#            표는 조각과 뜻을 짝지어 주지만, 이름 문자열의 *어느 자리*가 어느 조각인지는 안 보여 준다.
#            실제 문자열을 잘라 그 아래에 뜻을 매다는 편이 읽는 법을 그대로 가르친다.
# 타입 스펙: type-layers — 문자열 한 줄을 조각으로 나눈 층. 가로 위치가 곧 이름 안의 자리이고,
#           focal 은 서버 개인키만을 이용한 복호화의 제한을 설명하는 키 교환 조각이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 540
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-01 §3",
      "cipher suite 이름을 네 조각으로 읽는다",
      "원문 예제에서 서버가 고른 TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 를 이름 안의 자리대로 잘랐다. "
      "앞의 TLS 는 접두사이고 WITH 가 키 교환·인증 쪽과 암호·해시 쪽을 가르는 표지다. "
      "ECDHE는 서버 개인키만으로 사후 복호화할 수 없다. AES-GCM은 레코드 암호화와 무결성을 보호하고 SHA384는 PRF의 해시다.",
      "WITH 앞이 열쇠를 나누는 방법, 뒤가 나눈 열쇠로 하는 일입니다")

# 이름 문자열을 조각 폭에 맞춰 늘어놓는다 — 폭은 글자 수에 비례시킨다
PARTS = [
    ("TLS",     "접두사",       None,  False),
    ("ECDHE",   "키 교환",      ACC,   True),
    ("RSA",     "인증",         INFO,  False),
    ("WITH",    "가르는 표지",  None,  False),
    ("AES_256", "256비트 암호",  OK,    False),
    ("GCM",     "인증 암호 모드", OK,    False),
    ("SHA384",  "PRF 해시",     WARN,  False),
]
GAP, PAD = 8, 18
widths = [len(p[0]) * 11 + PAD * 2 for p in PARTS]
total = sum(widths) + GAP * (len(PARTS) - 1)
x = (W - 24 - total) / 2
# 자른 조각만 보이면 원래 문자열이 안 보인다 — 자르기 전 이름을 위에 한 줄 둔다
d.t(W / 2 - 12, 158, "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384", 13, SOFT, MONO)
d.t(W / 2 - 12, 178, "원문 예제에서 서버가 고른 이름", 11, MUTED, KR)

NY, NH = 212, 52                    # 이름 조각 띠
MY = 316                            # 뜻 칸

for (name, mean, c, focal), w in zip(PARTS, widths):
    if focal:
        d.o.append(f'<rect x="{x}" y="{NY}" width="{w}" height="{NH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif c:
        d.tone(x, NY, w, NH, c, 6)
    else:
        d.box(x, NY, w, NH, PAPER2, RULE, 1.0, 6)
    col = ACC if focal else (c if c else SOFT)
    d.t(x + w / 2, NY + 32, name, 13, col, MONO, "middle", 600)
    # 뜻은 아래로 내려 단다
    d.line(x + w / 2, NY + NH, x + w / 2, MY - 16, col if c or focal else RULE, 1.2)
    d.t(x + w / 2, MY, mean, 12, col if c or focal else MUTED, KR)
    x += w + GAP

# WITH 가 가르는 두 구역
d.line(24, 366, W - 48, 366, RULE, 0.8, "4 6")
d.t(24, 394, "WITH 앞 — 열쇠를 어떻게 나눌 것인가", 12, ACC, KR, "start", 600)
d.t(24, 416, "ECDHE: 임시 키 합의 · RSA: 서버 서명", 13, MUTED, KR, "start")
d.t(500, 394, "WITH 뒤 — 나눈 열쇠로 무엇을 할 것인가", 12, OK, KR, "start", 600)
d.t(500, 416, "AES-GCM: 레코드 보호 · SHA384: PRF 해시", 13, MUTED, KR, "start")

d.chip(W / 2 - 12, 458, "ECDHE · DHE: 서버 개인키만으로 사후 복호화 불가", ACC, 12)

d.legend(H - 44, [("키 합의 방식", ACC), ("서버 인증", INFO),
                  ("암호화·무결성", OK), ("PRF 해시", WARN)])
d.save("04-01.cipher-suite-anatomy.svg")
