import requests
import aiocryptopay
from aiocryptopay import AioCryptoPay, Networks
from aiocryptopay.models.update import Update
import asyncio

crypto_api = '101298:AAJZwArQifXWJyfPUZctjQUVyha4GsrOFUS'
crypto = AioCryptoPay(token=crypto_api, network=Networks.MAIN_NET)


async def create_invoice():
    invoice = await crypto.create_invoice(asset='USDT', amount=1)
    await crypto.close()
    return invoice


loop = asyncio.get_event_loop()
invoice = loop.run_until_complete(create_invoice())

print(invoice.pay_url)




