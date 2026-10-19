# 타입 스펙: type-process
# 사실 출처: NPG Ch.11 Listing 11-6~11-8, crypto/tls
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 440
d = D(W, H, "PROCESS · TLS SERVER LISTENER & HANDSHAKE",
      "tls.NewListener 래핑과 지연 핸드셰이크 처리 단계",
      "일반 TCP 소켓을 TLS 리스너로 감싸고 첫 Read/Write 에서 지연 핸드셰이크를 거쳐 에코를 처리합니다.",
      lead="Go 의 tls.Conn 은 Accept 가 아닌 첫 I/O 호출에서 실제 TLS 핸드셰이크를 협상합니다.")

def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO

y0 = 170
BW, BH = 160, 88
GAP = 25
X0 = 30

steps = [
    ("net.Listen 바인딩", "localhost:34443 소켓", INFO),
    ("tls.NewListener", "cert.pem 키쌍 탑재", INFO),
    ("Accept() 호출", "TCP 스트림 연결 수락", INFO),
    ("첫 Read / Write", "지연 핸드셰이크 자동 실행", ACC),
    ("에코 및 유휴 감시", "SetDeadline 타임아웃", OK),
]

for i, (title, sub, c) in enumerate(steps):
    x = X0 + i * (BW + GAP)
    if c == ACC:
        d.tone(x, y0, BW, BH, c, 6, "18", 1.2)
    else:
        d.tone(x, y0, BW, BH, c, 6, "14", 1.0)
    d.t(x + BW / 2, y0 + 34, title, 13, c if c != INFO else INK, kr(title), "middle", 600)
    d.t(x + BW / 2, y0 + 58, sub, 11, MUTED, kr(sub), "middle")
    
    # 단계 번호 칩
    d.chip(x + BW / 2, y0 - 14, f"단계 {i+1}", c,  11, 3)

# 단계 간 수평 화살표
arrow_labels = ["리스너 래핑", "연결 대기", "지연 협상", "세션 확립"]
for i in range(4):
    x1 = X0 + i * (BW + GAP) + BW
    x2 = x1 + GAP
    ym = y0 + BH / 2
    d.arrow([(x1 + 2, ym), (x2 - 4, ym)], c=MUTED, m="ar")

# 지연 핸드셰이크 강조 주석 상자 (Stage 4 아래)
x_focal = X0 + 3 * (BW + GAP) - 40
d.box(x_focal, y0 + BH + 24, BW + 80, 48, fill="#161B22", stroke=ACC, sw=1.0)
d.t(x_focal + (BW + 80) / 2, y0 + BH + 44, "지연 핸드셰이크 (Lazy)", 11, ACC, KR, "middle", 600)
d.t(x_focal + (BW + 80) / 2, y0 + BH + 60, "Accept 시점이 아닌 첫 I/O 에서 협상",  11, MUTED, KR, "middle")

# 화살표: Stage 4 -> 강조 상자
d.arrow([(x_focal + (BW + 80) / 2, y0 + BH), (x_focal + (BW + 80) / 2, y0 + BH + 20)], c=ACC, m="acc")

d.legend(390, [("네트워크 및 리스너 준비", INFO), ("핵심 지연 핸드셰이크", ACC), ("정상 서비스 및 감시", OK)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "11-01.server-listener-handshake.svg"
d.save(str(svg_path))
print("ok 11-01 server-listener-handshake")
