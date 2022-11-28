import asyncssh, asyncio
command = ['show version']
host = '3.13.93.157'
port=22, 
user='amar' 
password='cisco'
    
device = (host, port, user,password)
async def async_ssh(command, device):
    conn = await asyncssh.connect(command, device)
    output = await conn.run(command, device)

loop = asyncio.get_event_loop()
loop.run_until_complete(async_ssh(command, device))


'''
import aiohttp
import asyncio

async def fetch(client):
  async with client.get('https://docs.aiohttp.org/en/stable/client_reference.html') as resp:
    assert resp.status == 200
    return await resp.text()

async def main():
  async with aiohttp.ClientSession() as client:
    html = await fetch(client)
    print(html)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
'''