def requestFieldDeferred(url, field):
    d = nonblockingGet(url)

    def onCompletion(response):
        document = json.load(response)
        return document[field]

    def onFailure(failure):
        failure.trap(UnicodeDecodeError)

    d.addCallback(onCompletion)
    d.addErrback(onFailure)

    return d


def requestFieldGenerator(url, field):
    try:
        document = yield nonblockingGet(url)
    except UnicodeDecodeError:
        pass
    document = json.load(response)
    return document[field]

