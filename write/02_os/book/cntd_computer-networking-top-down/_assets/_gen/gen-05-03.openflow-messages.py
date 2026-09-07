# 타입 스펙: type-swimlane — 두 레인 사이를 오가는 메시지를 방향별로 갈라 놓는다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.5.2 OpenFlow Protocol (TCP 6653, 메시지 7종)
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, KR, MONO

W, H = 1000, 620
d = D(W, H, "SECTION 5.5.2 · OPENFLOW MESSAGES",
      "내려가는 넷과 올라오는 셋",
      "OpenFlow 가 컨트롤러와 스위치 사이에서 나르는 메시지. 내려가는 것은 표를 바꾸거나 값을 묻는 명령이고, 올라오는 것은 스위치가 겪은 일의 보고다.",
      "TCP 위에서 돌고 기본 포트는 6653 입니다")

# 두 레인
d.tone(24, 116, 952, 34, ACC, 6, "0C", 1.2)
d.t(500, 139, "컨트롤러 → 스위치 · 명령", 12, ACC, KR, "middle", 600)
DOWN = [("Configuration", "설정 값을 묻고 정합니다"),
        ("Modify-State", "흐름 표 항목을 더하고 지우고 고칩니다"),
        ("Read-State", "흐름 표와 포트의 통계·계수기를 모읍니다"),
        ("Send-Packet", "지정한 포트로 패킷 하나를 내보냅니다")]
for i, (name, sub) in enumerate(DOWN):
    x = 24 + i * 240
    d.box(x, 166, 224, 78, PAPER2, f"{ACC}66", 1.2, 7)
    d.t(x + 112, 194, name, 12, ACC, MONO, "middle", 600)
    d.t(x + 112, 218, sub, 11, MUTED, KR)
    d.path(f"M {x + 112} 244 L {x + 112} 268", ACC, 1.3, m="acc")

d.box(24, 274, 952, 46, PAPER, RULE, 1.2, 8)
d.t(500, 302, "OpenFlow 위에서 도는 TCP 연결 · 기본 포트 6653", 12, INK, KR, "middle", 600)

UP = [("Flow-Removed", "표 항목이 사라졌음을 알립니다"),
      ("Port-status", "포트 상태가 바뀌었음을 알립니다"),
      ("Packet-in", "일치하는 항목이 없던 패킷을 올려보냅니다")]
for i, (name, sub) in enumerate(UP):
    x = 24 + i * 320
    d.path(f"M {x + 152} 372 L {x + 152} 322", INFO, 1.3, m="info")
    d.box(x, 378, 304, 78, PAPER2, f"{INFO}66", 1.2, 7)
    d.t(x + 152, 406, name, 12, INFO, MONO, "middle", 600)
    d.t(x + 152, 430, sub, 11, MUTED, KR)

d.tone(24, 472, 952, 34, INFO, 6, "0C", 1.2)
d.t(500, 495, "스위치 → 컨트롤러 · 보고", 12, INFO, KR, "middle", 600)

d.t(30, 542, "Packet-in 이 4장의 이야기와 이어집니다. 흐름 표에 일치하는 항목이 없는 패킷을 컨트롤러로 보내는 동작이,", 11, MUTED, KR, "start")
d.t(30, 562, "일치 실패를 폐기가 아니라 질문으로 바꿉니다.", 11, MUTED, KR, "start")

d.legend(576, [("내려가는 명령", ACC), ("올라오는 보고", INFO)])

out = pathlib.Path(__file__).resolve().parent.parent / "05-03.openflow-messages.svg"
d.save(out)
print("→", out)
