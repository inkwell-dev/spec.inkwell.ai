const { chromium } = require('/nm/@playwright/test');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file:///out/report.html', { waitUntil: 'load' });
  await page.pdf({
    path: '/out/Inkwell-PFE-Report.pdf', format: 'A4', printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: '<div style="font-size:8pt;width:100%;text-align:center;color:#666">Inkwell.ai — End-of-Studies Project Report · <span class="pageNumber"></span></div>',
    margin: { top: '20mm', bottom: '20mm', left: '22mm', right: '20mm' },
  });
  await browser.close();
})();
