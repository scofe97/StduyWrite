# 14-01 §7 Wasm 모듈의 뼈대와 콜백 — 원문 14.5.4 의 index.ts.
# 본문(원문 14.5.4): 프로젝트를 띄우면 index.ts 에 TypeScript 클래스 둘이 생긴다. 첫째 AddHeaderRoot 는
#       Wasm 모듈의 커스텀 설정을 맡고, 둘째 AddHeader 는 요청 경로를 실제로 처리하는 콜백 함수를
#       구현하는 자리다. 예제는 AddHeader 의 onResponseHeaders 를 구현해, 설정이 비어 있으면
#       ("hello", "world!") 를 아니면 설정값을 응답 헤더에 붙이고 FilterHeadersStatusValues.Continue 를
#       돌려준다. 요청과 응답을 다루는 다른 유용한 함수로 onRequestHeaders · onRequestBody ·
#       onResponseHeaders · onResponseBody 가 있다. AddHeader 는 Context 를 상속하고 생성자에서
#       root_context 를 받아 필드로 들고 있다.
# 타입 스펙: type-uml-class — 정적 구조. 상속 화살표와 연산 칸이 이 타입의 논거이고 둘 다 원문에 있다.
#           클래스 3(최대 7) · 관계 2(최대 8) · 칸마다 멤버 5 이하 · coral 은 구현이 들어가는 클래스.
#           관계 어휘는 스펙대로 상속(속 빈 삼각형)과 연관(다중도 양끝)만 쓰고, 쓰지 않은 넷은 범례에
#           담지 않는다 — 프리미티브의 범례 스와치가 실선 사각형뿐이라 선의 모양을 구분해 그릴 수 없다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 664
d = D(W, H, "ISTIO IN ACTION · 14-01 §7",
      "설정을 드는 클래스와 요청을 만지는 클래스",
      "생성기가 만들어 주는 뼈대는 둘로 나뉜다. 뿌리 클래스가 모듈 설정을 들고, 색이 붙은 클래스가 "
      "요청 경로의 콜백을 구현한다. 예제가 손대는 것은 그 넷 중 하나뿐이다.",
      "언어는 골라도 되지만 Envoy 버전과 ABI 는 맞춰야 합니다")

def cls(x, y, w, name, stereo, attrs, ops, focal=False, italic=False):
    hn = 46
    ha = 22 * len(attrs) + (10 if attrs else 0)
    ho = 22 * len(ops) + (10 if ops else 0)
    h = hn + ha + ho
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    if stereo:
        d.t(x + w / 2, y + 18, stereo, 8, SOFT, MONO, "middle", 600)
    d.t(x + w / 2, y + (38 if stereo else 30), name, 13, ACC if focal else INK, MONO, "middle", 600)
    yy = y + hn
    if attrs:
        d.line(x, yy, x + w, yy, RULE, 0.9)
        for i, a in enumerate(attrs):
            d.t(x + 16, yy + 20 + i * 22, a, 9.5, MUTED, MONO, "start")
        yy += ha
    if ops:
        d.line(x, yy, x + w, yy, RULE, 0.9)
        for i, o in enumerate(ops):
            d.t(x + 16, yy + 20 + i * 22, o, 9.5, MUTED, MONO, "start")
    return h

CTX_X, CTX_Y, CTX_W = 588, 132, 332
ADD_X, ADD_Y, ADD_W = 588, 300, 332
ROOT_X, ROOT_Y, ROOT_W = 48, 300, 332

h_ctx = cls(CTX_X, CTX_Y, CTX_W, "Context", "«SDK 가 주는 기반»", [], [])
h_add = cls(ADD_X, ADD_Y, ADD_W, "AddHeader", None,
            ["+ root_context: AddHeaderRoot"],
            ["+ onRequestHeaders(): Status",
             "+ onRequestBody(): Status",
             "+ onResponseHeaders(a: u32): Status",
             "+ onResponseBody(): Status"], focal=True)
h_root = cls(ROOT_X, ROOT_Y, ROOT_W, "AddHeaderRoot", None,
             ["+ configuration: string"], [])

# 상속 — 속 빈 삼각형이 부모 쪽에
MX = ADD_X + ADD_W / 2
d.line(MX, ADD_Y, MX, CTX_Y + h_ctx + 14, INK, 1.2)
d.o.append(f'<polygon points="{MX} {CTX_Y + h_ctx} {MX - 9} {CTX_Y + h_ctx + 15} {MX + 9} {CTX_Y + h_ctx + 15}" '
           f'fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>')
tw = len("extends") * 6 + 12
d.o.append(f'<rect x="{MX + 12}" y="{CTX_Y + h_ctx + 22}" width="{tw}" height="14" fill="{PAPER}"/>')
d.t(MX + 18, CTX_Y + h_ctx + 32, "extends", 8, SOFT, MONO, "start", 600)

# 연관 — 다중도 양끝
AY = ADD_Y + 40
d.path(f"M {ADD_X} {AY} H {ROOT_X + ROOT_W + 2}", MUTED, 1.2, m="ar")
d.chip((ROOT_X + ROOT_W + ADD_X) / 2, AY - 22, "설정을 참조한다", MUTED, 9)
d.t(ROOT_X + ROOT_W + 16, AY + 18, "1", 8, SOFT, MONO, "start", 600)
d.t(ADD_X - 16, AY + 18, "1", 8, SOFT, MONO, "end", 600)

d.t(48, 540, "예제가 손대는 것은 onResponseHeaders 하나 — 설정이 비면 hello: world! 를, 아니면 설정값을 붙이고 Continue 를 돌려준다", 11, SOFT, KR, "start")
d.t(48, 564, "빌드 산출물은 .wasm 모듈을 레이어 하나로 담은 OCI 이미지이고, 메타데이터가 호환되는 Envoy 버전과 ABI 를 적는다", 11, MUTED, KR, "start")
d.t(48, 588, "SDK 는 넷이다 — C++ · Rust · AssemblyScript · TinyGo. 저자는 TypeScript 변종인 AssemblyScript 를 고른다", 11, SOFT, KR, "start")
d.legend(608, [("요청 경로의 콜백이 들어가는 클래스", ACC), ("설정을 드는 뿌리 클래스", MUTED)])
d.save("14-01.wasm-module.svg")
