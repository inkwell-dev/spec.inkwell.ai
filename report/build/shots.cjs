const { chromium } = require('/nm/@playwright/test');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  await p.emulateMedia({ media: 'print' });
  await p.goto('file:///out/report.html', { waitUntil: 'load' });
  await p.screenshot({ path: '/out/s1.png' });
  for (const [sel, name] of [['text=Table 2.2 – Functional requirements of the visitor', 's2'], ['text=4.1.4 Realisation', 's3'], ['text=Table 6.2 – Marketplace rules', 's4']]) {
    const el = p.locator(sel).first(); await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(200);
    await p.screenshot({ path: `/out/${name}.png` });
  }
  await b.close();
})();
