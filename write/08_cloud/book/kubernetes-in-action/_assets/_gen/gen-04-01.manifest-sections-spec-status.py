# 04-01 §매니페스트 네 섹션과 spec·status 흐름
# 본문: 사용자는 spec 에 원하는 상태를 쓰고 status 에서 실제 상태를 읽는다. 컨트롤러는 spec 을
#   읽어 실제 클러스터를 맞춘 뒤 status 를 쓴다. GET/PUT 은 섹션 하나가 아니라 오브젝트 전체를
#   주고받는다. 네 섹션 = Type metadata(apiVersion+kind) · Object metadata · Spec · Status.
# 타입 스펙: type-loop.md — 한 오브젝트 안의 네 칸과 그 둘레를 도는 루프가 함께 있어야 하므로, 오브젝트를
#           가운데 두고 사용자와 컨트롤러가 각각 어느 칸을 읽고 쓰는지를 화살표로 잇는다.
#           루프가 요점이므로 방향이 서로 반대인 것이 보여야 한다.
#           네 화살표가 오브젝트를 가운데 두고 한 바퀴 돈다 — ①사용자가 spec 을 쓰고 ②컨트롤러가 읽고
#           ③status 를 쓰고 ④사용자가 읽는다. 마지막이 처음으로 이어지고, 가운데 오브젝트가 상태를
#           쌓아 두는 공용 중심이라 정본이 말하는 "writes durable state back to one common center" 다.
#           정본의 방사형 링 대신 사각 고리로 그린 것이 어긋나는 지점이다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 724
d = D(W, H, "KUBERNETES IN ACTION · 04-01",
      "사용자는 spec 을 쓰고 컨트롤러는 status 를 쓴다",
      "한 오브젝트 안에서 쓰는 칸이 갈린다. 사용자는 spec 에 목표를 적고 status 를 읽으며, "
      "컨트롤러는 spec 을 읽어 실제를 맞춘 뒤 status 에 결과를 적는다.",
      lead="GET·PUT 은 섹션 하나가 아니라 오브젝트 전체를 주고받는다")

OBJ = (500, 400)
OW, SEC_H = 340, 76
# 오브젝트 존(324~676)과 좌우 상자 사이 코리도어가 14px 뿐이라 문장 칩이 존을 덮었다.
# 좌우를 바깥으로 밀고 칩은 번호만 남긴다 — 설명은 아래 산문이 맡는다.
USER, CTRLR = (150, 300), (850, 300)   # 폭 250 — 130/870 은 viewBox 를 20px 넘겼다

ddx.band(d, 104, 668, "spec 은 선언된 목표이고 status 는 관측된 결과다 — 컨트롤러는 둘의 차이를 줄인다")

def side(cx, cy, t, s, tag, c):
    d.box(cx - 125, cy - 54, 250, 108, PAPER2, c, 1.1, 6)
    d.t(cx, cy - 16, t, 13, c, KR, "middle", 600)
    d.t(cx, cy + 8, s, 11, MUTED, KR)
    d.t(cx, cy + 30, tag, 10, SOFT, KR)

side(*USER, "사용자 · kubectl", "create · apply · get", "서버가 아니라 오브젝트를 만진다", ACC)
side(*CTRLR, "Controller", "watch → compare → act", "타입마다 전담 컨트롤러가 있다", OK)

d.o.append(f'<rect x="{OBJ[0]-OW//2-16}" y="220" width="{OW+32}" height="368" rx="8" '
           f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
ddx.ring_label(d, OBJ[0] - OW // 2 - 16, 220, "Object Manifest — 네 섹션이 한 객체로 저장된다",
               11, INFO, off=16)

SECTIONS = [("apiVersion + kind", "1. Type metadata — 무슨 타입인가", INFO),
            ("metadata", "2. Object metadata — 이름·라벨·UID", INFO),
            ("spec", "3. Spec — 사용자가 쓰는 원하는 상태", ACC),
            ("status", "4. Status — 컨트롤러가 쓰는 실제 상태", OK)]
for i, (key, label, c) in enumerate(SECTIONS):
    y = 252 + i * (SEC_H + 12)
    d.o.append(f'<rect x="{OBJ[0]-OW//2}" y="{y}" width="{OW}" height="{SEC_H}" rx="6" '
               f'fill="{c}12" stroke="{c}" stroke-width="1.1"/>')
    d.t(OBJ[0], y + 30, key, 13, c, MONO, "middle", 600)
    d.t(OBJ[0], y + 54, ddx.fit(label, 10, OW - 20, key), 10, SOFT, KR)

SPEC_Y, STATUS_Y = 252 + 2 * 88 + 38, 252 + 3 * 88 + 38
d.path(f"M {USER[0]+125+6} {USER[1]} L 300 {USER[1]} L 300 {SPEC_Y} L {OBJ[0]-OW//2-10} {SPEC_Y}",
       ACC, 1.8, m="acc")
d.chip(300, 344, "①", ACC, 11)
d.path(f"M {OBJ[0]-OW//2-6} {STATUS_Y} L 300 {STATUS_Y} L 300 {USER[1]+54+18} "
       f"L {USER[0]} {USER[1]+54+18} L {USER[0]} {USER[1]+54+10}", MUTED, 1.5, m="ar")
d.chip(300, 552, "④", MUTED, 11)

d.path(f"M {OBJ[0]+OW//2+6} {SPEC_Y} L 700 {SPEC_Y} L 700 {CTRLR[1]} L {CTRLR[0]-125-10} {CTRLR[1]}",
       OK, 1.8, m="ok")
d.chip(700, 344, "②", OK, 11)
d.path(f"M {CTRLR[0]} {CTRLR[1]+54+6} L {CTRLR[0]} {STATUS_Y} L {OBJ[0]+OW//2+10} {STATUS_Y}",
       OK, 1.8, m="ok")
d.chip(700, 552, "③", OK, 11)

d.t(36, 612, "① 사용자가 spec 을 쓴다   ② 컨트롤러가 spec 을 읽는다   ③ 컨트롤러가 status 를 쓴다   ④ 사용자가 status 를 읽는다", 11, SOFT, KR, "start")
d.t(36, 636, "쓰는 칸이 갈려 있어 충돌하지 않는다 — 사용자가 status 를 쓰지 않고 컨트롤러가 "
             "spec 을 쓰지 않는다.", 12, MUTED, KR, "start")
d.legend(684, [("사용자가 쓰는 칸", ACC), ("컨트롤러가 쓰는 칸", OK), ("한 오브젝트", INFO)])
d.save("04-01-manifest-sections-spec-status.svg")
print("ok manifest-sections")
