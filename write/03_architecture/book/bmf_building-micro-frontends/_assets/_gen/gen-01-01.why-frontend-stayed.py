# 01-01 §5 — "프론트엔드는 팀이 늘어도 한 덩어리로 남았다"는 결과 하나와 그 원인들.
# 원문은 원인을 번호로 세지 않고 이어지는 산문으로 적는다. 넷으로 묶은 것은 노트의 읽기이므로
# 제목·부제에서 "저자가 든 넷"이라 단정하지 않는다 (본문 §5 의 hedge 와 표현을 맞춘다).
# 타입 스펙: type-fishbone — 관측된 결과 하나에 원인을 범주로 묶어 단다. 좌표는 스펙 §Math 공식 그대로.
#           축약: 스펙의 focal 은 "확정된 근본 원인"을 뜻하지만 원문은 근본 원인을 확정하지 않는다.
#           그래서 accent 는 저자가 가장 길게 정면으로 반박하는 원인("추상화는 은탄환이 아니다")에 준다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1440, 592
HEAD, CY = 1200, 320
d = D(W, H, "BUILDING MICRO-FRONTENDS · 01-01 §5",
      "프론트엔드는 왜 한 덩어리로 남았는가",
      "Introducing Micro-Frontends 절의 산문을 네 범주로 묶어 하나의 결과에 붙인 원인 분석도. 묶음은 노트의 읽기이고, 색이 붙은 뼈가 저자가 가장 길게 반박하는 원인이다.",
      "오른쪽 끝이 관측된 결과이고, 뼈 넷은 원문의 산문을 노트가 묶은 원인 범주입니다")

# k → (범주명, 위/아래, [하위 원인 두 개], accent 여부)
bones = [
    (1, "공유 라이브러리",   [(2, "여러 프로젝트·팀이 함께 씀"), (4, "유지보수·수동 테스트·소통 비용")], False),
    (2, "조기 추상화",       [(2, "두 번 쓰려고 수천 배 복잡해짐"), (4, "재사용 횟수를 과대평가")],       True),
    (3, "중앙집중 결정",     [(2, "규칙을 한 번 정하고 수년 유지"), (4, "한 결정 바꾸려면 전체 손봄")],   False),
    (4, "모놀리식 프론트엔드", [(2, "장수 플랫폼의 장기 개선 제약"), (4, "시간대 분산 팀에 불리")],        False),
]

def attach_x(k):  return HEAD - 160 - k * 160
def above(k):     return k % 2 == 1

# 1) 등뼈
d.arrow([(attach_x(4) - 160, CY), (HEAD - 4, CY)], INK, "ar", 1.2)

# 2) 뼈와 하위 원인 눈금 (선을 먼저 — 상자 채움이 선 끝을 덮게)
for k, name, subs, acc in bones:
    ax, up = attach_x(k), above(k)
    fx, fy = ax - 96, CY - 168 if up else CY + 168
    d.line(ax, CY, fx, fy, ACC if acc else MUTED, 1.4 if acc else 1.1)
    for m, label in subs:
        tx, ty = ax - 16 * m, CY - 28 * m if up else CY + 28 * m
        d.line(tx, ty, tx - 32, ty, SOFT, 1.0)
        d.t(tx - 36, ty - 4 if up else ty + 12, label, 9, MUTED, KR, "end")

# 3) 범주 태그 상자
for k, name, subs, acc in bones:
    fx = attach_x(k) - 96
    fy = CY - 168 if above(k) else CY + 168
    tw = len(name) * 13 + 24
    if acc:
        d.o.append(f'<rect x="{fx - tw / 2}" y="{fy - 14}" width="{tw}" height="28" rx="4" fill="{ACC}14" stroke="{ACC}" stroke-width="1.3"/>')
    else:
        d.box(fx - tw / 2, fy - 14, tw, 28, PAPER2, RULE, 1.0, 4)
    d.t(fx, fy + 5, name, 12, ACC if acc else INK, KR, "middle", 600)

# 4) 결과 상자
d.o.append(f'<rect x="{HEAD}" y="{CY - 40}" width="200" height="80" rx="6" fill="{ACC}14" stroke="{ACC}" stroke-width="1.4"/>')
d.t(HEAD + 100, CY - 10, "프론트엔드는 팀이 늘어도", 12, ACC, KR, "middle", 600)
d.t(HEAD + 100, CY + 10, "한 덩어리로 남았다", 12, ACC, KR, "middle", 600)
d.t(HEAD + 100, CY + 30, "OBSERVED EFFECT", 8, SOFT, MONO)

d.legend(540, [("저자가 가장 길게 반박하는 원인 · 관측된 결과", ACC)])
d.save("01-01.why-frontend-stayed.svg")
print("h 필요:", 540 + 22 + 16, " 실제:", H, " 최좌측 태그:", attach_x(4) - 96 - (len("모놀리식 프론트엔드") * 13 + 24) / 2)
