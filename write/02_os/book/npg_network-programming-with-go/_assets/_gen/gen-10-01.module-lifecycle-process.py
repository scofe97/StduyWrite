# 타입 스펙: type-process
# 사실 출처: NPG Ch.10 Listing 10-5, 10-6, 10-7 (RestrictPrefix module implementation), p.13-16
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 960, 440
d = D(W, H, "NPG CH.10 — CADDY MODULE LIFECYCLE PROCESS",
      "Caddy 미들웨어 모듈의 생명주기와 요청 처리 파이프라인",
      "모듈 등록부터 설정 디코딩, 프로비저닝, 검증, 런타임 체인 실행까지의 단계입니다",
      "caddy.RegisterModule, Provisioner, Validator, MiddlewareHandler 순차 실행")

y0, box_h = 108, 244
bw = 144
gap_w = 48

# Stage 1: 모듈 등록 (init)
s1_x = 24
d.box(s1_x, y0, bw, box_h, fill=PAPER2, stroke=WARN, sw=1.2, r=8)
d.t(s1_x + 14, y0 + 22, "STEP 1", 9, WARN, MONO, "start", 600)
d.t(s1_x + bw / 2, y0 + 44, "모듈 등록", 12, INK, KR, "middle", 600)
d.t(s1_x + bw / 2, y0 + 62, "init() 초기화", 11, MUTED, KR, "middle")

d.box(s1_x + 8, y0 + 74, bw - 16, 116, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(s1_x + 14, y0 + 94, "RegisterModule", 9, WARN, MONO, "start", 600)
d.t(s1_x + 14, y0 + 114, "모듈 ID:", 11, SOFT, KR, "start")
d.t(s1_x + 14, y0 + 130, "http.handlers.", 8, INK, MONO, "start")
d.t(s1_x + 14, y0 + 144, "restrict_prefix", 8, INK, MONO, "start")
d.t(s1_x + 14, y0 + 164, "New() 생성자 등록", 11, MUTED, KR, "start")

d.t(s1_x + bw / 2, y0 + 208, "caddy.ModuleInfo", 9, MUTED, MONO, "middle")
d.t(s1_x + bw / 2, y0 + 226, "글로벌 레지스트리", 11, MUTED, KR, "middle")

# 화살표 1: Stage 1 -> Stage 2
g1_x = s1_x + bw
d.line(g1_x, y0 + 120, g1_x + gap_w, y0 + 120, c=MUTED, sw=1.4)
d.arrow([(g1_x + gap_w - 12, y0 + 120), (g1_x + gap_w, y0 + 120)], c=MUTED, m="ar", sw=1.4)
d.t(g1_x + gap_w / 2, y0 + 110, "인스턴스", 11, MUTED, KR, "middle")

# Stage 2: 설정 디코딩
s2_x = g1_x + gap_w
d.box(s2_x, y0, bw, box_h, fill=PAPER2, stroke=INFO, sw=1.2, r=8)
d.t(s2_x + 14, y0 + 22, "STEP 2", 9, INFO, MONO, "start", 600)
d.t(s2_x + bw / 2, y0 + 44, "설정 역직렬화", 12, INK, KR, "middle", 600)
d.t(s2_x + bw / 2, y0 + 62, "JSON Unmarshal", 10, MUTED, MONO, "middle")

d.box(s2_x + 8, y0 + 74, bw - 16, 116, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(s2_x + 14, y0 + 94, "json.Unmarshal", 9, INFO, MONO, "start", 600)
d.t(s2_x + 14, y0 + 114, "구조체 태그 매핑:", 11, SOFT, KR, "start")
d.t(s2_x + 14, y0 + 130, 'Prefix string', 8, INK, MONO, "start")
d.t(s2_x + 14, y0 + 146, '`json:"prefix"`', 8, MUTED, MONO, "start")
d.t(s2_x + 14, y0 + 168, '설정값: "." 바인딩', 11, OK, KR, "start")

d.t(s2_x + bw / 2, y0 + 208, "JSON 키 주입", 11, MUTED, KR, "middle")
d.t(s2_x + bw / 2, y0 + 226, "필드 값 할당", 11, MUTED, KR, "middle")

# 화살표 2: Stage 2 -> Stage 3
g2_x = s2_x + bw
d.line(g2_x, y0 + 120, g2_x + gap_w, y0 + 120, c=INFO, sw=1.4)
d.arrow([(g2_x + gap_w - 12, y0 + 120), (g2_x + gap_w, y0 + 120)], c=INFO, m="info", sw=1.4)
d.t(g2_x + gap_w / 2, y0 + 110, "주입 완료", 11, INFO, KR, "middle")

# Stage 3: 프로비저닝 (Provision)
s3_x = g2_x + gap_w
d.box(s3_x, y0, bw, box_h, fill=PAPER2, stroke=ACC, sw=1.2, r=8)
d.t(s3_x + 14, y0 + 22, "STEP 3", 9, ACC, MONO, "start", 600)
d.t(s3_x + bw / 2, y0 + 44, "리소스 준비", 12, INK, KR, "middle", 600)
d.t(s3_x + bw / 2, y0 + 62, "caddy.Provisioner", 10, MUTED, MONO, "middle")

d.box(s3_x + 8, y0 + 74, bw - 16, 116, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(s3_x + 14, y0 + 94, "Provision(ctx)", 9, ACC, MONO, "start", 600)
d.t(s3_x + 14, y0 + 114, "의존성 주입 단계:", 11, SOFT, KR, "start")
d.t(s3_x + 14, y0 + 132, "ctx.Logger(p)", 9, INK, MONO, "start")
d.t(s3_x + 14, y0 + 150, "Zap 로거 획득", 11, MUTED, KR, "start")
d.t(s3_x + 14, y0 + 168, "모듈 컨텍스트 공유", 11, SOFT, KR, "start")

d.t(s3_x + bw / 2, y0 + 208, "로거 필드 저장", 11, MUTED, KR, "middle")
d.t(s3_x + bw / 2, y0 + 226, "p.logger 설정", 11, MUTED, KR, "middle")

# 화살표 3: Stage 3 -> Stage 4
g3_x = s3_x + bw
d.line(g3_x, y0 + 120, g3_x + gap_w, y0 + 120, c=ACC, sw=1.4)
d.arrow([(g3_x + gap_w - 12, y0 + 120), (g3_x + gap_w, y0 + 120)], c=ACC, m="acc", sw=1.4)
d.t(g3_x + gap_w / 2, y0 + 110, "준비 완료", 11, ACC, KR, "middle")

# Stage 4: 유효성 검증 (Validate)
s4_x = g3_x + gap_w
d.box(s4_x, y0, bw, box_h, fill=PAPER2, stroke=INFO, sw=1.2, r=8)
d.t(s4_x + 14, y0 + 22, "STEP 4", 9, INFO, MONO, "start", 600)
d.t(s4_x + bw / 2, y0 + 44, "유효성 검증", 12, INK, KR, "middle", 600)
d.t(s4_x + bw / 2, y0 + 62, "caddy.Validator", 10, MUTED, MONO, "middle")

d.box(s4_x + 8, y0 + 74, bw - 16, 116, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(s4_x + 14, y0 + 94, "Validate()", 9, INFO, MONO, "start", 600)
d.t(s4_x + 14, y0 + 114, "설정 기본값 보정:", 11, SOFT, KR, "start")
d.t(s4_x + 14, y0 + 132, 'if p.Prefix == ""', 8, INK, MONO, "start")
d.t(s4_x + 14, y0 + 148, '  p.Prefix = "."', 8, OK, MONO, "start")
d.t(s4_x + 14, y0 + 168, "기본값 보정 · nil 반환", 11, WARN, KR, "start")

d.t(s4_x + bw / 2, y0 + 208, "검증 통과 후", 11, MUTED, KR, "middle")
d.t(s4_x + bw / 2, y0 + 226, "체인 등록 승인", 11, MUTED, KR, "middle")

# 화살표 4: Stage 4 -> Stage 5
g4_x = s4_x + bw
d.line(g4_x, y0 + 120, g4_x + gap_w, y0 + 120, c=OK, sw=1.4)
d.arrow([(g4_x + gap_w - 12, y0 + 120), (g4_x + gap_w, y0 + 120)], c=OK, m="ok", sw=1.4)
d.t(g4_x + gap_w / 2, y0 + 110, "서빙 가동", 11, OK, KR, "middle")

# Stage 5: 런타임 요청 처리 (ServeHTTP)
s5_x = g4_x + gap_w
s5_w = W - 24 - s5_x
d.box(s5_x, y0, s5_w, box_h, fill=PAPER2, stroke=OK, sw=1.2, r=8)
d.t(s5_x + 14, y0 + 22, "STEP 5", 9, OK, MONO, "start", 600)
d.t(s5_x + s5_w / 2, y0 + 44, "요청 처리", 12, INK, KR, "middle", 600)
d.t(s5_x + s5_w / 2, y0 + 62, "MiddlewareHandler", 9, MUTED, MONO, "middle")

d.box(s5_x + 8, y0 + 74, s5_w - 16, 52, fill=PAPER, stroke=BAD, sw=0.8, r=4)
d.t(s5_x + 14, y0 + 94, "접두사 일치:", 11, BAD, KR, "start", 600)
d.t(s5_x + 14, y0 + 112, "404 Not Found 차단", 11, BAD, KR, "start")

d.box(s5_x + 8, y0 + 134, s5_w - 16, 52, fill=PAPER, stroke=OK, sw=0.8, r=4)
d.t(s5_x + 14, y0 + 154, "접두사 불일치:", 11, OK, KR, "start", 600)
d.t(s5_x + 14, y0 + 172, "next.ServeHTTP(w,r)", 8, OK, MONO, "start")

d.t(s5_x + s5_w / 2, y0 + 208, "런타임 반복 호출", 11, MUTED, KR, "middle")
d.t(s5_x + s5_w / 2, y0 + 226, "체인 위임 또는 차단", 11, MUTED, KR, "middle")

# 범례
d.legend(386, [
    ("등록 (init)", WARN),
    ("설정 및 검증", INFO),
    ("준비 (Provision)", ACC),
    ("정상 위임", OK),
    ("404 차단", BAD),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "10-01.module-lifecycle-process.svg"))
d.save(out)
print(f"saved: {out}")
