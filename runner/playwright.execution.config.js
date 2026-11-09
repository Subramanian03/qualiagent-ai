const path = require("path");

const {
  defineConfig
} = require("@playwright/test");


const defaultOutputDirectory =
  path.join(
    __dirname,
    "test-results",
    "executions"
  );


const executionOutputDirectory =
  process.env
    .QUALIAGENT_EVIDENCE_DIR ||
  defaultOutputDirectory;


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

  outputDir:
    executionOutputDirectory,

  use: {
    headless: true,

    screenshot:
      "only-on-failure",

    trace:
      "retain-on-failure",

    video: "off"
  }
});