# vim: tabstop=4 shiftwidth=4 expandtab foldmethod=marker :

"""asynchronous wrapper around machine.I2C and machine.SoftI2C"""

# Copyright (c) 2026 Tamas Tevesz <ice@extreme.hu>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from machine import I2C, SoftI2C
import asyncio

def with_lock(func):

    async def _with_lock(self, *args, **kwargs):
        async with self._lock:
            res = getattr(self._bus, func.__name__)(*args, **kwargs)
        await asyncio.sleep_ms(0)
        return res

    return _with_lock

class _as_I2C:

    def __init__(self, *args, **kwargs):
        self._lock = asyncio.Lock()

    @with_lock
    async def scan(self, *args, **kwargs):
        return self._bus.scan(*args, **kwargs)

    @with_lock
    async def start(self, *args, **kwargs):
        return self._bus.start(*args, **kwargs)

    @with_lock
    async def stop(self, *args, **kwargs):
        return self._bus.stop(*args, **kwargs)

    @with_lock
    async def readinto(self, *args, **kwargs):
        return self._bus.readinto(*args, **kwargs)

    @with_lock
    async def write(self, *args, **kwargs):
        return self._bus.write(*args, **kwargs)

    @with_lock
    async def readfrom(self, *args, **kwargs):
        return self._bus.readfrom(*args, **kwargs)

    @with_lock
    async def readfrom_into(self, *args, **kwargs):
        return self._bus.readfrom_into(*args, **kwargs)

    @with_lock
    async def writeto(self, *args, **kwargs):
        return self._bus.writeto(*args, **kwargs)

    @with_lock
    async def writevto(self, *args, **kwargs):
        return self._bus.writevto(*args, **kwargs)

    @with_lock
    async def readfrom_mem(self, *args, **kwargs):
        return self._bus.readfrom_mem(*args, **kwargs)

    @with_lock
    async def readfrom_mem_into(self, *args, **kwargs):
        return self._bus.readfrom_mem_into(*args, **kwargs)

    @with_lock
    async def writeto_mem(self, *args, **kwargs):
        return self._bus.writeto_mem(*args, **kwargs)

class aI2C(_as_I2C):
    """This class wraps machine.I2C with bus accesses guarded by an instance-specific
       asyncio.Lock, making handling devices on an I2C bus from asyncio tasks trivial.
    """

    def __init__(self, *args, **kwargs):
        """Construct and return a new asynchronous I2C object. The arguments are
           the same as for machine.I2C (see the machine.I2C documentation).

           All methods supported by machine.I2C are wrapped such that access to
           the bus is guarded by an instance-specific asyncio.Lock.

           This class wraps machine.I2C (i.e. the hardware I2C implementations).
        """
        self._bus = I2C(*args, **kwargs)
        super().__init__()

class aSoftI2C(_as_I2C):

    def __init__(self, *args, **kwargs):
        """Construct and return a new asynchronous I2C object. The arguments are
           the same as for machine.SoftI2C (see the machine.SoftI2C documentation).

           All methods supported by machine.SoftI2C are wrapped such that access to
           the bus is guarded by an instance-specific asyncio.Lock.

           This class wraps machine.SoftI2C (i.e. the software I2C implementations).
        """
        self._bus = SoftI2C(*args, **kwargs)
        super().__init__()
