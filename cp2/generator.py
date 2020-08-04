def generatorFunction():
    print("Begin")
    yield 1
    print("Continue")
    yield 2


g = generatorFunction()


def receivingGenerator():
    print("Begin")
    x = 1
    y = yield x
    print("Continue")
    z = yield x + y
    print("sum", x + y + z)

rg = receivingGenerator()


def failingGenertor():
    try:
        value = yield
    except ValueError:
        print("Caught ValueError")

# tracebackG = failingGenertor()
# next(tracebackG)
# tracebackG.throw(TypeError)

catchingG = failingGenertor()
next(catchingG)
catchingG.throw(ValueError)