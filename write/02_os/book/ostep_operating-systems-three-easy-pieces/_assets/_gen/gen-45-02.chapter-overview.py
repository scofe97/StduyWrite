# 45-02.chapter-overview — 키워드를 노드로, 앞 키워드에서 뒤 키워드로 넘어가는 관계를 화살표 라벨로 이은 편 전체 지도
# 행 하나가 본문 `##` 하나다. 왼쪽 칩은 절 번호, 노드는 그 절의 핵심 키워드와 실제 값, 화살표 라벨은 두 키워드 사이의 관계다.
# 노드와 관계는 본문 각 절의 `>` 요약과 핵심 요약에서 가져왔다. 값은 모두 본문 정답 3·4·5·6 의 실측이나 각주의 RFC 인용이다.
# 타입 스펙: type-process — 행마다 같은 의미 슬롯(문제 · 중간 · 대응)이 같은 자리에 반복된다("Stage framework with semantic slots").
#           화살표는 읽는 순서이고 라벨은 관계다. 형제 편 gen-44-02.chapter-overview.py 와 같은 열 간격을 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, OK, INFO, KR, MONO

W, H = 1000, 792
COL_X, STRIDE, NW, NH = 64, 344, 200, 64
ROW_Y, ROW_STRIDE = 104, 92

d = D(W, H, "CHAPTER MAP · 45-02",
      "TLS 는 서명한 키 교환으로 통로를 세우고 믿음은 출발점에서 시작한다",
      "45-02 편의 전체 지도. 첫 행은 연결마다 새 대칭 키를 합의해 순방향 비밀성을 얻는 방식, "
      "둘째 행은 중간자 공격을 서버의 서명(CertificateVerify)이 막는 방식, "
      "셋째 행은 핸드셰이크 세 단계와 클라이언트가 비밀번호로 뒤에 증명하는 이유, "
      "넷째 행은 Heartbleed 로 본 규격 결함과 구현 결함의 구분, "
      "다섯째 행은 쿠키와 도전 응답과 인증 서버의 비교, "
      "여섯째 행은 인증서의 좁은 보증과 HSTS, 일곱째 행은 SSH 첫 접속의 호스트 키 신뢰를 보인다.",
      lead="행은 본문 절, 화살표 라벨은 앞 키워드에서 뒤 키워드로 넘어가는 관계")


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


def node(i, j, title, sub, c=None):
    x, y = nx(j), ny(i)
    if c:
        d.tone(x, y, NW, NH, c, 6, "14", 1.4 if c == ACC else 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW / 2, y + 27, title, 14, c or INK, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 49, sub, 12, MUTED, kr(sub), "middle")


def harrow(i, j, label):
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    d.arrow([(x1 + 2, y), (x2 - 4, y)], MUTED, "ar", 1.4)
    d.t((x1 + x2) / 2, y - 10, label, 12, MUTED, kr(label), "middle", 600)


for i in range(7):
    d.chip(34, ny(i) + NH / 2 - 4, f"§{i + 1}", MUTED, 11, 4)

# §1 연결마다 새 대칭 키
node(0, 0, "연결마다 새 키", "동시 연결도 키가 다름", INFO)
node(0, 1, "키 교환", "Diffie-Hellman", None)
node(0, 2, "순방향 비밀성", "X25519MLKEM768", OK)
harrow(0, 0, "키를 합의")
harrow(0, 1, "장기 키와 분리")

# §2 중간자와 서버의 서명
node(1, 0, "중간자 공격", "양쪽에 자기 값을 보냄", INFO)
node(1, 1, "서버의 서명", "핸드셰이크 기록에 서명", None)
node(1, 2, "CertificateVerify", "개인 키를 가진 증거", ACC)
harrow(1, 0, "상대를 모름")
harrow(1, 1, "공개 키로 검증")

# §3 핸드셰이크 세 단계와 클라이언트 인증
node(2, 0, "클라이언트는 서명 못 함", "인증서도 개인 키도 없음", INFO)
node(2, 1, "세 단계", "키 교환 · 매개변수 · 인증", None)
node(2, 2, "비밀번호는 뒤에", "통로가 선 다음 전송", OK)
harrow(2, 0, "서버만 인증")
harrow(2, 1, "대칭 키가 보호")

# §4 규격 결함과 구현 결함
node(3, 0, "Heartbleed", "OpenSSL 1.0.1~1.0.1f", INFO)
node(3, 1, "구현 결함", "규격 결함이 아님", None)
node(3, 2, "조치 범위 판단", "1.0.1g 는 영향 없음", OK)
harrow(3, 0, "원인 분류")
harrow(3, 1, "버전으로 한정")

# §5 비밀번호와 공개 키 밖의 인증
# 세 방법을 나란히 견주는 절이라 문제·대응 색을 쓰지 않는다
node(4, 0, "쿠키", "Secure · HttpOnly", None)
node(4, 1, "도전 응답", "HMAC · 새 도전값", None)
node(4, 2, "인증 서버", "Kerberos 티켓", None)
harrow(4, 0, "비밀번호를 대신")
harrow(4, 1, "보증을 서버에")

# §6 HTTPS 인증서와 HSTS
node(5, 0, "인증서 확인 통과", "보증은 좁은 사실뿐", INFO)
node(5, 1, "HSTS", "http 주소를 https 로", None)
node(5, 2, "연결 끊음", "보안 전송 오류 전부", OK)
harrow(5, 0, "물러남 차단")
harrow(5, 1, "오류를 만나면")

# §7 SSH 호스트 키
node(6, 0, "첫 접속 호스트 키", "known_hosts 에 없음", INFO)
node(6, 1, "StrictHostKeyChecking", "기본값 ask", None)
node(6, 2, "키 변경 차단", "경고와 함께 막힘", OK)
harrow(6, 0, "확인해야 등록")
harrow(6, 1, "저장 뒤 대조")

d.legend(ny(6) + NH + 24, [("문제", INFO), ("이 편의 한 줄", ACC), ("대응", OK)])
d.save("45-02.chapter-overview.svg")
