class BaseError(Exception):
    pass


class RequestError(BaseError):
    """Request exception for errors that have associated URLs."""
    def __init__(self, url, message):
        self.url = url
        BaseError.__init__(self, "%s: %s" % (url, message))

    def __reduce__(self):
        # For pickling purposes.
        return self.__class__, (None, self.url)
