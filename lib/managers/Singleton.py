class Singleton(type):
    """A metaclass making any class into a singelton pattern class"""

    _instances = {}

    def __call__(cls, *args, **kwargs): # type: ignore
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]

    @staticmethod
    def reset(reset_class: object = None) -> None:
        """Resets all singelton classes"""
        if not reset_class:
            Singleton._instances = {}
            return

        if reset_class in Singleton._instances:
            Singleton._instances.pop(reset_class)