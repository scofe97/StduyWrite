# 타입 스펙: type-dp-security-matrix — 행 넷(앱 코드 mTLS · 사이드카 서비스 메시 · 투명 암호화 · 상호 인증 + 투명 암호화) × 열 다섯(신원 단위 · 앱 수정 · 추가 구성 요소 · 암호화하는 곳 · 대상 프로토콜). focal 은 마지막 행의 신원 단위 칸.
# 사실 출처: 추출본 ebpf8.txt 1086~1096행(앱마다 mTLS, 인증서로 신원 확인), 1098~1104행(서비스 메시 또는 네트워크로 내림), 1105~1137행(투명 암호화는 앱이 몰라도 되고 구성 요소가 없으며 노드 신원으로 IPsec·WireGuard 터널),
#   1140~1167행(앱 신원은 TLS 로 확인한 뒤 커널 암호화, SPIFFE/SPIRE), 1142~1146행(서비스 메시는 별도 구성 요소와 자원·지연·복잡도). 현재: Cilium 문서 network/servicemesh/mutual-authentication —
#   Beta, 워크로드 = 라벨 묶음 Cilium identity 의 SPIFFE ID, SPIRE 서버 필요(Helm 옵션), 암호화는 WireGuard·IPsec 을 사용자가 따로 켬, 로드맵의 "Integrate with WireGuard"·"Use auth secret for network encryption" 은 TODO.
#   사이드카 프록시의 L7 mTLS 와 TCP 연결 단위: runners-high 08_cloud cilium-up-and-running 14-01 §2 의 "mTLS 와의 구조적 차이". 앱 코드 mTLS 의 추가 구성 요소 칸은 ebpf8.txt 1091~1095행(인증서를 교환해 신원 확인)·1141~1143행(앱마다 처리하는 것은 큰 부담)에서 "인증서·앱이 직접".
# Layout formulas(type-dp-security-matrix §2): left_pad 12, comp_col_w 196(spec 208), comp_role_gap 12, role_col_w 124(spec 148), role_col_gap 8(spec 16), right_pad 12 → 폭 884 (본문 삽입 폭 880~1000 규칙),
#   header_h 52, row_h 36, row_stride 40, header_y=96(제목 블록 아래), row_y(k)=header_y+header_h+16+40k, legend_y_top=rows_bottom+20. 모든 좌표 4의 배수. 연결선 없음.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

LP, CW, GAP, RW, RG, RP = 12, 196, 12, 124, 8, 12
NCOL = 5
W = LP + CW + GAP + NCOL * RW + (NCOL - 1) * RG + RP
HY, HH, RH, RS = 96, 52, 36, 40
NROW = 4
ROW0 = HY + HH + 16
ROWS_BOTTOM = ROW0 + (NROW - 1) * RS + RH
LEG = ROWS_BOTTOM + 20
H = LEG + 64
d = D(W, H, "LEARNING EBPF · 08-02 §4",
      "신원은 라벨 identity 로 좁혀졌지만 암호화 키는 아직 노드 단위다",
      "앱 코드 mTLS 는 앱이 인증서로 신원을 확인하고 TCP 연결을 암호화한다. 사이드카 서비스 메시는 앱을 고치지 않지만 사이드카 프록시가 필요하다. 투명 암호화는 노드 신원으로 커널 IPsec·WireGuard 터널을 맺어 IP 패킷 전체를 감싼다. 상호 인증은 베타이고 SPIRE 서버가 필요하며 신원은 라벨 identity 이고 암호화는 따로 켠다.",
      "행은 방식, 열은 신원·부담·암호화 위치입니다")

def kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO
def colx(j): return LP + CW + GAP + j * (RW + RG)

COLS = ["신원 단위", "앱 수정", "추가 구성 요소", "암호화하는 곳", "대상 프로토콜"]
d.box(LP, HY, CW, HH, PAPER2, RULE, 0.9, 6)
d.t(LP + CW // 2, HY + 32, "방식", 13, MUTED, KR, "middle", 600)
for j, name in enumerate(COLS):
    d.box(colx(j), HY, RW, HH, PAPER2, RULE, 0.9, 6)
    d.t(colx(j) + RW // 2, HY + 32, name, 13, INK, KR, "middle", 600)

COMP = ["앱 코드 mTLS", "사이드카 서비스 메시", "투명 암호화", "상호 인증 + 투명 암호화"]
# 칸: (값, 부제 또는 None, 색 또는 None, focal)
CELLS = [
    [("앱", None, None, False), ("필요", None, WARN, False), ("인증서", "앱이 직접", WARN, False), ("앱 코드", None, None, False), ("TCP 연결", "보통", None, False)],
    [("앱", None, None, False), ("불필요", None, OK, False), ("사이드카", "프록시", WARN, False), ("사이드카", "프록시", None, False), ("TCP 연결", "보통", None, False)],
    [("노드", None, None, False), ("불필요", None, OK, False), ("없음", None, OK, False), ("커널", "IPsec·WireGuard", None, False), ("IP 패킷", None, None, False)],
    [("라벨 identity", "SPIFFE ID · 베타", ACC, True), ("불필요", None, OK, False), ("SPIRE 서버", None, WARN, False), ("커널 · 별도 설정", "IPsec·WireGuard", None, False), ("IP 패킷", None, None, False)],
]
for r, name in enumerate(COMP):
    y = ROW0 + r * RS
    d.box(LP, y, CW, RH, PAPER2, RULE, 0.9, 4)
    d.t(LP + 12, y + 23, name, 13, INK, KR, "start", 600)
    for j, (val, sub, c, focal) in enumerate(CELLS[r]):
        x = colx(j)
        if focal:
            d.o.append(f'<rect x="{x}" y="{y}" width="{RW}" height="{RH}" rx="4" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
        elif c:
            d.tone(x, y, RW, RH, c, 4, "12", 1.0)
        else:
            d.box(x, y, RW, RH, PAPER, RULE, 0.8, 4)
        tc = ACC if focal else (c or INK)
        if sub:
            d.t(x + RW // 2, y + 16, val, 13 if kr(val) == KR else 12, tc, kr(val), "middle", 600)
            d.t(x + RW // 2, y + 30, sub, 12 if kr(sub) == KR else 11, MUTED, kr(sub))
        else:
            d.t(x + RW // 2, y + 23, val, 13 if kr(val) == KR else 12, tc, kr(val), "middle", 600)

d.line(LP, LEG, W - 12, LEG, RULE, 0.8)
d.t(LP, LEG + 22, "LEGEND", 8, SOFT, MONO, "start")
x = 100
for lab, c in (("부담 없음", OK), ("부담 있음", WARN), ("현재 상태의 핵심", ACC)):
    d.o.append(f'<rect x="{x}" y="{LEG + 12}" width="14" height="12" rx="2" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
    d.t(x + 22, LEG + 22, lab, 11, MUTED, KR, "start")
    x += 44 + len(lab) * 13
d.save("08-02.encryption-matrix.svg")
