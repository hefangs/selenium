const { Builder, Key, By, until } = require('selenium-webdriver')
const { expect } = require('chai')
describe('Login page tests - Basic', function () {
  this.timeout(50000)
  let driver
  it('01', async () => {
    driver = await new Builder().forBrowser('chrome').build()
    await driver.get('https://www.baidu.com')
    const searchBox = await driver.findElement(By.id('kw'))
    await searchBox.sendKeys('selenium')
    const dropdownOption = await driver.wait(
      until.elementLocated(By.xpath('//*[@id="form"]/div/ul/li[5]')),
      3000
    )
    await dropdownOption.click()
    // 提交搜索
    await searchBox.sendKeys(Key.RETURN)
    const resultLink = await driver.wait(
      until.elementLocated(By.xpath('//*[@id="2"]/div/div[1]/h3/a')),
      3000
    )
    await resultLink.click()
    await driver.sleep(4000)
    await driver.quit()
  })
})
