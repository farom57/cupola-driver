import asyncio
from bleak import BleakScanner, BleakClient
import struct
from threading import Thread


class Cupola(object):

    def __init__(self):
        self._flask_loop = None
        self._connected = False
        self._address = None
        self._client = None
        self._STATE_UUID = "c3fe2f77-e1c8-4b1c-a0f3-ef88d0503121"
        self._HEAD_UUID = "c3fe2f77-e1c8-4b1c-a0f3-ef88d050313a"
        self._ALIVE_UUID = "c3fe2f77-e1c8-4b1c-a0f3-ef88d0503151"

        # self._loop = asyncio.get_event_loop()
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

        def bleak_thread(loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()

        self._thread = Thread(target=bleak_thread, args=(self._loop,))
        self._thread.start()

        self._disconnected_event = asyncio.Event()
        self._connected_event = asyncio.Event()

    def __del__(self):
        print('Stopping')
        self._loop.call_soon_threadsafe(self._loop.stop)

    async def connect(self):
        # try:
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
        asyncio.run_coroutine_threadsafe(self.maintain_connection(), self._loop)

        self._flask_loop = asyncio.get_event_loop()
        print('[waiting connection]')
        await self._connected_event.wait()
        print('[returned]')
        return self._connected

    async def maintain_connection(self):
        self._connected = await self._client.connect()

        self._flask_loop.call_soon_threadsafe(self._connected_event.set)
        if not self._connected:
            return

        print('[connected]')
        await self._client.write_gatt_char(self._STATE_UUID, bytearray([5]))
        print('[running]')
        await self._disconnected_event.wait()
        print('[disconnected]')

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
