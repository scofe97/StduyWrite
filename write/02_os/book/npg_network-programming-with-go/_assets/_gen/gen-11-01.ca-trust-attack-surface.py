# 타입 스펙: type-architecture
# 사실 출처: NPG Ch.11 In Certificate Authorities We Trust, How to Compromise TLS
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 520
d = D(W, H, "ARCHITECTURE · CA TRUST & ATTACK SURFACES",
      "CA 신뢰 체계와 TLS 를 무너뜨리는 세 가지 공격 지점",
      "인증서 신뢰 사슬 구조와 이를 위협하는 세 지점(CA 오발급, 루트 저장소 침해, 서버 메모리 탈취)입니다.",
      lead="신뢰의 고리 중 하나라도 깨지면 TLS 의 기밀성과 무결성 보장이 무너집니다.")

def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO

y_chain = 140
NW, NH = 200, 72

nodes_norm = [
    (24, y_chain, "OS 신뢰 저장소", "루트 CA 인증서 보관", INFO),
    (264, y_chain, "인증 기관 (CA)", "도메인 심사 및 암호 서명", OK),
    (504, y_chain, "서버 인증서", "호스트명 · 공개키 바인딩", OK),
    (744, y_chain, "클라이언트 검증", "서명 체인 대조 및 확인", OK),
]

for x, y, title, sub, c in nodes_norm:
    d.tone(x, y, NW, NH, c, 6, "16", 1.1)
    d.t(x + NW / 2, y + 30, title, 13, c, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 52, sub, 11, MUTED, kr(sub), "middle")

# 수평 화살표 (정상 신뢰 사슬)
for i in range(3):
    x1 = nodes_norm[i][0] + NW
    x2 = nodes_norm[i + 1][0]
    y_mid = y_chain + NH / 2
    d.arrow([(x1 + 2, y_mid), (x2 - 4, y_mid)], c=MUTED, m="ar")

# 세 공격 지점 (아래 행에 수직으로 정렬)
y_atk = 320
AW, AH = 220, 96

# 공격 2: 신뢰 저장소 변조 (Node 0 아래)
x_atk2 = 14
d.tone(x_atk2, y_atk, AW, AH, BAD, 6, "18", 1.2)
d.t(x_atk2 + AW / 2, y_atk + 26, "공격 2: 저장소 변조", 12, BAD, KR, "middle", 600)
d.t(x_atk2 + AW / 2, y_atk + 48, "공격자 루트 CA 인증서 주입", 11, INK, KR, "middle")
d.t(x_atk2 + AW / 2, y_atk + 70, "공격자가 서명한 인증서 모두 신뢰",  11, MUTED, KR, "middle")
cx2 = nodes_norm[0][0] + NW / 2
d.arrow([(cx2, y_atk), (cx2, y_chain + NH + 6)], c=BAD, m="bad")
d.t(cx2 + 10, y_atk - 26, "루트 주입",  11, BAD, KR, "start")

# 공격 1: CA 오발급 (Node 1 아래)
x_atk1 = 254
d.tone(x_atk1, y_atk, AW, AH, BAD, 6, "18", 1.2)
d.t(x_atk1 + AW / 2, y_atk + 26, "공격 1: CA 오발급", 12, BAD, KR, "middle", 600)
d.t(x_atk1 + AW / 2, y_atk + 48, "중간 CA 잘못 발급 (TURKTRUST)", 11, INK, KR, "middle")
d.t(x_atk1 + AW / 2, y_atk + 70, "그 중간 CA 로 사칭 인증서 발급",  11, MUTED, KR, "middle")
cx1 = nodes_norm[1][0] + NW / 2
d.arrow([(cx1, y_atk), (cx1, y_chain + NH + 6)], c=BAD, m="bad")
d.t(cx1 + 10, y_atk - 26, "권한 남용",  11, BAD, KR, "start")

# 공격 3: 서버 침해 (Node 2 아래)
x_atk3 = 494
d.tone(x_atk3, y_atk, AW, AH, BAD, 6, "18", 1.2)
d.t(x_atk3 + AW / 2, y_atk + 26, "공격 3: 서버 침해", 12, BAD, KR, "middle", 600)
d.t(x_atk3 + AW / 2, y_atk + 48, "서버 침해 후 메모리 직접 덤프", 11, INK, KR, "middle")
d.t(x_atk3 + AW / 2, y_atk + 70, "활성 세션 키 탈취로 복호화",  11, MUTED, KR, "middle")
cx3 = nodes_norm[2][0] + NW / 2
d.arrow([(cx3, y_atk), (cx3, y_chain + NH + 6)], c=BAD, m="bad")
d.t(cx3 + 10, y_atk - 26, "메모리 탈취",  11, BAD, KR, "start")

d.legend(460, [("신뢰 앵커", INFO), ("정상 신뢰 사슬", OK), ("침해 공격 지점", BAD)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "11-01.ca-trust-attack-surface.svg"
d.save(str(svg_path))
print("ok 11-01 ca-trust-attack-surface")
