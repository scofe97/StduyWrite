# 타입 스펙: type-flowchart — 컨테이너에 정보를 넣는 길이 시점(빌드 · 실행)에서 갈라져 다섯 경로가 되고, 경로마다 막다른 판정(탈락 · 조건부 · 선호)으로 끝난다. 빌드 시점 둘은 하나의 탈락으로 합쳐진다. focal 은 선호되는 5번 경로.
# 사실 출처: 노트 L90~L96(다섯 경로 표), L98~L105(1·2 하드코딩 탈락), L107~L113(3 네트워크, 드묾, X.509), L115~L140(4 덤프 · inspect · 순환 불가), L142~L146(5 파일 마운트 선호)
# Layout conventions: 열 다섯 cx=128+176k, 상자 160x60(경로 y=296), 판정 y=408 h80, 마름모 cx=392 cy=204 폭176 높이88. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


W, H = 960, 584
d = D(W, H, "FLOWCHART · 12-01 §2",
      "빌드 시점 둘은 탈락이고, 실행 시점 셋 중 파일 마운트가 선호됩니다",
      "컨테이너에 정보를 넣는 길은 빌드 시점의 이미지 안 파일과 이미지 설정 환경 변수, 실행 시점의 네트워크 수신과 docker run -e 환경 변수와 볼륨 마운트 다섯이다. "
      "앞의 둘은 하드코딩이라 탈락하고, 네트워크는 드물며, 환경 변수는 눈총을 받고, 볼륨 마운트가 선호된다.",
      lead="이미지에 넣는 길은 소스 열람과 재빌드 때문에, 환경 변수는 덤프와 순환 불가 때문에 막힙니다")

BW, BH = 160, 60
CX = [128, 304, 480, 656, 832]
RY, VY, VH = 296, 408, 80

# 시작과 갈림길
d.tone(272, 100, 240, 36, SOFT, 18, "12", 1.2)
d.t(392, 123, "컨테이너에 정보 넣기", 13, INK, KR, "middle", 600)
d.arrow([(392, 138), (392, 158)], SOFT, "soft", 1.3)
pts = "392,160 480,204 392,248 304,204"
d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{MUTED}" stroke-width="1.3"/>')
d.t(392, 209, "넣는 시점은?", 13, INK, KR, "middle", 600)

# 빌드 쪽 출구와 버스
d.line(302, 204, 216, 204, SOFT, 1.3)
d.line(216, 204, 216, 268, SOFT, 1.3)
d.line(CX[0], 268, CX[1], 268, SOFT, 1.3)
d.chip(259, 204, "빌드", MUTED, 11, 5)
# 실행 쪽 출구와 버스
d.line(482, 204, 656, 204, SOFT, 1.3)
d.line(656, 204, 656, 268, SOFT, 1.3)
d.line(CX[2], 268, CX[4], 268, SOFT, 1.3)
d.chip(569, 204, "실행", MUTED, 11, 5)
for cx in CX:
    d.arrow([(cx, 268), (cx, RY - 2)], SOFT, "soft", 1.3)

# 경로 상자
ROUTES = [
    ("1", "파일", "이미지 루트 파일시스템", False),
    ("2", "환경 변수", "이미지 설정 안", False),
    ("3", "네트워크", "인터페이스로 수신", False),
    ("4", "환경 변수", "docker run -e", False),
    ("5", "볼륨", "호스트 볼륨 마운트", True),
]
for cx, (num, title, sub, focal) in zip(CX, ROUTES):
    x = cx - BW // 2
    fit(title, 13, BW - 32)
    fit(sub, 12, BW - 16)
    if focal:
        d.tone(x, RY, BW, BH, ACC, 6, "1F", 1.6)
    else:
        d.box(x, RY, BW, BH)
    d.t(x + 12, RY + 20, num, 11, ACC if focal else SOFT, MONO, "start")
    d.t(cx, RY + 28, title, 13, INK, KR, "middle", 600)
    d.t(cx, RY + 48, sub, 12, INFO, kr(sub), "middle")

# 판정으로 가는 화살표: 1·2 는 하나로 합친다
for cx in CX[:2]:
    d.line(cx, RY + BH + 2, cx, 384, BAD, 1.5)
d.line(CX[0], 384, CX[1], 384, BAD, 1.5)
d.o.append(f'<circle cx="216" cy="384" r="4" fill="{BAD}"/>')
d.arrow([(216, 384), (216, VY - 2)], BAD, "bad", 1.5)
for cx, c, m in ((CX[2], WARN, "warn"), (CX[3], WARN, "warn"), (CX[4], OK, "ok")):
    d.arrow([(cx, RY + BH + 2), (cx, VY - 2)], c, m, 1.5)


def verdict(cx, w, c, title, sub1, sub2):
    fit(title, 14, w - 16)
    fit(sub1, 12, w - 16)
    fit(sub2, 12, w - 16)
    d.tone(cx - w // 2, VY, w, VH, c, 6, "14", 1.2)
    d.t(cx, VY + 28, title, 14, c, kr(title), "middle", 600)
    d.t(cx, VY + 48, sub1, 12, MUTED, kr(sub1), "middle")
    d.t(cx, VY + 66, sub2, 12, MUTED, kr(sub2), "middle")


verdict(216, 232, BAD, "탈락 · 하드코딩", "소스 접근자 전원 열람", "재빌드 없이 변경 불가")
verdict(CX[2], BW, WARN, "드묾", "호출 코드 필요", "X.509 인증서 필요")
verdict(CX[3], BW, WARN, "눈총", "크래시 덤프", "inspect · 순환 불가")
verdict(CX[4], BW, OK, "선호", "tmpfs 메모리 유지", "재시작 없는 순환")

d.legend(528, [("탈락", BAD), ("조건부", WARN), ("선호", OK), ("논점", ACC), ("경로 내용", INFO)])
d.save(str(ASSETS / "12-01.five-routes.svg"))
print("ok 12-01 five-routes")
