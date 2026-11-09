const { test, expect } = require('@playwright/test');

test.describe('Negative login scenarios', () => {
  test('Login with valid username and incorrect password', async ({ page }) => {
    // Test data - replace with actual values or environment variables
    const validUsername = process.env.VALID_USERNAME || 'valid_user@example.com';
    const invalidPassword = process.env.INVALID_PASSWORD || 'wrongPassword123';
    const loginUrl = process.env.LOGIN_URL || 'https://example.com/login';

    // Step 1: Navigate to the login page
    await page.goto(loginUrl);
    await expect(page).toHaveURL(/.*login.*/i);
    // Verify login page elements are visible
    const usernameInput = page.locator('#username');
    const passwordInput = page.locator('#password');
    const submitButton = page.locator('button[type="submit"]');
    await expect(usernameInput).toBeVisible();
    await expect(passwordInput).toBeVisible();
    await expect(submitButton).toBeVisible();

    // Step 2: Enter valid username
    await usernameInput.fill(validUsername);
    await expect(usernameInput).toHaveValue(validUsername);

    // Step 3: Enter incorrect password
    await passwordInput.fill(invalidPassword);
    await expect(passwordInput).toHaveValue(invalidPassword);

    // Step 4: Submit the login form
    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle' }).catch(() => {}),
      submitButton.click()
    ]);

    // Step 5: Verify error feedback is displayed and no authenticated session is created
    const errorMessage = page.locator('.error-message, .alert-danger, .notification-error');
    await expect(errorMessage).toBeVisible();
    await expect(errorMessage).toContainText(/invalid|incorrect|failed/i);

    // Optional: Ensure we are still on the login page (no redirect to dashboard)
    await expect(page).toHaveURL(/.*login.*/i);
  });
});