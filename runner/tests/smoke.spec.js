const {
  test,
  expect
} = require("@playwright/test");

test(
  "QualiAgent Playwright runner smoke test",
  async ({ page }) => {

    await page.setContent(`
      <html>
        <head>
          <title>QualiAgent Runner</title>
        </head>

        <body>
          <h1>QualiAgent</h1>
          <p>Runner operational</p>
        </body>
      </html>
    `);

    await expect(
      page.getByRole(
        "heading",
        {
          name: "QualiAgent"
        }
      )
    ).toBeVisible();

    await expect(
      page.getByText(
        "Runner operational"
      )
    ).toBeVisible();
  }
);