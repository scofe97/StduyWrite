# 타입 스펙: type-flowchart
# 사실 출처: NPG Ch.11 Listing 11-17~11-19(opts.Roots = serverPool = caCertPool("clientCert.pem")), crypto/tls.Config.GetConfigForClient, net.SplitHostPort, net.LookupAddr
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 500
d = D(W, H, "NPG CH.11 — CLIENT ADDRESS VERIFICATION FLOWCHART",
      "서버의 접속 주소 추출 및 인증서 SAN 검증 흐름",
      "GetConfigForClient 로 소켓 주소를 확보하고 VerifyPeerCertificate 로 인증서 이름을 대조합니다",
      "GetConfigForClient 클로저 · net.SplitHostPort · net.LookupAddr PTR · opts.DNSName 대조")

# 1. ClientHello 수신 상자 (INFO)
bx1, by1, bw1, bh1 = 30, 140, 180, 230
d.tone(bx1, by1, bw1, bh1, INFO, op="14", sw=1.0)
d.t(bx1 + bw1 / 2, by1 + 24, "ClientHello 수신", 12, INFO, KR, "middle", 600)
d.line(bx1 + 12, by1 + 38, bx1 + bw1 - 12, by1 + 38, RULE, 0.8)

d.chip(bx1 + bw1 / 2, by1 + 68, "GetConfigForClient", INFO, 11)
d.t(bx1 + bw1 / 2, by1 + 94, "연결별 Config 반환", 11, MUTED, KR, "middle")

d.chip(bx1 + bw1 / 2, by1 + 130, "hello.Conn", INFO, 11)
d.t(bx1 + bw1 / 2, by1 + 156, "RemoteAddr() 조회", 11, MUTED, KR, "middle")

d.chip(bx1 + bw1 / 2, by1 + 190, "net.SplitHostPort", OK, 11)
d.t(bx1 + bw1 / 2, by1 + 214, "IPv4·IPv6 주소 분리", 11, MUTED, KR, "middle")

# 화살표 1: GetConfigForClient -> 주소 해석 및 후보 생성
d.arrow([(210, 255), (268, 255)], c=MUTED, m="ar")

# 2. 역방향 DNS 및 후보 목록 구성 상자 (ACC)
cx1, cy1, cw1, ch1 = 268, 140, 210, 230
d.tone(cx1, cy1, cw1, ch1, ACC, op="14", sw=1.1)
d.t(cx1 + cw1 / 2, by1 + 24, "검증 후보군 생성", 12, ACC, KR, "middle", 600)
d.line(cx1 + 12, cy1 + 38, cx1 + cw1 - 12, cy1 + 38, RULE, 0.8)

d.chip(cx1 + cw1 / 2, cy1 + 68, "net.LookupAddr", ACC, 11)
d.t(cx1 + cw1 / 2, cy1 + 94, "PTR 레코드 역방향 조회", 11, MUTED, KR, "middle")

d.chip(cx1 + cw1 / 2, cy1 + 130, "hostnames 슬라이스", ACC, 11)
d.t(cx1 + cw1 / 2, cy1 + 156, "PTR 이름 + 클라이언트 IP", 11, MUTED, KR, "middle")

d.t(cx1 + cw1 / 2, cy1 + 190, '["localhost", "127.0.0.1"]', 10, MUTED, MONO, "middle")
d.t(cx1 + cw1 / 2, cy1 + 212, "후보 목록 클로저 전달", 11, MUTED, KR, "middle")

# 화살표 2: 후보 생성 -> 검증 분기
d.arrow([(478, 255), (536, 255)], c=MUTED, m="ar")

# 3. VerifyPeerCertificate 루프 상자 (WARN)
vx1, vy1, vw1, vh1 = 536, 140, 210, 230
d.tone(vx1, vy1, vw1, vh1, WARN, op="14", sw=1.1)
d.t(vx1 + vw1 / 2, vy1 + 24, "VerifyPeerCertificate", 12, WARN, KR, "middle", 600)
d.line(vx1 + 12, vy1 + 38, vx1 + vw1 - 12, vy1 + 38, RULE, 0.8)

d.chip(vx1 + vw1 / 2, vy1 + 68, "Roots: serverPool", WARN, 11)
d.t(vx1 + vw1 / 2, vy1 + 94, "clientCert.pem 을 읽은 풀", 11, MUTED, KR, "middle")

d.chip(vx1 + vw1 / 2, vy1 + 130, "opts.DNSName 대조", WARN, 11)
d.t(vx1 + vw1 / 2, vy1 + 156, "chain[0].Verify(opts)", 10, MUTED, MONO, "middle")

d.t(vx1 + vw1 / 2, vy1 + 190, "leaf 인증서 SAN 비교", 11, MUTED, KR, "middle")
d.t(vx1 + vw1 / 2, vy1 + 212, "후보군 순차 대조", 11, MUTED, KR, "middle")

# 분기 1: 성공 -> 핸드셰이크 통과 (OK)
d.arrow([(746, 200), (814, 200)], c=OK, m="ok")
d.t(780, 190, "일치", 11, OK, KR, "middle", 600)

ox1, oy1, ow1, oh1 = 814, 155, 120, 90
d.tone(ox1, oy1, ow1, oh1, OK, op="18", sw=1.2)
d.t(ox1 + ow1 / 2, oy1 + 28, "검증 통과", 12, OK, KR, "middle", 600)
d.t(ox1 + ow1 / 2, oy1 + 50, "return nil", 11, OK, MONO, "middle")
d.t(ox1 + ow1 / 2, oy1 + 72, "핸드셰이크 완료", 11, INK, KR, "middle")

# 분기 2: 실패 -> 핸드셰이크 차단 (BAD)
d.arrow([(746, 310), (814, 310)], c=BAD, m="bad")
d.t(780, 300, "불일치", 11, BAD, KR, "middle", 600)

fx1, fy1, fw1, fh1 = 814, 265, 120, 90
d.tone(fx1, fy1, fw1, fh1, BAD, op="18", sw=1.2)
d.t(fx1 + fw1 / 2, fy1 + 28, "검증 실패", 12, BAD, KR, "middle", 600)
d.t(fx1 + fw1 / 2, fy1 + 50, "bad_certificate", 10, BAD, MONO, "middle")
d.t(fx1 + fw1 / 2, fy1 + 72, "소켓 즉시 종료", 11, INK, KR, "middle")

# 범례
d.legend(456, [
    ("소켓 주소 확보", INFO),
    ("후보 목록 구성", ACC),
    ("인증서 SAN 대조", WARN),
    ("상호 인증 성공", OK),
    ("인증 실패 차단", BAD),
])

out_path = os.path.join(os.path.dirname(__file__), "..", "11-02.client-addr-verification.svg")
d.save(out_path)
print("saved:", out_path)
