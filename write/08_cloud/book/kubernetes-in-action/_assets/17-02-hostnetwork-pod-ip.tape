# 17-02 §3 — hostNetwork 파드는 노드 IP를 쓴다
#
# 재생성: cd <이 파일이 있는 디렉토리> && vhs 17-02-hostnetwork-pod-ip.tape
#
# 전제. KUBECONFIG 는 kind 전용 사본을 물린다. 전역 kubeconfig 에는
# 회사 운영 클러스터가 함께 등록돼 있어 그대로 쓰면 오발사 위험이 있다.
# 아래 경로가 없으면 다음으로 다시 만든다:
#   kubectl config view --minify --flatten --context=kind-k8s-lab > /tmp/kind-only.kubeconfig

Output "17-02-hostnetwork-pod-ip.gif"

Require kubectl

Set Shell "bash"
Set Width 1440
Set Height 460
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
Type "export PS1='$ '"
Enter
Type "clear"
Enter
Show

Sleep 1s

Type "kubectl -n kube-system get po -o custom-columns=NAME:.metadata.name,POD-IP:.status.podIP,NODE-IP:.status.hostIP"
Sleep 600ms
Enter

Wait+Screen /kube-proxy/
Sleep 6s
