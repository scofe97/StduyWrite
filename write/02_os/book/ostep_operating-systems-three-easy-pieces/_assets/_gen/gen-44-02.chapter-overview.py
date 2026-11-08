# 44-02.chapter-overview — 키워드를 노드로, 앞 키워드에서 뒤 키워드로 넘어가는 관계를 화살표 라벨로 이은 편 전체 지도
# 행 하나가 본문 `##` 하나다. 왼쪽 칩은 절 번호, 노드는 그 절의 핵심 키워드와 실제 값, 화살표 라벨은 두 키워드 사이의 관계다.
# 노드와 관계는 본문 각 절의 `>` 요약과 핵심 요약에서 가져왔다.
# 타입 스펙: type-process — 행마다 같은 의미 슬롯(문제 · 결과 · 대응)이 같은 자리에 반복된다("Stage framework with semantic slots").
#           화살표는 읽는 순서이고 라벨은 관계다. 형제 편 gen-04-02.chapter-overview.py 와 같은 stride 를 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, OK, INFO, KR, MONO

W, H = 1000, 552
COL_X, STRIDE, NW, NH = 64, 344, 200, 64
ROW_Y, ROW_STRIDE = 104, 104

d = D(W, H, "CHAPTER MAP · 44-02",
      "암호는 키에서 깨지고 OS 는 세 자리에 암호를 쓴다",
      "44-02 편의 전체 지도. 첫 행은 키가 새거나 키 선택이 무너지는 경로와, 후보가 줄면 무차별 대입이 쉬워진다는 점, 무작위 키로 막는 방법, "
      "둘째 행은 OS 가 키를 쥐면 암호가 숨기지 못한다는 한계와 예외 세 자리, "
      "셋째 행은 전체 디스크 암호화의 보호 범위와 비밀번호 보관함의 타협, "
      "넷째 행은 서명한 capability 가 위조를 막으면서 만료와 신원을 담는 방식을 보인다.",
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

for i, sec in enumerate(("§1", "§2", "§3", "§4")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

# §1 키가 깨지는 자리
node(0, 0, "키 관리 결함", "유출 · 공유 · 줄어든 선택", ACC)
node(0, 1, "무차별 대입", "32가지 키는 6번째에 발견", None)
node(0, 2, "무작위 키", "getrandom · /dev/urandom", OK)
harrow(0, 0, "후보가 줄면")
harrow(0, 1, "엔트로피로 선택")

# §2 OS 가 키를 쥔 기계
node(1, 0, "OS 가 키 보유", "복호 키와 데이터가 한 기계", INFO)
node(1, 1, "숨길 수 없음", "믿으면 불필요 · 불신하면 복사", None)
node(1, 2, "세 자리", "해시 · 전송 · 하드웨어 접근", OK)
harrow(1, 0, "복호 가능")
harrow(1, 1, "예외 세 자리")

# §3 저장 데이터 암호화
node(2, 0, "전체 디스크 암호화", "aes-xts-plain64", INFO)
node(2, 1, "장치 이동만 방어", "키는 부팅 뒤 OS·하드웨어에", None)
node(2, 2, "비밀번호 보관함", "RAM 키 · 로그아웃 때 폐기", OK)
harrow(2, 0, "보호 범위")
harrow(2, 1, "편의와 최소 권한")

# §4 서명한 capability
node(3, 0, "서명한 capability", "rights=read · 서명 256바이트", INFO)
node(3, 1, "위조 불가", "write 로 바꾸면 검증 실패", None)
node(3, 2, "만료 · 신원 · 주소", "JWT exp 클레임", OK)
harrow(3, 0, "개인 키 서명")
harrow(3, 1, "무결성 보장 정보")

d.legend(ny(3) + NH + 24, [("문제", INFO), ("이 편의 한 줄", ACC), ("대응", OK)])
d.save("44-02.chapter-overview.svg")
