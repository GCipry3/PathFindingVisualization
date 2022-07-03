import time


def timeIt(fun):
    def wrapper(*args, **kwargs):
        start = time.time()
        output = fun(*args, **kwargs)
        end = time.time()
        print("The {} function lasted {} ns".format(fun.__name__, int((end - start)*1000000000)))
        return output

    return wrapper
