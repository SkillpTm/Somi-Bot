class Singleton(type):
    """A metaclass making any class into a singelton pattern class"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]

    @staticmethod
    def reset():
        """Resets all singelton classes"""
        Singleton._instances = {}