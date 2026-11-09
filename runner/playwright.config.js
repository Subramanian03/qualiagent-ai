const { defineConfig } =
  require("@playwright/test");

module.exports = defineConfig({
  testDir: ".",
  timeout: 30000,

  expect: {
    timeout: 5000
  },

  workers: 1,
  retries: 0,

  reporter: [
    ["line"]
  ],

  use: {
    headless: true,
    trace: "off",
    screenshot: "off",
    video: "off"
  }
});