"""
There is a list of most active Stocks on Yahoo Finance [https://finance.yahoo.com/most-active].
You need to compose several sheets based on data about companies from this list.
To fetch data from webpage you can use requests lib. To parse html you can use beautiful soup lib or lxml.
Sheets which are needed:
1. 5 stocks with most youngest CEOs and print sheet to output. You can find CEO info in Profile tab of concrete stock.
    Sheet's fields: Name, Code, Country, Employees, CEO Name, CEO Year Born.
2. 10 stocks with best 52-Week Change. 52-Week Change placed on Statistics tab.
    Sheet's fields: Name, Code, 52-Week Change, Total Cash
3. 10 largest holds of Blackrock Inc. You can find related info on the Holders tab.
    Blackrock Inc is an investment management corporation.
    Sheet's fields: Name, Code, Shares, Date Reported, % Out, Value.
    All fields except first two should be taken from Holders tab.


Example for the first sheet (you need to use same sheet format):
==================================== 5 stocks with most youngest CEOs ===================================
| Name        | Code | Country       | Employees | CEO Name                             | CEO Year Born |
---------------------------------------------------------------------------------------------------------
| Pfizer Inc. | PFE  | United States | 78500     | Dr. Albert Bourla D.V.M., DVM, Ph.D. | 1962          |
...

About sheet format:
- sheet title should be aligned to center
- all columns should be aligned to the left
- empty line after sheet

Write at least 2 tests on your choose.
Links:
    - requests docs: https://docs.python-requests.org/en/latest/
    - beautiful soup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    - lxml docs: https://lxml.de/
"""
import requests
import time
from prettytable import PrettyTable as pt
from bs4 import BeautifulSoup

URL = "https://finance.yahoo.com"
URL_most_active = URL + "/most-active"
headers = {'User-Agent': 'PostmanRuntime/7.30.0', 'Host': 'finance.yahoo.com'}
prePage = requests.get(URL_most_active, headers=headers)
preSoup = BeautifulSoup(prePage.content, "html.parser")
preResults = preSoup.find(id="fin-scr-res-table")

stockAmount = preResults.find("span", class_="Mstart(15px) Fw(500) Fz(s)")
stockAmountNum = stockAmount.text.split()[2]
# TBD
# stockAmountNum = str(70)
print(f"{stockAmountNum} active stocks now!\n")


def profile(d):
    time.sleep(1)
    question_pos = d["URL"].find("?")
    URL_profile_ending = d["URL"][:question_pos] + "/profile" + d["URL"][question_pos:]
    URL_profile = URL + URL_profile_ending

    profile_page = requests.get(URL_profile, headers=headers)
    profile_soup = BeautifulSoup(profile_page.content, "html.parser")

    qsp_profile = profile_soup.find("div", attrs={"data-test": "qsp-profile"})
    employees_table = profile_soup.find("tbody")
    try:
        ceo_row = employees_table.find(
            "td", string=lambda text: "ceo" in text.lower() or "chief exec. officer" in text.lower()
        )
        d["CEO_Name"] = str(ceo_row.previous_sibling.text)
        d["CEO_Year_Born"] = str(ceo_row.next_sibling.next_sibling.next_sibling.text)
        if d["CEO_Year_Born"] == "N/A":
            d["CEO_Year_Born"] = ""
    except AttributeError:
        d["CEO_Name"] = ""
        d["CEO_Year_Born"] = ""
        print(f"stock does not have a CEO: {d}")

    d["Country"] = str(qsp_profile.contents[1].contents[0].contents[4])
    d["Employees"] = str(qsp_profile.contents[1].contents[1].contents[10].text)


time.sleep(5)
page = requests.get(URL_most_active + "?count=" + stockAmountNum, headers=headers)

soup = BeautifulSoup(page.content, "html.parser")

src_tab_rows = soup.find("tbody")

stock_list = []
for src_tab_row in src_tab_rows.contents:
    stock_dict = {}
    stock_dict["URL"] = src_tab_row.find("a")["href"]
    stock_dict["Code"] = src_tab_row.find("a").text.strip()
    stock_dict["Name"] = src_tab_row.find("td", attrs={"aria-label": "Name"}).text.strip()
    profile(stock_dict)  # enriching by Country, Employees, CEO_Name, CEO_Year_Born
    stock_list.append(stock_dict)

five_youngest_ceo = sorted(stock_list, key=lambda x: x["CEO_Year_Born"], reverse=True)[:5]

five_youngest_ceo_table = pt()
# Add headers
five_youngest_ceo_table.title = "5 stocks with most youngest CEOs"
five_youngest_ceo_table.field_names = ["Name", "Code", "Country", "Employees", "CEO Name", "CEO Year Born"]

for row in five_youngest_ceo:
    five_youngest_ceo_table.add_row(
        [row["Name"], row["Code"], row["Country"], row["Employees"], row["CEO_Name"], row["CEO_Year_Born"]])

print(five_youngest_ceo_table)


# /usr/bin/python3 /Users/odruzhinin/git_repos/PYTHON-BASIC/practice/6_web_scraping/stock_info.py
# 243 active stocks now!
#
# stock does not have a CEO: {'URL': '/quote/TEVA?p=TEVA', 'Code': 'TEVA', 'Name': 'Teva Pharmaceutical Industries Limited', 'CEO_Name': '', 'CEO_Year_Born': ''}
# stock does not have a CEO: {'URL': '/quote/SQ?p=SQ', 'Code': 'SQ', 'Name': 'Block, Inc.', 'CEO_Name': '', 'CEO_Year_Born': ''}
# stock does not have a CEO: {'URL': '/quote/UMC?p=UMC', 'Code': 'UMC', 'Name': 'United Microelectronics Corporation', 'CEO_Name': '', 'CEO_Year_Born': ''}
# stock does not have a CEO: {'URL': '/quote/LYG?p=LYG', 'Code': 'LYG', 'Name': 'Lloyds Banking Group plc', 'CEO_Name': '', 'CEO_Year_Born': ''}
# stock does not have a CEO: {'URL': '/quote/DADA?p=DADA', 'Code': 'DADA', 'Name': 'Dada Nexus Limited', 'CEO_Name': '', 'CEO_Year_Born': ''}
# +----------------------------------------------------------------------------------------------------------------------+
# |                                           5 stocks with most youngest CEOs                                           |
# +-------------------------+------+----------------------+-----------+----------------------------------+---------------+
# |           Name          | Code |       Country        | Employees |             CEO Name             | CEO Year Born |
# +-------------------------+------+----------------------+-----------+----------------------------------+---------------+
# |        Snap Inc.        | SNAP |    United States     |   5,661   |       Mr. Evan T. Spiegel        |      1991     |
# |       StoneCo Ltd.      | STNE | George Town KY1-1002 |           |    Mr. Thiago dos Santos Piau    |      1990     |
# | Robinhood Markets, Inc. | HOOD |    United States     |   3,400   |       Mr. Vladimir  Tenev        |      1987     |
# |   Meta Platforms, Inc.  | META |    United States     |   87,314  |    Mr. Mark Elliot Zuckerberg    |      1984     |
# | Rivian Automotive, Inc. | RIVN |    United States     |   10,422  | Mr. Robert Joseph Scaringe Ph.D. |      1984     |
# +-------------------------+------+----------------------+-----------+----------------------------------+---------------+