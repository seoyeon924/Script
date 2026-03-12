import path from 'node:path';
import { chromium } from 'playwright';
import { CONFIG } from './config.js';
import { appendLog, ensureDir, fileExists, nowStamp, writeLog } from './utils.js';

async function capture(page, name) {
  const stamp = nowStamp();
  const target = path.join(CONFIG.artifactDir, `${stamp}-${name}.png`);
  await page.screenshot({ path: target, fullPage: true });
  return target;
}

async function tryUpload(page, inputPath, logPath) {
  const fileInputs = page.locator('input[type="file"]');
  const count = await fileInputs.count();
  if (count === 0) {
    await appendLog(logPath, 'No file input found on the current page.');
    return false;
  }
  await fileInputs.first().setInputFiles(inputPath);
  await appendLog(logPath, `Attached input file: ${inputPath}`);
  return true;
}

async function clickIfVisible(page, selectors, logPath) {
  for (const selector of selectors) {
    const locator = page.locator(selector).first();
    if (await locator.count()) {
      try {
        await locator.click();
        await appendLog(logPath, `Clicked selector: ${selector}`);
        return true;
      } catch (error) {
        await appendLog(logPath, `Failed clicking selector ${selector}: ${error.message}`);
      }
    }
  }
  return false;
}

async function dumpInteractiveElements(page, logPath, name) {
  const elements = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('button, a, input[type="file"], [role="button"], [data-testid]'))
      .slice(0, 250)
      .map((el) => ({
        tag: el.tagName,
        text: (el.innerText || el.getAttribute('aria-label') || el.getAttribute('title') || '').trim().replace(/\s+/g, ' ').slice(0, 160),
        testid: el.getAttribute('data-testid'),
        href: el.getAttribute('href'),
      }))
      .filter((item) => item.text || item.testid);
  });
  await appendLog(logPath, `${name} interactive elements:\n${JSON.stringify(elements, null, 2)}`);
}

async function main() {
  await ensureDir(CONFIG.artifactDir);
  const logPath = path.join(CONFIG.artifactDir, `${nowStamp()}-tableau-public.log`);
  await writeLog(logPath, 'Starting Tableau Public automation prototype');

  if (!(await fileExists(CONFIG.authStatePath))) {
    throw new Error(`Missing auth state: ${CONFIG.authStatePath}. Run npm run auth first.`);
  }

  if (!(await fileExists(CONFIG.latestInputPath))) {
    throw new Error(`Missing latest input file: ${CONFIG.latestInputPath}`);
  }

  const browser = await chromium.launch({ headless: false, slowMo: 150 });
  const context = await browser.newContext({
    storageState: CONFIG.authStatePath,
    acceptDownloads: true,
  });
  const page = await context.newPage();
  page.setDefaultTimeout(CONFIG.defaultTimeoutMs);

  try {
    await page.goto(CONFIG.tableauCreateUrl, { waitUntil: 'domcontentloaded' });
    await appendLog(logPath, `Opened ${CONFIG.tableauCreateUrl}`);
    await capture(page, 'discover');
    await dumpInteractiveElements(page, logPath, 'discover');

    await clickIfVisible(
      page,
      [
        '[data-testid="CreateLink"]',
        'button:has-text("Create")',
        '[aria-label*="Create"]',
      ],
      logPath
    );
    await page.waitForTimeout(1500);
    await capture(page, 'create-menu');
    await dumpInteractiveElements(page, logPath, 'create-menu');

    const uploaded = await tryUpload(page, CONFIG.latestInputPath, logPath);
    if (!uploaded) {
      await appendLog(logPath, 'Falling back to home page to search for upload controls.');
      await page.goto(CONFIG.tableauPublicHome, { waitUntil: 'domcontentloaded' });
      await capture(page, 'home');
      await dumpInteractiveElements(page, logPath, 'home');
      await tryUpload(page, CONFIG.latestInputPath, logPath);
    }

    await appendLog(
      logPath,
      'Prototype completed. Workbook authoring, chart placement, save, and download steps still need site-specific selectors.'
    );
    await capture(page, 'final-state');
  } finally {
    await context.close();
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
