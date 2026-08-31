# 07-01 §4 xDS 유형별 푸시 횟수 — 원문 7.2.2 의 pilot_xds_pushes 다섯 줄을 그대로.
# 원문: cds 756 · eds 1077 · lds 671 · rds 538 · sds 55.
# 타입 스펙: type-bar — 범주 다섯의 정확한 수치 비교가 논점이라 면적 비율(treemap)이 아니라 막대를 쓴다.
#           막대 5개(4~8), y 축은 0 에서 시작, 초점 막대 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, KR, MONO

W, H = 1000, 572
d = D(W, H, "ISTIO IN ACTION · 07-01 §4",
      "istiod 가 xDS 유형마다 몇 번 밀어냈는가",
      "원문 7.2.2 의 pilot_xds_pushes 다섯 줄. 엔드포인트 디스커버리가 가장 잦은 것이 3장의 설명과 맞는다. "
      "파드가 뜨고 지는 일은 리스너나 라우트가 바뀌는 일보다 훨씬 자주 일어난다.",
      "SDS 의 55 는 같은 출력의 citadel_server_csr_count 55 와 같은 수입니다")

PL, PR, PT, PB = 96, W - 40, 116, 424
rows = [("EDS", "엔드포인트", 1077, True),
        ("CDS", "클러스터", 756, False),
        ("LDS", "리스너", 671, False),
        ("RDS", "라우트", 538, False),
        ("SDS", "시크릿", 55, False)]
YMAX, n = 1200, len(rows)
pitch = (PR - PL) / n
bw = pitch * 0.58
def Y(v): return PB - v / YMAX * (PB - PT)
for g in range(0, YMAX + 1, 200):
    d.line(PL, Y(g), PR, Y(g), RULE, 1.0 if g == 0 else 0.8)
    d.t(PL - 12, Y(g) + 4, f"{g}", 8, SOFT, MONO, "end")
d.t(PL - 12, PT - 16, "푸시 횟수", 9, SOFT, KR, "end")
d.line(PL, PT, PL, PB, RULE, 0.8)
for i, (code, kor, v, focal) in enumerate(rows):
    cx = PL + pitch * (i + 0.5)
    x, y = cx - bw / 2, Y(v)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{PB - y}" rx="4" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.o.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{PB - y}" rx="4" fill="rgba(139,152,169,0.15)" stroke="{MUTED}" stroke-width="1"/>')
    mw = len(str(v)) * 7 + 10                      # 격자선 위에 값이 얹히지 않도록 종이색 마스크
    d.o.append(f'<rect x="{cx - mw / 2}" y="{y - 24}" width="{mw}" height="16" fill="{PAPER}"/>')
    d.t(cx, y - 12, f"{v}", 10, ACC if focal else MUTED, MONO)
    d.t(cx, PB + 26, code, 12, ACC if focal else INK, MONO, "middle", 600)
    d.t(cx, PB + 46, kor, 11, MUTED, KR, "middle")
d.t((PL + PR) / 2, PB + 74, "istiod 가 기동 이후 각 xDS API 로 밀어낸 설정 갱신 횟수", 11, SOFT, KR)
d.legend(528, [("가장 잦은 갱신", ACC)])
d.save("07-01.xds-pushes.svg")
