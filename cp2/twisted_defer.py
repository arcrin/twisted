from twisted.internet.defer import Deferred


# d = Deferred()
#
#
# def cbPrint(result, positional, **kwargs):
#     print("result =", result, "positional =", positional, "kwargs =", kwargs)
#
#
# print(d.addCallback(cbPrint, "positional", keyword=1) is d)
#
# print(d.callback("result"))


d4 = Deferred()


def cbWillFail(number):
    return 1 / 0


def ebValueError(failure):
    failure.trap(ValueError)
    print("Failure was ValueError")


def ebTypeErrorAndZeroDivisionError(failure):
    exceptionType = failure.trap(TypeError, ZeroDivisionError)
    print("Failure was", exceptionType)

#
# d4.addCallback(cbWillFail)
# d4.addErrback(ebValueError)
# d4.addErrback(ebTypeErrorAndZeroDivisionError)
# d4.callback(0)

# d5 = Deferred()
# d5.addErrback(print)
#
# try:
#     1 / 0
# except:
#     d5.errback()

outerDeferred = Deferred()
def printAndPassThrough(result, *args):
    print("printAndPassThrough", " ".join(args), "received", result)
    return result

outerDeferred.addCallback(printAndPassThrough, '1')
innerDeferred = Deferred()
innerDeferred.addCallback(printAndPassThrough, '2', 'a')
innerDeferred.addCallback(printAndPassThrough, '2', 'b')

def returnInnerDeferred(result, number):
    print("returnInnerDeferred #", number, "received", result)
    print("Returning innerDeferred...")
    return innerDeferred.callback('inner result')

outerDeferred.addCallback(returnInnerDeferred, '2')
outerDeferred.addCallback(printAndPassThrough, '3')
outerDeferred.addCallback(printAndPassThrough, '4')



