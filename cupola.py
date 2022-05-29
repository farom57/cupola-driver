import asyncio
from bleak import BleakScanner, BleakClient
import struct
from threading import Thread
import datetime


class Cupola(object):

    def __init__(self, address=None):
        self._flask_loop = None
        self._connected = False
        self._address = address  # normally 5B:AB:B6:09:F8:CD but it may change at each new firmware
        self._client = None
        self._STATE_UUID = "c3fe2f77-e1c8-4b1c-a0f3-ef88d0503121"
        self._HEAD_UUID = "c3fe2f77-e1c8-4b1c-a0f3-ef88d050313a"
        self._MAG_UUID = "c3fe2f77-e1c8-4b1c-a0f3-ef88d0503131"
        self._ALIVE_UUID = "c3fe2f77-e1c8-4b1c-a0f3-ef88d0503151"
        self._heading = None
        self.mag_measurements = []

        # Start a thread to perform BLE operation in the background
        self._ble_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._ble_loop)

        def bleak_thread(loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()

        self._thread = Thread(target=bleak_thread, args=(self._ble_loop,))
        self._thread.start()

        # Events to communicate between background and foreground tasks
        self._disconnected_event = asyncio.Event()
        self._disconnect_command = asyncio.Event()
        self._connected_event = asyncio.Event()

    def __del__(self):
        print('Stopping')
        self._ble_loop.call_soon_threadsafe(self._ble_loop.stop)

    async def connect(self):

        if self._connected:
            if self._client.is_connected:
                print('already connected')
                return True
            else:
                print('This should not happen')
                self._connected = False

        # scan ble devices (ignored if the MAC address is already known)

        if self._address is None:
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

        # start the connection task in the other Thread
        asyncio.run_coroutine_threadsafe(self.maintain_connection(), self._ble_loop)

        # waiting for the other thread to signal the connection
        self._flask_loop = asyncio.get_event_loop()
        print('[waiting connection]')
        await self._connected_event.wait()
        print('[returned]')
        return self._connected

    async def maintain_connection(self):
        print('[connecting]')
        self._connected = await self._client.connect()

        # signal to Cupola.connect() that it can terminate.
        self._flask_loop.call_soon_threadsafe(self._connected_event.set)

        if not self._connected:
            print('Failed to establish the connection')
            return

        print('[connected]')

        # Send command to change the State to ON (start continuous IMU and mag measurements)
        await self._client.write_gatt_char(self._STATE_UUID, bytearray([5]))
        print('[running]')
        await self._client.start_notify(self._MAG_UUID, self.notification_handler)
        print('notification enabled')

        # wait until the disconnection either from Cupola.disconnect() or from the device (disconnected_callback())
        disconnected_event_task = asyncio.create_task(self._disconnected_event.wait())
        disconnect_command_task = asyncio.create_task(self._disconnect_command.wait())
        done, pending = await asyncio.wait([disconnected_event_task, disconnect_command_task],
                                           return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()

        if self._client.is_connected:
            await self._client.disconnect()
        self._connected = False

        print('[disconnected]')

    def disconnected_callback(self, client):
        self._disconnected_event.set()

    async def disconnect(self):
        print(self.mag_measurements)
        if not self._connected:
            print('already disconnected')
            return True
        else:
            self._ble_loop.call_soon_threadsafe(self._disconnect_command.set)
            return True

    def notification_handler(self, sender, data):
        ts = datetime.datetime.now().timestamp()
        mag = [float(value) for value in data.decode().split(',')]
        measurement = [ts, mag[0], mag[1],mag[2]]
        print("mag: ", measurement)
        self.mag_measurements.append(measurement)

    @property
    def connected(self):
        return self._connected

    @property
    def heading(self):
        if self._heading is not None:
            return self._heading
        else:
            raise ValueError('No heading received yet')
