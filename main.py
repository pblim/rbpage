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
    'Cherub Galaxia': '71',
    'Cronoss Summons Mumu': '71',
    'Demonic Agent Falston': '71',
    'Ereve Deathman': '71',
    'Guardian Hestia': '71',
    'Queen Zyrnna': '71',
    'Ketra Commander Tayr': '71',
    'Blinding Fire Barakiel': '2'
}


def days_hours_minutes(td):
    return td.days, td.seconds // 3600, (td.seconds // 60) % 60

def resp_date():
    converted_to_gmt2

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
    #pprint(rblist_sorted)
    return rblist_sorted


#get_boses()

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
