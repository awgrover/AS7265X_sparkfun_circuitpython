import struct
from adafruit_bus_device.i2c_device import I2CDevice

class Device:
    """Class for communicating with an I2C device.

    Allows reading and writing 8-bit, 16-bit, and byte array values to
    registers on the device."""

    def __init__(self, address, i2c):
        """Create an instance of the I2C device at the specified address using
        the specified I2C interface object."""
        self._address = address
        self._i2c = i2c
        self.i2c_device = I2CDevice(i2c, address)
        self.buf2 = bytearray(2)

    def writeRaw8(self, value):
        """Write an 8-bit value on the bus (without register)."""
        value = value & 0xFF
        self._i2c.writeto(self._address, value.to_bytes(1, "little"))

    def write8(self, register, value):
        """Write an 8-bit value to the specified register."""
        value = value & 0xFF
        buf = self.buf2
        buf[0] = register
        buf[1] = value
        with self.i2c_device as i2c:
            i2c.write(buf)

        #self._i2c.writeto_mem(self._address, register, value.to_bytes(1, "little"))

    def write16(self, register, value):
        """Write a 16-bit value to the specified register."""
        value = value & 0xFFFF
        self.i2c.writeto_mem(self._address, register, value)

    def writeBlock(self, register, value):
        self._i2c.writeto_mem(self._address, register, value)

    def readBlock(self, register, nbytes):
        return self._i2c.readfrom_mem(self._address, register, nbytes)

    def readRaw8(self):
        """Read an 8-bit value on the bus (without register)."""
        return int.from_bytes(self._i2c.readfrom(self._address, 1),
                              'little' ) & 0xFF

    def readU8(self, register):
        """Read an unsigned byte from the specified register."""
        buf = self.buf2
        buf[0] = register
        with self.i2c_device as i2c:
            i2c.write(buf, end=1)
            i2c.readinto(buf, end=1)
        return buf[0]

        return int.from_bytes(
            self._i2c.readfrom_mem(self._address, register, 1), 'little') & 0xFF

    def readS8(self, register):
        """Read a signed byte from the specified register."""
        result = self.readU8(register)
        if result > 127:
            result -= 256
        return result

    def readU16(self, register, little_endian=True):
        """Read an unsigned 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        result = int.from_bytes(
            self._i2c.readfrom_mem(self._address, register, 2),
            'little' if little_endian else 'big') & 0xFFFF
        return result

    def readS16(self, register, little_endian=True):
        """Read a signed 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        result = self.readU16(register, little_endian)
        if result > 32767:
            result -= 65536
        return result

    def readU16LE(self, register):
        """Read an unsigned 16-bit value from the specified register, in little
        endian byte order."""
        return self.readU16(register, little_endian=True)

    def readU16BE(self, register):
        """Read an unsigned 16-bit value from the specified register, in big
        endian byte order."""
        return self.readU16(register, little_endian=False)

    def readS16LE(self, register):
        """Read a signed 16-bit value from the specified register, in little
        endian byte order."""
        return self.readS16(register, little_endian=True)

    def readS16BE(self, register):
        """Read a signed 16-bit value from the specified register, in big
        endian byte order."""
        return self.readS16(register, little_endian=False)
