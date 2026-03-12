import fs from 'node:fs/promises';
import path from 'node:path';

export async function ensureDir(dirPath) {
  await fs.mkdir(dirPath, { recursive: true });
}

export async function writeLog(filePath, content) {
  await ensureDir(path.dirname(filePath));
  await fs.writeFile(filePath, `${content}\n`, 'utf8');
}

export async function appendLog(filePath, content) {
  await ensureDir(path.dirname(filePath));
  await fs.appendFile(filePath, `${content}\n`, 'utf8');
}

export async function fileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

export function nowStamp() {
  return new Date().toISOString().replaceAll(':', '-');
}
