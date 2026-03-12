import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const root = path.resolve(__dirname, '../../../');

export const CONFIG = {
  root,
  authStatePath: path.resolve(root, 'automation/tableau-public/.auth/tableau-public.json'),
  artifactDir: path.resolve(root, 'automation/tableau-public/artifacts'),
  latestInputPath: path.resolve(root, 'runs/latest/input/sample_sales.csv'),
  tableauPublicHome: 'https://public.tableau.com/',
  tableauPublicProfile: 'https://public.tableau.com/app/profile/',
  tableauCreateUrl: 'https://public.tableau.com/app/discover',
  defaultTimeoutMs: 30_000,
};
