import asyncio
from bleak import BleakScanner, BleakClient
import struct
from threading import Thread

class Cupola(object):

    def __init__(self):
        self._connected = False
        self._address = None
        self._client = None
        self._STATE_UUID = "c3fe2f77-e1c8-4b1c-a0f3-ef88d0503121"
        self._HEAD_UUID = "c3fe2f77-e1c8-4b1c-a0f3-ef88d050313a"
        self._ALIVE_UUID = "c3fe2f77-e1c8-4b1c-a0f3-ef88d0503151"

        #self._loop = asyncio.get_event_loop()
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        def bleak_thread(loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()
        self._thread = Thread(target=bleak_thread, args=(self._loop,))
        self._thread.start()

        self._disconnected_event = asyncio.Event()

    def __del__(self):
        print('Stopping')
        self._loop.call_soon_threadsafe(self._loop.stop)

    async def connect(self):
        #try:
        if self._client is not None:
            if self._client.is_connected:
                print('already connected')
                return True

        print('[scanning]')
        devices = await BleakScanner.discover()

        for d in devices:
            print(d)
            if d.name == "Cupola":
                self._address = d.address
                print(self._address)
                self._client = BleakClient(self._address, disconnected_callback=self.disconnected_callback)
                break
        if self._address is None:
            print("Error: Cupola not found")
            return False
        print('[connecting]')

        print('[running]')
        asyncio.run_coroutine_threadsafe(self.maintain_connection(), self._loop)
        print('[exiting]')

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

    async def maintain_connection(self):
        res = await self._client.connect()
        print(res)
        print('[connected]')
        await self._client.write_gatt_char(self._STATE_UUID, bytearray([5]))
        print('[running]')
        await self._disconnected_event.wait()
        # while True:
        #     print("Connected:", self._client.is_connected)
        #     await asyncio.sleep(1)
        #     await self._client.write_gatt_char(self._ALIVE_UUID, bytearray([5]))
        print('[stop]')

    def disconnected_callback(self, client):
        print("Disconnected callback called!")
        self._disconnected_event.set()

    async def disconnect(self):
        if not self._client.is_connected:
            print('already disconnected')
            return True
        else:
            await self._client.disconnect()
            print('[disconnected]')
            return True


