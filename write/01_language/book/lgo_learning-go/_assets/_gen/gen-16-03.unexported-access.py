# 16-03.unexported-access — 리플렉션이 내보내지 않은 필드 b 의 오프셋 8 을 알려 주고, unsafe.Add 로 그 자리를 짚어 *bool 로 바꿔 쓴다
# 본문 요구(16-03 §3 「리플렉션과 unsafe 로 내보내지 않은 필드에 닿고…」): HasUnexportedField{A int; b bool; C string} 은 32바이트,
#           A 0 · b 8 · C 16. reflect.TypeOf(huf).Elem().FieldByName("b") 의 Offset 8 → unsafe.Add(unsafe.Pointer(huf), 8) → (*bool) → *b = true.
# 타입 스펙: type-architecture — 윗줄은 구조체의 메모리 막대(32바이트, 칸 폭 22), 아랫줄은 왼→오른 흐름 노드 넷. 마지막 노드에서 b 칸으로
#           올라가는 직교 화살표. focal 은 b 칸 하나.
# 사실 출처: Learning Go 2판 16장 「Accessing Unexported Fields」, go1.27.1 실행(2026-09-29) — 32, 0, 16, b offset 8, {10 false hello} → {10 true hello}.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 984, 470
X0, CW, CH, YM = 176, 22, 40, 140
NW, NH, ST, YN = 200, 60, 236, 292
X = [28 + i * ST for i in range(4)]


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def node(x, title, sub, c=None):
    if c:
        d.tone(x, YN, NW, NH, c, 6, "12", 1.1)
    else:
        d.box(x, YN, NW, NH)
    d.t(x + NW / 2, YN + 26, title, 12, c or INK, kr(title), "middle", 600)
    d.t(x + NW / 2, YN + 46, sub, 11, MUTED, kr(sub), "middle")


d = D(W, H, "ARCHITECTURE · 16-03 §3",
      "리플렉션이 위치를, unsafe 가 쓰기를 맡아 막힌 필드에 닿습니다",
      "HasUnexportedField 는 32바이트로 A 가 0, 내보내지 않은 b 가 8, C 가 16 바이트째에 있다. 다른 패키지는 b 를 직접 쓸 수 없지만, 리플렉션의 FieldByName 이 "
      "b 의 StructField 와 Offset 8 을 돌려준다. 구조체 포인터를 unsafe.Pointer 로 바꿔 unsafe.Add 로 8 을 더하고 *bool 로 바꾸면 b 에 true 를 쓸 수 있다.",
      lead="윗줄은 구조체의 메모리, 아랫줄은 b 의 자리를 찾아 쓰는 순서입니다.")

d.t(X0 - 14, YM + 25, "HasUnexportedField", 12, INK, MONO, "end", 600)
segs = [("A int", 0, 8, INFO), ("b", 8, 1, ACC), ("pad", 9, 7, None), ("C string", 16, 16, INFO)]
for lab, off, n, c in segs:
    x = X0 + off * CW
    if c:
        d.tone(x + 1, YM, n * CW - 2, CH, c, 3, "22" if c == ACC else "12", 1.4 if c == ACC else 1.0)
        d.t(x + n * CW / 2, YM + 25, lab, 11, c, MONO, "middle", 600)
    else:
        d.o.append(f'<rect x="{x + 1}" y="{YM + 1}" width="{n * CW - 2}" height="{CH - 2}" rx="3" fill="none" stroke="{SOFT}" stroke-width="0.8" stroke-dasharray="3 3"/>')
        d.t(x + n * CW / 2, YM + 25, lab, 11, MUTED, MONO, "middle")
for k in (0, 8, 16, 32):
    d.t(X0 + k * CW, YM - 10, str(k), 10, MUTED, MONO, "middle")

node(X[0], 'FieldByName("b")', "reflect.StructField", INFO)
node(X[1], "sf.Offset == 8", "위치만 알려 줌")
node(X[2], "unsafe.Add(start, 8)", "구조체 포인터 + 8", INFO)
node(X[3], "*(*bool)(pos) = true", "막힌 필드에 씀", ACC)
for i in range(3):
    d.arrow([(X[i] + NW + 2, YN + NH / 2), (X[i + 1] - 4, YN + NH / 2)], SOFT, "soft", 1.3)
bx = X0 + 8 * CW + CW / 2
tx = X[3] + NW / 2
d.arrow([(tx, YN - 2), (tx, YN - 36), (bx, YN - 36), (bx, YM + CH + 4)], ACC, "acc", 1.3)
d.t(bx + 10, YN - 44, "이 칸을 가리킴", 11, ACC, KR, "start", 600)

d.legend(414, [("리플렉션·unsafe 단계", INFO), ("내보내지 않은 필드", ACC)])
d.save("16-03.unexported-access.svg")
print("ok 16-03 unexported-access")
