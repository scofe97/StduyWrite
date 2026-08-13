# 17-01 §3 — node selector 는 노드 label 이 붙는 순간 반응한다
#
# 재생성: cd <이 파일이 있는 디렉토리> && vhs 17-01-node-selector-transition.tape
#
# 전제 1. KUBECONFIG 는 kind 전용 사본을 물린다(운영 클러스터 오발사 방지).
#   kubectl config view --minify --flatten --context=kind-k8s-lab > /tmp/kind-only.kubeconfig
# 전제 2. 매니페스트는 실습 저장소에 있다.
#   ~/study/k8s_in_action/17-daemonset/01-node-selector/daemonset-demo-gpu.yaml
# 전제 3. 시작 상태는 gpu label 없음 + demo 없음.
#   kubectl label node k8s-lab-worker2 gpu- ; kubectl -n ch17-lab delete ds demo

Output "17-01-node-selector-transition.gif"

Require kubectl

Set Shell "bash"
Set Width 1440
Set Height 560
Set FontSize 19
Set FontFamily "JetBrains Mono"
Set Theme "GitHub Dark"
Set Padding 26
Set Framerate 24
Set TypingSpeed 22ms
Set CursorBlink false

Hide
Type "export KUBECONFIG=/tmp/kind-only.kubeconfig"
Enter
Type "cd ~/study/k8s_in_action/17-daemonset/01-node-selector"
Enter
Type "kubectl label node k8s-lab-worker2 gpu- >/dev/null 2>&1; kubectl delete ds demo --ignore-not-found >/dev/null 2>&1"
Enter
Type "while kubectl get po -l app=demo --no-headers 2>/dev/null | grep -q .; do sleep 1; done; echo CLEAN"
Enter
Wait+Screen /CLEAN/
Type "export PS1='$ '"
Enter
Type "clear"
Enter
Show

Sleep 800ms

Type "kubectl apply -f daemonset-demo-gpu.yaml"
Sleep 400ms
Enter
Wait+Screen /created/
Sleep 1s

Type "kubectl get ds demo"
Sleep 400ms
Enter
Wait+Screen /gpu=cuda/
Sleep 2s

Screenshot "17-01-node-selector-pending.png"
Sleep 1s

Enter

Type "kubectl label node k8s-lab-worker2 gpu=cuda"
Sleep 400ms
Enter
Wait+Screen /labeled/
Sleep 2s

Enter

Type "kubectl rollout status ds demo --timeout=60s"
Sleep 400ms
Enter
Wait+Screen /successfully rolled out/
Sleep 1s

Type "kubectl get ds demo"
Sleep 400ms
Enter
Sleep 2s

Type "kubectl get po -l app=demo -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName"
Sleep 400ms
Enter
Wait+Screen /Running/
Sleep 2s

Screenshot "17-01-node-selector-scheduled.png"

Sleep 4s
