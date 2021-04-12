import abc


class ISerializable(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def serialize(self): ...

    @staticmethod
    @abc.abstractmethod
    def deserialize(d: dict): ...

