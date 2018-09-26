from requests_html import HTMLSession
session = HTMLSession()
r = session.get("http://money.finance.sina.com.cn/corp/go.php/" +
                      "vMS_MarketHistory/stockid/601006.phtml?year=2018&jidu=2")
table = r.html.xpath("//*[@id='FundHoldSharesTable']")[0]
trArray = table.xpath("//tr")
trArray = trArray[2:len(trArray)]
gpList = list()
for tr in trArray:
    gp = list()
    for td in tr.xpath("//td"):
        gp.append(td.text)
    gpList.append(gp)
for gp in gpList:
    print(gp)




