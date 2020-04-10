import datetime
from operator import itemgetter
from pprint import pprint
from bs4 import BeautifulSoup
from flask import render_template, Flask
from requests_html import HTMLSession


class Raidboss:

    def __init__(self):

        self.custom_list = {
            'Under Queenant Dron': '1380',
            'King Tiger Karuta': '5700',
            'Uruka': '5700',
            'Ocean Flame Ashakiel': '5700',
            'Amber': '4260',
            'Varka Commnder Mos': '4260',
            'Archon Susceptor': '4260',
            'Shax The Death Lord': '4260',
            'Papurrion Pingolpin': '4260',
            'Cherub Garacsia': '4260',
            'Cronoss Summons Mumu': '4260',
            'Demonic Agent Falston': '4260',
            'Ereve Deathman': '4260',
            'Geyser Guardian Hestia': '4260',
            'Jeruna Queen': '4260',
            'Ketra Commander Tayr': '4260',
            'Blinding Fire Barakiel': '120',
            'Hallate The Death Lord': '120',
            'Kernon': '120',
            'Golkonda Longhorn': '120',
            'Domb Death Cabrio': '120'
        }

        self.epic_list = {
            'Core': '4290',
            'Orfen': '4290',
            'Zaken': '5010',
            'Queen Ant': '5010',
            'Baium': '7170',
            'Antharas1': '10050',
            'Valakas': '12930'
        }

        self.drop_list = {
            'King Tiger Karuta': 'Heavy Plat set',
            'Uruka': 'Robe/Light Plat set',
            'Ocean Flame Ashakiel': 'Light plat set',
            'Amber': 'Light helmet',
            'Varka Commnder Mos': 'Robe helmet',
            'Archon Susceptor': 'Robe gloves',
            'Cherub Garacsia': 'Light gloves',
            'Cronoss Summons Mumu': 'Heavy gloves',
            'Demonic Agent Falston': 'Light main',
            'Ereve Deathman': 'Robe main',
            'Geyser Guardian Hestia': 'Light boots',
            'Jeruna Queen': 'Heavy helmet',
            'Ketra Commander Tayr': 'Heavy main',
            'Shax The Death Lord': 'Robe boots'
        }

    def get_time_left(self, tod, nextresp):
        timeleft = tod + datetime.timedelta(minutes=int(nextresp)) - datetime.datetime.now()
        resp_date = str(tod + datetime.timedelta(minutes=int(nextresp)))
        return timeleft, resp_date

    def get_window_time_left(self, resp_date, rb_name):
        if rb_name in self.epic_list:
            window_interval = 30
        else:
            window_interval = 60

        window_end = datetime.datetime.strptime(resp_date, '%Y-%m-%d %H:%M:%S') \
                                                + datetime.timedelta(minutes=window_interval)

        if window_end > datetime.datetime.now():
            windows_left = window_end - datetime.datetime.now()
        else:
            windows_left = datetime.datetime.now() - window_end
        windows_left = str(windows_left).split('.', 2)[0]
        # print("RB " + str(rb_name) + " R%ESP DATE " + str(
        #     datetime.datetime.strptime(resp_date, '%Y-%m-%d %H:%M:%S')) + " NOW "
        #       + str(datetime.datetime.now()) + " LEFTE " + str(windows_left) + " WINDOW END " + str(window_end))
        return windows_left

    def get_boses(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
                   'Cache-Control': 'max-age=0',
                   'Connection': 'keep-alive'}
        cookies = {'BPG': 'd22de90cf34137d3ca19812e9467eada'}
        session = HTMLSession()
        response = session.get('https://lineage2forever.org/', headers=headers, cookies=cookies, timeout=90)
        # pprint(response.content)
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
                rb_name = lines[0]

                if rb_name == 'Antharas1':
                    lines[1] = '07/04/2020 00:20'
                    lines[2] = 'Dead'

                if rb_name in self.drop_list:
                    drop = self.drop_list[rb_name]
                else:
                    drop = ''

                if lines[2] == 'Dead':
                    converted_to_gmt2 = datetime.datetime.strptime(lines[1], '%d/%m/%Y %H:%M') + datetime.timedelta(
                        hours=1)
                    if rb_name in self.epic_list:
                        timeleft, resp_date = self.get_time_left(converted_to_gmt2, self.epic_list[rb_name])
                    elif rb_name in self.custom_list:
                        timeleft, resp_date = self.get_time_left(converted_to_gmt2, self.custom_list[rb_name])
                    else:
                        timeleft, resp_date = self.get_time_left(converted_to_gmt2, 1380)

                    if timeleft <= datetime.timedelta():
                        in_window_time_left = self.get_window_time_left(resp_date, rb_name)
                        rblist.append([rb_name, lines[2],
                                       'WINDOW ' + str(in_window_time_left) + ' left',
                                       resp_date,
                                       drop])
                    else:
                        timeleft = str(timeleft).split('.', 2)[0]
                        rblist.append([lines[0], lines[2], timeleft, resp_date, drop])
                else:
                    rblist.append([lines[0], lines[2], lines[1], '', drop])

        rblist_sorted = sorted(rblist, key=itemgetter(3), reverse=False)
        # pprint(rblist_sorted)
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
