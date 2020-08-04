import requests
import json


def requestField(url, field):
    results = requests.get(url).json()
    return results[field]


def someOtherFunction(...):
    ...
    url = calculateURL(...)
    value = requestsField(url, 'someInteger')
    return value + 1

x = someOtherFunction(...)


def someOtherFunction(value):
    return value + 1

x = someOtherFunction(requestField(calculateURL(...), 'someInteger'))


def requestField(url, field):
    def onCompletion(response):
        document = json.loads(response)
        value = response[field]

    nonblockingGet(url, onCompletion=onCompletion)


def requestField(url, field, useField):
    def onCompletion(response):
        document = json.loads(response)
        value = response[field]
        useField(value)

    nonblockingGet(url, onCompletion=onCompletion)


def someOtherFunction(useValue):
    url = calculateURL(...)
    def addValue(value):
        useValue(value + 1)
    requestField(url, "someInteger", useField=addValue)