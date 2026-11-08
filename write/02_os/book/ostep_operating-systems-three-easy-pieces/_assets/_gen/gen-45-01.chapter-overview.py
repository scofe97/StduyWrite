# 45-01 개념도 — 이 편의 네 절이 각각 어떤 문제에서 출발해 어떤 도구로 가는지.
# 한 행이 한 절이다. 노드는 키워드, 가로 화살표 라벨은 노드 사이의 관계다.
# 본문 근거: 이 노트 「1. 원격 기계의 인증」·「2. CA 서명으로 공개 키를 이름에 묶는 인증서」·「3. 솔트 붙은 느린 해시로 지키는 비밀번호」·「4. 메시지 하나에서 멈추는 인증」.
# 공식 근거: RFC 5280 §4.1.1.3·§6, NIST SP 800-63B-4 §3.1.1.2, OWASP Password Storage Cheat Sheet.
# 타입 스펙: type-process — 절마다 한 행, 행마다 노드 셋과 라벨 있는 가로 화살표 둘.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, ACC, OK, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 116
W, H = 984, 596


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "OSTEP · 45-01 OVERVIEW",
      "인증은 키·인증서·해시로 쌓고 메시지 하나에서 멈춘다",
      "한 행이 한 절이다. 첫 행은 정책을 강제할 수 없는 원격 기계를 비밀번호나 공개 키로 인증하는 흐름이다. "
      "둘째 행은 공개 키의 주인을 CA 서명으로 묶고 신뢰를 미리 설치된 CA 키에서 출발시키는 흐름이다. "
      "셋째 행은 저장소가 새도 비밀번호가 드러나지 않게 솔트와 느린 해시를 쓰는 흐름이다. "
      "넷째 행은 인증이 메시지 하나만 보증하므로 재전송을 막을 묶는 장치가 더 필요하다는 흐름이다.",
      lead="가로 화살표의 라벨이 노드 사이의 관계이고, 왼쪽 칩이 절 번호이다.")


def node(i, j, title, sub, c):
    x, y = nx(j), ny(i)
    d.tone(x, y, NW, NH, c, 6, "14", 1.1)
    d.t(x + NW / 2, y + 28, title, 14, INK, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 48, sub, 13, MUTED, kr(sub), "middle")


def harrow(i, j, label, c=SOFT, m="soft"):
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    d.arrow([(x1 + 2, y), (x2 - 4, y)], c, m, 1.3)
    d.t((x1 + x2) / 2, y - 8, label, 13, c if c != SOFT else MUTED, kr(label), "middle", 600)


for i, sec in enumerate(("1", "2", "3", "4")):
    d.chip(32, ny(i) + NH / 2 - 4, sec, MUTED, 12, 6)

# 1. 원격 기계의 인증
node(0, 0, "원격 기계", "정책을 강제할 수 없는 상대", INFO)
node(0, 1, "인증", "무엇을 아는가로 확인", OK)
node(0, 2, "비밀번호 · 공개 키", "쓰는 방향이 서로 다름", ACC)
harrow(0, 0, "비트만 보임")
harrow(0, 1, "방향으로 갈림", ACC, "acc")

# 2. 인증서
node(1, 0, "공개 키의 주인", "키는 비밀이 아님", INFO)
node(1, 1, "인증서", "CA 서명 · tbsCertificate", OK)
node(1, 2, "신뢰 앵커", "미리 설치된 CA 공개 키", ACC)
harrow(1, 0, "서명으로 묶음")
harrow(1, 1, "확인의 출발점", ACC, "acc")

# 3. 비밀번호 저장
node(2, 0, "저장소 유출", "평문이면 전부 노출", INFO)
node(2, 1, "솔트 붙은 해시", "솔트가 다르면 해시도 다름", OK)
node(2, 2, "느린 비용 계수", "scrypt 한 번에 수백 ms", ACC)
harrow(2, 0, "사용자마다 다른 값")
harrow(2, 1, "추측 비용을 올림", ACC, "acc")

# 4. 메시지 하나에서 멈추는 인증
node(3, 0, "메시지 하나의 인증", "확인되는 것은 그 메시지", INFO)
node(3, 1, "메시지마다 다른 값", "복사본과 새것을 가름", OK)
node(3, 2, "TLS · 세션 인증", "다음 편에서 다룸", ACC)
harrow(3, 0, "재전송 위험")
harrow(3, 1, "묶는 장치", ACC, "acc")

d.legend(556, [("출발하는 문제", INFO), ("쓰는 도구", OK), ("남는 과제 · 얻는 결과", ACC)])
d.save("45-01.chapter-overview.svg")
