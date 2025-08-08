import { test, expect } from '@playwright/test';

test('should log in successfully', async ({ page }) => {
	await page.goto('/login');

	await page.getByPlaceholder('Email').fill('stripe_02@example.com');
	await page.getByPlaceholder('Password').fill('test1234');
	await page.getByTestId('agreement').check();

	// await page.getByRole('button', { name: /login/i }).click();
	await page.getByRole('button', { name: 'Login', exact: true }).click();

	// Wait for the user to be redirected or user info to appear
	await expect(page).toHaveURL('/'); // or whatever route

	// Optional: check user-specific UI
	await expect(page.getByText(/Welcome/i)).toBeVisible();
});
