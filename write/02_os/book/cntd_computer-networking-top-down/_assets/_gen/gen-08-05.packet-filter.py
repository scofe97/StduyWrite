# 타입 스펙: type-dp-security-matrix — 정책 한 줄이 규칙 한 줄로 어떻게 옮겨지는가를 격자로.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.9.1 Table 8.5 (책 616쪽) —
#   다섯 정책과 그 설정, 조직망 130.207/16 과 웹 서버 130.207.244.203 은 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, WARN, BAD, KR, MONO

W, H = 1000, 700
d = D(W, H, "SECTION 8.9.1 · POLICY TO RULE",
      "정책 한 줄이 규칙 한 줄이 됩니다",
      "판단 재료가 헤더 필드로 한정되므로, 정책도 주소와 포트와 플래그로 표현할 수 있는 것만 옮겨진다.",
      "다섯 정책과 설정은 원문 Table 8.5 의 것입니다 (조직망 130.207/16)")

ROWS = [("바깥 웹 접근 차단", "어느 IP 든 포트 80 으로 나가는 패킷을 버립니다"),
        ("공개 웹 서버 외 인바운드 TCP 차단", "130.207.244.203:80 을 뺀 들어오는 TCP SYN 을 버립니다"),
        ("웹 라디오의 대역폭 점유 차단", "DNS 를 뺀 들어오는 UDP 를 버립니다"),
        ("스머프 DoS 이용 차단", "브로드캐스트 주소로 가는 ICMP 핑을 버립니다"),
        ("트레이스라우트 차단", "나가는 ICMP TTL 만료 트래픽을 버립니다")]
LX, LW = 24, 352
RX, RW = 400, 576
Y0, RH, STRIDE = 172, 56, 64
d.t(LX, 150, "정책", 11, SOFT, KR, "start", 600)
d.t(RX, 150, "방화벽 설정", 11, SOFT, KR, "start", 600)
for i, (pol, rule) in enumerate(ROWS):
    y = Y0 + i * STRIDE
    d.tone(LX, y, LW, RH, INFO, 6, "14", 1.2)
    d.t(LX + LW / 2, y + 34, pol, 11, INFO, KR)
    d.tone(RX, y, RW, RH, BAD, 6, "12", 1.1)
    d.t(RX + 20, y + 34, rule, 11, BAD, KR, "start")

PY = Y0 + 5 * STRIDE + 8
d.tone(24, PY, 952, 96, ACC, 8, "16", 1.4)
d.t(44, PY + 28, "ACK 비트 하나가 방향을 가릅니다", 12, ACC, KR, "start", 600)
d.line(44, PY + 40, 956, PY + 40, RULE, 0.8)
d.t(44, PY + 64, "TCP 연결의 첫 세그먼트만 ACK 가 0 이고 나머지는 전부 1 입니다.", 11, MUTED, KR, "start")
d.t(44, PY + 84, "그래서 들어오는 ACK=0 을 거르면 밖에서 시작하는 연결만 정확히 죽고 안에서 시작한 것은 삽니다.",
    11, MUTED, KR, "start")

d.t(24, PY + 132, "다만 외부 주소에 기댄 정책은 출발지를 위조한 데이터그램에 아무 보호도 주지 못합니다.", 11, SOFT, KR, "start")
d.legend(PY + 148, [("정책", INFO), ("규칙", BAD), ("방향을 가르는 재료", ACC)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-05.packet-filter.svg"
d.save(out); print("→", out.name)
