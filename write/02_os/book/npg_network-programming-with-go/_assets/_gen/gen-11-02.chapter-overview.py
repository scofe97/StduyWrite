# 11-02.chapter-overview — 상호 TLS 는 직접 만든 인증서로 클라이언트를 검증하고 접속 주소를 맞춥니다
# 본문 요구(11-02 「학습 목표」 개념도 문단): 절 네 개를 가로 한 줄로 잇고, 절 사이로 넘어가는 값을 화살표에 단다.
#   §1 서버가 RequireAndVerifyClientCert 로 클라이언트 인증서를 요구 → §2 ClientAuth 용도·SAN 을 담은 인증서를 만든다
#   → §3 서버가 기본 검증(체인·기간·용도)에 접속 주소 ↔ SAN 대조를 더한다 → §4 tls.Dial 은 성공하고 거절은 Read 에서 116·42 경고로 드러난다.
# 타입 스펙: type-architecture — 노드 4개 가로 한 줄. 노드 x = 20 + j·240, 폭 200, 높이 110, y = 150.
#           절 사이 화살표는 노드 위를 넘는 아치(오른쪽 노드 위 30px 지점까지), 넘어가는 값은 아치 위 칩.
# 사실 출처: 노트 11-02 핵심 요약(35~41줄), §1 RequireAndVerifyClientCert, §2 ExtKeyUsage·SAN, §3 기본 검증·주소 대조, §4 Dial·Read 경고.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, KR, MONO

W, H = 960, 340
X0, STRIDE, NW, NH, NY = 20, 240, 200, 110, 150
ARCH_Y = NY - 34


def nx(j):
    return X0 + j * STRIDE


def fam(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "NPG CH.11 — 11-02 OVERVIEW",
      "상호 TLS 는 직접 만든 인증서로 클라이언트를 검증하고 접속 주소를 맞춥니다",
      "서버가 요구한 클라이언트 인증서를 직접 만들고, 서버가 기본 검증에 접속 주소 대조를 더하며, 거절은 클라이언트의 Read 에서 드러납니다",
      "절 사이 화살표 위 칩은 다음 절로 넘어가는 값입니다")

nodes = [
    ("§1", "서버가 요구", [("RequireAndVerifyClientCert", MUTED), ("CertificateRequest", MUTED)]),
    ("§2", "인증서 만들기", [("ExtKeyUsage ClientAuth", MUTED), ("SAN localhost · 127.0.0.1", MUTED)]),
    ("§3", "서버 검증", [("기본: 체인 · 기간 · 용도", MUTED), ("더함: 접속 주소 ↔ SAN", ACC)]),
    ("§4", "결과 확인", [("tls.Dial 성공", OK), ("Read 에서 116 · 42 경고", BAD)]),
]

for j, (sec, title, vals) in enumerate(nodes):
    x = nx(j)
    d.box(x, NY, NW, NH, stroke=RULE, sw=0.9, r=8)
    d.t(x + 14, NY + 22, sec, 10, SOFT, MONO, "start", 600)
    d.t(x + NW / 2, NY + 40, title, 14, INK, KR, "middle", 600)
    for k, (v, c) in enumerate(vals):
        vy = NY + 68 + k * 24
        if c == ACC:
            d.o.append(f'<rect x="{x + 10}" y="{vy - 15}" width="{NW - 20}" height="22" rx="4" '
                       f'fill="{ACC}18" stroke="{ACC}" stroke-width="1.2"/>')
        d.t(x + NW / 2, vy, v, 11, c, fam(v), "middle", 600 if c in (ACC, OK, BAD) else 400)

arches = ["클라이언트 인증서 필요", "clientCert.pem", "통과 / 경고"]
for j, lab in enumerate(arches):
    x1 = nx(j) + NW - 30
    x2 = nx(j + 1) + 30
    d.arrow([(x1, NY), (x1, ARCH_Y), (x2, ARCH_Y), (x2, NY - 2)], c=MUTED, m="ar", sw=1.3)
    cx = (x1 + x2) / 2
    w = 112 if j != 0 else 128
    d.o.append(f'<rect x="{cx - w / 2}" y="{ARCH_Y - 11}" width="{w}" height="22" rx="4" '
               f'fill="{PAPER}" stroke="{MUTED}" stroke-width="0.8"/>')
    d.t(cx, ARCH_Y + 4, lab, 11, INK, fam(lab), "middle")

d.legend(292, [("이 편이 더한 검증", ACC), ("성공", OK), ("거절 경고", BAD)])
out_path = pathlib.Path(__file__).resolve().parent.parent / "11-02.chapter-overview.svg"
d.save(str(out_path))
print("ok 11-02 overview:", out_path)
