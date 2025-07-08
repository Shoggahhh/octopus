from abc import ABC, abstractmethod


class FileDownloader(ABC):
    def __init__(self, brand: str):
        if not brand:
            raise ValueError("Brand is must provided")
        self.brand = brand

    @abstractmethod
    def download(self, **kwargs):
        pass
