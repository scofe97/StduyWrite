# 타입 스펙: type-flowchart — 재전송 뒤 관측된 증거로 실제 손실과 오탐을 분기.
# Layout conventions: 위→아래 72px stride, 한 결정에 출구 둘.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, PAPER2, RULE, KR

W, H = 920, 552
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 14-03", "재전송은 뒤늦은 증거로 다시 판정한다",
      "타이머 만료나 중복 ACK만으로 손실을 확정하지 않는다. 재전송 뒤 돌아온 ACK, 타임스탬프, DSACK으로 손실인지 오탐인지 구분해 응답한다.",
      "지연·재정렬·복제도 손실과 같은 첫 신호를 만듭니다")

CX, CW, CH = 460, 456, 56
steps = [(112, "RTO 만료 · 중복 ACK", "손실을 의심하는 첫 신호"),
         (192, "미확인 바이트 재전송", "타이머 또는 빠른 재전송"),
         (272, "뒤늦은 ACK · TSecr · DSACK", "원본과 재전송본을 비교할 증거")]
for i,(y,name,sub) in enumerate(steps):
    if i < len(steps)-1:
        d.arrow([(CX,y+CH+4),(CX,y+80-8)], MUTED,"ar",1.5)
    d.box(CX-CW/2,y,CW,CH,PAPER2,RULE,1,20 if i==0 else 6)
    d.t(CX,y+25,name,14,ACC if i==2 else INK,KR,"middle",600)
    d.t(CX,y+45,sub,11,MUTED)

# 두 출구를 가진 결정 마름모.
DY, DW, DH = 392, 180, 64
d.arrow([(CX,272+CH+4),(CX,DY-8)],MUTED,"ar",1.5)
d.o.append(f'<polygon points="{CX},{DY} {CX+DW/2},{DY+DH/2} {CX},{DY+DH} {CX-DW/2},{DY+DH/2}" fill="{ACC}14" stroke="{ACC}" stroke-width="1.4"/>')
d.t(CX,DY+DH/2+5,"실제 손실?",14,ACC,KR,"middle",600)

BY, BH, BW, LX, RX = 472, 56, 320, 24, 576
for x,name,sub,color in [(LX,"실제 손실","구멍 복구 계속",WARN),(RX,"오탐","불필요한 재전송 영향 완화",OK)]:
    d.tone(x,BY,BW,BH,color,6,"12",1.2)
    d.t(x+BW/2,BY+24,name,14,color,KR,"middle",600)
    d.t(x+BW/2,BY+44,sub,11,MUTED)
d.arrow([(CX-DW/2,DY+DH/2),(LX+BW/2,DY+DH/2),(LX+BW/2,BY-8)],WARN,"warn",1.5)
d.arrow([(CX+DW/2,DY+DH/2),(RX+BW/2,DY+DH/2),(RX+BW/2,BY-8)],OK,"ok",1.5)
d.t(300,DY+DH/2-10,"예",11,WARN)
d.t(620,DY+DH/2-10,"아니오",11,OK)
d.save("14-03.chapter-overview.svg")
