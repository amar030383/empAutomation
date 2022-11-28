import asyncio
from fbnet.command_runner.thrift_client import AsyncioThriftClient
from fbnet.command_runner_asyncio.CommandRunner import ttypes as fcr_ttypes
from fbnet.command_runner_asyncio.CommandRunner.Command import Client as FcrClient

class TimeoutException(Exception):
    pass

username='amar'
password = 'cisco'
hostname = '3.13.93.157'

device = fcr_ttypes.Device(hostname=hostname, username=username, password=password)

async def bulk_run(device_to_commands):
    async with AsyncioThriftClient(FcrClient, 'localhost', 12345) as client:
        res = await client.bulk_run(device_to_commands)
        for device_name, v in res.items():
            print(device_name + 'masaged  output:  =============')
            for cmd_re in v:
                if 'Timeout' in cmd_re.status:
                    raise TimeoutException()
                print('cmd: ' + cmd_re.command + '\n')
                print('status: ' + cmd_re.status + '\n')
                print('result: ' + cmd_re.output + '\n')
loop = asyncio.get_event_loop()
device_to_commands = {    
    device: ['conf t', 'show clock'],
}
results = loop.run_until_complete(bulk_run(device_to_commands)) 




