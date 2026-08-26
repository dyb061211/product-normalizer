class ProductNormalizerError(Exception):
    pass


class FileReadError(ProductNormalizerError):
    pass


class MissingRequiredColumnError(ProductNormalizerError):
    pass


class InvalidDataError(ProductNormalizerError):
    pass
