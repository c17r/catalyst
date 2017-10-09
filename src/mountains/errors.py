
class MountainException(Exception):
    pass


class RetrieveError(MountainException):
    pass


class MissingDataError(MountainException):
    pass


class InvalidDataError(MountainException):
    pass
