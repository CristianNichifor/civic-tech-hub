const { test, expect } = require('@playwright/test');
for (const width of [390, 1280]) {
  test(`directory is navigable at ${width}px`, async ({ page }) => {
    await page.setViewportSize({ width, height: 900 });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto('/');
    await expect(page.locator('h1')).toBeVisible();
    const links = page.locator('a[href]');
    expect(await links.count()).toBeGreaterThan(0);
    for (const link of await links.all()) {
      expect((await link.getAttribute('href')).trim()).not.toBe('');
    }
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
    expect(overflow, 'page must fit the viewport').toBe(false);
    expect(errors).toEqual([]);
  });
}
