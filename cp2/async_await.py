# async def function():
#     pass
#
#
# async def returnsValue(value):
#     return 1
#
#
# async def awaitsCoroutine(c):
#     value = await c
#     print(value)
#
#
# def plainGenerator():
#     yield 1
#
#
# async def brokenCoroutineAwaitsGenerator():
#     await plainGenerator()
#
# def g1():
#     yield from g2
#
#
# def g2():
#     yield from g3
#
#
# def g3():
#     yield from g4
#
#
# def g4():
#     yield from g5
#
#
# def g5():
#     yield 1
#
#
# import types
# @types.coroutine
# def makeBase():
#     return (yield "hello from  a base object")
#
#
# async def awaitsBase(base):
#     value = await base
#     print("From awaitsBase:", value)
#
#
# awaiter = awaitsBase(makeBase())
#

class FutureLike(object):
    _MISSING = "MISSING"

    def __init__(self):
        self.result = self._MISSING

    def __next__(self):
        if self.result is self._MISSING:
            return self
        raise StopIteration(self.result)

    def __iter__(self):
        return self

    def __await__(self):
        return iter(self)


async def awaitFutureLike(obj):
    result = await obj
    print(result)

obj = FutureLike()
coro = awaitFutureLike(obj)
assert coro.send(None) is obj
obj.result = "the result"
try:
    coro.send(None)
except StopIteration:
    pass
