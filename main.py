import datetime
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from flask import render_template, Flask
from operator import itemgetter

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

"""
['Domb Death Cabrio', 'Alive', '-', ''],
['Under Queenant Dron', 'Dead', 'WINDOW', '2020-04-05 16:56:00'],
['Jeruna Queen', 'Dead', '-1 day, 23:41:09', '2020-04-05 17:09:00'],
['Blinding Fire Barakiel', 'Dead', '0:37:09', '2020-04-05 18:05:00'],
['Geyser Guardian Hestia', 'Dead', '1:16:09', '2020-04-05 18:44:00'],
['Cherub Garacsia', 'Dead', '3:01:09', '2020-04-05 20:29:00'],
['Shax The Death Lord', 'Dead', '19:49:09', '2020-04-06 13:17:00'],
['Hallate The Death Lord', 'Dead', '20:15:09', '2020-04-06 13:43:00'],
['Golkonda Longhorn', 'Dead', '20:16:09', '2020-04-06 13:44:00'],
['Kernon', 'Dead', '20:23:09', '2020-04-06 13:51:00'],
['Uruka', 'Dead', '1 day, 0:34:09', '2020-04-06 18:02:00'],
['King Tiger Karuta', 'Dead', '1 day, 4:06:09', '2020-04-06 21:34:00'],
['Antharas1', 'Dead', '1 day, 6:06:09', '2020-04-06 23:34:00'],
['Queen Ant', 'Dead', '1 day, 13:10:09', '2020-04-07 06:38:00'],
['Zaken', 'Dead', '1 day, 14:35:09', '2020-04-07 08:03:00'],
['Ocean Flame Ashakiel', 'Dead', '1 day, 23:45:09', '2020-04-07 17:13:00'],
['Demonic Agent Falston', 'Dead', '1 day, 23:54:09', '2020-04-07 17:22:00'],
['Cronoss Summons Mumu', 'Dead', '2 days, 0:53:09', '2020-04-07 18:21:00'],
['Ereve Deathman', 'Dead', '2 days, 1:37:09', '2020-04-07 19:05:00'],
['Amber', 'Dead', '2 days, 1:53:09', '2020-04-07 19:21:00'],
['Archon Susceptor', 'Dead', '2 days, 1:55:09', '2020-04-07 19:23:00'],
['Varka Commnder Mos', 'Dead', '2 days, 1:55:09', '2020-04-07 19:23:00'],
['Ketra Commander Tayr', 'Dead', '2 days, 2:05:09', '2020-04-07 19:33:00'],
['Papurrion Pingolpin', 'Dead', '2 days, 2:33:09', '2020-04-07 20:01:00'],
['Orfen', 'Dead', '2 days, 4:07:09', '2020-04-07 21:35:00'],
['Valakas', 'Dead', '2 days, 8:01:09', '2020-04-08 01:29:00'],
['Baium', 'Dead', '3 days, 1:26:09', '2020-04-08 18:54:00']]"""

def get_boses():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'}
    cookies = {'atualstudio_language': 'en', 'BPG': '61fe52f4447379ddac4da8ee6cd2690d'}
    response = requests.get('https://lineage2forever.org/', headers=headers, cookies=cookies)
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
                    else:
                        resp_date = str(converted_to_gmt2 + datetime.timedelta(hours=int(epic_list[rb_name])))
                        t = str(timeleft).split('.', 2)[0]
                        # print(rb_name + " TIMELEFT EPIC " + str(t))
                        rblist.append([lines[0], lines[2], str(t), resp_date])
                else:
                    resp_date = str(converted_to_gmt2 + datetime.timedelta(hours=23))
                    timeleft = converted_to_gmt2 + datetime.timedelta(hours=23) - datetime.datetime.now()
                    t = str(timeleft).split('.', 2)[0]
                    rblist.append([lines[0], lines[2], str(t), resp_date])
                    # print(f'{lines[0]} - {lines[2]} TIMELEFT - {t}')
            else:
                # print(f'{lines[0]} - {lines[1]}')
                rblist.append([lines[0], lines[2], lines[1], ''])

    rblist_sorted = sorted(rblist, key=itemgetter(3), reverse=False)
    pprint(rblist_sorted)
    return rblist_sorted

get_boses()

app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html', list_header="RB",
                           rblist=get_boses(), site_title="ATB")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=False)

'''Core  72 hours +/- 1 hour (retail level no custom drops)
Orfen  72 hours +/- 1 hour (retail level no custom drops)
Zaken  84 hours +/- 1 hour (retail level no custom drops)
Queen Ant  84 hours +/- 1 hour 
Queen Ant DRONE 24 hours +/- 1 hour :fire: NEW RAID BOSS 
Baium  120 hours +/- 1 hour
Antharas  168 hours +/- 1 hour
Valakas   216 hours +/- 1 hour

King Tiger Karuta  -  4 days +/-1 hour respawn time (Drop full Platinum - location PI cave) OPPOSITE SIDE OF SAILREN
:fire: Uruka - 4 days +/-1 hour respawn time (Drop full Platinum - location PI beach) :boom: NEW RETAIL LOCATION
:fire: Ocean Flame Ashakiel   - 4 days +/-1 hour respawn (Drop full Platinum - location near PI Sailren) NEAR SAILREN

Amber    - 3 days +/- 1 hour respawn time (Various drops including Platinum parts) RETAIL LOCATION
Varka Commnder Mos    - 3 days +/- 1 hour respawn time (Various drops including Platinum parts) RETAIL LOCATION
Archon Susceptor    - 3 days +/- 1 hour respawn time (Various drops including Platinum parts) RETAIL LOCATION
Death Lord SHAX    - 3 days +/- 1 hour respawn time (Various drops including Platinum parts) RETAIL LOCATION
Papurrion Pingolpin   - 3 days +/- 1 hour respawn time (Various drops including Platinum parts)  RETAIL LOCATION
Anima27/03/2020
Cherub Galaxia    - 3 days +/- 1 hour respawn time (Various drops including Platinum parts) RETAIL LOCATION
Cronoss Summons Mumu    - 3 days +/- 1 hour respawn time (Various drops including Platinum parts) RETAIL LOCATION
Demonic Agent Falston    - 3 days +/- 1 hour respawn time (Various drops including Platinum parts) RETAIL LOCATION
Ereve Deathman    - 3 days +/- 1 hour respawn time (Various drops including Platinum parts) RETAIL LOCATION
Guardian Hestia    - 3 days +/- 1 hour respawn time (Various drops including Platinum parts) RETAIL LOCATION
Queen Zyrnna    - 3 days +/- 1 hour respawn time (Various drops including Platinum parts) RETAIL LOCATION
Ketra Commander Tayr    - 3 days +/- 1 hour respawn time (Various drops including Platinum parts) RETAIL LOCATION'''
