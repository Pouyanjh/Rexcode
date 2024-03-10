from datetime import datetime, timezone

from django.http import HttpResponseRedirect
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import zibal

from bank.models import Order
from bank.paydb.pay_utils import idpaycreatepay, idpaycreatedb, idpayverify, idpayupdatedb
from bank.serializer import orderserializer


@api_view(['POST'])
def addorderview(request):
    data = request.data
    order = Order.objects.create(
        title = data['title'],
        totalprice = data['price'],
        paymentmethod = data['payment'],
        user = data['user']
    )
    serializer = orderserializer(order, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def payorder(request, pk):
    try:
        order = Order.objects.get(_id=pk)
    except Order.DoesNotExist:
        return Response({'detail': 'order not found !'}, status=status.HTTP_404_NOT_FOUND)


    else:
        if order.is_paid:
            return Response({'detail': 'order already paid !'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                response = idpaycreatepay(order)
            except:
                return Response({'detail': 'the zibal server connection was established !'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                if (str(response.status_code).startswith('2')):
                    json = response.json()
                    print(json)
                    if (idpaycreatedb(order, json['trackId'])):

                        return Response(response, status=status.HTTP_200_OK)
                    else:
                        return Response({'detail': 'db error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def Idpaycallback(request):
    orderId = request.GET.get('orderId')
    success = request.GET.get('success')
    trackId = request.GET.get('trackId')
    callbackpaystatus = request.GET.get('status')
    print(callbackpaystatus)


    try:

        order = Order.objects.get(_id=orderId)
        pay_entry = zibal.objects.get(transId=trackId, order=order)

        if order.is_paid:
            return HttpResponseRedirect(f"https://localhost:5173/payresult/{success}/{orderId}/{trackId}")
    except:
        return Response({'detail': 'transaction processing error!'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # transactionn verify
        if (str(callbackpaystatus) == '2'):
            try:
                response = idpayverify(trackId)
            except:

                dbstatus = idpayupdatedb(pay_entry, 400, trackId)
                return HttpResponseRedirect(
                    f"https://localhost:5173/payresult/{orderId}/{trackId}/{success}/?db={dbstatus}")
            else:
                if (str(response.status_code).startswith('2')):

                    resjson = response.json()
                    print(resjson)
                    order = Order.objects.get(_id=orderId)
                    zib1al = zibal.objects.get(order=order)
                    print(zib1al)
                    zib1al.lastStatus = resjson['status']
                    zib1al.amountPaid = resjson['amount']
                    zib1al.cardNo = resjson['cardNumber']
                    zib1al.Condition = resjson['message']
                    zib1al.save()

                    order.is_paid = True
                    order.save()
                    print(order)
                    return HttpResponseRedirect(
                        f"https://localhost:5173/payresult/{callbackpaystatus}/{trackId}/{orderId}/{success}")



                else:
                        dbstatus = idpayupdatedb(pay_entry, 400, trackId)
                        return HttpResponseRedirect(
                            f"https://localhost:5173/payresult/{orderId}/{trackId}/{success}/?db={dbstatus}")


        else:
            idpayupdatedb(pay_entry, callbackpaystatus, trackId)
            return HttpResponseRedirect(
                f"https://localhost:5173/payresult/{orderId}/{trackId}/{success}")








