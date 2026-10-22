# 타입 스펙: type-process — 단계 틀 위에 칸마다 같은 슬롯(번호·벡터 이름·책의 장)이 반복되는 stage framework. 코드 → 빌드 → 레지스트리 → 실행 네 단계에 공격 벡터 9종을 배정한다. focal 은 컨테이너 이스케이프.
# 사실 출처: 노트 L83~L95(벡터 9종과 장 번호), L87(코드), L88~L89(빌드), L90(레지스트리·공급망), L91~L95(실행 중). 네 단계 이름은 L67 "컨테이너 생애주기" 와 각 벡터 설명의 단계 서술(빌드 단계·레지스트리 저장·실행 시점)에서 읽은 구분이다.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, WARN, INFO, KR, MONO

W, H = 984, 556


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "PROCESS · 01-01 §2",
      "공격 벡터 9종은 생애주기 네 단계에 걸치고 실행 단계에 가장 몰립니다",
      "컨테이너 생애주기는 코드, 이미지 빌드, 레지스트리 보관, 실행의 네 단계다. 코드에 1번, 빌드에 2·3번, 레지스트리에 4번 공급망 공격이 있고, "
      "실행 단계에는 설정·호스트·시크릿·네트워킹·이스케이프 다섯이 몰린다. 카드 끝의 장 번호는 책이 그 주제를 다루는 곳이다.",
      lead="카드의 번호는 책이 부르는 벡터 순서, 장 번호는 그 주제를 본격적으로 다루는 장입니다.")

CW, GAP, X0 = 204, 32, 36
HY, HH = 108, 56
CY0, CST, CH = 188, 60, 48

STAGES = [
    ("코드", "개발자가 씀", INFO, [
        (1, "취약한 애플리케이션 코드", "이미지 스캐닝 · 7장", False),
    ]),
    ("빌드", "이미지로 만듦", INFO, [
        (2, "잘못 설정된 이미지", "root 로 실행 설정 · 6장", False),
        (3, "빌드 머신 공격", "빌드 과정 조작 · 6장", False),
    ]),
    ("레지스트리", "저장 후 당겨옴", INFO, [
        (4, "공급망 공격", "바꿔치기 · 변조 · 6장", False),
    ]),
    ("실행", "호스트에서 가동", WARN, [
        (5, "잘못 설정된 컨테이너", "불필요한 권한 · 9장", False),
        (6, "취약한 호스트", "구버전 컴포넌트 · 4장", False),
        (7, "노출된 시크릿", "자격증명 · 토큰 · 12장", False),
        (8, "안전하지 않은 네트워킹", "네트워킹 10장 · 11장", False),
        (9, "컨테이너 이스케이프", "격리 4장 · 강화 8장", True),
    ]),
]

for j, (name, sub, c, cards) in enumerate(STAGES):
    x = X0 + j * (CW + GAP)
    fit(name, 13, CW - 16)
    fit(sub, 12, CW - 16)
    d.tone(x, HY, CW, HH, c, 6, "14", 1.2)
    d.t(x + 16, HY + 22, f"단계 {j + 1}", 11, SOFT, MONO, "start")
    d.t(x + CW / 2, HY + 26, name, 13, c, KR, "middle", 600)
    d.t(x + CW / 2, HY + 46, sub, 12, MUTED, KR, "middle")
    if j < len(STAGES) - 1:
        d.arrow([(x + CW + 2, HY + HH // 2), (x + CW + GAP - 4, HY + HH // 2)], SOFT, "soft", 1.3)
    for i, (n, title, chap, focal) in enumerate(cards):
        y = CY0 + i * CST
        fit(title, 13, CW - 44)
        fit(chap, 12, CW - 32)
        if focal:
            d.tone(x, y, CW, CH, ACC, 6, "1F", 1.6)
        else:
            d.box(x, y, CW, CH)
        d.t(x + 16, y + 20, str(n), 12, ACC if focal else c, MONO, "start", 600)
        d.t(x + 34, y + 20, title, 13, ACC if focal else INK, KR, "start", 600)
        d.t(x + 34, y + 38, chap, 12, MUTED, kr(chap), "start")

d.legend(H - 56, [("코드·빌드·보관 중", INFO), ("실행 중", WARN), ("이스케이프", ACC)])
d.save(str(ASSETS / "01-01.attack-vectors.svg"))
print("ok 01-01 attack-vectors")
