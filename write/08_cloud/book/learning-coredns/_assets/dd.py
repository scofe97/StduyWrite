"""Diagram Design 렌더 프리미티브 — 스타일 계약 준수.
좌표는 각 도식에서 공식으로 산출해 넘긴다. 여기서는 그리기만 한다."""
PAPER="#0D1117"; PAPER2="#161B22"; INK="#F5F5F3"; MUTED="#8B98A9"
SOFT="#5E6B7E"; RULE="rgba(191,192,192,0.22)"; ACC="#F08A59"
OK="#3FB98C"; WARN="#E3B341"; BAD="#F0616D"; INFO="#6A95D8"
KR="'Geist','Apple SD Gothic Neo','Noto Sans KR','Malgun Gothic',sans-serif"
MONO="'Geist Mono','Noto Sans Mono CJK KR',monospace"

def esc(t):
    return (str(t).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))

class D:
    def __init__(s,w,h,eyebrow,title,desc,lead=None):
        s.w,s.h=w,h; s.o=[]
        s.o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" role="img" aria-labelledby="dt dd">')
        s.o.append('<defs>')
        for n,c in (("ar",MUTED),("ok",OK),("warn",WARN),("bad",BAD),("info",INFO),("acc",ACC),("soft",SOFT)):
            s.o.append(f'<marker id="{n}" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6.5" markerHeight="6.5" orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="{c}"/></marker>')
        s.o.append('</defs>')
        s.o.append(f'<title id="dt">{esc(title)}</title><desc id="dd">{esc(desc)}</desc>')
        s.o.append(f'<rect width="{w}" height="{h}" fill="{PAPER}"/>')
        s.o.append(f'<text x="12" y="26" font-family="{MONO}" font-size="8" letter-spacing="0.18em" fill="{SOFT}">{esc(eyebrow)}</text>')
        s.o.append(f'<text x="12" y="52" font-family="{KR}" font-size="20" font-weight="600" fill="{INK}">{esc(title)}</text>')
        if lead: s.o.append(f'<text x="12" y="74" font-family="{KR}" font-size="11" fill="{MUTED}">{esc(lead)}</text>')
    def box(s,x,y,w,h,fill=PAPER2,stroke=RULE,sw=0.9,r=6):
        s.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def tone(s,x,y,w,h,c,r=6,op="14",sw=1.2):
        s.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{c}{op}" stroke="{c}" stroke-width="{sw}"/>')
    def t(s,x,y,txt,size=12,fill=INK,fam=None,anchor="middle",weight=400,op=None):
        fam=fam or KR
        a=f' opacity="{op}"' if op else ""
        s.o.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam}" font-size="{size}" font-weight="{weight}" fill="{fill}"{a}>{esc(txt)}</text>')
    def line(s,x1,y1,x2,y2,c=RULE,sw=0.8,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ""
        s.o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{sw}"{d}/>')
    def arrow(s,pts,c=MUTED,m="ar",sw=1.4,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ""
        p=" ".join(("M" if i==0 else "L")+f" {x} {y}" for i,(x,y) in enumerate(pts))
        s.o.append(f'<path d="{p}" fill="none" stroke="{c}" stroke-width="{sw}" marker-end="url(#{m})"{d}/>')
    def path(s,d,c=MUTED,sw=1.4,m=None,dash=None):
        mk=f' marker-end="url(#{m})"' if m else ""
        ds=f' stroke-dasharray="{dash}"' if dash else ""
        s.o.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{sw}"{mk}{ds}/>')
    def chip(s,cx,cy,txt,c=MUTED,size=9,pad=7):
        w=len(str(txt))*(size*0.62 if not any('가'<=ch<='힣' for ch in str(txt)) else size*1.0)+pad*2
        s.o.append(f'<rect x="{cx-w/2}" y="{cy-9}" width="{w}" height="18" rx="4" fill="{PAPER}" stroke="{c}" stroke-width="0.8"/>')
        s.t(cx,cy+4,txt,size,c,MONO if not any('가'<=ch<='힣' for ch in str(txt)) else KR)
    def legend(s,y,items):
        s.line(12,y,s.w-48,y,RULE,0.8)
        s.t(12,y+22,"LEGEND",8,SOFT,MONO,"start")
        x=100
        for lab,c in items:
            s.o.append(f'<rect x="{x}" y="{y+12}" width="14" height="12" rx="2" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
            s.t(x+22,y+22,lab,10,MUTED,KR,"start"); x+=44+len(lab)*13
    def save(s,p):
        s.o.append('</svg>'); open(p,"w",encoding="utf-8").write("\n".join(s.o)); return p

class Seq(D):
    """시퀀스: 참여자 레인 + 시간축 왕복. 상태는 레인 옆 칩으로."""
    def lanes(s,names,y0=104,lane_w=210):
        s.LX={}; n=len(names)
        span=(s.w-48-24)-lane_w
        for i,(nm,sub) in enumerate(names):
            x=24+lane_w/2+(span*i/(n-1) if n>1 else 0)
            s.LX[nm]=x
            s.box(x-lane_w/2,y0,lane_w,44,PAPER2,RULE,1.0)
            s.t(x,y0+20,nm,12,INK,KR,"middle",600)
            s.t(x,y0+37,sub,9,MUTED,MONO)
        s.lane_top=y0+44
        return s.LX
    def rails(s,ybot):
        for x in s.LX.values():
            s.line(x,s.lane_top+6,x,ybot,RULE,1.0,"3 6")
    def msg(s,a,b,label,y,c=MUTED,mk="ar",dash=None,sub=None):
        x1,x2=s.LX[a],s.LX[b]; d=1 if x2>x1 else -1
        s.path(f"M {x1+10*d} {y} L {x2-12*d} {y}",c,1.5,m=mk,dash=dash)
        mx=(x1+x2)/2
        s.t(mx,y-9,label,11,c,MONO,"middle",600)
        if sub: s.t(mx,y+15,sub,9,MUTED)
    def selfmsg(s,a,label,y,c=MUTED,sub=None):
        x=s.LX[a]
        s.path(f"M {x+10} {y-10} L {x+58} {y-10} L {x+58} {y+10} L {x+13} {y+10}",c,1.4,m="ar")
        s.t(x+68,y-4,label,10,c,MONO,"start")
        if sub: s.t(x+68,y+11,sub,9,MUTED,KR,"start")
    def state(s,a,txt,y,c):
        x=s.LX[a]
        w=len(txt)*7.0+18
        s.o.append(f'<rect x="{x-w/2}" y="{y-10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x,y+4,txt,9.5,c,MONO)
