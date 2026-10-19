# 타입 스펙: type-architecture
# 사실 출처: NPG Ch.11 Securing Communications with TLS, RFC 8446, crypto/tls
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 116
W, H = 984, 750

def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO

def nx(j):
    return COL_X + j * STRIDE

def ny(i):
    return ROW_Y + i * ROW_STRIDE

d = D(W, H, "ARCHITECTURE · 11-01 OVERVIEW",
      "TLS 핸드셰이크와 CA 신뢰 사슬 및 Go 클라이언트·서버·피닝",
      "11-01 의 키워드 개념도입니다. §1 줄은 핸드셰이크와 공유 비밀 및 세션 키 전방 비밀성입니다. "
      "§2 줄은 루트 CA 신뢰 저장소와 인증서 서명 및 세 가지 침해 경로입니다. "
      "§3 줄은 기본 클라이언트의 검증 실패, 시험 인증서를 믿는 ts.Client() 의 성공, 옆길인 InsecureSkipVerify, TCP 위에 바로 TLS 를 여는 tls.Dialer 입니다. "
      "§4 줄은 tls.NewListener 래핑과 첫 I/O 지연 핸드셰이크입니다. "
      "§5 줄은 RootCAs 명시 지정과 믿을 인증서를 그 서버 하나로 좁히는 피닝입니다.",
      lead="화살표 위 글자는 두 단계의 관계, 왼쪽 칩은 그 줄을 다루는 절입니다.")

def node(i, j, title, sub, c=None):
    x, y = nx(j), ny(i)
    if c:
        d.tone(x, y, NW, NH, c, 6, "14", 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW / 2, y + 27, title, 14, c or INK, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 48, sub, 11, MUTED, kr(sub), "middle")

def harrow(i, j, label, c=SOFT, m="soft"):
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    d.arrow([(x1 + 2, y), (x2 - 4, y)], c, m, 1.3)
    d.t((x1 + x2) / 2, y - 9, label, 11, c if c != SOFT else MUTED, kr(label), "middle", 600)

for i, sec in enumerate(("§1", "§2", "§3", "§4", "§5")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

# §1 TLS 1.3 핸드셰이크와 세션 키
node(0, 0, "Client·Server Hello", "버전 · 스위트 · key_share", INFO)
node(0, 1, "ECDHE 공유 비밀", "임시 키쌍 교환", OK)
node(0, 2, "전방 비밀성 세션 키", "세션 종료 즉시 폐기", ACC)
harrow(0, 0, "키 교환 매개변수")
harrow(0, 1, "HKDF 로 파생", ACC, "acc")

# §2 CA 신뢰 체계와 침해 경로
node(1, 0, "루트 CA 신뢰 저장소", "OS 내장 신뢰 앵커", INFO)
node(1, 1, "X.509 서버 인증서", "발급 기관 암호 서명", OK)
node(1, 2, "세 가지 침해 경로", "CA오발급·루트변조·탈취", ACC)
harrow(1, 0, "신뢰 체인 서명")
harrow(1, 1, "취약 지점 분석", ACC, "acc")

# §3 클라이언트 인증서 검증
node(2, 0, "기본 클라이언트", "알 수 없는 CA 오류", INFO)
node(2, 1, "ts.Client()", "시험 인증서 신뢰 · 성공", OK)
node(2, 2, "tls.Dialer 연결 상태", "ConnectionState 점검", OK)
harrow(2, 0, "인증서를 믿게 함", OK, "ok")
harrow(2, 1, "TCP 위 바로 TLS")
# 옆길: InsecureSkipVerify 는 성공 경로가 아니라 검증을 끄는 우회
cx0, yb = nx(0) + NW / 2, ny(2) + NH
side = "옆길 InsecureSkipVerify · 검증 생략, 중간자 위험"
# 한글 11px, 그 밖의 글자 6.4px 로 폭을 어림해 상자를 글자에 맞춘다
side_w = sum(11 if "가" <= ch <= "힣" else 6.4 for ch in side) + 20
d.path(f"M {cx0} {yb + 2} L {cx0} {yb + 24} L {nx(1) - 4} {yb + 24}", WARN, 1.2, m="warn", dash="4 4")
d.box(nx(1), yb + 14, side_w, 20, fill="#0D1117", stroke=WARN, sw=0.8, r=4)
d.t(nx(1) + 10, yb + 28, side, 11, WARN, KR, "start")

# §4 서버 리스너와 지연 핸드셰이크
node(3, 0, "net.Listen 바인딩", "TCP 스트림 리스너", INFO)
node(3, 1, "tls.NewListener 래핑", "인증서 · 키쌍 탑재", OK)
node(3, 2, "첫 Read/Write 지연", "소켓 I/O 시점 협상", OK)
harrow(3, 0, "리스너 장착")
harrow(3, 1, "핸드셰이크 지연", OK, "ok")

# §5 인증서 피닝
node(4, 0, "x509.NewCertPool", "서버 인증서 PEM 적재", INFO)
node(4, 1, "RootCAs 명시 지정", "OS 신뢰 저장소 우회", OK)
node(4, 2, "단일 서버 신뢰 격리", "다른 서명 인증서 거부", ACC)
harrow(4, 0, "신뢰 풀 구성")
harrow(4, 1, "신뢰 범위 한정", ACC, "acc")

d.legend(690, [("설정 및 입력", INFO), ("보안 통신", OK), ("핵심 검증 경계", ACC), ("위험한 옆길", WARN)])
svg_path = pathlib.Path(__file__).resolve().parent.parent / "11-01.chapter-overview.svg"
d.save(str(svg_path))
print("ok 11-01 chapter-overview")
