import requests
from os.path import join, exists
from pathlib import Path

# from - https://www.bbc.com/mediacentre/speeches/
# Array.prototype.slice.call(document.getElementsByClassName('link')).map(a => a.href)
links = ['https://www.bbc.com/mediacentre/speeches/2022/liliane-landor-global-conference-for-media-freedom',
         'https://www.bbc.com/mediacentre/speeches/2021/richard-sharp-vlv',
         'https://www.bbc.com/mediacentre/speeches/2021/richard-sharp-rts-cambridge',
         'https://www.bbc.com/mediacentre/speeches/2021/westminster-media-forum-the-future-of-news',
         'https://www.bbc.com/mediacentre/speeches/2021/rhodri-talfan-davies-westminster-media-forum-april',
         'https://www.bbc.com/mediacentre/speeches/2021/across-the-uk',
         'https://www.bbc.com/mediacentre/speeches/2021/clare-sumner-the-future-of-the-bbc',
         'https://www.bbc.com/mediacentre/speeches/2020/jonathan-wall-radio-festival-keynote',
         'https://www.bbc.com/mediacentre/speeches/2020/a-roadmap-for-reform',
         'https://www.bbc.com/mediacentre/speeches/jamie-angus-yleisradio-bbc-finnish',
         'https://www.bbc.com/mediacentre/speeches/2020/fran-unsworth-ebu',
         'https://www.bbc.com/mediacentre/speeches/2020/tim-davie-intro-speech',
         'https://www.bbc.com/mediacentre/speeches/2020/tony-hall-edinburgh',
         'https://www.bbc.com/mediacentre/speeches/2020/trust-in-the-age-of-disruption',
         'https://www.bbc.com/mediacentre/speeches/2020/david-clementi-salford',
         'https://www.bbc.com/mediacentre/speeches/2020/james-purnell-abo',
         'https://www.bbc.com/mediacentre/speeches/2020/tony-hall-new-year',
         'https://www.bbc.com/mediacentre/speeches/2019/clementi-vlv',
         'https://www.bbc.com/mediacentre/speeches/2019/ken-macquarrie-belfast',
         'https://www.bbc.com/mediacentre/speeches/2019/charlotte-moore-iplayer',
         'https://www.bbc.com/mediacentre/speeches/2019/tony-hall-rts',
         'https://www.bbc.com/mediacentre/speeches/2019/tony-hall-fco',
         'https://www.bbc.com/mediacentre/speeches/2019/tony-hall-ara',
         'https://www.bbc.com/mediacentre/speeches/david-clementi-ara',
         'https://www.bbc.com/mediacentre/speeches/2019/james-purnell-education-festival',
         'https://www.bbc.com/mediacentre/speeches/2019/james-purnell-radio-festival',
         'https://www.bbc.com/mediacentre/speeches/2019/tony-hall-lords',
         'https://www.bbc.com/mediacentre/speeches/2019/clementi-omc',
         'https://www.bbc.com/mediacentre/speeches/2019/tony-hall-ou',
         'https://www.bbc.com/mediacentre/speeches/2019/tony-hall-media-telecoms',
         'https://www.bbc.com/mediacentre/speeches/2019/tony-hall-bbc-scotland-channel-launch',
         'https://www.bbc.com/mediacentre/speeches/2019/alison-kirkham',
         'https://www.bbc.com/mediacentre/speeches/tim-davie-vlv-2018',
         'https://www.bbc.com/mediacentre/speeches/tony-hall-news-xchange-2018',
         'https://www.bbc.com/mediacentre/speeches/2018/tony-hall-pbi-seoul',
         'https://www.bbc.com/mediacentre/speeches/2018/charlotte-moore-steve-hewlett',
         'https://www.bbc.com/mediacentre/speeches/2018/tony-hall-occ',
         'https://www.bbc.com/mediacentre/speeches/2018/tony-hall-soe',
         'https://www.bbc.com/mediacentre/speeches/2018/tony-hall-rts',
         'https://www.bbc.com/mediacentre/speeches/2018/david-clementi-annual-report',
         'https://www.bbc.com/mediacentre/speeches/2018/tony-hall-ara-2017-18',
         'https://www.bbc.com/mediacentre/speeches/tony-hall-staff-inclusion',
         'https://www.bbc.com/mediacentre/speeches/2018/james-purnell-ebu',
         'https://www.bbc.com/mediacentre/speeches/2018/tony-hall-prominence',
         'https://www.bbc.com/mediacentre/speeches/2018/tony-hall-prospect-national-conference',
         'https://www.bbc.com/mediacentre/speeches/2018/bob-shennan-radio-academy',
         'https://www.bbc.com/mediacentre/speeches/2018/matthew-postgate',
         'https://www.bbc.com/mediacentre/speeches/2018/patrick-holland-bbc-two-season',
         'https://www.bbc.com/mediacentre/speeches/2018/david-clementi-vlv',
         'https://www.bbc.com/mediacentre/speeches/2018/tony-hall-annual-plan',
         'https://www.bbc.com/mediacentre/speeches/2018/radiodays-bob-shennan',
         'https://www.bbc.com/mediacentre/speeches/2018/anne-bulford-enders',
         'https://www.bbc.com/mediacentre/speeches/2018/alan-davey-abo',
         'https://www.bbc.com/mediacentre/speeches/2017/tony-hall-own-it',
         'https://www.bbc.com/mediacentre/speeches/2017/james-purnell-vlv',
         'https://www.bbc.com/mediacentre/speeches/2017/tony-hall-local-radio',
         'https://www.bbc.com/mediacentre/speeches/2017/donalda-mackinnon-angus-macleod',
         'https://www.bbc.com/mediacentre/speeches/2017/tony-hall-roscoe',
         'https://www.bbc.com/mediacentre/speeches/2017/david-clementi-cambridge',
         'https://www.bbc.com/mediacentre/speeches/2017/tony-hall-autumn-priorities',
         'https://www.bbc.com/mediacentre/speeches/2017/david-clementi-annual-report',
         'https://www.bbc.com/mediacentre/speeches/2017/matthew-postgate-ai',
         'https://www.bbc.com/mediacentre/speeches/2017/david-clementi-annual-plan',
         'https://www.bbc.com/mediacentre/speeches/2017/tony-hall-annual-plan',
         'https://www.bbc.com/mediacentre/speeches/2017/alison-kirkham-factual-tv-launch-may-2017',
         'https://www.bbc.com/mediacentre/speeches/2017/anne-bulford-dtg-summit',
         'https://www.bbc.com/mediacentre/speeches/2017/piers-wenger',
         'https://www.bbc.com/mediacentre/speeches/2017/tony-hall-tomorrows-world',
         'https://www.bbc.com/mediacentre/speeches/2017/fran-unsworth-vlv',
         'https://www.bbc.com/mediacentre/speeches/2017/tony-hall-culture-uk',
         'https://www.bbc.com/mediacentre/speeches/2017/radiodays-bob-shennan',
         'https://www.bbc.com/mediacentre/speeches/2017/anne-bulford-media-telecoms-conference',
         'https://www.bbc.com/mediacentre/speeches/2017/tony-hall-diversity-fair-access',
         'https://www.bbc.com/mediacentre/speeches/2017/james-purnell-speaker',
         'https://www.bbc.com/mediacentre/speeches/2017/alan-davey-abo',
         'https://www.bbc.com/mediacentre/speeches/2017/tony-hall-ny-message',
         'https://www.bbc.com/mediacentre/speeches/2016/james-heath-wmf',
         'https://www.bbc.com/mediacentre/speeches/2016/tony-hall-vlv',
         'https://www.bbc.com/mediacentre/speeches/2016/annual-report-2015-16',
         'https://www.bbc.com/mediacentre/speeches/2016/charlotte-moore-vlv',
         'https://www.bbc.com/mediacentre/speeches/2016/james-heath-westminster',
         'https://www.bbc.com/mediacentre/speeches/2016/helen-boaden-radiodays',
         'https://www.bbc.com/mediacentre/speeches/2016/tony-hall-enders',
         'https://www.bbc.com/mediacentre/speeches/2016/charlotte-moore-vision',
         'https://www.bbc.com/mediacentre/speeches/2016/alan-davey-abo',
         'https://www.bbc.com/mediacentre/speeches/2015/alan-davey-vlv',
         'https://www.bbc.com/mediacentre/speeches/2015/mark-linsey-press-launch',
         'https://www.bbc.com/mediacentre/speeches/2015/tony-hall-cardiff',
         'https://www.bbc.com/mediacentre/speeches/2015/jonty-claypole',
         'https://www.bbc.com/mediacentre/speeches/robin-pembrooke-iptc',
         'https://www.bbc.com/mediacentre/speeches/2015/bbc-music-john-peel-lecture',
         'https://www.bbc.com/mediacentre/speeches/2015/iansmall-bbccharter',
         'https://www.bbc.com/mediacentre/speeches/2015/alice-webb-childrens-vision',
         'https://www.bbc.com/mediacentre/speeches/2015/tony-hall-cif',
         'https://www.bbc.com/mediacentre/speeches/2015/tony-hall-rts',
         'https://www.bbc.com/mediacentre/speeches/2015/fran-unsworth-ibc-forum',
         'https://www.bbc.com/mediacentre/speeches/2015/tony-hall-distinctive-bbc',
         'https://www.bbc.com/mediacentre/speeches/2015/eisteddfod-speech',
         'https://www.bbc.com/mediacentre/speeches/2015/case-for-welsh-language-broadcasting',
         'https://www.bbc.com/mediacentre/speeches/2015/helen-boaden-rig']

if __name__ == '__main__':
    i = 0
    if not exists(join('.', 'downloaded_html')):
        Path(join('.', 'downloaded_html')).mkdir(exist_ok=True)
    Path('index.txt').touch()
    with open('index.txt', 'w') as index:
        for link in links:
            i += 1
            print(i)
            filename = join('.', 'downloaded_html', f'{str(i)}.html')
            Path(filename).touch()
            response = requests.get(link)
            with open(filename, 'wb') as html:
                html.write(response.content)
            index.write(f'{i} {link}\n')
    print('done')
