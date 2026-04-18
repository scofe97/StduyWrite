import { defineConfig, devices } from '@playwright/test';
import path from 'path';
import dotenv from 'dotenv';

// .env 파일 로드 (있는 경우)
dotenv.config();

const MOCK_SERVER_URL = `http://localhost:${process.env.MOCK_SERVER_PORT || 3002}`;
const TPS_BASE_URL = process.env.TPS_BASE_URL || '';

export default defineConfig({
  // 테스트 파일 패턴
  testDir: '.',
  testMatch: '**/*.spec.ts',
  testIgnore: ['**/node_modules/**', '**/python/**'],

  // 전역 설정
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,

  // 리포터 설정
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['list'],
  ],

  // 공통 설정
  use: {
    baseURL: MOCK_SERVER_URL,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    actionTimeout: 10000,
  },

  // 프로젝트별 설정
  projects: [
    // --- Mock Server 기반 테스트 ---
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        baseURL: MOCK_SERVER_URL,
      },
    },
    {
      name: 'firefox',
      use: {
        ...devices['Desktop Firefox'],
        baseURL: MOCK_SERVER_URL,
      },
    },
    {
      name: 'webkit',
      use: {
        ...devices['Desktop Safari'],
        baseURL: MOCK_SERVER_URL,
      },
    },

    // --- 모바일 에뮬레이션 ---
    {
      name: 'mobile-chrome',
      use: {
        ...devices['Pixel 7'],
        baseURL: MOCK_SERVER_URL,
      },
    },
    {
      name: 'mobile-safari',
      use: {
        ...devices['iPhone 14'],
        baseURL: MOCK_SERVER_URL,
      },
    },

    // --- TPS 실제 환경 (조건부) ---
    ...(TPS_BASE_URL ? [{
      name: 'tps-real',
      use: {
        ...devices['Desktop Chrome'],
        baseURL: TPS_BASE_URL,
        storageState: path.join(__dirname, '.auth', 'tps-user.json'),
      },
      testDir: './07-tps-real-world/practice',
      testMatch: 'tps-*.spec.ts',
    }] : []),
  ],

  // Mock Server 자동 기동
  webServer: {
    command: 'node mock-server/server.js',
    port: parseInt(process.env.MOCK_SERVER_PORT || '3002'),
    reuseExistingServer: !process.env.CI,
    timeout: 10000,
  },
});
