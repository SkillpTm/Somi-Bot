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

LASTFM_TIMEFRAMES_ARTIST = {
    "Past Week": "LAST_7_DAYS",
    "Past Month": "LAST_30_DAYS",
    "Past Quarter": "LAST_90_DAYS",
    "Past Half a Year": "LAST_180_DAYS",
    "Past Year": "LAST_365_DAYS",
    "All Time": "ALL"
}

LASTFM_TIMEFRAMES_ARTIST_TEXT = {
    "LAST_7_DAYS": "Past Week",
    "LAST_30_DAYS": "Past Month",
    "LAST_90_DAYS": "Past Quarter",
    "LAST_180_DAYS": "Past Half a Year",
    "LAST_365_DAYS": "Past Year",
    "ALL": "All Time"
}

LASTFM_COOKIES = {
    'lfmjs': '1',
    'lfmjs': '1',
    'csrftoken': '6zRrtLZ4F4yaIO3UXQcnq5dJl46DNZLPtDzVtDdbGme9Gq6DFLDbNQ3zDwgXueo0',
    'cbsiaa': '30749071722051451962625534806414',
    'OptanonAlertBoxClosed': '2022-10-27T23:18:21.030Z',
    'lfmanon': '0',
    'not_first_visit': '1',
    'X-UA-Device-Type': 'desktop',
    'X-UA-Country-Code': 'DE',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Tue+Nov+29+2022+04%3A43%3A25+GMT%2B0100+(Central+European+Standard+Time)&version=6.30.0&isIABGlobal=false&hosts=&consentId=fddc6872-772b-481b-b806-85080a041a29&interactionCount=2&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A1%2C5%3A1&geolocation=DE%3BNW&AwaitingReconsent=false',
    'AMCVS_10D31225525FF5790A490D4D%40AdobeOrg': '1',
    's_vnum': '1672285405759%26vn%3D1',
    's_invisit': 'true',
    's_lv_undefined_s': 'More%20than%2030%20days',
    's_cc': 'true',
    'dw-tag': 'content',
    'sessionid': '.eJyNkctu2lAURb8Fj8PVfT-Y1QQHUoQLhNB4Yt0nWDzri-OkVf-9JsmgHVTtbOucvY6WdH4kpW4u27KJvi63Om6TQeJ80M3-ktwk0cdYnY5l5bqxDARhilgfUxj61Gre15SovlSQae4ZDxR3zG_33rDBYLBajhaT2y4gKAVUWJA_e0bbnT9ey_twAK03oG1boM_nCK4l8LEHqzqmH9WOPzd17BBCWXBYW2s41xA75iwSwSnkqPEySE6YgYpwAgVVUCCBMWSIMqQ45pgxQiXkFNGehLAHkQmnJZ6i5apqlHoWuAcBBnfqyDe6XYwn4TQ8fD5XX6drPAc7e_v4asfFZqrzTGbD2WjYPO6yvLBtZr5_u0f5pFrPi1WaPl2F47swwsFrr510xDoLGReik6M4YEewEey_hf-qm35afLkfD_XdtqlzPTaFfhq1c1DLQ_Oy5g8ZfE1Hl4ci5rPZ8-ZqdnkzOzb7_U3SxbL2m_fn_csh-fkLrlanyg:1ozrWr:9ugWQkx6Fn94PWQLF7jBkVgfC0I',
    '_BB.bs': 'f|1',
    '_BB.d': '1|||1',
    's_getNewRepeat': '1669693408671-New',
    's_lv_undefined': '1669693408671',
    'prevPageType': 'user_door',
    'utag_main': f'v_id:01841b9a87430013f83e48ed38ee03086001407e00bd0{SomiBot.Keychain.LAST_FM_COOKIES}',
    's_sq': '%5B%5BB%5D%5D',
    'AMCV_10D31225525FF5790A490D4D%40AdobeOrg': '1585540135%7CMCIDTS%7C19326%7CMCMID%7C90877986730923803489208349555939581115%7CMCAID%7CNONE%7CMCOPTOUT-1669700608s%7CNONE%7CvVersion%7C4.4.0',
}

LASTFM_HEADERS = {
    'authority': 'www.last.fm',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': f'lfmjs=1; lfmjs=1; csrftoken=6zRrtLZ4F4yaIO3UXQcnq5dJl46DNZLPtDzVtDdbGme9Gq6DFLDbNQ3zDwgXueo0; cbsiaa=30749071722051451962625534806414; OptanonAlertBoxClosed=2022-10-27T23:18:21.030Z; lfmanon=0; not_first_visit=1; X-UA-Device-Type=desktop; X-UA-Country-Code=DE; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Nov+29+2022+04%3A43%3A25+GMT%2B0100+(Central+European+Standard+Time)&version=6.30.0&isIABGlobal=false&hosts=&consentId=fddc6872-772b-481b-b806-85080a041a29&interactionCount=2&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A1%2C5%3A1&geolocation=DE%3BNW&AwaitingReconsent=false; AMCVS_10D31225525FF5790A490D4D%40AdobeOrg=1; s_vnum=1672285405759%26vn%3D1; s_invisit=true; s_lv_undefined_s=More%20than%2030%20days; s_cc=true; dw-tag=content; sessionid=.eJyNkctu2lAURb8Fj8PVfT-Y1QQHUoQLhNB4Yt0nWDzri-OkVf-9JsmgHVTtbOucvY6WdH4kpW4u27KJvi63Om6TQeJ80M3-ktwk0cdYnY5l5bqxDARhilgfUxj61Gre15SovlSQae4ZDxR3zG_33rDBYLBajhaT2y4gKAVUWJA_e0bbnT9ey_twAK03oG1boM_nCK4l8LEHqzqmH9WOPzd17BBCWXBYW2s41xA75iwSwSnkqPEySE6YgYpwAgVVUCCBMWSIMqQ45pgxQiXkFNGehLAHkQmnJZ6i5apqlHoWuAcBBnfqyDe6XYwn4TQ8fD5XX6drPAc7e_v4asfFZqrzTGbD2WjYPO6yvLBtZr5_u0f5pFrPi1WaPl2F47swwsFrr510xDoLGReik6M4YEewEey_hf-qm35afLkfD_XdtqlzPTaFfhq1c1DLQ_Oy5g8ZfE1Hl4ci5rPZ8-ZqdnkzOzb7_U3SxbL2m_fn_csh-fkLrlanyg:1ozrWr:9ugWQkx6Fn94PWQLF7jBkVgfC0I; _BB.bs=f|1; _BB.d=1|||1; s_getNewRepeat=1669693408671-New; s_lv_undefined=1669693408671; prevPageType=user_door; utag_main=v_id:01841b9a87430013f83e48ed38ee03086001407e00bd0{_sn:3$_ss:1$_st:1669695208675$vapi_domain:last.fm$_pn:1%3Bexp-session$ses_id:1669693405718%3Bexp-session;} s_sq=%5B%5BB%5D%5D; AMCV_10D31225525FF5790A490D4D%40AdobeOrg=1585540135%7CMCIDTS%7C19326%7CMCMID%7C90877986730923803489208349555939581115%7CMCAID%7CNONE%7CMCOPTOUT-1669700608s%7CNONE%7CvVersion%7C4.4.0',
    'if-none-match': 'W/"c299815cb0d1941866f7e33f30f51b82"',
    'sec-ch-ua': '"Whale";v="3", " Not;A Brand";v="99", "Chromium";v="106"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.114 Whale/3.17.145.12 Safari/537.36',
}