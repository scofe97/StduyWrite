# 01-01 §2 — 언제 쪼갤 것인가. 저자가 감각 대신 관측을 근거로 삼은 순서를 판단 논리로 세운다.
# 본문 논지: "쪼갤 시점은 조직이 커진 때가 아니라 확장 성격을 셀 수 있게 된 때"이며,
#           순서를 뒤집으면 어떤 경계를 그어야 할지 모르는 채 나누게 된다(§3 의 실패).
# 타입 스펙: type-flowchart — 모양이 종류를 나른다. 마름모 판단 · 사각형 행동 · 타원 종료 · 잉크 점 합류.
#           coral 은 가장 결과가 큰 판단 하나에만 — "관측이 있는가".
import sys; sys.path.insert(0, ".")
from dd import D, ACC, WARN, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 664
d = D(W, H, "BUILDING MICRO-FRONTENDS · 01-01 §2",
      "언제 쪼갤 것인가 — 감각이 아니라 관측이 근거다",
      "저자는 배포가 느려졌다는 체감이 아니라 API 별 확장 성격의 차이를 세고 나서 분할로 갔다.",
      "마름모가 판단이고 사각형이 행동입니다. 왼쪽 갈래가 순서를 뒤집었을 때의 결말입니다")

CX, DIA_W, DIA_H = 560, 300, 88          # 판단 마름모
BOX_W, BOX_H = 260, 64

def diamond(cx, cy, w, h, label, sub, focal=False):
    c = ACC if focal else INK
    pts = f"{cx},{cy-h/2} {cx+w/2},{cy} {cx},{cy+h/2} {cx-w/2},{cy}"
    fill = f"{ACC}12" if focal else PAPER2
    d.o.append(f'<polygon points="{pts}" fill="{fill}" stroke="{c}" stroke-width="{1.4 if focal else 1.0}"/>')
    d.t(cx, cy - 2, label, 13, c, KR, "middle", 600)
    if sub: d.t(cx, cy + 18, sub, 10, MUTED, KR)

def rect(cx, cy, label, sub, c=None, w=BOX_W, h=BOX_H):
    c = c or RULE
    d.box(cx - w / 2, cy - h / 2, w, h, PAPER2, c, 1.1, 6)
    d.t(cx, cy - 4, label, 13, INK, KR, "middle", 600)
    if sub: d.t(cx, cy + 17, sub, 10, MUTED, KR)

def oval(cx, cy, label, c, w=300, h=52):
    d.o.append(f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="20" '
               f'fill="{c}12" stroke="{c}" stroke-width="1.3"/>')
    d.t(cx, cy + 5, label, 13, c, KR, "middle", 600)

Y0, Y1, Y2, Y3, Y4 = 118, 236, 356, 468, 578

# 시작 — 모놀리스가 성공해 조직이 커진 상태
oval(CX, Y0, "모놀리스가 성공하고 조직이 커졌다", SOFT, 340, 48)

# 판단 하나 — 이 편의 focal
d.arrow([(CX, Y0 + 24), (CX, Y1 - DIA_H / 2 - 2)], MUTED, "ar", 1.4)
diamond(CX, Y1, DIA_W, DIA_H, "확장 성격을 셀 수 있는가", "로그·대시보드에 근거가 있는가", focal=True)

# NO — 왼쪽·아래. 감각만 있는 상태
NX = 200
d.arrow([(CX - DIA_W / 2, Y1), (NX, Y1), (NX, Y2 - BOX_H / 2 - 2)], WARN, "warn", 1.4)
d.t(CX - DIA_W / 2 - 44, Y1 - 10, "아니오", 11, WARN, KR)
rect(NX, Y2, "감각만 있다", "배포가 느리다 · 릴리스가 무섭다 · 회의가 길다", WARN, 300)
d.arrow([(NX, Y2 + BOX_H / 2), (NX, Y3 - 26)], WARN, "warn", 1.4)
oval(NX, Y3, "경계를 모르는 채 나눈다", WARN, 300, 48)
d.arrow([(NX, Y3 + 24), (NX, Y4 - 24)], WARN, "warn", 1.4, "5 5")
oval(NX, Y4, "§3 의 실패 — 큰 진흙 공", WARN, 300, 48)

# YES — 오른쪽·아래. 관측이 근거가 된 상태
YX = 760
d.arrow([(CX + DIA_W / 2, Y1), (YX, Y1), (YX, Y2 - BOX_H / 2 - 2)], OK, "ok", 1.4)
d.t(CX + DIA_W / 2 + 26, Y1 - 10, "예", 11, OK, KR)
rect(YX, Y2, "관측을 센다", "캐시 듣는 API 는 CDN 이 받음 · 오리진 압박은 소수", OK, 320)
d.arrow([(YX, Y2 + BOX_H / 2), (YX, Y3 - BOX_H / 2 - 2)], OK, "ok", 1.4)
rect(YX, Y3, "그 경계로 분할한다", "저장소까지 나눔 · 공유하지 않음", OK, 320)
d.arrow([(YX, Y3 + BOX_H / 2), (YX, Y4 - 24)], OK, "ok", 1.4)
oval(YX, Y4, "탈중앙 생태계 — 팀이 자기 묶음을 소유", OK, 340, 48)

d.legend(620, [("이 편의 판단", ACC), ("순서를 뒤집은 갈래", WARN), ("저자가 실제로 간 길", OK)])
d.save("01-01.when-to-split.svg")
print("h 필요:", 620 + 22 + 16, " 실제:", H)
