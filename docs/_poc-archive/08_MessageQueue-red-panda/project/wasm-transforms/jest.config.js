module.exports = {
  preset: "ts-jest",
  testEnvironment: "node",
  roots: ["<rootDir>/src"],
  moduleFileExtensions: ["ts", "js"],
  // @redpanda-data/transform-sdk는 WASM 런타임에서만 동작하므로 mock
  moduleNameMapper: {
    "^@redpanda-data/transform-sdk$": "<rootDir>/src/__mocks__/transform-sdk.ts",
  },
};
