# 04-02 §3 「인증서는 어떻게 만들어지는가」 — 파일 넷과 CSR 이 누구 손에서 생겨 어디로 건너가는지.
# 본문 요구: 표가 "누가 갖는가"를 파일별로 적고, 세 걸음이 "개인키는 서버를 떠나지 않고 CSR 만 CA 로 갑니다.
#            CA 는 개인키를 본 적이 없으면서도 그 공개키에 서명할 수 있고" 라고 적는다. `ca.crt` 는
#            "클라이언트가 미리 갖고 있음" 이다. 표와 명령만으로는 어느 파일이 경계를 넘고 어느 파일이
#            안 넘는지가 한눈에 안 선다 — 주체별 칸에 파일을 놓고, 칸을 넘는 화살표만 그린다.
# 타입 스펙: type-swimlane — 주체(CA·서버·클라이언트)를 가로지르며 넘겨받는 절차. 가로 레인 셋,
#           열은 걸음 순서(stride 200), 레인 높이 136 에 슬롯 둘(48 높이). 레인 경계를 넘는 화살표가 논지이고
#           focal 은 CA 개인키로 서명이 찍히는 단 한 자리다. 개인키 두 칸에서는 나가는 화살표가 없다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

W, H = 960, 616
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-02 §3",
      "인증서 발급 세 걸음 — 어느 파일이 누구 손에 놓이는가",
      "CA 가 자기 키 쌍과 자기 서명 인증서를 만들고, 서버가 자기 키 쌍과 CSR 을 만든다. CSR 만 CA 로 건너가 "
      "CA 개인키로 서명을 받아 서버 인증서가 되어 돌아온다. 클라이언트는 CA 인증서를 미리 갖고 있다가 "
      "핸드셰이크에서 받은 서버 인증서의 CA 서명을 검증한다. 개인키 둘은 어느 경계도 넘지 않는다.",
      "make-certs.sh 기준입니다. 개인키 두 칸에서는 나가는 화살표가 없습니다")

CX = [224, 424, 624, 824]            # 열 stride 200
BW, BH = 176, 48
LANE_TOP = [128, 264, 400]           # 레인 stride 136
LANE_H = 136

def slot(lane, k):                   # k=0 위 칸, k=1 아래 칸 → 상자의 top
    return LANE_TOP[lane] + 16 + k * 56
def cy(lane, k): return slot(lane, k) + BH / 2

# ── 열 머리와 레인 ────────────────────────────────────────────
for x, lab in zip(CX, ("1 · CA 생성", "2 · 키 쌍과 CSR", "3 · CA 서명", "4 · 핸드셰이크")):
    d.t(x, 112, lab, 13, SOFT, KR, "middle", 600)
for y in LANE_TOP + [LANE_TOP[-1] + LANE_H]:
    d.line(24, y, W - 48, y, RULE, 0.8)
for i, (nm, sub) in enumerate((("CA", "발급자"), ("서버", "a.test"), ("클라이언트", "s_client"))):
    d.t(24, LANE_TOP[i] + 32, nm, 13, INK, _kr(nm), "start", 600)
    d.t(24, LANE_TOP[i] + 52, sub, 13 if _kr(sub) is KR else 12, MUTED, _kr(sub), "start")

# ── 연결선 먼저(z-order) ──────────────────────────────────────
# ca.key → 서명 자리
d.arrow([(CX[0] + BW / 2, cy(0, 0)), (CX[2] - BW / 2 - 8, cy(0, 0))], MUTED, "ar", 1.4)
d.t(CX[1], cy(0, 0) - 8, "서명에 쓰는 키", 13, MUTED, KR)
# a.test.csr → 서명 자리 (레인 경계를 넘는 유일한 서버발 화살표)
d.arrow([(CX[1] + BW / 2, cy(1, 0)), (CX[2] - 16, cy(1, 0)), (CX[2] - 16, slot(0, 0) + BH + 8)], MUTED, "ar", 1.4)
d.t((CX[1] + BW / 2 + CX[2] - 16) / 2, cy(1, 0) - 8, "서명 요청", 13, MUTED, KR)
# 서명 자리 → a.test.crt (서버 레인으로 돌아옴)
d.arrow([(CX[2] + BW / 2, cy(0, 0)), (CX[3], cy(0, 0)), (CX[3], slot(1, 0) - 8)], INFO, "info", 1.4)
d.t((CX[2] + BW / 2 + CX[3]) / 2, cy(0, 0) - 8, "서명된 인증서", 13, INFO, KR)
# a.test.crt → 클라이언트 (핸드셰이크마다)
d.arrow([(CX[3], slot(1, 0) + BH), (CX[3], slot(2, 0) - 8)], INFO, "info", 1.4)
d.t(CX[3] - 12, cy(1, 1) + 4, "Certificate 메시지", 13, INFO, KR, "end")
# ca.crt → 클라이언트 (미리)
d.arrow([(CX[0], slot(0, 1) + BH), (CX[0], slot(2, 0) - 8)], INFO, "info", 1.4)
d.t(CX[0] + 12, cy(1, 0) + 4, "미리 설치", 13, INFO, KR, "start")
# 클라이언트 안에서 — ca.crt 로 받은 인증서의 CA 서명 검증
d.arrow([(CX[0] + BW / 2, cy(2, 0)), (CX[3] - BW / 2 - 8, cy(2, 0))], OK, "ok", 1.4)
d.t((CX[1] + CX[2]) / 2, cy(2, 0) - 8, "CA 서명 검증", 13, OK, KR, "middle", 600)

# ── 파일 칸 ───────────────────────────────────────────────────
def cell(col, lane, k, title, sub, c=None, focal=False):
    x, top = CX[col] - BW / 2, slot(lane, k)
    if focal:
        d.o.append(f'<rect x="{x}" y="{top}" width="{BW}" height="{BH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif c:
        d.tone(x, top, BW, BH, c, 8)
    else:
        d.box(x, top, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(CX[col], top + 20, title, 13, (ACC if focal else (c or INK)), _kr(title), "middle", 600)
    d.t(CX[col], top + 38, sub, 13 if _kr(sub) is KR else 12, MUTED, _kr(sub))

cell(0, 0, 0, "ca.key", "CA 개인키", WARN)
cell(0, 0, 1, "ca.crt", "CA 공개키 · 자기 서명", INFO)
cell(2, 0, 0, "CA 개인키로 서명", "x509 -req -CAkey", focal=True)

cell(1, 1, 0, "a.test.csr", "공개키 + 이름")
cell(1, 1, 1, "a.test.key", "서버 개인키", WARN)
cell(3, 1, 0, "a.test.crt", "이름 + 공개키 + CA 서명", INFO)

cell(0, 2, 0, "ca.crt", "신뢰 앵커", INFO)
cell(3, 2, 0, "a.test.crt", "받은 사본", INFO)

d.legend(H - 40, [("개인키 · 경계를 넘지 않음", WARN), ("인증서 · 공개 문서", INFO),
                  ("검증", OK), ("CA 서명이 찍히는 자리", ACC)])
d.save("04-02.cert-issuance.svg")
