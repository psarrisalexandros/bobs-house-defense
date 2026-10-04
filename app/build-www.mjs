/* Builds app/www, the folder that goes inside the native app: the game exactly as it is on the web,
   plus the native layer in front of it. The web version in the repository root is not touched. */
import { cpSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
const here = dirname(fileURLToPath(import.meta.url)), root = join(here, '..'), out = join(here, 'www');
rmSync(out, { recursive: true, force: true }); mkdirSync(out);
for (const f of ['privacy.html', 'terms.html', 'icon-192.png', 'icon-512.png', 'icon-180.png']) cpSync(join(root, f), join(out, f));
for (const f of ['config.js', 'native.js']) cpSync(join(here, 'native', f), join(out, f));
cpSync(join(here, 'node_modules', '@capacitor', 'core', 'dist', 'capacitor.js'), join(out, 'capacitor.js'));
let html = readFileSync(join(root, 'index.html'), 'utf8');
const sw = `<script>if('serviceWorker' in navigator)navigator.serviceWorker.register('sw.js').catch(()=>{});</script>`;
if (!html.includes(sw)) throw new Error('service worker line not found in index.html');
html = html.replace(sw, '');                                   /* the app carries its own files; no web cache needed */
html = html.replace(/<link rel="manifest"[^>]*>\s*/, '');
const tag = '<script src="capacitor.js"></script>\n<script src="config.js"></script>\n<script src="native.js"></script>\n';
const at = html.indexOf('<script>');
if (at < 0) throw new Error('game script not found in index.html');
html = html.slice(0, at) + tag + html.slice(at);
writeFileSync(join(out, 'index.html'), html);
console.log('www built:', html.length, 'bytes');
