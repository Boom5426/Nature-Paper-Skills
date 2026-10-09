/** Rebuild the original social cards. No remote assets or model calls. */
import { chromium } from '@playwright/test';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';
const browser = await chromium.launch({
  ...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE ? { executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE } : {}),
  args: ['--no-sandbox'],
});
try {
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  await mkdir('public', { recursive: true });
  for (const [locale, headline, accent, description] of [
    ['en', 'Better arguments.', 'Clearer papers.', 'An open-source scientific writing workflow for your AI agent.'],
    ['zh', '把研究写清楚，', '让证据说话。', '从科学论证、论文图表到投稿与返修的开源 AI 工作流。'],
  ]) {
    await page.setContent(`<!doctype html><html lang="${locale}"><meta charset="utf-8"><style>
      *{box-sizing:border-box}body{margin:0;background:#f6f5f1;color:#1f2c43;font-family:Arial,'Noto Sans CJK SC',sans-serif;padding:52px 64px;width:1200px;height:630px;overflow:hidden}
      .brand{display:flex;align-items:center;gap:18px;font-weight:700;font-size:27px}.icon{width:44px;height:48px;border:3px solid #66509c;border-radius:6px;display:grid;place-items:center;color:#66509c;font-size:30px}
      .kicker{margin-top:58px;color:#685393;font-size:15px;letter-spacing:2px;font-weight:700}.headline{position:relative;z-index:2;font:70px/1.12 Georgia,'Noto Serif CJK SC',serif;letter-spacing:-2px;margin:24px 0 20px;max-width:760px}.headline em{color:#66509c;font-weight:400}p{font-size:23px;line-height:1.55;max-width:710px;color:#4d5b6c}
      .paper{position:absolute;right:62px;top:220px;width:225px;height:275px;background:white;border:1px solid #d9d6e0;border-radius:10px;padding:27px;transform:rotate(5deg);box-shadow:0 18px 45px #28365114}.paper span{display:block;background:#dce1e7;height:7px;margin:13px 0;border-radius:3px}.paper .claim{background:#eae4f3;color:#66509c;font-size:13px;padding:15px 10px;margin-top:24px}.foot{position:absolute;bottom:35px;left:64px;font-size:15px;letter-spacing:1px;color:#647082}
      </style><div class="brand"><div class="icon">✓</div>Nature Paper Skills</div><div class="kicker">SCIENCE FIRST. SENTENCE SECOND.</div><h1 class="headline">${headline}<br><em>${accent}</em></h1><p>${description}</p><div class="paper" aria-hidden="true"><strong>RESULTS</strong><span></span><span></span><span style="width:70%"></span><div class="claim">Claim ↔ Evidence</div><span></span><span style="width:65%"></span></div><div class="foot">CODEX · CLAUDE CODE · OPEN SOURCE</div></html>`, { waitUntil: 'load' });
    await page.screenshot({ path: path.resolve('public', `og-${locale}.png`) });
  }
} finally { await browser.close(); }
console.log('Generated original English and Chinese 1200×630 social cards.');
