# 타입 스펙: type-state, type-data-flow — 03-01 생애주기 및 수신 버퍼 갱신 과정
import subprocess, sys, os
d = os.path.dirname(__file__)
subprocess.run([sys.executable, os.path.join(d, "gen-03-01.session-lifecycle.py")], check=True)
subprocess.run([sys.executable, os.path.join(d, "gen-03-01.receive-window.py")], check=True)
