/**
 * PII 마스킹 함수 단위 테스트
 *
 * 실행: npm test
 */
import { maskName, maskPhone, maskEmail, maskCustomerInfo } from "./transform";

describe("PII 마스킹", () => {

  describe("maskName", () => {
    it("이름 첫 글자만 남기고 마스킹", () => {
      expect(maskName("홍길동")).toBe("홍**");
    });

    it("두 글자 이름", () => {
      expect(maskName("홍길")).toBe("홍*");
    });

    it("한 글자 이름은 그대로", () => {
      expect(maskName("홍")).toBe("홍");
    });

    it("영문 이름", () => {
      expect(maskName("Alice")).toBe("A****");
    });
  });

  describe("maskPhone", () => {
    it("하이픈 있는 전화번호", () => {
      expect(maskPhone("010-1234-5678")).toBe("010-****-5678");
    });

    it("하이픈 없는 전화번호", () => {
      expect(maskPhone("01012345678")).toBe("010-****5678");
    });
  });

  describe("maskEmail", () => {
    it("일반 이메일", () => {
      expect(maskEmail("hong@example.com")).toBe("ho**@example.com");
    });

    it("짧은 로컬 파트", () => {
      expect(maskEmail("ab@test.com")).toBe("a**@test.com");
    });

    it("@ 없는 문자열은 그대로", () => {
      expect(maskEmail("invalid")).toBe("invalid");
    });
  });

  describe("maskCustomerInfo", () => {
    it("전체 고객 정보 마스킹", () => {
      const input = {
        name: "홍길동",
        phone: "010-1234-5678",
        email: "hong@example.com",
        address: "서울시 강남구 테헤란로 123",
      };

      const result = maskCustomerInfo(input);

      expect(result.name).toBe("홍**");
      expect(result.phone).toBe("010-****-5678");
      expect(result.email).toBe("ho**@example.com");
      expect(result.address).toBe("***");
    });

    it("일부 필드만 있는 경우", () => {
      const input = { name: "김철수" };
      const result = maskCustomerInfo(input);

      expect(result.name).toBe("김**");
      expect(result.phone).toBeUndefined();
    });
  });
});
