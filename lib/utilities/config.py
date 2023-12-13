####################################################################################################

import nextcord

####################################################################################################

from lib.utilities.SomiBot import SomiBot



TEXT_CHANNELS = [
    nextcord.ChannelType.text,
    nextcord.ChannelType.news,
    nextcord.ChannelType.public_thread,
    nextcord.ChannelType.news_thread,
    nextcord.ChannelType.private_thread
]

LASTFM_TIMEFRAMES = {
    "Past Week": "7day",
    "Past Month": "1month",
    "Past Quarter": "3month",
    "Past Half a Year": "6month",
    "Past Year": "12month",
    "All Time": "overall"
}

LASTFM_TIMEFRAMES_TEXT = {
    "7day": "of the past week:",
    "1month": "of the past month:",
    "3month": "of the past quarter:",
    "6month": "of the past half a year:",
    "12month": "of the past year:",
    "overall": "of all time:"
}

LASTFM_TIMEFRAMES_WEBSCRAPING = {
    "Past Week": "LAST_7_DAYS",
    "Past Month": "LAST_30_DAYS",
    "Past Quarter": "LAST_90_DAYS",
    "Past Half a Year": "LAST_180_DAYS",
    "Past Year": "LAST_365_DAYS",
    "All Time": "ALL"
}

LASTFM_TIMEFRAMES_WEBSCRAPING_TEXT = {
    "LAST_7_DAYS": "Past Week",
    "LAST_30_DAYS": "Past Month",
    "LAST_90_DAYS": "Past Quarter",
    "LAST_180_DAYS": "Past Half a Year",
    "LAST_365_DAYS": "Past Year",
    "ALL": "All Time"
}

LASTFM_COOKIES = {
    'lfmjs': '1',
    'not_first_visit': '1',
    'lfmjs': '1',
    'AMCVS_10D31225525FF5790A490D4D%40AdobeOrg': '1',
    's_vnum': '1704870515428%26vn%3D1',
    's_invisit': 'true',
    's_lv_undefined_s': 'First%20Visit',
    's_cc': 'true',
    '_BB.bs': 'e|2',
    'cbsiaa': '29295054553451461000195955174954',
    'lpfrmo': '0',
    'X-UA-Device-Type': 'desktop',
    'X-UA-Country-Code': 'DE',
    'prevPageType': 'user_door',
    'dw-tag': 'content%3Bmasthead-nav',
    '_BB.d': '0|||3',
    'OptanonAlertBoxClosed': '2023-12-11T07:33:47.883Z',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Mon+Dec+11+2023+08%3A33%3A48+GMT%2B0100+(Central+European+Standard+Time)&version=202310.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&genVendors=&consentId=8f743b59-08c2-4447-b6f6-8c562b09a7f9&interactionCount=1&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A1%2C5%3A1&AwaitingReconsent=false&geolocation=%3B',
    'utag_main': f'{SomiBot.Keychain.LAST_FM_COOKIES}',
    's_getNewRepeat': '1702280028421-New',
    's_lv_undefined': '1702280028422',
    's_sq': 'cbsilastfmsite%3D%2526c.%2526a.%2526activitymap.%2526page%253Dlastfm%25253A%25252Flogin%2526link%253DLET%252520ME%252520IN%252521%2526region%253Dlogin%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dlastfm%25253A%25252Flogin%2526pidt%253D1%2526oid%253DLET%252520ME%252520IN%252521%2526oidt%253D3%2526ot%253DSUBMIT',
    'AMCV_10D31225525FF5790A490D4D%40AdobeOrg': '1585540135%7CMCIDTS%7C19703%7CMCMID%7C91822223998886246946005506264433378921%7CMCAID%7CNONE%7CMCOPTOUT-1702287229s%7CNONE%7CvVersion%7C4.4.0',
    'csrftoken': '2NDZKG3CvQ9ZbYod4o4Z7ytdLjzYSoLZhrJtXueNV9qOcVM2R5LRfMppfwZxOiXw',
    'lfmanon': '0',
    'sessionid': '.eJyNjs2O2jAURp-FSN2VyHZsJ2ZJA-VnZkpAEMgmunZsQskQiCFmWvXdCy2LmUWl7q50z9F3fno5XM5lfrG6yUuwpdfzgoQ8q2YxSV9erm8x32_QYDRda_G0cQOsyNz77Flt7a4-5LvixkseGR4J2dWayi7FBe8Ck6YbCKVUVGgDSt2cd0N_tF6vt1wM5uP4dmBEEeYUsY-cBLXXhztcmVffaek753w4Hq1_h_zH3182tv9Ab_7x0tibInCABTcGSyDSKIVNgQqgUGgZCkCcs5BLMJgIIhhilLGAMkw5RghhwQRjOKSC0Q4g1EH4qtpTOu3vWxDtQlbPHeQTPx4ZM5lN9fYgsvmqnmQNnPrOj2dl9bqeNiN0dAnKkgkZotROqMqviAyr1Zejbq4_6iTS0T3Y_g1GoIxGuuCFVmEUUCFFyABHGIKQUKb-O_ifue21zmwIw0v2NdymZZ2mq_bkfFXwzX49XM-hz3jwrczRjpy397Lzo2wOetmOt81gvahw5twb0Zckrp_0d1ENnVxttuMFQDoLkk9B7P36DSgyt0A:1rCalm:TZZmlqkf-BxhjIbOdmq7LmvtLHxejc7M8--4wzt5vOA',
}

LASTFM_HEADERS = {
    'authority': 'www.last.fm',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': 'lfmjs=1; not_first_visit=1; lfmjs=1; AMCVS_10D31225525FF5790A490D4D%40AdobeOrg=1; s_vnum=1704870515428%26vn%3D1; s_invisit=true; s_lv_undefined_s=First%20Visit; s_cc=true; _BB.bs=e|2; cbsiaa=29295054553451461000195955174954; lpfrmo=0; X-UA-Device-Type=desktop; X-UA-Country-Code=DE; prevPageType=user_door; dw-tag=content%3Bmasthead-nav; _BB.d=0|||3; OptanonAlertBoxClosed=2023-12-11T07:33:47.883Z; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Dec+11+2023+08%3A33%3A48+GMT%2B0100+(Central+European+Standard+Time)&version=202310.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&genVendors=&consentId=8f743b59-08c2-4447-b6f6-8c562b09a7f9&interactionCount=1&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A1%2C5%3A1&AwaitingReconsent=false&geolocation=%3B; utag_main=v_id:018c57b4c8d2008d136a2169a0c804081001407900978$_sn:1$_ss:0$_pn:5%3Bexp-session$_st:1702281828245$ses_id:1702278514898%3Bexp-session$vapi_domain:last.fm; s_getNewRepeat=1702280028421-New; s_lv_undefined=1702280028422; s_sq=cbsilastfmsite%3D%2526c.%2526a.%2526activitymap.%2526page%253Dlastfm%25253A%25252Flogin%2526link%253DLET%252520ME%252520IN%252521%2526region%253Dlogin%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dlastfm%25253A%25252Flogin%2526pidt%253D1%2526oid%253DLET%252520ME%252520IN%252521%2526oidt%253D3%2526ot%253DSUBMIT; AMCV_10D31225525FF5790A490D4D%40AdobeOrg=1585540135%7CMCIDTS%7C19703%7CMCMID%7C91822223998886246946005506264433378921%7CMCAID%7CNONE%7CMCOPTOUT-1702287229s%7CNONE%7CvVersion%7C4.4.0; csrftoken=2NDZKG3CvQ9ZbYod4o4Z7ytdLjzYSoLZhrJtXueNV9qOcVM2R5LRfMppfwZxOiXw; lfmanon=0; sessionid=.eJyNjs2O2jAURp-FSN2VyHZsJ2ZJA-VnZkpAEMgmunZsQskQiCFmWvXdCy2LmUWl7q50z9F3fno5XM5lfrG6yUuwpdfzgoQ8q2YxSV9erm8x32_QYDRda_G0cQOsyNz77Flt7a4-5LvixkseGR4J2dWayi7FBe8Ck6YbCKVUVGgDSt2cd0N_tF6vt1wM5uP4dmBEEeYUsY-cBLXXhztcmVffaek753w4Hq1_h_zH3182tv9Ab_7x0tibInCABTcGSyDSKIVNgQqgUGgZCkCcs5BLMJgIIhhilLGAMkw5RghhwQRjOKSC0Q4g1EH4qtpTOu3vWxDtQlbPHeQTPx4ZM5lN9fYgsvmqnmQNnPrOj2dl9bqeNiN0dAnKkgkZotROqMqviAyr1Zejbq4_6iTS0T3Y_g1GoIxGuuCFVmEUUCFFyABHGIKQUKb-O_ifue21zmwIw0v2NdymZZ2mq_bkfFXwzX49XM-hz3jwrczRjpy397Lzo2wOetmOt81gvahw5twb0Zckrp_0d1ENnVxttuMFQDoLkk9B7P36DSgyt0A:1rCalm:TZZmlqkf-BxhjIbOdmq7LmvtLHxejc7M8--4wzt5vOA',
    'if-none-match': 'W/"2e21386ba31730a721190fddaa7f13cd"',
    'referer': 'https://www.last.fm/login',
    'sec-ch-ua': '"Whale";v="3", "Not-A.Brand";v="8", "Chromium";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Whale/3.22.205.26 Safari/537.36',
}