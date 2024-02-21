import requests, json
from bank.models import zibal, Order
from datetime import datetime, timezone
from django.utils.timezone import make_aware
from bank.paydb.zibalstatus import ZIBAL_STATUS

ZIBAL_HEADER = {
    'Content-Type': 'application/json'
}


def idpaycreatepay(order):
    body = {
        'merchant': "zibal",
        'orderId': str(order._id),
        'amount': int(order.totalprice * 10),
        'callbackUrl': 'http://127.0.0.1:8000/callback/',
    }

    response = requests.post(
        'https://gateway.zibal.ir/v1/request',
        data=json.dumps(body),
        headers=ZIBAL_HEADER
    )

    return response


def idpaycreatedb(order, trackId):
    try:
        znibal = zibal.objects.create(
            order=order,
            transId=trackId,
            lastStatus=0,
            amountPaid=(order.totalprice * 10)
        )

        return True
    except:
        return False


def idpayupdatedb(pay_entry, lastStatus, trackId):
    try:
        pay_entry.lastStatus = lastStatus
        pay_entry.trackIdpay = trackId
        pay_entry.save()
        return True
    except:
        return False


def idpayverify(trackId):
    body = {
        'trackId': int(trackId),
        'merchant': "zibal"
    }
    response = (requests.post(
        'https://gateway.zibal.ir/v1/verify',
        data=json.dumps(body),
        headers=ZIBAL_HEADER
    ))
    print(response)

    return response