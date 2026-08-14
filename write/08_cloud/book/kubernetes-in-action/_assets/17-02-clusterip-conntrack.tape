# 17-02 §3 — ClusterIP 는 어디에도 붙어 있지 않고, conntrack 이 실주소와 짝지어 둔다
#
# 재생성: cd <이 파일이 있는 디렉토리> && vhs 17-02-clusterip-conntrack.tape
#
# 전제 1. KUBECONFIG 는 kind 전용 사본을 물린다. 전역 kubeconfig 에는
# 회사 운영 클러스터가 함께 등록돼 있어 그대로 쓰면 오발사 위험이 있다.
# 아래 경로가 없으면 다음으로 다시 만든다:
#   kubectl config view --minify --flatten --context=kind-k8s-lab > /tmp/kind-only.kubeconfig
#
# 전제 2. docker exec 는 KUBECONFIG 와 무관하게 로컬 docker 데몬에 나간다.
# 녹화 전 `docker ps` 로 kind 노드 3 대 외에 아무것도 떠 있지 않음을 확인했다.

Output "17-02-clusterip-conntrack.gif"

Require kubectl
Require docker

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

Type "kubectl -n default get svc kubernetes"
Sleep 600ms
Enter
Wait+Screen /10.96.0.1/
Sleep 1s

Type "docker exec k8s-lab-control-plane ip -br -4 addr"
Sleep 600ms
Enter
Wait+Screen /172.21.0.4/
Sleep 1s

Type "docker exec k8s-lab-control-plane conntrack -L -d 10.96.0.1 | head -1"
Sleep 600ms
Enter
Wait+Screen /ESTABLISHED/
Sleep 6s
