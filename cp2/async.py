def requetField(url, field):
    def onCompletion(response):
        document = json.load(response)

        return  document[field]

    placeholder = nonblockingGet(url)
    return placeholder.addCallback(onCompletion)


def someOtherFunction(...):
    url = calculateURL(...)
    def addValue(value):
        return value + 1
    placeholder = requetField(url, "someInteger")
    return placeholder.addCallback(addValue)


def manyCallbacks(url, useValue, ...):
    def addValue(result):
        return divideValue(result + 2)

    def divideValue(result):
        return multiplyValue(result // 3)

    def multiplyValue(result):
        return uesValuse(result * 4)

def manyCallbacks(url, ...):
    def addValue(result):
        return result + 2

    def divideValue(result):
        return result // 3

    def multiplyValue(result):
        return result * 4

    placeholder = requestField(url, "someInteger")
    placeholder.addCallback(addValue)
    placeholder.addCallback(divideValue)
    placeholder.addCallback(multiplyValue)
    return placeholder


class Deferred(object):
    def __init__(self):
        self._callbacks = []

    def addCallbacks(self, callback):
        self._callbacks.append(callback)

    def callback(self, result):
        for callback in self._callbacks:
            result = callback(result)

def requestField(url):
    response = requests.get(url).content
    try:
        return response.decode('utf-8')
    except UnicodeDecodeError:
        # Handle this case


def passthrough(obj):
    return obj


class Deferred(object):
    def __init__(self):
        self._callbacks = []

    def addCallback(self, callback):
        self._callbacks.append((callback, passthrough))

    def addErrbacl(self, errback):
        self._callbacks.append((passthrough, errback))

    def callback(self, result):
        for callback, errback in self._callbacks:
            if isinstance(result, BaseException):
                handler = errback
            else:
                handler = callback
            try:
                result = handler(result)
            except BaseException as e:
                result = e

