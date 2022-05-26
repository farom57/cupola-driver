import asyncio
from bleak import BleakScanner, BleakClient
import struct

class Cupola(object):

    def __init__(self):
        self._connected = False
        self._address = None
        self._client = BleakClient(self._address)
        self._STATE_UUID = "c3fe2f77-e1c8-4b1c-a0f3-ef88d0503121"
        self._HEAD_UUID = "c3fe2f77-e1c8-4b1c-a0f3-ef88d050313a"

    async def connect(self):
        #try:
        if self._client.is_connected:
            print('already connected')
            return True
        else:

            print('[scanning]')
            devices = await BleakScanner.discover()
            for d in devices:
                print(d)
                if d.name == "Cupola":
                    self._address = d.address
                    print(self._address)
                    self._client = BleakClient(self._address)
                    break
            if self._address is None:
                print("Error: Cupola not found")
                return False
            print('[connecting]')
            res = await self._client.connect()
            print(res)
            print('[connected]')

        await self._client.write_gatt_char(self._STATE_UUID, bytearray([5]))
        print('[running]')
        await asyncio.sleep(30)
        print('[stop]')
        # while self._client.is_connected:
        #     try:
        #         val = await self._client.read_gatt_char(self._HEAD_UUID)
        #         # print(val)
        #         valf = struct.unpack('f', val)[0]
        #         print(valf)
        #
        #     except Exception as e:
        #         print(e)
        #     await asyncio.sleep(1)

        return True

        #except Exception as e:
        #    print(e)
        #    return False

    async def disconnect(self):
        if not self._client.is_connected:
            print('already disconnected')
            return True
        else:
            await self._client.disconnect()
            print('[disconnected]')
            return True


