// =============================================================================
// Shared Library: buildDocker
//
// Docker 이미지를 빌드하고 Registry에 push하는 공통 함수이다.
// 여러 프로젝트의 Jenkinsfile에서 재사용할 수 있다.
//
// 사용 예시:
//   buildDocker(
//       imageName:  'my-app',
//       tag:        env.BUILD_NUMBER,
//       dockerfile: 'Dockerfile',
//       context:    '.',
//       registry:   'localhost:5000'
//   )
// =============================================================================

def call(Map config) {
    // 파라미터 기본값 설정
    def imageName  = config.imageName  ?: error('imageName은 필수 파라미터이다')
    def tag        = config.tag        ?: 'latest'
    def dockerfile = config.dockerfile ?: 'Dockerfile'
    def context    = config.context    ?: '.'
    def registry   = config.registry   ?: 'localhost:5000'

    def fullImageName = "${registry}/${imageName}"

    echo "=== Docker Build 시작 ==="
    echo "이미지: ${fullImageName}:${tag}"
    echo "Dockerfile: ${dockerfile}"
    echo "Context: ${context}"

    // TODO: Docker 이미지를 빌드하라
    // 힌트: docker.build() 메서드를 사용한다
    // 참고: https://www.jenkins.io/doc/book/pipeline/docker/
    //
    // def image = docker.build(
    //     "${fullImageName}:${tag}",
    //     "-f ${dockerfile} ${context}"
    // )
    echo 'TODO: docker.build() 호출 구현'

    // TODO: 빌드된 이미지를 Registry에 push하라
    // 힌트: docker.withRegistry()로 Registry 인증을 감싸고, image.push()를 호출한다
    // 질문: withRegistry의 두 번째 인자(credentialsId)는 언제 필요한가?
    //
    // docker.withRegistry("http://${registry}") {
    //     image.push("${tag}")
    //     image.push('latest')
    // }
    echo 'TODO: docker.withRegistry() + image.push() 구현'

    echo "=== Docker Build 완료 ==="

    // 빌드된 이미지 정보를 반환하여 후속 단계에서 사용할 수 있게 한다
    return [
        image:     fullImageName,
        tag:       tag,
        fullName:  "${fullImageName}:${tag}"
    ]
}
