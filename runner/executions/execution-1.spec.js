const { test, expect } = require('@playwright/test');

test('Verify login behaviour', async ({ page }) => {
  await page.goto(process.env.BASE_URL);

  await page.getByLabel('Username').fill(
    process.env.TEST_USERNAME
  );

  await page.getByLabel('Password').fill(
    process.env.TEST_PASSWORD
  );

  await page.getByRole('button', {
    name: 'Login'
  }).click();

  await expect(page).toHaveURL(
    /inventory|dashboard/
  );
});


