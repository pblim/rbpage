import datetime
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from flask import render_template, Flask
from operator import itemgetter
from apscheduler.schedulers.background import BackgroundScheduler

epic_list = {
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
"""[['Core', 'Alive', '-', ''],
 ['Blinding Fire Barakiel', 'Dead', '0:47:49', '2020-04-05 21:43:00'],
 ['Shax The Death Lord', 'Dead', '16:21:49', '2020-04-06 13:17:00'],
 ['Hallate The Death Lord', 'Dead', '20:50:49', '2020-04-06 17:46:00'],
 ['Golkonda Longhorn', 'Dead', '20:50:49', '2020-04-06 17:46:00'],
 ['Uruka', 'Dead', '21:06:49', '2020-04-06 18:02:00'],
 ['Kernon', 'Dead', '21:11:49', '2020-04-06 18:07:00'],
 ['Under Queenant Dron', 'Dead', '21:19:49', '2020-04-06 18:15:00'],
 ['Domb Death Cabrio', 'Dead', '22:56:49', '2020-04-06 19:52:00'],
 ['King Tiger Karuta', 'Dead', '1 day, 0:38:49', '2020-04-06 21:34:00'],
 ['Antharas1', 'Dead', '1 day, 2:38:49', '2020-04-06 23:34:00'],
 ['Queen Ant', 'Dead', '1 day, 9:42:49', '2020-04-07 06:38:00'],
 ['Zaken', 'Dead', '1 day, 11:07:49', '2020-04-07 08:03:00'],
 ['Jeruna Queen', 'Dead', '1 day, 20:13:49', '2020-04-07 17:09:00'],
 ['Ocean Flame Ashakiel', 'Dead', '1 day, 20:17:49', '2020-04-07 17:13:00'],
 ['Demonic Agent Falston', 'Dead', '1 day, 20:26:49', '2020-04-07 17:22:00'],
 ['Cronoss Summons Mumu', 'Dead', '1 day, 21:25:49', '2020-04-07 18:21:00'],
 ['Geyser Guardian Hestia', 'Dead', '1 day, 21:48:49', '2020-04-07 18:44:00'],
 ['Ereve Deathman', 'Dead', '1 day, 22:09:49', '2020-04-07 19:05:00'],
 ['Amber', 'Dead', '1 day, 22:25:49', '2020-04-07 19:21:00'],
 ['Archon Susceptor', 'Dead', '1 day, 22:27:49', '2020-04-07 19:23:00'],
 ['Varka Commnder Mos', 'Dead', '1 day, 22:27:49', '2020-04-07 19:23:00'],
 ['Ketra Commander Tayr', 'Dead', '1 day, 22:37:49', '2020-04-07 19:33:00'],
 ['Papurrion Pingolpin', 'Dead', '1 day, 23:05:49', '2020-04-07 20:01:00'],
 ['Cherub Garacsia', 'Dead', '1 day, 23:33:49', '2020-04-07 20:29:00'],
 ['Orfen', 'Dead', '2 days, 0:39:49', '2020-04-07 21:35:00'],
 ['Valakas', 'Dead', '2 days, 4:33:49', '2020-04-08 01:29:00'],
 ['Baium', 'Dead', '2 days, 21:58:49', '2020-04-08 18:54:00']]"""


def get_boses():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'}
    cookies = {'atualstudio_language': 'en', 'BPG': '61fe52f4447379ddac4da8ee6cd2690d'}
    response = requests.get('https://lineage2forever.org/', headers=headers, cookies=cookies, timeout=20)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', attrs={'class': 'table'})
    try:
        rows = table.find_all('tr')
    except:
        exit(1)

    data = []

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    # pprint(data)
    rblist = []
    for lines in data:
        if len(lines) == 3:
            if lines[2] == 'Dead':
                converted_to_gmt2 = datetime.datetime.strptime(lines[1], '%d/%m/%Y %H:%M') + datetime.timedelta(hours=1)
                rb_name = lines[0]
                if rb_name in epic_list:
                    resp_date = str(converted_to_gmt2 + datetime.timedelta(hours=int(epic_list[rb_name])))
                    timeleft = converted_to_gmt2 + datetime.timedelta(
                        hours=int(epic_list[rb_name])) - datetime.datetime.now()
                    if timeleft <= datetime.timedelta():
                        rblist.append([lines[0], lines[2], 'WINDOW', resp_date])
                        print(str(lines[0]))
                    else:
                        resp_date = str(converted_to_gmt2 + datetime.timedelta(hours=int(epic_list[rb_name])))
                        t = str(timeleft).split('.', 2)[0]
                        rblist.append([lines[0], lines[2], str(t), resp_date])
                else:
                    resp_date = str(converted_to_gmt2 + datetime.timedelta(hours=23))
                    timeleft = converted_to_gmt2 + datetime.timedelta(hours=23) - datetime.datetime.now()
                    if timeleft <= datetime.timedelta():
                        rblist.append([lines[0], lines[2], 'WINDOW', resp_date])
                    else:
                        t = str(timeleft).split('.', 2)[0]
                        rblist.append([lines[0], lines[2], str(t), resp_date])
                        # print(f'{lines[0]} - {lines[2]} TIMELEFT - {t}')
            else:
                rblist.append([lines[0], lines[2], lines[1], ''])

    rblist_sorted = sorted(rblist, key=itemgetter(3), reverse=False)
    pprint(rblist_sorted)
    return rblist_sorted


# get_boses()

app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html', list_header="RB",
                           rblist=get_boses(), site_title="ATB")


if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
