package com.runnershigh.modulith;

import org.junit.jupiter.api.Test;
import org.springframework.modulith.core.ApplicationModules;
import org.springframework.modulith.docs.Documenter;

class ModularityTests {

    ApplicationModules modules = ApplicationModules.of(ModulithApplication.class);

    @Test
    void verifyModularity() {
        // 모듈 구조 검증 - internal 패키지 규칙 위반 시 실패
        modules.verify();
    }

    @Test
    void printModules() {
        // 현재 모듈 구조 출력
        modules.forEach(System.out::println);
    }

    @Test
    void generateDocumentation() {
        // 모듈 문서 자동 생성 (build/spring-modulith-docs/)
        new Documenter(modules).writeDocumentation();
    }
}
