# 09-01.chapter-overview — 키워드를 노드로, 앞 키워드에서 뒤 키워드로 넘어가는 관계를 화살표 라벨로 이은 편 전체 지도
# 행 하나가 본문 `##` 하나다. 왼쪽 칩은 절 번호, 노드는 그 절의 핵심 키워드와 실제 값, 화살표 라벨은 두 키워드 사이의 관계다.
# 노드 근거: §1 은 「argocd-server 인증서 선택 순서」(Secret 이 없으면 자체 서명 인증서, 브라우저 경고)·
#            「서버 --insecure 와 앞단 TLS」(Ingress 가 TLS 를 끝내는 구조에서만),
#            §2 는 절 도입(x509: certificate signed by unknown authority)과 「인증서 등록 방법」(argocd cert add-tls, 키는 호스트 이름),
#            §3 은 절 도입(authentication required)과 「저장소 Secret 의 구조」(사용자 이름·토큰, controller 와 server 가 읽어 repo-server 에 넘김)다.
#            값은 모두 본문에 있는 것이다. focal 은 핵심 요약 첫 문장(구간마다 믿는 쪽의 설정이 다르다)에 맞춰 §2 가운데 노드에 둔다.
# 타입 스펙: type-process — 행마다 같은 의미 슬롯(문제 · 중간 · 대응)이 같은 자리에 반복된다("Stage framework with semantic slots").
#           화살표는 읽는 순서이고 라벨은 관계다. 색은 문제 INFO, 대응 OK, 이 편의 한 줄 ACC 다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, OK, INFO, KR, MONO

W, H = 1000, 424
COL_X, STRIDE, NW, NH = 64, 344, 200, 64
ROW_Y, ROW_STRIDE = 104, 92

d = D(W, H, "CHAPTER MAP · 09-01",
      "TLS 연결은 둘이고 인증서를 내는 쪽과 믿는 쪽이 구간마다 다르다",
      "09-01 편의 전체 지도. 첫 행은 브라우저와 CLI 가 argocd-server 로 가는 구간에서 자체 서명 인증서가 argocd-server-tls Secret 으로 바뀌고 "
      "앞단이 TLS 를 끝내면 서버 insecure 를 쓰는 흐름, "
      "둘째 행은 사설 CA 를 모르는 x509 오류가 argocd-tls-certs-cm 등록으로 풀려 접속되는 흐름, "
      "셋째 행은 보호된 저장소의 인증 필요 오류가 저장소 Secret 의 사용자 이름과 토큰으로 풀려 repo-server 가 접속하는 흐름을 보인다.",
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


for i in range(3):
    d.chip(34, ny(i) + NH / 2 - 4, f"§{i + 1}", MUTED, 11, 4)

# §1 서버 TLS 인증서와 --insecure
node(0, 0, "자체 서명 인증서", "브라우저 경고", INFO)
node(0, 1, "argocd-server-tls", "tls.crt · tls.key", None)
node(0, 2, "앞단 TLS 종료", "서버 --insecure", OK)
harrow(0, 0, "Secret 교체")
harrow(0, 1, "앞단이 끝내면")

# §2 사설 CA 저장소 인증서 등록
node(1, 0, "unknown authority", "x509 오류", INFO)
node(1, 1, "argocd-tls-certs-cm", "호스트 이름이 키", ACC)
node(1, 2, "CA 등록 뒤 접속", "argocd cert add-tls", OK)
harrow(1, 0, "CA 를 등록")
harrow(1, 1, "호스트별 신뢰")

# §3 보호된 저장소의 HTTPS 자격 증명
node(2, 0, "저장소 인증 필요", "authentication required", INFO)
node(2, 1, "저장소 Secret", "사용자 이름 · 토큰", None)
node(2, 2, "repo-server 접속", "controller·server 가 전달", OK)
harrow(2, 0, "argocd repo add")
harrow(2, 1, "자격 증명 전달")

d.legend(ny(2) + NH + 24, [("문제", INFO), ("이 편의 한 줄", ACC), ("대응", OK)])
d.save("09-01.chapter-overview.svg")
