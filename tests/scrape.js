const puppeteer = require('puppeteer');
const fs = require('fs'); 

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('https://ev-database.org/#group=vehicle-group&rs-pr=10000_100000&rs-er=0_1000&rs-ld=0    _1000&rs-ac=2_23&rs-dcfc=0_400&rs-ub=10_200&rs-tw=0_2500&rs-ef=100_350&rs-sa=-1_5&rs-w=1000_3500&rs-c=0_500    0&rs-y=2010_2030&s=1', {waitUntil: 'networkidle0'}); // Wait for the page to fully load
  const htmlContent = await page.content();
  fs.writeFileSync('page_test_1.html', htmlContent);
  await browser.close();
})();

