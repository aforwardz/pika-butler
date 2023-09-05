import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil import parser
import traceback


ZHIBOBA_MATCH_URL = "https://www.zhiboba.fun/zuqiujijin/"

MATCH_DETAIL_PAGE = "https://www.dongqiudi.com/liveDetail/{mid}"


class MatchDay(object):
    MAIN_TEAM = '迈阿密国际'
    FOCUS_TEAMS = {
        '英超': ['曼城', '曼联', '阿森纳', '利物浦', '切尔西', '布莱顿', '热刺', '纽卡', '维拉'],
        '西甲': ['巴塞罗那', '巴萨', '皇家马德里', '皇马', '马德里竞技', '马竞'],
        '德甲': ['拜仁', '多特', '柏林'],
        '意甲': ['米兰'],
        '法甲': ['巴黎'],
        '欧冠': ['*'],
    }

    def __init__(self):
        self.today = datetime(2023, 9, 4).date() # datetime.today().date()

    def handle(self):
        pass

    def search_dqd_matches(self, url):
        cookie = {"dqduid": "rBUEB2TnEWccaiM1FrDmAg==; Hm_lvt_335923ce349a3b7756120f8e8fbfa3d6=1692864971; Hm_lpvt_335923ce349a3b7756120f8e8fbfa3d6=1692868001"}

        headers = {"Accept": "application/json, text/plain, */*", "Host": "www.dongqiudi.com",
                   "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}

        try:
            matches = requests.get(url, headers=headers, cookies=cookie).json()
            matches = matches.get('content', {}).get('matches', [])
        except:
            matches = []

        matches = [m for m in matches if m.get('status', '') == 'Played']

        for m in matches:
            match_id = m.get('match_id')
            if not match_id:
                continue
            match_url = MATCH_DETAIL_PAGE.format(mid=match_id)

            highlight_desc = ""
            try:
                dp = requests.get(match_url, headers=headers, cookies=cookie)
                soup = BeautifulSoup(dp.content, 'html.parser')
                highlights = soup.find_all(attrs={"class": 'brilliant-moment'})[0]
                highlights = [h.text.strip() for h in highlights.find_all(attrs={"target": '_blank'})]
                highlights.reverse()
                highlight_desc = self._highlight_naturalize(highlights)
            except Exception as e:
                print(e)

    def _match_result_naturalize(self, match):
        pass

    def _highlight_naturalize(self, hls):
        res = []

        for hl in hls:
            nl, td = "", ""
            hl = hl.strip()
            hl = [h for h in hl.split(' ') if h]

            if len(hl) > 1 and hl[0].endswith("'"):
                mt = hl[0].strip("'")
                if "+" in mt:
                    half, extra = mt.split('+')
                    td = ("上半场" if half == '45' else "下半场") + "补时第{}分钟".format(extra)
                else:
                    td = "第{}分钟".format(mt)

                nl = "{td}， {hl}".format(td=td, hl=hl[1])
            else:
                nl = "{hl}".format(hl=hl[1])

            res.append(nl)

        return "比赛开始，{}。".format(";\n".join(res) if res else "")

    def is_focus_match(self, title):
        if not title:
            return False

        for league, teams in self.FOCUS_TEAMS.items():
            if league in title:
                if league == '欧冠':
                    teams = [t for ft in self.FOCUS_TEAMS.values() for t in ft]
                for t in teams:
                    if t in title:
                        return True

        if self.MAIN_TEAM in title:
            return True

        return False

    def search_zhiboba_matches(self, url):
        ZHIBOBA_PREFIX = "https://www.zhiboba.fun"
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}

        match_records = []
        try:
            ml = requests.get(url, headers=headers)
            if ml.status_code == 200 and ml.content:
                soup = BeautifulSoup(ml.content, 'html.parser')
                matches = soup.find(attrs={"class": 'wz'})
                if matches:
                    for match in matches.find_all('li'):
                        # print(match)
                        s = match.find('span')
                        s = s.text if s else ''
                        if not s:
                            continue
                        mt = parser.parse(s)
                        et = datetime(self.today.year, self.today.month, self.today.day, 9, 0)
                        bt = et - timedelta(hours=14)
                        if not (bt <= mt <= et):
                            continue
                        a = match.find('a')
                        link = a.attrs.get('href', '') if a else ''
                        title = a.text if a else ''
                        if not link or not title:
                            continue
                        if not self.is_focus_match(title):
                            continue
                        title = title.strip().replace('全场集锦', '').strip()
                        print(s, link, title)
                        match_records.append({'time': str(mt), 'link': ZHIBOBA_PREFIX + link, 'title': title})
        except Exception as e:
            print(e)

        match_records.reverse()
        # get highlights
        for match in match_records:
            try:
                match['highlights'] = []
                dp = requests.get(match.get('link'), headers=headers)
                if dp.status_code == 200 and dp.content:
                    soup = BeautifulSoup(dp.content, 'html.parser')
                    content = soup.find(id='wzContent')
                    if content:
                        for p in content.find_all('p'):
                            hl = p.find('strong')
                            if hl:
                                hl = hl.text.strip().strip('↓')
                                if not hl or hl.startswith('【'):
                                    continue
                                match['highlights'].append(hl)
            except Exception as e:
                traceback.print_exc()
                print(e)

        with open('../temp/match_day_%s.json' % self.today.strftime('%Y%m%d'), 'w', encoding='utf-8') as f:
            json.dump(match_records, f)

        return match_records


if __name__ == '__main__':
    # ch_options = Options()
    # ch_options.add_argument("--headless")
    # driver = webdriver.Chrome(options=ch_options)
    # driver.get("https://www.zhiboba.fun/zuqiujijin/156177.html")
    #
    # try:
    #     WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located((By.ID, 'wzContent')))
    #     print(driver.page_source)
    # finally:
    #     driver.close()

    md = MatchDay()
    records = md.search_zhiboba_matches(ZHIBOBA_MATCH_URL)
    print(records)



