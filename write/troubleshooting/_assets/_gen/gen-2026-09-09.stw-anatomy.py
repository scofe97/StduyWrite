# 2026-09-09 E 문항 — STW 4.17초의 내부 구성.
# 논지는 "이 시간이 전부 GC 시간이 아니다"이다. 막대 하나를 두 구간으로 갈라
# 실제 수집과 로그 쓰기 블로킹의 비율을 보이고, 로그가 그 합계를 GC 로 기록한다는
# 것을 아래에 붙인다. focal 은 블로킹 구간.
# 타입 스펙: type-bar — 범주별 수치 비교. 여기서는 누적 막대로 구간 분해.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, BAD, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 800, 424
BX, BW = 150, 560
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-09 E",
      "STW 안에 무엇이 들어 있나",
      "관측된 멈춤 1.59초를 구간으로 가른 그림. 실제 수집은 0.12초이고 나머지 1.47초는 "
      "GC 로그를 쓰는 write() 가 커널에서 막힌 시간이다. 멈춤을 풀기 전에 로그를 쓰므로 "
      "그 대기가 STW 에 포함되고, 로그에는 합계가 GC 멈춤으로 기록된다.",
      lead="GC 가 오래 걸린 것이 아니라 로그를 쓰다 막혔습니다")

# 배경 부하 없을 때
y1 = 122
d.t(BX - 16, y1 + 20, "배경 부하 없음", 12, MUTED, KR, "end")
w_ok = BW * 0.12 / 1.59
d.tone(BX, y1, w_ok, 32, OK, 4)
d.t(BX + w_ok + 12, y1 + 21, "0.25초 미만 — 정상", 12, OK, KR, "start")

# 배경 150MB/s 쓰기
y2 = 190
d.t(BX - 16, y2 + 20, "배경 150MB/s 쓰기", 12, MUTED, KR, "end")
d.tone(BX, y2, w_ok, 32, INFO, 4)
d.t(BX + w_ok / 2, y2 + 21, "0.12", 11, INFO, MONO)
d.tone(BX + w_ok, y2, BW - w_ok, 32, ACC, 4)
d.t(BX + w_ok + (BW - w_ok) / 2, y2 + 21, "1.47초 — write() 가 커널에서 막힘", 12, ACC, KR)

# 합계 브래킷
d.line(BX, y2 + 44, BX + BW, y2 + 44, RULE, 1.0)
d.t(BX + BW / 2, y2 + 66, "GC 로그에는 이 합계가 STW 1.59초로 기록됩니다", 12, BAD, KR)

# 범례성 설명
d.t(BX - 16, 292, "구간", 11, SOFT, MONO, "end")
d.t(BX, 292, "실제 수집 작업", 12, INFO, KR, "start")
d.t(BX + 150, 292, "로그 쓰기 대기", 12, ACC, KR, "start")

d.t(12, 330, "막히는 이유는 둘입니다. OS 가 내려쓰는 중인 페이지에 다시 쓰려면 기다리고(stable page write),",
    12, MUTED, KR, "start")
d.t(12, 350, "저널링 파일시스템은 새 블록 할당 시 저널 커밋이 끝나야 write() 가 반환됩니다.",
    12, MUTED, KR, "start")

d.legend(H - 40, [("로그 쓰기가 잡아먹은 시간", ACC), ("실제 수집", INFO)])
d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-09.stw-anatomy.svg"))
print("ok stw-anatomy")
