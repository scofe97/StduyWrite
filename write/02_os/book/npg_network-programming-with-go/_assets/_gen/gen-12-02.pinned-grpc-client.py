# 타입 스펙: type-process
# 사실 출처: 12-02 §4 클라이언트 코드, go doc google.golang.org/grpc.NewClient(v1.84.0), 12-02 실행 결과(TLSv1.3·ALPN h2, 출력 표)
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W, H = 940, 500
d = D(W, H, "PROCESS · PINNED GRPC CLIENT FLOW",
      "인증서 피닝 클라이언트와 첫 RPC 때 열리는 연결",
      "클라이언트가 서버 자신의 인증서 cert.pem 을 읽어 그것 하나만 담은 풀을 RootCAs 로 넘기고, "
      "grpc.NewClient 로 연결 객체만 만든 뒤 첫 RPC 에서 TCP·TLS 1.3·HTTP/2 를 열어 할 일 표를 찍는 순서입니다.",
      lead="피닝은 CA 가 아니라 서버 자신의 cert.pem 을 믿는 일이고, 연결은 첫 RPC 때 열립니다.")

CW, CH = 260, 110
XS = [50, 340, 630]
Y1, Y2 = 120, 280

def card(x, y, step, title, sub1, sub2, c=INFO):
    d.tone(x, y, CW, CH, c, 8, "12", 1.1)
    d.chip(x + 36, y + 20, step, c, 10, 4)
    d.t(x + CW / 2 + 15, y + 24, title, 13, INK, KR, "middle", 600)
    d.line(x + 15, y + 42, x + CW - 15, y + 42, RULE, 0.8)
    d.t(x + 20, y + 66, sub1, 11, c, MONO, "start", 500)
    d.t(x + 20, y + 90, sub2, 11, MUTED, KR, "start")

# 1행: 믿을 인증서 고르기
card(XS[0], Y1, "STEP 1", "서버 인증서 읽기", "os.ReadFile(\"cert.pem\")", "서버 자신의 인증서 PEM", INFO)
card(XS[1], Y1, "STEP 2", "인증서 하나만 담은 풀", "AppendCertsFromPEM(caCert)", "운영체제 CA 는 넣지 않음", INFO)
card(XS[2], Y1, "STEP 3", "TLS 자격 증명", "RootCAs: certPool", "credentials.NewTLS 로 감쌈", OK)

d.arrow([(XS[0] + CW + 4, Y1 + CH / 2), (XS[1] - 6, Y1 + CH / 2)], SOFT, "soft", 1.4)
d.arrow([(XS[1] + CW + 4, Y1 + CH / 2), (XS[2] - 6, Y1 + CH / 2)], SOFT, "soft", 1.4)

d.arrow([(XS[2] + CW / 2, Y1 + CH + 4),
         (XS[2] + CW / 2, Y1 + CH + 24),
         (XS[0] + CW / 2, Y1 + CH + 24),
         (XS[0] + CW / 2, Y2 - 6)], OK, "ok", 1.4)

# 2행: 연결과 호출
card(XS[0], Y2, "STEP 4", "연결 객체 만들기", "grpc.NewClient(addr, …)", "I/O 없음 · 자격 증명은 필수", OK)
card(XS[1], Y2, "STEP 5", "첫 RPC 에서 연결", "rosie.Add(ctx, chores)", "TCP · TLS 1.3 · HTTP/2 순서", ACC)
card(XS[2], Y2, "STEP 6", "할 일 표 찍기", "2  [X]  Wash dishes", "List 응답을 탭으로 나눠 찍음", ACC)

d.arrow([(XS[0] + CW + 4, Y2 + CH / 2), (XS[1] - 6, Y2 + CH / 2)], ACC, "acc", 1.4)
d.arrow([(XS[1] + CW + 4, Y2 + CH / 2), (XS[2] - 6, Y2 + CH / 2)], ACC, "acc", 1.4)

d.legend(H - 48, [("믿을 인증서", INFO), ("자격 증명과 연결 객체", OK), ("RPC 와 출력", ACC)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "12-02.pinned-grpc-client.svg"
d.save(str(svg_path))
print(f"ok {svg_path.name}")
