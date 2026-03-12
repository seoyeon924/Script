import { chromium } from 'playwright';
import { CONFIG } from './config.js';
import { ensureDir } from './utils.js';

async function main() {
  await ensureDir(new URL('../.auth/', import.meta.url).pathname);
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  console.log('Opening Tableau Public. Log in manually, then press Enter in this terminal.');
  await page.goto(CONFIG.tableauPublicHome, { waitUntil: 'domcontentloaded' });

  process.stdin.setEncoding('utf8');
  await new Promise((resolve) => {
    process.stdin.once('data', () => resolve());
  });

  await context.storageState({ path: CONFIG.authStatePath });
  console.log(`Saved auth state to ${CONFIG.authStatePath}`);
  await browser.close();
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
