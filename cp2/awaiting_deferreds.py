from twisted.internet.defer import Deferred, ensureDeferred, DeferredList, gatherResults
import operator

# async def awaitFutureLike(obj):
#     result = await obj
#     print(result)


# obj = Deferred()
# coro = awaitFutureLike(obj)
# assert coro.send(None) is obj
# obj.callback("the result")
# try:
#     coro.send(None)
# except StopIteration:
#     pass

# d = Deferred()
#
#
# def cb1(result):
#     print(result, "was received by cb1")
#     return result
#
#
# def cb2(result):
#     print(result + 2)
#     return result + 2
#
# d.addCallback(cb1)
# d.addCallback(cb2)
#
#
# async def awaitDeferred():
#     await d
#     print("end")
#
# g = awaitDeferred()

# async def asyncIncrement(d):
#     x = await d
#     return x + 1
#
# awaited = Deferred()
# deferred_add = ensureDeferred(asyncIncrement(awaited))
# deferred_add.addCallback(print)
# awaited.callback(1)


# url1 = Deferred()
# url2 = Deferred()
# urlList = DeferredList([url1, url2])
# urlList.addCallback(print)
# url2.callback("url2")
# url1.callback("url1")


# noValue = Deferred()
# getsValue = Deferred()
# waitsForOne = DeferredList([noValue, getsValue], fireOnOneCallback=True)
# waitsForOne.addCallback(print)
# getsValue.callback("the value")


d1, d2 = Deferred(), Deferred()
results = gatherResults([d1, d2])
results.addCallback(print)
d1.callback(1)
d2.callback(2)
