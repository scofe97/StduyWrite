# 17-02 §1 — privileged 는 capability 를 전부 add 한 것보다 넓다
#
# 재생성: cd <이 파일이 있는 디렉토리> && vhs 17-02-privileged-vs-capabilities.tape
#
# 전제 1. KUBECONFIG 는 kind 전용 사본을 물린다(운영 클러스터 오발사 방지).
#   kubectl config view --minify --flatten --context=kind-k8s-lab > /tmp/kind-only.kubeconfig
#   사본에 default namespace 가 남아 있으면 지운다 — 없는 namespace 를 가리키면 조회가 실패한다.
# 전제 2. 조회만 한다. 매니페스트를 적용하지 않으므로 클러스터 상태를 바꾸지 않는다.
# 전제 3. kube-proxy·kindnet 은 kind 클러스터가 기본 설치한다.

Output "17-02-privileged-vs-capabilities.gif"

Require kubectl

Set Shell "bash"
Set Width 1440
Set Height 380
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
Type "export PS1='$ '"
Enter
Type "clear"
Enter
Show

Sleep 800ms

Type "kubectl get ds kube-proxy -n kube-system -o jsonpath='{..containers[0].securityContext}'; echo"
Sleep 400ms
Enter
Wait+Screen /privileged/
Sleep 2s

Type "kubectl get ds kindnet -n kube-system -o jsonpath='{..containers[0].securityContext}'; echo"
Sleep 400ms
Enter
Wait+Screen /NET_ADMIN/
Sleep 2500ms

Enter

Type "kubectl exec -n kube-system ds/kube-proxy -- grep CapEff /proc/self/status"
Sleep 400ms
Enter
Wait+Screen /000001ffffffffff/
Sleep 2s

Type "kubectl exec -n kube-system ds/kindnet -- grep CapEff /proc/self/status"
Sleep 400ms
Enter
Wait+Screen /a80435fb/
Sleep 6s
