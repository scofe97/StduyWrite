# 타입 스펙: type-sequence
# 사실 출처: NPG Ch.11 §3 Listing 11-17~11-19, §4 실패 시험(attacker.example.com), crypto/tls/handshake_server.go sendAlert(alertBadCertificate)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

def is_kr(txt):
    return any("가" <= c <= "힣" for c in str(txt))

def fam_of(txt):
    return KR if is_kr(txt) else MONO

W, H = 960, 1024
d = Seq(W, H, "NPG CH.11 — CLIENT ADDRESS VERIFICATION SEQUENCE",
        "서버의 접속 주소 추출 및 인증서 SAN 검증 흐름",
        "GetConfigForClient 로 소켓 주소를 확보하고 VerifyPeerCertificate 로 인증서 이름을 대조합니다",
        "GetConfigForClient 클로저 · net.SplitHostPort · net.LookupAddr PTR · opts.DNSName 대조")

# ── 참여자 레인 정의 ──────────────────────────────────────────────────────────
# 4의 배수 그리드 준수
x1 = 92    # 클라이언트
x2 = 336   # 서버 crypto/tls
x3 = 608   # GetConfigForClient 클로저
x4 = 868   # 리졸버(PTR)

LX = {
    "client": x1,
    "server": x2,
    "closure": x3,
    "resolver": x4,
}
d.LX = LX

actors = [
    ("client", x1, 144, "클라이언트", "tls.Dial"),
    ("server", x2, 176, "서버 crypto/tls", "handshake_server.go"),
    ("closure", x3, 208, "GetConfigForClient 클로저", "연결별 tls.Config"),
    ("resolver", x4, 144, "리졸버(PTR)", "net.LookupAddr"),
]

y_box = 104
h_box = 44
for _, cx, bw, name, sub in actors:
    d.box(cx - bw / 2, y_box, bw, h_box, PAPER2, RULE, 1.0)
    d.t(cx, y_box + 20, name, 12, INK, KR, "middle", 600)
    d.t(cx, y_box + 36, sub, 11, MUTED, fam_of(sub), "middle")

# ── 레일 (생명선 점선) ────────────────────────────────────────────────────────
y_rail_top = y_box + h_box + 6  # 154
y_rail_bot = 944
for cx in LX.values():
    d.line(cx, y_rail_top, cx, y_rail_bot, RULE, 1.0, "3 6")

# ── 활성 막대 (Activation bars: ALT 틀과 분리된 호출 구간) ─────────────────
# 클로저: GetConfigForClient 실행 구간
d.box(x3 - 4, 216, 8, 220, fill=PAPER2, stroke=RULE, sw=0.8, r=2)
# 리졸버: LookupAddr 실행 구간
d.box(x4 - 4, 304, 8, 44, fill=PAPER2, stroke=RULE, sw=0.8, r=2)

# ── 메시지 헬퍼 ───────────────────────────────────────────────────────────────
def msg_call(a, b, label, y, c=INFO, mk="info", dash=None, sw=1.4):
    xa, xb = LX[a], LX[b]
    dr = 1 if xb > xa else -1
    x_start = xa + 4 * dr
    x_end = xb - 6 * dr
    d.path(f"M {x_start} {y} L {x_end} {y}", c, sw, m=mk, dash=dash)
    mx = (xa + xb) / 2
    d.t(mx, y - 8, label, 11, c, fam_of(label), "middle", 600)

def self_loop(actor, y, l1, l2=None, c=MUTED, mk="ar", c_l1=None, c_l2=None):
    xa = LX[actor]
    d.path(f"M {xa + 4} {y - 10} L {xa + 28} {y - 10} L {xa + 28} {y + 10} L {xa + 7} {y + 10}", c, 1.3, m=mk)
    d.t(xa + 36, y - 3 if l2 else y + 4, l1, 11, c_l1 or INK, fam_of(l1), "start", 600 if c_l1 else 400)
    if l2:
        d.t(xa + 36, y + 13, l2, 11, c_l2 or MUTED, fam_of(l2), "start")

# ── 1. ClientHello ────────────────────────────────────────────────────────────
msg_call("client", "server", "ClientHello", 180, c=INFO, mk="info")

# ── 2. GetConfigForClient(hello) ──────────────────────────────────────────────
msg_call("server", "closure", "GetConfigForClient(hello)", 220, c=INFO, mk="info")

# ── 3. 소켓 주소 추출 ────────────────────────────────────────────────────────
self_loop("closure", 264,
          'RemoteAddr() → net.SplitHostPort',
          '→ "127.0.0.1"',
          c=MUTED, mk="ar", c_l1=INK, c_l2=INFO)

# ── 4. PTR 역방향 조회 ────────────────────────────────────────────────────────
msg_call("closure", "resolver", 'net.LookupAddr("127.0.0.1")', 308, c=MUTED, mk="ar")

# ── 5. 리졸버 응답 ────────────────────────────────────────────────────────────
msg_call("resolver", "closure", '["localhost"]', 344, c=MUTED, mk="ar", dash="4 3")

# ── 6. hostnames 후보 목록 구성 ──────────────────────────────────────────────
self_loop("closure", 388,
          'hostnames = ["localhost", "127.0.0.1"]',
          'append(hostnames, ip) · IP 덧붙임',
          c=MUTED, mk="ar", c_l1=INK, c_l2=MUTED)

# ── 포커스: hostnames 보관 브래킷 (6 -> 11) ────────────────────────────────
# 강조색(ACC) 1곳: 6에서 생성된 hostnames가 11(VerifyPeerCertificate)까지 유지됨
d.path(f"M {x3 - 6} 392 L {x3 - 16} 392 L {x3 - 16} 596 L {x3 - 6} 596", ACC, 1.5)
d.t(x3 - 24, 496, "hostnames 보관", 11, ACC, KR, "end", 600)

# ── 7. 연결 전용 Config 반환 ─────────────────────────────────────────────────
msg_call("closure", "server", "이 연결 전용 *tls.Config", 432, c=MUTED, mk="ar", dash="4 3")

# ── 8. CertificateRequest ─────────────────────────────────────────────────────
msg_call("server", "client", "CertificateRequest", 472, c=INFO, mk="info")

# ── 9. 클라이언트 인증서 제출 ────────────────────────────────────────────────
# 2줄 라벨 (화살표 바로 위)
d.path(f"M {x1 + 4} 516 L {x2 - 6} 516", INFO, 1.4, m="info")
d.t((x1 + x2) / 2, 516 - 20, "Certificate (clientCert.pem)", 11, INK, MONO, "middle")
d.t((x1 + x2) / 2, 516 - 7, "+ CertificateVerify", 11, INFO, MONO, "middle", 600)

# ── 10. 서버 기본 검증 (체인·기간·용도) ───────────────────────────────────────
self_loop("server", 560,
          "기본 검증: ClientCAs 체인",
          "유효 기간 · ClientAuth 용도",
          c=MUTED, mk="ar", c_l1=INK, c_l2=MUTED)

# ── 11. VerifyPeerCertificate 호출 ───────────────────────────────────────────
# 2줄 라벨 (화살표 바로 위)
d.path(f"M {x2 + 4} 608 L {x3 - 6} 608", INFO, 1.4, m="info")
d.t((x2 + x3) / 2, 608 - 18, "VerifyPeerCertificate", 11, INFO, MONO, "middle", 600)
d.t((x2 + x3) / 2, 608 - 6, "(verifiedChains)", 10, MUTED, MONO, "middle")

# ── 12. leaf SAN 후보 대조 루프 ──────────────────────────────────────────────
self_loop("closure", 648,
          "chain[0].Verify(DNSName=후보)",
          "후보 호스트명 순차 대조",
          c=MUTED, mk="ar", c_l1=INK, c_l2=MUTED)

# ── ALT 결합 프래그먼트 틀 (클라이언트 · 서버 · 클로저 3개 생명선만 포괄) ─────
fx = 44
fy = 684
fw = 612
fh = 244
d.box(fx, fy, fw, fh, fill="rgba(245,245,245,0.03)", stroke=RULE, sw=1.0, r=4)

# ALT 연산자 탭
d.box(fx, fy, 40, 16, fill=PAPER2, stroke=RULE, sw=1.0, r=2)
d.t(fx + 20, fy + 12, "ALT", 8, SOFT, MONO, "middle", 600)

# ── ALT 분기 1: [SAN 에 후보가 있음] ──────────────────────────────────────────
d.t(fx + 52, fy + 18, "[SAN 에 후보가 있음]", 11, OK, KR, "start", 600)

# 클로저 -> 서버: return nil
msg_call("closure", "server", "return nil", 732, c=OK, mk="ok", dash="4 3")

# 서버 -> 클라이언트: 핸드셰이크 완료 (강조색 ACC: headline success)
msg_call("server", "client", "Application Data · Read 정상", 768, c=ACC, mk="acc", sw=1.8)

# ── ALT 구분선 ────────────────────────────────────────────────────────────────
y_div = 800
d.line(fx + 8, y_div, fx + fw - 8, y_div, c=RULE, sw=1.0, dash="4 3")

# ── ALT 분기 2: [SAN 이 attacker.example.com 뿐] ──────────────────────────────
d.t(fx + 52, y_div + 18, "[SAN 이 attacker.example.com 뿐]", 11, BAD, KR, "start", 600)

# 클로저 -> 서버: client authentication failed
msg_call("closure", "server", "client authentication failed", 848, c=BAD, mk="bad", dash="4 3")

# 서버 -> 클라이언트: bad_certificate(42) 경고
msg_call("server", "client", "bad_certificate(42) 경고", 884, c=BAD, mk="bad", sw=1.4)

# 클라이언트 쪽 에러 라벨 (Read 호출 결과)
d.t(x1 + 10, 908, "Read: remote error: tls: bad certificate", 11, BAD, MONO, "start")

# ── 범례 ─────────────────────────────────────────────────────────────────────
d.legend(976, [
    ("기본 핸드셰이크 교환", INFO),
    ("후보 보관 · 통과", ACC),
    ("검증 승인 (nil)", OK),
    ("인증 실패 (Alert)", BAD),
])

out_path = os.path.join(os.path.dirname(__file__), "..", "11-02.client-addr-verification.svg")
d.save(out_path)
print("saved:", out_path)
