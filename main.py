from settings import settings
from download_services import (
    DownloaderFromYandex,
    DownloaderFromGoogle,
    DownloaderFromMailRu,
    DownloaderFromLinkAuth,
    DownloaderFromLink,
    DownloaderFromOutlookExchange,
)
from file_service import FileDownloader
from ftp_service import ftp_client

if __name__ == "__main__":

    """
    Example:

    my_brand = DownloaderFromYandex("my_brand")
    my_brand.download("some_url", "file_name", "xls")

    """
    my_brand = DownloaderFromYandex("my_brand")
    my_brand.download("some_url", "file_name", "xls")
    ftp_client.transfer_to_ftp()
