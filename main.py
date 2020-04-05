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
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=False)
