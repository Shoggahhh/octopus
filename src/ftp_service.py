import ftplib
import os

from logger import logger
from settings import settings


class FTPClient:
    def __init__(
        self,
        ftp_host: str = settings.octopus_settings.ftp_host,
        ftp_user: str = settings.octopus_settings.ftp_user,
        ftp_password: str = settings.octopus_settings.ftp_password,
        ftp_path: str = settings.octopus_settings.ftp_path,
    ):
        self.brand = None
        self.ftp_host = ftp_host
        self.ftp_user = ftp_user
        self.ftp_password = ftp_password
        self.ftp_path = ftp_path

    def transfer_to_ftp(self) -> None:
        ftp_server = ftplib.FTP(self.ftp_host, self.ftp_user, self.ftp_password)
        ftp_server.encoding = "utf-8"

        error_code = ""
        try:
            ftp_server.cwd(f"{self.ftp_path}{self.brand}")
        except ftplib.all_errors as ex:
            error_code = str(ex).split(None, 1)[0]
            logger.error(ex)

        if error_code == "550":
            logger.info(f"create new directory: {self.ftp_path}{self.brand}")
            ftp_server.mkd(f"{self.ftp_path}{self.brand}")
            ftp_server.cwd(f"{self.ftp_path}{self.brand}")

        files = []
        for file in os.listdir(settings.octopus_settings.path_to_file):
            if self.brand == file.split(".")[0] and file.split(".")[-1] != "zip":
                path_to_file = f'{settings.octopus_settings.path_to_file}{self.brand}.{file.split(".")[-1]}'
                files.append(path_to_file)

        for i in files:
            try:
                logger.info("transfer file to ftp")
                with open(i, "rb") as file:
                    ftp_server.storbinary(f"STOR {os.path.basename(i)}", file)
                    data = ftplib.FTP.retrlines(ftp_server, "LIST")
                    logger.info(data)
            except Exception as ex:
                logger.error(f"{self.brand}: {ex}")

        ftp_server.quit()


ftp_client = FTPClient()
