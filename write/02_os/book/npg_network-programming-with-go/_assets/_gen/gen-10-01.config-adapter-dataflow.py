# 타입 스펙: type-data-flow
# 사실 출처: NPG Ch.10 Listing 10-3 (TOML configuration adapter), p.9-11
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 960, 420
d = D(W, H, "NPG CH.10 — CONFIG ADAPTER DATA FLOW",
      "TOML 설정 어댑터의 JSON 변환 및 Caddy 로드 흐름",
      "사람 친화적인 TOML 문서를 Caddy 네이티브 JSON 으로 변환하여 엔진에 주입합니다",
      "Adapt 메서드의 바이트 수신, 맵 구조 변환, JSON 직렬화와 런타임 소비 단계")

y0, box_h = 108, 226
bw = 188

# Stage 1: caddy.toml
s1_x = 24
d.box(s1_x, y0, bw, box_h, fill=PAPER2, stroke=WARN, sw=1.2, r=8)
d.t(s1_x + 16, y0 + 22, "STAGE 1", 9, WARN, MONO, "start", 600)
d.t(s1_x + bw / 2, y0 + 44, "caddy.toml 입력", 12, INK, KR, "middle", 600)
d.t(s1_x + bw / 2, y0 + 62, "사람 친화적 설정", 11, MUTED, KR, "middle")

d.box(s1_x + 10, y0 + 74, bw - 20, 96, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(s1_x + 18, y0 + 96, "[apps.http.servers.hello]", 9, WARN, MONO, "start")
d.t(s1_x + 18, y0 + 116, 'listen = [":2020"]', 9, INK, MONO, "start")
d.t(s1_x + 18, y0 + 138, "# 주석 지원", 11, SOFT, KR, "start")
d.t(s1_x + 18, y0 + 156, "# 여러 줄 문자열", 11, SOFT, KR, "start")

d.t(s1_x + bw / 2, y0 + 192, "--config caddy.toml", 10, MUTED, MONO, "middle")
d.t(s1_x + bw / 2, y0 + 210, "--adapter toml", 10, MUTED, MONO, "middle")

# 화살표 1: Stage 1 -> Stage 2 (수평)
gap1_x = s1_x + bw
gap1_w = 66
d.line(gap1_x, y0 + 120, gap1_x + gap1_w, y0 + 120, c=MUTED, sw=1.4)
d.arrow([(gap1_x + gap1_w - 12, y0 + 120), (gap1_x + gap1_w, y0 + 120)], c=MUTED, m="ar", sw=1.4)
d.t(gap1_x + gap1_w / 2, y0 + 110, "TOML 바이트", 11, MUTED, KR, "middle")

# Stage 2: TOML 어댑터 (Adapt)
s2_x = gap1_x + gap1_w
d.box(s2_x, y0, bw, box_h, fill=PAPER2, stroke=ACC, sw=1.2, r=8)
d.t(s2_x + 16, y0 + 22, "STAGE 2", 9, ACC, MONO, "start", 600)
d.t(s2_x + bw / 2, y0 + 44, "TOML 어댑터 변환", 12, INK, KR, "middle", 600)
d.t(s2_x + bw / 2, y0 + 62, "caddyconfig.Adapter", 10, MUTED, MONO, "middle")

d.box(s2_x + 10, y0 + 74, bw - 20, 96, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(s2_x + 18, y0 + 96, "func Adapt()", 9, ACC, MONO, "start", 600)
d.t(s2_x + 18, y0 + 116, "1. toml.LoadBytes()", 9, INK, MONO, "start")
d.t(s2_x + 18, y0 + 138, "2. tree.ToMap()", 9, INK, MONO, "start")
d.t(s2_x + 18, y0 + 156, "3. json.Marshal()", 9, OK, MONO, "start")

d.t(s2_x + bw / 2, y0 + 192, "RegisterAdapter", 10, MUTED, MONO, "middle")
d.t(s2_x + bw / 2, y0 + 210, 'init() 에 "toml" 등록', 11, MUTED, KR, "middle")

# 화살표 2: Stage 2 -> Stage 3 (수평)
gap2_x = s2_x + bw
gap2_w = 66
d.line(gap2_x, y0 + 120, gap2_x + gap2_w, y0 + 120, c=OK, sw=1.4)
d.arrow([(gap2_x + gap2_w - 12, y0 + 120), (gap2_x + gap2_w, y0 + 120)], c=OK, m="ok", sw=1.4)
d.t(gap2_x + gap2_w / 2, y0 + 110, "JSON 바이트", 11, OK, KR, "middle")

# Stage 3: Caddy 네이티브 JSON
s3_x = gap2_x + gap2_w
d.box(s3_x, y0, bw, box_h, fill=PAPER2, stroke=OK, sw=1.2, r=8)
d.t(s3_x + 16, y0 + 22, "STAGE 3", 9, OK, MONO, "start", 600)
d.t(s3_x + bw / 2, y0 + 44, "Caddy 표준 JSON", 12, INK, KR, "middle", 600)
d.t(s3_x + bw / 2, y0 + 62, "정규화 규격", 11, MUTED, KR, "middle")

d.box(s3_x + 10, y0 + 74, bw - 20, 96, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(s3_x + 18, y0 + 96, '{"apps": {', 9, MUTED, MONO, "start")
d.t(s3_x + 18, y0 + 116, '  "http": {"servers": {', 9, MUTED, MONO, "start")
d.t(s3_x + 18, y0 + 138, '    "hello": {', 9, INK, MONO, "start")
d.t(s3_x + 18, y0 + 156, '      "listen": [":2020"]', 9, OK, MONO, "start")

d.t(s3_x + bw / 2, y0 + 192, "엔진 직접 해석", 11, MUTED, KR, "middle")
d.t(s3_x + bw / 2, y0 + 210, "REST API 와 동일 규격", 11, MUTED, KR, "middle")

# 화살표 3: Stage 3 -> Stage 4 (수평)
gap3_x = s3_x + bw
gap3_w = 66
d.line(gap3_x, y0 + 120, gap3_x + gap3_w, y0 + 120, c=INFO, sw=1.4)
d.arrow([(gap3_x + gap3_w - 12, y0 + 120), (gap3_x + gap3_w, y0 + 120)], c=INFO, m="info", sw=1.4)
d.t(gap3_x + gap3_w / 2, y0 + 110, "엔진 주입", 11, INFO, KR, "middle")

# Stage 4: Caddy 엔진 로드
s4_x = gap3_x + gap3_w
s4_w = W - 24 - s4_x
d.box(s4_x, y0, s4_w, box_h, fill=PAPER2, stroke=INFO, sw=1.2, r=8)
d.t(s4_x + 16, y0 + 22, "STAGE 4", 9, INFO, MONO, "start", 600)
d.t(s4_x + s4_w / 2, y0 + 44, "런타임 로드", 12, INK, KR, "middle", 600)
d.t(s4_x + s4_w / 2, y0 + 62, "Caddy 인프라 엔진", 11, MUTED, KR, "middle")

d.box(s4_x + 10, y0 + 74, s4_w - 20, 96, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(s4_x + 18, y0 + 96, "caddy.Load()", 9, INFO, MONO, "start", 600)
d.t(s4_x + 18, y0 + 116, "1. JSON 언마샬", 11, INK, KR, "start")
d.t(s4_x + 18, y0 + 138, "2. 모듈 프로비저닝", 11, INK, KR, "start")
d.t(s4_x + 18, y0 + 156, "3. 리스너 바인드", 11, OK, KR, "start")

d.t(s4_x + s4_w / 2, y0 + 192, "net.Listen :2020", 10, OK, MONO, "middle")
d.t(s4_x + s4_w / 2, y0 + 210, "무중단 서빙 개시", 11, MUTED, KR, "middle")

# 범례
d.legend(366, [
    ("설정 파일 (TOML)", WARN),
    ("어댑터 변환기", ACC),
    ("Caddy 표준 (JSON)", OK),
    ("런타임 엔진 구동", INFO),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "10-01.config-adapter-dataflow.svg"))
d.save(out)
print(f"saved: {out}")
