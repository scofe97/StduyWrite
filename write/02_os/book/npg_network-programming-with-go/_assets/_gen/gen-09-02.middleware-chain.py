# 타입 스펙: type-layers
# 09-02 미들웨어 체인의 계층 구조와 요청·응답 흐름
# 사실 출처: NPG Ch.9 Listing 9-14 (StripPrefix + RestrictPrefix + FileServer), Listing 9-15 (drainAndClose + ServeMux + HandlerFunc)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 960, 420
d = D(W, H, "NPG CH.9 — MIDDLEWARE LAYER STACK",
      "미들웨어 체인의 계층 구조와 호출 흐름",
      "감싼 순서대로 요청이 안으로 들어가고 응답이 밖으로 나옵니다",
      "라우팅 보호 스택과 정적 파일 보호 스택의 실제 계층 구성")

# 공통 흐름 표시기 (좌측 여백: 요청과 응답을 나란히 분리)
d.t(30, 130, "요청 ↓", 11, ACC, KR, "middle", 600)
d.arrow([(30, 142), (30, 280)], c=ACC, m="acc")

d.t(54, 304, "응답 ↑", 11, OK, KR, "middle", 600)
d.arrow([(54, 292), (54, 154)], c=OK, m="ok")

# Stack 1: 라우터 래핑 스택 (Listing 9-15)
x1, y0, sw, lh = 76, 120, 396, 56

d.t(x1 + sw / 2, y0 - 14, "Mux 라우팅 파이프라인 (Listing 9-15)", 13, INK, KR, "middle", 600)

# L1: drainAndClose (ACC)
d.tone(x1, y0, sw, lh, ACC, op="18", sw=1.2)
d.t(x1 + 16, y0 + 24, "L1", 9, ACC, MONO, "start")
d.t(x1 + 46, y0 + 24, "drainAndClose", 13, INK, MONO, "start", 600)
d.t(x1 + sw - 14, y0 + 24, "요청 본문 비우고 닫기", 11, MUTED, KR, "end")
d.t(x1 + 46, y0 + 44, "io.Copy(io.Discard, r.Body) + r.Body.Close()", 10, MUTED, MONO, "start")

# L2: ServeMux (INFO)
y_mux = y0 + lh + 10
d.tone(x1, y_mux, sw, lh, INFO, op="16", sw=1.0)
d.t(x1 + 16, y_mux + 24, "L2", 9, INFO, MONO, "start")
d.t(x1 + 46, y_mux + 24, "http.ServeMux", 13, INK, MONO, "start", 600)
d.t(x1 + sw - 14, y_mux + 24, "최장 일치 패턴 라우팅", 11, MUTED, KR, "end")
d.t(x1 + 46, y_mux + 44, '등록 경로: "/" · "/hello" · "/hello/there/"', 11, MUTED, KR, "start")

# L3: HandlerFunc (OK)
y_h = y_mux + lh + 10
d.tone(x1, y_h, sw, lh, OK, op="16", sw=1.0)
d.t(x1 + 16, y_h + 24, "L3", 9, OK, MONO, "start")
d.t(x1 + 46, y_h + 24, "http.HandlerFunc", 13, INK, MONO, "start", 600)
d.t(x1 + sw - 14, y_h + 24, "최종 엔드포인트 응답", 11, MUTED, KR, "end")
d.t(x1 + 46, y_h + 44, "204 NoContent / 200 OK 응답 본문 작성", 11, MUTED, KR, "start")


# Stack 2: 정적 파일 보호 스택 (Listing 9-14)
x2 = 508

d.t(x2 + sw / 2, y0 - 14, "정적 파일 보호 파이프라인 (Listing 9-14)", 13, INK, KR, "middle", 600)

# L1: http.StripPrefix (INFO)
d.tone(x2, y0, sw, lh, INFO, op="16", sw=1.0)
d.t(x2 + 16, y0 + 24, "L1", 9, INFO, MONO, "start")
d.t(x2 + 46, y0 + 24, "http.StripPrefix", 13, INK, MONO, "start", 600)
d.t(x2 + sw - 14, y0 + 24, "경로 접두사 제거", 11, MUTED, KR, "end")
d.t(x2 + 46, y0 + 44, 'URL 경로에서 "/static/" 접두사를 잘라냄', 11, MUTED, KR, "start")

# L2: RestrictPrefix (ACC)
d.tone(x2, y_mux, sw, lh, ACC, op="18", sw=1.2)
d.t(x2 + 16, y_mux + 24, "L2", 9, ACC, MONO, "start")
d.t(x2 + 46, y_mux + 24, "RestrictPrefix", 13, INK, MONO, "start", 600)
d.t(x2 + sw - 14, y_mux + 24, "민감 파일 404 차단", 11, MUTED, KR, "end")
d.t(x2 + 46, y_mux + 44, 'path.Clean 후 "." 접두 세그먼트 차단', 11, MUTED, KR, "start")

# L3: http.FileServer (OK)
d.tone(x2, y_h, sw, lh, OK, op="16", sw=1.0)
d.t(x2 + 16, y_h + 24, "L3", 9, OK, MONO, "start")
d.t(x2 + 46, y_h + 24, "http.FileServer", 13, INK, MONO, "start", 600)
d.t(x2 + sw - 14, y_h + 24, "디스크 파일 서비스", 11, MUTED, KR, "end")
d.t(x2 + 46, y_h + 44, 'http.Dir("../files/") 정적 파일 스트림 반환', 11, MUTED, KR, "start")

# 범례
d.legend(352, [
    ("커스텀 미들웨어", ACC),
    ("표준 라이브러리 핸들러", INFO),
    ("최종 응답 핸들러", OK),
])

out_path = os.path.join(os.path.dirname(__file__), "..", "09-02.middleware-chain.svg")
d.save(out_path)
print("saved:", out_path)
