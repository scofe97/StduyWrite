# 17-01 §2 — toleration 을 안 적어도 컨트롤러가 붙여 준다
#
# 재생성: cd <이 파일이 있는 디렉토리> && vhs 17-01-auto-toleration.tape
#
# 전제 1. KUBECONFIG 는 kind 전용 사본을 물린다(운영 클러스터 오발사 방지).
#   kubectl config view --minify --flatten --context=kind-k8s-lab > /tmp/kind-only.kubeconfig
#   사본에 default namespace 가 남아 있으면 지운다 — 없는 namespace 를 가리키면 apply 가 실패한다.
# 전제 2. 매니페스트는 실습 저장소에 있다.
#   ~/study/k8s_in_action/17-daemonset/02-auto-toleration/daemonset-demo-plain.yaml
# 전제 3. 시작 상태는 demo 없음.
#   kubectl delete ds demo --ignore-not-found

Output "17-01-auto-toleration.gif"

Require kubectl

Set Shell "bash"
Set Width 1440
Set Height 500
Set FontSize 19
Set FontFamily "JetBrains Mono"
Set Theme "GitHub Dark"
Set Padding 26
Set Framerate 24
Set TypingSpeed 18ms
Set CursorBlink false

Hide
Type "export KUBECONFIG=/tmp/kind-only.kubeconfig"
Enter
Type "cd ~/study/k8s_in_action/17-daemonset/02-auto-toleration"
Enter
Type "kubectl delete ds demo --ignore-not-found --wait=true >/dev/null 2>&1"
Enter
Sleep 8s
Type "export PS1='$ '"
Enter
Type "clear"
Enter
Show

Sleep 800ms

Type "grep -c tolerations daemonset-demo-plain.yaml"
Sleep 400ms
Enter
Sleep 2s

Enter

Type "kubectl apply -f daemonset-demo-plain.yaml"
Sleep 400ms
Enter
Sleep 1500ms

Type "kubectl rollout status ds demo --timeout=60s >/dev/null && echo READY"
Sleep 400ms
Enter
Wait+Screen /READY/
Sleep 2s

Enter

Type `kubectl get po -l app=demo -o jsonpath='{range .items[0].spec.tolerations[*]}{.key}{"  "}{.effect}{"\n"}{end}'`
Sleep 400ms
Enter
Sleep 6s
