const { defineConfig } = require('@playwright/test');
module.exports = defineConfig({
  testDir: './tests',
  forbidOnly: !!process.env.CI,
  use: { baseURL: 'http://127.0.0.1:48180', trace: 'retain-on-failure' },
  webServer: { command: 'python3 -m http.server 48180 --bind 127.0.0.1 --directory .', url: 'http://127.0.0.1:48180', reuseExistingServer: false },
});
