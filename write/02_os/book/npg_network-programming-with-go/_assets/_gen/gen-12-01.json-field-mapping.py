# 타입 스펙: type-flowchart
# 사실 출처: RFC 8259, encoding/json, NPG Ch.12 Listing 12-10~12-12
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 980, 520
d = D(W, H, "FLOWCHART · JSON FIELD MAPPING",
      "JSON 이 공개 필드만 싣고 any 로 풀 때 숫자를 float64 로 담는 규칙",
      "대문자 공개 필드만 JSON 키가 되고 소문자 secret 은 빠지며, 풀 때는 받는 타입(구조체인지 any 인지)에 따라 숫자 타입이 갈립니다.",
      lead="RFC 8259 는 정수와 실수를 나누지 않아 any 로 풀면 모든 JSON 숫자가 float64 가 됩니다.")

# 1. 원본 구조체 정의 (좌측)
d.tone(36, 160, 244, 150, INFO, 6, "14", 1.1)
d.t(158, 188, "Go 구조체 (secret 을 더한 예)", 13, INFO, KR, "middle", 600)
d.t(158, 214, "type Chore struct {", 11, INK, MONO, "middle")
d.t(158, 234, "  Complete    bool   (공개)", 11, OK, MONO, "middle")
d.t(158, 254, "  Description string (공개)", 11, OK, MONO, "middle")
d.t(158, 274, "  secret      int    (비공개)", 11, BAD, MONO, "middle")
d.t(158, 294, "}", 11, INK, MONO, "middle")

# 화살표 1 -> 2
d.arrow([(280, 235), (324, 235)], c=SOFT, m="soft")
d.t(302, 224, "인코딩", 11, MUTED, KR, "middle")

# 2. 직렬화된 JSON 텍스트 (중앙)
d.tone(328, 160, 272, 150, OK, 6, "14", 1.1)
d.t(464, 188, "JSON 텍스트 (143 B)", 13, OK, KR, "middle", 600)
d.t(464, 214, "[", 11, INK, MONO, "middle")
d.t(464, 234, '  {"Complete": false,', 11, INK, MONO, "middle")
d.t(464, 254, '   "Description": "Mop floors"},', 11, INK, MONO, "middle")
d.t(464, 274, "  …  (secret 키 없음)", 11, BAD, KR, "middle")
d.t(464, 294, "]", 11, INK, MONO, "middle")

# 화살표 2 -> 3 분기 (직교 라우팅)
# 상단 분기: 구체 타입
d.arrow([(600, 205), (644, 205), (644, 165), (684, 165)], c=OK, m="ok")
d.t(644, 152, "구조체로 풀 때", 11, OK, KR, "middle")

# 하단 분기: interface{}
d.arrow([(600, 265), (644, 265), (644, 305), (684, 305)], c=WARN, m="warn")
d.t(644, 320, "any 로 풀 때", 11, WARN, KR, "middle")

# 3-1. 구체 구조체 디코딩 (우상단)
d.tone(688, 120, 256, 100, OK, 6, "14", 1.1)
d.t(816, 148, "Decode(&[]*Chore)", 13, OK, MONO, "middle", 600)
d.t(816, 172, "Complete    → bool (false)", 11, INK, MONO, "middle")
d.t(816, 192, 'Description → string ("Mop...")', 11, INK, MONO, "middle")
d.t(816, 208, "선언한 타입 그대로", 11, MUTED, KR, "middle")

# 3-2. interface{} 디코딩 (우하단)
d.tone(688, 260, 256, 110, WARN, 6, "14", 1.1)
d.t(816, 288, "Decode(&any / interface{})", 13, WARN, MONO, "middle", 600)
d.t(816, 312, "숫자는 모두 float64", 11, INK, MONO, "middle")
d.t(816, 332, "9007199254740993 →", 11, BAD, MONO, "middle")
d.t(816, 352, "9007199254740992", 11, BAD, MONO, "middle")

d.legend(450, [("Go 구조체", INFO), ("공개 필드·구조체로 풀기", OK), ("any 로 풀기", WARN), ("빠지거나 바뀌는 값", BAD)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "12-01.json-field-mapping.svg"
d.save(str(svg_path))
print("ok 12-01 json-field-mapping")
