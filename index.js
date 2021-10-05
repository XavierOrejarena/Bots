
// const puppeteer = require('../sample_puppeteer/puppeteer');
const puppeteer = require('../sample_puppeteer/node_modules/puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: true,args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({
    width: 1280,
    height: 720,
    deviceScaleFactor: 1,
  });
  const lands = [];
  const fs = require('fs');
  fs.appendFileSync('file.json', "[");
  for (var i = 1; i < 15001; i++) {
    await page.goto('https://marketplace.wanakafarm.com/#/lands/'+i.toString());
    await page.waitFor(3000);
    let data = await page.evaluate(() => {
      i = document.getElementsByTagName("span")[4].innerText || 0;
      if (i != 0) {i = 2}

        if (document.getElementsByTagName("div")[56].innerText == "__") {
            land = {
              id: document.getElementsByTagName("div")[23].innerText,
              Name : document.getElementsByTagName("div")[37].innerText,
              Enviroment : document.getElementsByTagName("div")[42].innerText,
              Birth : "-",
              Seasons : "-",
              Level : "-",
              Increase_Mutant_Rate : "-",
              Description : document.getElementsByTagName("div")[84].innerText,
              Rare : "-",
              Time_Reduce: "-",
              PriceWana: document.getElementsByTagName("span")[4].innerText || 0,
              Owner: document.getElementsByTagName("a")[2].innerText,
              sprint : "-",
              summer : "-",
              autumn : "-",
              winter : "-",
            }
        }else {
          land = {
            id: document.getElementsByTagName("div")[23+i].innerText,
            Name : document.getElementsByTagName("div")[41+i].innerText,
            Enviroment : document.getElementsByTagName("div")[46+i].innerText,
            Birth : document.getElementsByTagName("div")[65+i].innerText,
            Seasons : document.getElementsByTagName("div")[70+i].innerText[0],
            Level : document.getElementsByTagName("div")[75+i].innerText,
            Increase_Mutant_Rate : document.getElementsByTagName("div")[80+i].innerText,
            Description : document.getElementsByTagName("div")[88+i].innerText,
            Rare : document.getElementsByTagName("div")[60+i].innerText,
            Time_Reduce: document.getElementsByTagName("div")[85+i].innerText,
            PriceWana: document.getElementsByTagName("span")[4].innerText || 0,
            Owner: document.getElementsByTagName("a")[2].innerText,
            sprint : document.getElementsByTagName("img")[4+(i/2)].className.search('active') > 0 || 0,
            summer : document.getElementsByTagName("img")[5+(i/2)].className.search('active') > 0 || 0,
            autumn : document.getElementsByTagName("img")[6+(i/2)].className.search('active') > 0 || 0,
            winter : document.getElementsByTagName("img")[7+(i/2)].className.search('active') > 0 || 0,
          }
        }
      return land
    });
    
    // lands.push(data);
    
    if (i < 15000) {
      fs.appendFileSync('file.json', JSON.stringify(data)+",");
    } else {
      fs.appendFileSync('file.json', JSON.stringify(data));
    }
    // await console.log(data);
  }
  fs.appendFileSync('file.json', "]");
  // fs.writeFileSync('file.json', JSON.stringify(lands));
  // await console.log(lands);
  await browser.close();
})();