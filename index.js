
// const puppeteer = require('puppeteer');
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
  fs.unlinkSync('file.json')
  fs.appendFileSync('file.json', "[");
  for (var i = 1; i < 100; i++) {
    await page.goto('https://marketplace.wanakafarm.com/#/lands/'+i.toString());
    await page.waitFor(3000);
    let data = await page.evaluate(() => {
      j = document.getElementsByTagName("span")[4].innerText || 0;
      if (j != 0) {j = 2}
        cofre = document.getElementsByTagName("div")[56].innerText;
        if (cofre.search("__") > -1) {
            land = {
              id: document.getElementsByTagName("div")[23+j].innerText,
              Name : document.getElementsByTagName("div")[37+j].innerText,
              Enviroment : document.getElementsByTagName("div")[42+j].innerText,
              Birth : "-",
              Seasons : "-",
              Level : "-",
              Increase_Mutant_Rate : "-",
              Description : document.getElementsByTagName("div")[84+j].innerText,
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
            id: document.getElementsByTagName("div")[23+j].innerText,
            Name : document.getElementsByTagName("div")[41+j].innerText,
            Enviroment : document.getElementsByTagName("div")[46+j].innerText,
            Birth : document.getElementsByTagName("div")[65+j].innerText,
            Seasons : document.getElementsByTagName("div")[70+j].innerText[0],
            Level : document.getElementsByTagName("div")[75+j].innerText,
            Increase_Mutant_Rate : document.getElementsByTagName("div")[80+j].innerText,
            Description : document.getElementsByTagName("div")[88+j].innerText,
            Rare : document.getElementsByTagName("div")[60+j].innerText,
            Time_Reduce: document.getElementsByTagName("div")[85+j].innerText,
            PriceWana: document.getElementsByTagName("span")[4].innerText || 0,
            Owner: document.getElementsByTagName("a")[2].innerText,
            sprint : document.getElementsByTagName("img")[4+(j/2)].className.search('active') > 0 || 0,
            summer : document.getElementsByTagName("img")[5+(j/2)].className.search('active') > 0 || 0,
            autumn : document.getElementsByTagName("img")[6+(j/2)].className.search('active') > 0 || 0,
            winter : document.getElementsByTagName("img")[7+(j/2)].className.search('active') > 0 || 0,
          }
        }
      return land
    });
    
    // lands.push(data);
    
    if (i < 99) {
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