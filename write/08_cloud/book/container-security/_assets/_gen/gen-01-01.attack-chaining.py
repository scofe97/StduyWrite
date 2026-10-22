# 타입 스펙: type-flowchart — 공격 체이닝 4단계를 시작(타원)·단계(사각형)·끝(타원)으로 잇고, 단계 사이마다 점선 보안 경계를 세운다. 마름모는 쓰지 않고 2단계 상자에 두 출구를 "또는"으로 적는 것으로 축약했다. focal 은 호스트 root 획득.
# 사실 출처: 노트 L103~L109(보안 경계 정의, 경계가 많을수록 어렵다), L115~L118(체이닝 4단계: 원격 코드 실행 · 이스케이프 취약점 또는 안전하지 않은 설정 · 호스트 root · 호스트가 닿는 모든 것), L117(컨테이너가 root 면 3단계 사소)
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, BAD, INFO, KR, MONO

W, H = 984, 372


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "FLOWCHART · 01-01 §3",
      "공격은 보안 경계를 하나씩 넘으며 진행되고, 컨테이너가 root 면 세 번째 단계가 사소해집니다",
      "공격자는 의존성 취약점으로 컨테이너 안에서 코드를 실행하는 것으로 시작한다. 컨테이너 밖으로 나가는 출구는 이스케이프 취약점과 안전하지 않은 설정 둘이고, "
      "하나만 열려 있어도 호스트에 닿는다. 컨테이너가 root 로 돌고 있었다면 호스트 root 를 얻는 단계가 사소해진다.",
      lead="점선이 단계 사이의 보안 경계입니다. 경계가 많을수록 목표에 닿기 어렵습니다.")

NW, GAP, X0 = 196, 52, 22
NY, NH = 120, 104

STEPS = [
    # (번호, 제목, 설명 줄, 모양, 색)
    (1, "컨테이너 안 코드 실행", ["의존성 취약점 · 원격"], 20, INFO),
    (2, "컨테이너 밖으로", ["이스케이프 취약점", "또는 안전하지 않은 설정"], 6, INFO),
    (3, "호스트 root 획득", ["컨테이너가 root 면 사소"], 6, ACC),
    (4, "닿는 모든 것", ["호스트", "호스트의 모든 컨테이너"], 20, BAD),
]

for i, (n, title, subs, rx, c) in enumerate(STEPS):
    x = X0 + i * (NW + GAP)
    fit(title, 13, NW - 16)
    d.tone(x, NY, NW, NH, c, rx, "1F" if c == ACC else "14", 1.6 if c == ACC else 1.2)
    d.t(x + NW / 2, NY + 28, str(n), 11, ACC if c == ACC else SOFT, MONO, "middle", 600)
    d.t(x + NW / 2, NY + 52, title, 13, c if c == ACC else INK, kr(title), "middle", 600)
    for k, s in enumerate(subs):
        fit(s, 12, NW - 24)
        d.t(x + NW / 2, NY + 74 + k * 18, s, 12, MUTED, kr(s), "middle")
    if i < len(STEPS) - 1:
        gx = x + NW + GAP / 2
        cy = NY + NH // 2
        d.arrow([(x + NW + 4, cy), (x + NW + GAP - 6, cy)], SOFT, "soft", 1.4)
        # 점선 경계: 화살표가 지나는 자리에 세로로
        d.line(gx, NY - 20, gx, NY + NH + 46, BAD, 1.3, "5 5")
        d.chip(gx, NY + NH + 56, f"경계 {i + 1}", BAD, 11)

d.legend(H - 56, [("시작 · 끝", INFO), ("넘는 단계", INFO), ("핵심 단계", ACC), ("보안 경계", BAD)])
d.save(str(ASSETS / "01-01.attack-chaining.svg"))
print("ok 01-01 attack-chaining")
