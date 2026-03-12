import fs from 'node:fs/promises';
import path from 'node:path';
import { chromium } from 'playwright';
import { CONFIG } from './config.js';
import { ensureDir, nowStamp } from './utils.js';

async function main() {
  await ensureDir(CONFIG.artifactDir);
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto(CONFIG.tableauPublicHome, { waitUntil: 'networkidle', timeout: 60_000 });

  const stamp = nowStamp();
  const htmlPath = path.join(CONFIG.artifactDir, `${stamp}-discover.html`);
  const jsonPath = path.join(CONFIG.artifactDir, `${stamp}-discover-elements.json`);
  const screenshotPath = path.join(CONFIG.artifactDir, `${stamp}-discover.png`);

  await fs.writeFile(htmlPath, await page.content(), 'utf8');
  await page.screenshot({ path: screenshotPath, fullPage: true });

  const data = await page.evaluate(() => {
    const nodes = Array.from(document.querySelectorAll('button, a, input, [role="button"], [data-testid]'));
    return nodes.slice(0, 500).map((el) => ({
      tag: el.tagName,
      text: (el.innerText || el.getAttribute('aria-label') || el.getAttribute('title') || '').trim().replace(/\s+/g, ' ').slice(0, 200),
      href: el.getAttribute('href'),
      type: el.getAttribute('type'),
      role: el.getAttribute('role'),
      testid: el.getAttribute('data-testid'),
      className: el.className,
      id: el.id,
    }));
  });

  await fs.writeFile(jsonPath, JSON.stringify(data, null, 2), 'utf8');
  console.log(JSON.stringify({ htmlPath, jsonPath, screenshotPath }, null, 2));
  await browser.close();
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
