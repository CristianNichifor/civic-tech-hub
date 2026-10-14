const { test, expect } = require('@playwright/test');

const HUB = 'https://projects.cristian-nichifor.com/';

test('sends visitors to the projects hub', async ({ page }) => {
  await page.route(`${HUB}**`, route => route.fulfill({ contentType: 'text/html', body: '<title>hub</title>' }));
  await page.goto('/');
  await page.waitForURL(HUB);
});

test('tells crawlers the hub is canonical and not to index this page', async ({ request }) => {
  const html = await (await request.get('/')).text();
  expect(html).toContain(`<link rel="canonical" href="${HUB}">`);
  expect(html).toMatch(/<meta name="robots" content="noindex[^"]*">/);
  expect(html).toContain(`<meta http-equiv="refresh" content="0; url=${HUB}">`);
});

for (const width of [390, 1280]) {
  test(`fallback link is usable at ${width}px`, async ({ page }) => {
    // Hold the redirect so the page itself stays on screen.
    await page.route(`${HUB}**`, () => new Promise(() => {}));
    await page.setViewportSize({ width, height: 900 });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto('/');
    await expect(page.locator('h1')).toBeVisible();
    await expect(page.locator(`a[href="${HUB}"]`).first()).toBeVisible();
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
    expect(overflow, 'page must fit the viewport').toBe(false);
    expect(errors).toEqual([]);
  });
}
