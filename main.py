import datetime
from pprint import pprint
from bs4 import BeautifulSoup
from flask import render_template, Flask
from operator import itemgetter
from requests_html import HTMLSession


class Raidboss:

    def __init__(self):

        self.epic_list = {
            'Core': '71',
            'Orfen': '71',
            'Zaken': '83',
            'Queen Ant': '83',
            'Under Queenant Dron': '23',
            'Baium': '119',
            'Antharas1': '167',
            'Valakas': '215',
            'King Tiger Karuta': '95',
            'Uruka': '95',
            'Ocean Flame Ashakiel': '95',
            'Amber': '71',
            'Varka Commnder Mos': '71',
            'Archon Susceptor': '71',
            'Shax The Death Lord': '71',
            'Papurrion Pingolpin': '71',
            'Anima': '71',
            'Cherub Garacsia': '71',
            'Cronoss Summons Mumu': '71',
            'Demonic Agent Falston': '71',
            'Ereve Deathman': '71',
            'Geyser Guardian Hestia': '71',
            'Jeruna Queen': '71',
            'Ketra Commander Tayr': '71',
            'Blinding Fire Barakiel': '2'
        }

    def get_time_left(self, tod, nextresp):
        timeleft = tod + datetime.timedelta(hours=int(nextresp)) - datetime.datetime.now()
        resp_date = str(tod + datetime.timedelta(hours=int(nextresp)))
        return timeleft, resp_date

    def get_boses(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
                   'Cache-Control': 'max-age=0',
                   'Connection': 'keep-alive'}
        cookies = {'BPG': '96ddda0017fe6d958a9df5700e90bb00'}
        session = HTMLSession()
        response = session.get('https://lineage2forever.org/', headers=headers, cookies=cookies, timeout=20)
        print(response.content)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', attrs={'class': 'table'})
        try:
            rows = table.find_all('tr')
        except:
            pass
            # Ye I know :)

        data = []

        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])

        rblist = []

        for lines in data:
            if len(lines) == 3:
                if lines[2] == 'Dead':
                    converted_to_gmt2 = datetime.datetime.strptime(lines[1], '%d/%m/%Y %H:%M') + datetime.timedelta(
                        hours=1)
                    rb_name = lines[0]
                    if rb_name in self.epic_list:
                        timeleft, resp_date = self.get_time_left(converted_to_gmt2, self.epic_list[rb_name])
                    else:
                        timeleft, resp_date = self.get_time_left(converted_to_gmt2, 23)

                    if timeleft <= datetime.timedelta():
                        rblist.append([rb_name, lines[2], 'WINDOW', resp_date])
                    else:
                        timeleft = str(timeleft).split('.', 2)[0]
                        rblist.append([lines[0], lines[2], timeleft, resp_date])
                else:
                    rblist.append([lines[0], lines[2], lines[1], ''])

        rblist_sorted = sorted(rblist, key=itemgetter(3), reverse=False)
        pprint(rblist_sorted)
        return rblist_sorted


boss = Raidboss()
boss.get_boses()

app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html', list_header="RB",
                           rblist=boss.get_boses(), site_title="ATB")


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=False)
