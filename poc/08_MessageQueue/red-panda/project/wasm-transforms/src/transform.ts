/**
 * Redpanda WASM Data Transform: PII 마스킹
 *
 * 원본 주문 이벤트(raw-orders)에서 개인정보를 마스킹한 뒤
 * cleaned-orders 토픽으로 출력한다.
 *
 * 배포:
 *   npm run build
 *   rpk transform deploy \
 *     --name pii-masking \
 *     --input-topic raw-orders \
 *     --output-topic cleaned-orders \
 *     --file dist/transform.wasm
 *
 * 참고: https://docs.redpanda.com/current/develop/data-transforms/
 */
import { onRecordWritten } from "@redpanda-data/transform-sdk";

// ─── 엔트리포인트 ───────────────────────────────────────
onRecordWritten((event, writer) => {
  try {
    const rawValue = event.record.value;
    if (!rawValue) {
      return; // tombstone (삭제 이벤트) → 무시
    }

    const data = JSON.parse(rawValue.text());

    // customerInfo 필드가 있으면 PII 마스킹 적용
    if (data.customerInfo) {
      data.customerInfo = maskCustomerInfo(data.customerInfo);
    }

    writer.write({
      ...event.record,
      value: JSON.stringify(data),
    });
  } catch (error) {
    // 파싱 실패 시 원본 그대로 통과 (데이터 유실 방지)
    console.error("Transform error:", error);
    writer.write(event.record);
  }
});

// ─── PII 마스킹 함수들 ─────────────────────────────────

interface CustomerInfo {
  name?: string;
  phone?: string;
  email?: string;
  address?: string;
  [key: string]: unknown;
}

function maskCustomerInfo(info: CustomerInfo): CustomerInfo {
  const masked = { ...info };

  if (masked.name) {
    masked.name = maskName(masked.name);
  }
  if (masked.phone) {
    masked.phone = maskPhone(masked.phone);
  }
  if (masked.email) {
    masked.email = maskEmail(masked.email);
  }
  if (masked.address) {
    masked.address = "***";
  }

  return masked;
}

/**
 * 이름 마스킹: 첫 글자만 노출
 * "홍길동" → "홍**"
 */
function maskName(name: string): string {
  if (name.length <= 1) return name;
  return name.charAt(0) + "*".repeat(name.length - 1);
}

/**
 * 전화번호 마스킹: 가운데 4자리 숨김
 * "010-1234-5678" → "010-****-5678"
 */
function maskPhone(phone: string): string {
  return phone.replace(/(\d{3})-?\d{4}(-?\d{4})/, "$1-****$2");
}

/**
 * 이메일 마스킹: 로컬 파트 절반만 노출
 * "hong@example.com" → "ho**@example.com"
 */
function maskEmail(email: string): string {
  const atIndex = email.indexOf("@");
  if (atIndex <= 0) return email;

  const local = email.substring(0, atIndex);
  const domain = email.substring(atIndex);
  const visibleLength = Math.max(1, Math.floor(local.length / 2));
  return local.substring(0, visibleLength) + "**" + domain;
}

// ─── 테스트용 export ────────────────────────────────────
export { maskName, maskPhone, maskEmail, maskCustomerInfo };
