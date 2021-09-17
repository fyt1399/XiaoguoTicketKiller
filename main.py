# 票星球 黄埔剧场中剧场 笑果抢票专用
# 需要手动获得header里的passId，方法为点击进入一场演出，在获取对应页面的时候会把passId set到Cookie里
# showId在url里可以获得

import requests
import geobuf
import re
import json

# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/92.0.4515.159 Safari/537.36",
    "access-token": "eyJ0eXAiOiJKV1QiLCJjdHkiOiJKV1QiLCJ6aXAiOiJERUYiLCJhbGciOiJSUzUxMiJ9"
                    ".eNqEkM0OgjAQhN9lzxxasKVwxHjw5E800WOBNZBAa0prjMZ3d5FEPelxZme_2ewdrA6"
                    "-WZqThdyErosgDOgmfYeyvc1tjZDD-rCBCIZQFm"
                    "-LNM23thtFsT8utuT0vtqPgJo8yWdcCEy0lvFJCMaZKJWs1bT4L6bhEQFez63DXdtTB5dJnKV8pjLG2AuxOqPT3v7EZNRWOdT-Q-GpjFkqEpXQveiqRhv__QEq_W6L4IJuaK0hc3qP0SNpDD-eAAAA__8.SYdEAUXDCSfzbVouOnY2Di-MiYvIhEWpmmyPmVI1XpCLqc0GbHjq1PItAKbDB3O2ld3cTIGw1GWr5dGMBswhDJkFIF-VLsFvW2TqJ4t4EcDVaz737YXU4GHnpEyauyi87WnV3Bt4lWC3bmtuGDZfiDf4WreNCanneZLvQ0ja-Uo",
    "Origin": "https://m.piaoxingqiu.com",
    'Referer': 'https://m.piaoxingqiu.com/order/confirm',
    'passId': '61440d0919ab7f144190951c',
}

proxies = {
    'https': None,
    'http': None,
}


def preOrder(showId, sessionId, ticketItem):
    url = 'https://m.piaoxingqiu.com/pxq_buyerapi/buyer/v2/preorder'

    param = {
        'show': (None, showId),
        'price': (None, ticketItem['qty'] * ticketItem['ticketPrice']),
        'session': (None, sessionId),
        'qty': (None, ticketItem['qty']),
        'ticketItems': (None, json.dumps([ticketItem])),
        'src': (None, 'web'),
    }

    response = requests.post(url=url, files=param, headers=headers, proxies=proxies)

    return response.json()['data']


def queryPriceItems(showId, sessionId, ticketItem):
    url = 'https://m.piaoxingqiu.com/pxq_buyerapi/buyer/v1/order/price_items'

    param = {
        'showId': (None, showId),
        'clientId': (None, '000'),
        'showSessionId': (None, sessionId),
        'locationCityId': (None, 310105),
        'deliverMethod': (None, 'EXPRESS'),
        'ticketItems': (None, json.dumps([ticketItem])),
    }

    response = requests.post(url=url, files=param, headers=headers, proxies=proxies)

    return response.json()['data']


def order(showId, sessionId, price, transferFee, priceItem, ticketItem, agreeId):
    url = "https://m.piaoxingqiu.com/pxq_buyerapi/buyer/v1/order"

    param = {
        'source': (None, 'm_web'),
        'user': (None, '000'),
        'show': (None, showId),
        'session': (None, sessionId),
        'price': (None, int(price)),
        'agreed': (None, 1),
        'deliverMethod': (None, 'EXPRESS'),
        'presale': (None, 1),
        'total': (None, int(price + transferFee)),
        'discount': (None, 0),
        'agreementOID': (None, agreeId),
        'audienceIds': (None, json.dumps(['614155f86d96f7136b3de088', '6141572b6d96f7136b3def1e'])),
        'deliver': (None, 2),
        'deliver_fee': (None, 0),
        'province': (None, '31'),
        'city': (None, '01'),
        'district': (None, '05'),
        'address': (None, '茅台路270弄16号楼404'),
        'express': (None, 1),
        'receiver': (None, '傅耘天'),
        'cellphone': (None, 18159826576),
        'priceItems': (None, json.dumps(priceItem)),
        'ticketItems': (None, json.dumps([ticketItem])),
        'locationCityId': (None, 3101),
        'src': (None, 'web')
    }

    response = requests.post(url=url, files=param, headers=headers, proxies=proxies)

    if (response.json()['statusCode'] == 200):
        print('抢票成功 请付款')
        return True
    else:
        return False


def queryTickets(sessionId):
    url = "https://m.piaoxingqiu.com/pxq_buyerapi/buyer/v2/show_sessions/{}/seats/sale_info".format(sessionId)

    param = {
        'src': 'web'
    }

    response = requests.get(url, headers=headers, params=param, proxies=proxies)
    return response.json()['data']


def queryTicketInfo(showId, showSessionId, seatPlanId, ticketSeatId, zoneConcreteId, seatId):
    url = "https://m.piaoxingqiu.com/pxq_buyerapi/buyer/v2/tickets"

    param = {
        'seatTicket': [{'comboZoneExclusion': 'false',
                        'qty': 1,
                        'seatPlanId': seatPlanId,
                        'ticketSeatId': ticketSeatId,
                        'zoneConcreteId': zoneConcreteId,
                        'seatId': seatId
                        }],
        'showId': showId,
        'showSessionId': showSessionId,
        'src': 'web',
        'zones': []
    }

    response = requests.post(url=url, json=param, headers=headers, proxies=proxies)
    return response.json()['data']['zoneSeatInfos'][0]


def querySeatGeoBuf(zoneGeoBufUrl):
    param = {
        'src': 'web'
    }

    response = requests.get(zoneGeoBufUrl, headers=headers, params=param, proxies=proxies)
    seatList = geobuf.decode(response.content)['features']

    return seatList


def querySkuInfo(showId):
    url = ('https://m.piaoxingqiu.com/pxq_buyerapi/buyer/v1/shows/{}/sku').format(showId)
    param = {
        'src': 'web'
    }

    response = requests.get(url, headers=headers, params=param, proxies=proxies)
    session = response.json()['data']['sessions'][0]
    sessionId = session['showSessionId']
    seatPlanId = session['seatPlans'][2]['seatPlanId']

    return {'sessionId': sessionId, 'seatPlanId': seatPlanId}


def queryStaticInfo(sessionId):
    url = ('https://m.piaoxingqiu.com/pxq_buyerapi/buyer/v1/show_sessions/{}/seats/static_resource').format(sessionId)
    param = {
        'src': 'web'
    }

    response = requests.get(url, headers=headers, params=param, proxies=proxies)
    seatData = response.json()['data'][3]
    geobufUrl = seatData['url']
    zoneConcreteId = seatData['zoneConcreteId']

    return {'geobufUrl': geobufUrl, 'zoneConcreteId': zoneConcreteId}


def startGetTicket(showId):
    skuInfo = querySkuInfo(showId)
    sessionId = skuInfo['sessionId']
    seatPlanId = skuInfo['seatPlanId']

    staticInfo = queryStaticInfo(sessionId)
    geobufUrl = staticInfo['geobufUrl']
    zoneConcreteId = staticInfo['zoneConcreteId']

    seatList = querySeatGeoBuf(geobufUrl)
    seatMap = {}
    for i in range(0, len(seatList)):
        seatMap[seatList[i]['properties']['seatConcreteId']] = seatList[i]['geometry']['coordinates']

    ticketList = queryTickets(sessionId)
    lastTicketInfo = None
    for i in range(0, len(ticketList)):
        if ticketList[i]['seatConcreteId'] in seatMap:
            ticketInfo = queryTicketInfo(showId, sessionId, seatPlanId, ticketList[i]['ticketSeatId'], zoneConcreteId,
                                         ticketList[i]['seatConcreteId'])
            ticketInfo['ticketSeatId'] = ticketList[i]['ticketSeatId']
            if lastTicketInfo is None:
                lastTicketInfo = ticketInfo
            else:
                lastRow = getRowAndColumn(lastTicketInfo['ticketSeatDesc'])['row']
                nowRow = getRowAndColumn(ticketInfo['ticketSeatDesc'])['row']
                lastColumn = getRowAndColumn(lastTicketInfo['ticketSeatDesc'])['column']
                nowColumn = getRowAndColumn(ticketInfo['ticketSeatDesc'])['column']
                if lastRow == nowRow and abs(lastColumn - nowColumn) <= 2:
                    ticketItem = {
                        'showId': showId,
                        'showSessionId': sessionId,
                        'seatPlanId': seatPlanId,
                        'ticketPrice': int(ticketInfo['ticketPrice']),
                        'ticketId': ticketInfo['channelTicketId'],
                        'qty': 2,
                        'itemType': 'SINGLE',
                        'ticketSeatIds': [lastTicketInfo['ticketSeatId'], ticketInfo['ticketSeatId']],
                        'zoneConcreteId': ticketInfo['zoneConcreteId']
                    }
                    preOrderInfo = preOrder(showId, sessionId, ticketItem)
                    priceItem = queryPriceItems(showId, sessionId, ticketItem)
                    return order(showId, sessionId, ticketItem['ticketPrice'] * ticketItem['qty'],
                                 priceItem[1]['priceItemVal'], priceItem, ticketItem, preOrderInfo['agreement'][
                                     'orderAgreementOID'])
                    break
                else:
                    lastTicketInfo = ticketInfo


def getRowAndColumn(str):
    result = re.match('(\d{1,2})排(\d{1,2})座', str)
    if result is None:
        return None
    else:
        return {'row': int(result.group(1)), 'column': int(result.group(2))}


getTicketResult = False
try:
    getTicketResult = startGetTicket('614000d3e24c3a7ec7eab5bd')
except:
    getTicketResult = False
while not getTicketResult:
    try:
        getTicketResult = startGetTicket('614000d3e24c3a7ec7eab5bd')
    except:
        getTicketResult = False
