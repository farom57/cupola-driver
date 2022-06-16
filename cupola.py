import asyncio
import pickle
from typing import Tuple

from bleak import BleakScanner, BleakClient
import struct
from threading import Thread
import datetime
import csv
import numpy as np
import math

from numpy import ndarray

T_CALIB = 600  # 10 minutes, it must be sufficient for several turns of the dome
STEPS = 72  # number of steps for the calibration (1 every 5°)


class Cupola(object):

    def __init__(self, address=None):

        self.mag_error = None
        self.command = 0
        self._azimuth = None
        self._flask_loop = None
        self._connected = False
        self._address = address  # normally 5B:AB:B6:09:F8:CD but it may change at each new firmware
        self._client = None
        self._STATE_UUID = "c3fe2f77-e1c8-4b1c-a0f3-ef88d0503121"
        self._HEAD_UUID = "c3fe2f77-e1c8-4b1c-a0f3-ef88d050313a"
        self._MAG_UUID = "c3fe2f77-e1c8-4b1c-a0f3-ef88d0503131"
        self._ALIVE_UUID = "c3fe2f77-e1c8-4b1c-a0f3-ef88d0503151"
        self._RFCMD_UUID = "c3fe2f77-e1c8-4b1c-a0f3-ef88d0503171"
        self.log_measurements = []  # Size Nx6: timestamp, meas_x, meas_y, meas_z, heading, err
        self.calib_measurements = []  # Size Nx4: dt, meas_x, meas_y, meas_z
        self._tstart_calib = 0  # date of calibration starting
        self._calibrating = False

        # saved data, first set defaults
        self._calibrated = False
        self._calib_data = None  # numpy array size STEPS x 3: meas_x, meas_y, meas_z
        self.calib_offset = 0
        self.park_azimuth = None
        self.home_azimuth = None
        self.load_settings()

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
        self._connected_event.clear()
        print('[returned]')
        return self._connected

    async def maintain_connection(self):
        print('[connecting]')
        self._connected = await self._client.connect()
        print('...')
        # signal to Cupola.connect() that it can terminate.
        self._flask_loop.call_soon_threadsafe(self._connected_event.set)

        if not self._connected:
            print('Failed to establish the connection')
            return

        print('[connected]')
        await self._client.start_notify(self._MAG_UUID, self.notification_handler)
        print('notification enabled')

        # wait until the disconnection either from Cupola.disconnect() or from the device (disconnected_callback())
        disconnected_event_task = asyncio.create_task(self._disconnected_event.wait())
        disconnect_command_task = asyncio.create_task(self._disconnect_command.wait())

        # write to the alive char every 5s. Monitor for disconnect tast or event
        while (True):
            read_alive_task = asyncio.create_task(self._client.read_gatt_char(self._ALIVE_UUID))
            done, pending = await asyncio.wait([disconnected_event_task, disconnect_command_task, read_alive_task],
                                               return_when=asyncio.FIRST_COMPLETED, timeout=5.)

            if read_alive_task in pending or read_alive_task.exception() is not None:  # if fail to write it's likely that the connection is dead
                print('Disconnection caused by connection error')
                for task in pending:
                    task.cancel()
                break

            print("alive:", read_alive_task.result())

            done, pending = await asyncio.wait([disconnected_event_task, disconnect_command_task],
                                               return_when=asyncio.FIRST_COMPLETED, timeout=5.)

            if disconnected_event_task in done:
                print('Disconnection from the device')
                for task in pending:
                    task.cancel()
                break
            if disconnect_command_task in done:
                print('Disconnection command')
                for task in pending:
                    task.cancel()
                break

        if self._client.is_connected:
            await self._client.disconnect()
        self._connected = False

        self._disconnected_event.clear()
        self._disconnect_command.clear()
        print('[disconnected]')

    def disconnected_callback(self, client):
        self._disconnected_event.set()

    async def disconnect(self):
        print(self.log_measurements)
        if not self._connected:
            print('already disconnected')
            return True
        else:
            self._ble_loop.call_soon_threadsafe(self._disconnect_command.set)
            return True

    async def notification_handler(self, sender, data):
        ts = datetime.datetime.now().timestamp()
        mag = [float(value) for value in data.decode().split(',')]
        if self.calibrated:
            angle, self.mag_error = self.compute_heading([mag[0], mag[1], mag[2]])
            self._azimuth = angle + self.calib_offset
            measurement = [ts, mag[0], mag[1], mag[2], self._azimuth, self.mag_error]
        else:
            measurement = [ts, mag[0], mag[1], mag[2], np.nan, np.nan]
        # print("mag: ", measurement)
        self.log_measurements.append(measurement)

        dt = ts - self._tstart_calib
        if 0 < dt < T_CALIB:
            print("calib ", dt / T_CALIB * 100., "%", measurement)
            measurement_calib = [dt, mag[0], mag[1], mag[2]]
            self.calib_measurements.append(measurement_calib)
        if dt > T_CALIB and self._calibrating:
            print("Stopping")
            await self.turn_stop()
            print("Stopped")
            self.compute_calibration()
            self._calibrating = False

    async def start_calib(self):
        self.calib_measurements = []
        self._tstart_calib = datetime.datetime.now().timestamp() + 5  # start calibration in 5s to let the cupola accelerate
        self._calibrating = True
        asyncio.run_coroutine_threadsafe(self.turn_right(), self._ble_loop)  # start rotation to the right

    async def turn_left(self):
        await self._client.write_gatt_char(self._RFCMD_UUID, bytearray([3]))
        self.command = 3

    async def turn_right(self):
        await self._client.write_gatt_char(self._RFCMD_UUID, bytearray([4]))
        self.command = 4

    async def turn_up(self):
        await self._client.write_gatt_char(self._RFCMD_UUID, bytearray([1]))
        self.command = 1

    async def turn_down(self):
        await self._client.write_gatt_char(self._RFCMD_UUID, bytearray([2]))
        self.command = 2

    async def turn_stop(self):
        await self._client.write_gatt_char(self._RFCMD_UUID, bytearray([0]))
        self.command = 0

    @property
    def connected(self):
        return self._connected

    @property
    def calibrated(self):
        return self._calibrated

    @property
    def calibrating(self):
        return self._calibrating

    @property
    def azimuth(self):
        if self._azimuth is not None:
            return self._azimuth
        else:
            raise ValueError('No heading received yet')

    def test(self):
        with open('calib_measurements.csv') as file:
            reader = csv.reader(file, delimiter='\t', quoting=csv.QUOTE_NONNUMERIC)

            for row in reader:
                self.calib_measurements.append(row)

            self.compute_calibration()

    def compute_calibration(self):
        data = np.array(self.calib_measurements)
        n = data.shape[0]

        t = data[:, 0]
        data = data[:, 1:]
        mean = data.sum(axis=0) / n
        data = data - mean  # remove offset

        # find rotation speed using a kind of Fourier transform
        amp_max = 0
        T_max = 0
        for T in np.linspace(T_CALIB / 20, T_CALIB, 1000):  # rotation period in s
            S = np.sin(2 * np.pi * t / T)
            C = np.cos(2 * np.pi * t / T)
            amp = np.sum(np.square(np.dot(S, data)) + np.square(np.dot(C, data)))
            if amp > amp_max:
                T_max = T
                amp_max = amp

        print(f"Rotation period: {T_max}s")

        data = data + mean  # restore offset

        # all measurements within the same step are averaged
        calib_data = np.zeros((STEPS, 3))
        nb_calib_data = np.zeros((STEPS, 1))
        steps = np.linspace(0, 360, STEPS, endpoint=False)
        for i in range(n):
            meas = data[i, :]
            step = math.floor(((t[i] / T_max) % 1.) * STEPS)
            calib_data[step, :] += meas
            nb_calib_data[step] += 1

        calib_data /= nb_calib_data
        self._calib_data = calib_data

        print("Calibrated")
        self._calibrated = True

        # recompute angle and error for all data point for verification
        angle = np.zeros((n, 1))
        err = np.zeros((n, 1))
        for i in range(n):
            angle[i], err[i] = self.compute_heading([data[i, 0], data[i, 1], data[i, 2]])

        # rebuild self.calib_measurements with added angle and err
        data = np.c_[t, data, angle, err]
        self.calib_measurements = list(data)

    def compute_heading(self, mag_field: list[float]) -> tuple[float, float]:
        meas = np.array(mag_field)
        # print(f"compute heading: meas={meas}")

        # compute distance from measurement to calibrated data to find the nearest calibrated point
        dist = np.linalg.norm(self._calib_data - meas, axis=1)
        nearest = np.argmin(dist)
        # print(dist)
        # print(f"compute heading: nearest={nearest}")

        # retrieve the actual angle by interpolation: projection of the measurement on the vector between the
        # calibrated points before and after the nearest point
        prev2next = self._calib_data[(nearest + 1) % STEPS, :] - self._calib_data[(nearest - 1) % STEPS, :]
        prev2meas = meas - self._calib_data[(nearest - 1) % STEPS, :]
        frac_idx = (nearest - 1) + np.dot(prev2meas, prev2meas) / np.dot(prev2next, prev2next) * 2
        frac_idx %= STEPS
        angle = frac_idx * 360. / STEPS
        err = np.linalg.norm(prev2meas - prev2next * np.dot(prev2meas, prev2next) / np.dot(prev2next, prev2next))
        # print(f"compute heading: frac_idx={frac_idx} angle={angle} err={err}")

        return angle, err

    def load_settings(self):
        try:
            with open('settings.dat', 'rb') as file:
                self._calibrated, self._calib_data, self.calib_offset, self.park_azimuth, self.home_azimuth = pickle.load(
                    file)
                print("settings loaded")
        except FileNotFoundError:
            print("settings.dat not found. Loading default settings")

    def save_settings(self):
        with open('settings.dat', 'wb') as file:
            pickle.dump(
                [self._calibrated, self._calib_data, self.calib_offset, self.park_azimuth, self.home_azimuth],
                file)
            print("settings saved")

    def turn_azimuth(self, azimuth):
        print("Turn azimuth not yet implemented")


