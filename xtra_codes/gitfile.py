import asyncio
from fbnet.command_runner.thrift_client import AsyncioThriftClient
# Import FCR Thrift Types
from fbnet.command_runner_asyncio.CommandRunner import ttypes as fcr_ttypes
# Import FCR Service Client
from fbnet.command_runner_asyncio.CommandRunner.Command import Client as FcrClient
import getpass
# Device Information
hostname = 'dev-001'
username = 'netbot'
password = getpass.getpass('%s Password: ' % username)

# Destination device
device = fcr_ttypes.Device(hostname=hostname, username=username, password=password)

async def run(cmd, device):
    async with AsyncioThriftClient(FcrClient, 'localhost', 5000) as client:
        res = await client.run(cmd, device)
        # type of res is `struct CommandResult`
        print(res.output)

loop = asyncio.get_event_loop()
loop.run_until_complete(run('uname -a\nip -4 add list eth0', device))