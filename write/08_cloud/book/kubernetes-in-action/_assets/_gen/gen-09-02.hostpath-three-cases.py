# 09-02 §2 — type 검사가 무엇을 바꾸는가
# 본문이 kind 실측 셋을 든다. 표로 옮기면 "검사의 효과"가 안 보이므로, 같은 hostPath 에서
# type 만 달리했을 때 결과가 어떻게 갈리는지가 축이어야 한다.
# 타입 스펙: type-dp-security-matrix.md — 행은 type 값 셋, 열은 경로 상태와 결과다. 같은 hostPath 에서 type 만 달리했을 때
#           무엇이 갈리는지가 칸으로 드러난다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, KR
import ddx

d = D(1260, 620, "KUBERNETES IN ACTION · 09-02",
      "type 이 조용한 오작동을 즉시 실패로 바꾼다",
      "type 이 없으면 경로가 기대와 달라도 조용히 마운트돼 나중에 앱이 엉뚱하게 오작동한다. "
      "type 을 지정하면 시작 시점에 명확히 실패시켜 문제를 events 로 드러낸다.",
      "같은 hostPath 를 type 만 바꿔 kind 에서 돌린 결과")

ddx.matrix(
    d, x0=24, hdr_y=148, row_h=92, gap=12, focal_col=3,
    cols=[(250, "설정"), (300, "경로 상태"), (300, "쿠버네티스가 한 일"), (330, "결과")],
    rows=[
        ([("path: /", "type 없음"), ("존재한다", "노드 루트"),
          ("그대로 마운트", "아무것도 검사하지 않는다"),
          ("노드 전체가 보인다", "조용히 성공한다")], BAD),
        ([("DirectoryOrCreate", "/tmp/hostpath-demo"), ("없다", "만들어야 한다"),
          ("만들어 준다", "drwxr-xr-x root root · 755"),
          ("정상 기동", "권한은 kubelet 사용자")], OK),
        ([("Directory", "/tmp/does-not-exist-xyz"), ("없다", "만들지 않는다"),
          ("검사에서 막는다", "hostPath type check failed"),
          ("ContainerCreating 에 멈춘다", "기동 실패")], ACC),
    ])

d.t(24, 480, "세 번째가 실패이지만 가장 안전하다. 첫 번째처럼 조용히 지나가면 문제가 한참 뒤 앱의 오작동으로 "
             "나타나고, 그때는 원인이 볼륨이라는 것조차 알기 어렵다.", 11, MUTED, KR, "start")
d.t(24, 502, "FileOrCreate·DirectoryOrCreate 로 쿠버네티스가 만들 때 권한은 각각 644·755 이고, "
             "소유자·그룹은 kubelet 을 돌리는 쪽이다.", 11, MUTED, KR, "start")
d.legend(532, [("조용히 지나간다", BAD), ("만들어 준다", OK), ("즉시 실패시킨다", ACC)])
d.save("09-02-hostpath-three-cases.svg")
print("ok")
