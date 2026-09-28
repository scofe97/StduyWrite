# 13-03.dup-shadow — MarshalJSON 안의 익명 struct: 바깥 DateOrdered string 이 Dup 안의 DateOrdered time.Time 을 가린다
# 본문 요구(13-03 §3 「임베딩과 Dup 으로 한 필드만 덮어씁니다」): tmp 는 DateOrdered string 필드와 임베딩된 Dup 을 가진다.
#           Dup 은 바탕 타입이 Order 라 필드는 같고 메서드는 없어서 json.Marshal(tmp) 가 MarshalJSON 을 다시 부르지 않는다.
#           같은 이름의 바깥 필드가 이기므로 date_ordered 는 RFC822Z 문자열로 나가고 나머지 필드는 Dup 에서 나온다.
# 타입 스펙: type-nested — 바깥 상자 tmp, 그 안에 필드 상자 하나와 임베딩 상자 Dup, Dup 안에 필드 넷. 한 겹당 안쪽 여백 24.
#           가려진 필드는 WARN 점선, 이기는 필드는 ACC.
# 사실 출처: Learning Go 2판 13장 「Custom JSON Parsing」, 원서 예제 저장소 ch13 sample_code/custom_json2 와
#           Dup 없이 json.Marshal(o) 를 부른 재현(fatal error: stack overflow)을 go1.25.1 로 실행(2026-09-28).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 560
d = D(W, H, "NESTED · 13-03 §3",
      "바깥의 DateOrdered string 이 Dup 안의 time.Time 필드를 가립니다",
      "Order.MarshalJSON 안에서 만든 익명 struct tmp 의 구조. tmp 는 json 이름 date_ordered 인 DateOrdered string 필드와 임베딩된 Dup 을 가진다. "
      "Dup 은 바탕 타입이 Order 라 ID, Items, DateOrdered, CustomerID 필드는 같지만 메서드는 없다. 이름이 같은 필드는 바깥 것이 이겨 date_ordered 는 RFC822Z 문자열로 나가고, "
      "Dup 에 메서드가 없으니 json.Marshal(tmp) 가 MarshalJSON 을 다시 부르지 않아 스택이 넘치지 않는다.",
      lead="바깥 상자가 tmp, 안쪽 상자가 임베딩된 Dup 입니다.")

# tmp
d.o.append(f'<rect x="24" y="100" width="912" height="380" rx="10" fill="none" stroke="{INFO}" stroke-width="1.2"/>')
d.t(44, 126, "tmp — 익명 struct", 13, INFO, KR, "start", 600)
d.t(916, 126, "json.Marshal(tmp)", 12, MUTED, MONO, "end", 600)
# 바깥 필드
d.tone(48, 146, 400, 70, ACC, 6, "14", 1.4)
d.t(68, 176, "DateOrdered string", 13, ACC, MONO, "start", 600)
d.t(68, 200, "json:\"date_ordered\" · RFC822Z 로 채움", 11, MUTED, KR, "start")
d.t(472, 186, "같은 이름이면 바깥 필드가 이김", 12, ACC, KR, "start", 600)
# Dup
d.o.append(f'<rect x="48" y="236" width="864" height="220" rx="8" fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
d.t(68, 262, "Dup — type Dup Order", 13, INK, MONO, "start", 600)
d.t(892, 262, "필드는 같음 · 메서드는 없음", 11, MUTED, KR, "end", 600)
fields = [("ID string", "id", None), ("Items []Item", "items", None), ("DateOrdered time.Time", "가려짐", WARN), ("CustomerID string", "customer_id", None)]
for i, (f, tag, c) in enumerate(fields):
    x = 72 + (i % 2) * 420
    y = 284 + (i // 2) * 84
    if c:
        d.o.append(f'<rect x="{x}" y="{y}" width="396" height="64" rx="6" fill="{WARN}10" stroke="{WARN}" stroke-width="1.1" stroke-dasharray="5 4"/>')
        d.t(x + 20, y + 28, f, 13, WARN, MONO, "start", 600)
        d.t(x + 20, y + 49, "json 출력에서 무시됨", 11, WARN, KR, "start")
    else:
        d.box(x, y, 396, 64)
        d.t(x + 20, y + 28, f, 13, INK, MONO, "start", 600)
        d.t(x + 20, y + 49, "json:\"" + tag + "\" · 그대로 나감", 11, MUTED, MONO, "start")

d.legend(500, [("바깥 필드가 이김", ACC), ("가려져 무시됨", WARN), ("임베딩 구조", INFO)])
d.save("13-03.dup-shadow.svg")
print("ok 13-03 dup")
