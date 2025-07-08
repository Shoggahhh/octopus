import ftplib
import json
import os

# import shutil
# from datetime import date
from urllib.parse import urlencode, quote

# from zipfile import ZipFile

from exchangelib import Credentials, Account, DELEGATE, FileAttachment, EWSTimeZone

from datetime import datetime
from logger import logger
import requests
from settings import settings

# import win32com.client as win32


class Octopus:
    def __init__(self, brand):
        self.BRAND = brand
        self.FTP_HOST = settings.octopus_settings.ftp_host
        self.FTP_USER = settings.octopus_settings.ftp_user
        self.FTP_PASSWORD = settings.octopus_settings.ftp_password
        self.FTP_PATH = settings.octopus_settings.ftp_path
        self.PATH_TO_FILE = settings.octopus_settings.path_to_file

        self.EMAIL = settings.octopus_settings.email
        self.PASSWORD = settings.octopus_settings.password

    def auth_and_download_from_link(
        self,
        tag_login: str,
        tag_password: str,
        login: str,
        password: str,
        base_url: str,
        url_to_file: str,
    ) -> None:
        """
        :param tag_login: Имя поля, которое хранится в теге login
        :param tag_password: Имя поля, которое хранится в теге password
        :param login: Логин, который нужно написать в поле login
        :param password: Пароль, который нужно написать в поле login
        :param base_url: Страница, где требуется аутентификация
        :param url_to_file: Ссылка до файла, который нужно скачать
        :return:

        Метод, если требуется скачать файл с сайта, где требуется аутентификация

        """
        logger.info(f"\n{self.BRAND}")

        session = requests.Session()

        user = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
        headers = {"user-agent": user}

        data = {
            tag_login: login,
            tag_password: password,
        }
        try:
            logger.info("authorization...")

            session.post(base_url, data=data, headers=headers)

            logger.info("authorization completed")

            logger.info("request to file")

            get_file = session.get(url_to_file, headers=headers)

            with open(f"{self.PATH_TO_FILE}{self.BRAND}.xlsx", "wb") as f:
                f.write(get_file.content)

            logger.info(
                f"status code: {get_file.status_code} {self.BRAND}: download is complete"
            )
        except Exception as ex:
            logger.error(f"{self.BRAND}: {ex}")

    def get_file_from_link(self, url: str) -> None:
        """
        :param url: Ссылка до файла
        :return:
        Метод для скачивания файла по прямой ссылке
        """
        logger.info(f"\n{self.BRAND}")
        logger.info("request to file")
        try:
            get_file = requests.get(url)

            with open(
                f'{self.PATH_TO_FILE}{self.BRAND}.{url.split(".")[-1]}', "wb"
            ) as f:
                f.write(get_file.content)

            logger.info(
                f"status code: {get_file.status_code} {self.BRAND}: download is complete"
            )
        except Exception as ex:
            logger.error(f"{self.BRAND}: {ex}")

    def find_massage_from_outlook_exchange(
        self, sender: str, theme_of_message: str
    ) -> None:
        """
        :param sender: Отправитель
        :param theme_of_message: Тема письма
        :return:

        Метод для скачивания файла с Outlook
        """
        logger.info(f"\n{self.BRAND}")

        credentials = Credentials(self.EMAIL, self.PASSWORD)
        account = Account(
            primary_smtp_address=self.EMAIL,
            credentials=credentials,
            autodiscover=True,
            access_type=DELEGATE,
        )

        moscow_tz = EWSTimeZone("Europe/Moscow")
        today_moscow = datetime.now(moscow_tz).date()

        try:
            for item in account.inbox.filter(
                sender=sender, subject__contains=theme_of_message
            ).order_by("-datetime_received"):
                moscow_received = item.datetime_received.astimezone(moscow_tz)
                if moscow_received.date() != today_moscow:
                    continue
                for att in item.attachments:
                    if isinstance(att, FileAttachment):
                        with open(
                            f"{self.PATH_TO_FILE}/{self.BRAND}.{str(att.name).split('.')[-1]}",
                            "wb",
                        ) as f:
                            f.write(att.content)
                        logger.info(f"file is saved")
                    else:
                        logger.info("file not found")
                break
        except Exception as ex:
            logger.error(f"{self.BRAND}: {ex}")

    # def find_massage_from_outlook(self, sender: str, theme_of_message: str) -> None:
    #     """
    #     :param sender: Отправитель
    #     :param theme_of_message: Тема письма
    #     :return:
    #
    #     Метод для скичавания файла с Outlook
    #     Метод работает только на Windows для поиска файла на почте Outlook
    #     Чтобы работать с web версией нужно зарегестрировать приложение на Azure
    #
    #     """
    #     logger.info(f"\n{self.BRAND}")
    #     outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
    #
    #     main_folder = outlook.Folders.Item(2)
    #     sub_folder = main_folder.Folders("Входящие").Folders("ОСТАТКИ")
    #     # folder = outlook.GetDefaultFolder(6)
    #
    #     messages = sub_folder.Items
    #     messages.Sort("[ReceivedTime]", True)
    #     today_now = date.today()
    #     try:
    #         for message in messages:
    #             if (
    #                 message.SenderEmailAddress == sender
    #                 and message.Subject == theme_of_message
    #                 and message.ReceivedTime.date() == today_now
    #             ):
    #                 logger.info("Message found")
    #                 logger.info("get attachments")
    #                 try:
    #                     for att in message.Attachments:
    #                         att.SaveAsFile(
    #                             f'{self.PATH_TO_FILE}{self.BRAND}.{str(att).split(".")[-1]}'
    #                         )
    #                         logger.info(f"{self.BRAND}: file saved")
    #                 except Exception as ex:
    #                     logger.error(f"{self.BRAND} - {ex}: file not found")
    #     except Exception as ex:
    #         logger.error(f"{self.BRAND}: {ex}")

    def get_file_from_mailru(self, url: str, name: str) -> None:
        """
        :param url: Ссылка на файлы
        :param name: Имя файла
        :return:

        Метод для скачивания файла с mail диск
        """
        logger.info(f"\n{self.BRAND}")
        id_mailru = f'{url.split("/")[-2]}/{url.split("/")[-1]}'
        api_mailru = f"https://cloud.mail.ru/api/v4/public/list?weblink={id_mailru}"

        file_name = ""

        try:
            response = requests.get(api_mailru)
            response.raise_for_status()

            logger.info(f"status_code: {response.status_code}")

            response = response.text
            data = json.loads(response)

            check = False
            for item in data["list"]:
                data_name = item["name"]
                if name.lower() in data_name.lower():
                    check = True
                    file_name = item["weblink"].split("/")[-1]
                    logger.info(f'"{name}" found')
                    break

            if check is False:
                return logger.error(f'"{name}" not found')

        except requests.exceptions.HTTPError as ex:
            logger.error(ex)

        try:
            temp = requests.get(url)
            temp.raise_for_status()

            logger.info(f"status_code: {temp.status_code}")

            temp = temp.text

            link = temp.partition('"weblink_get":')[2].partition(
                ',"weblink_thumbnails"'
            )[0]
            link = (
                link.partition('"url":"')[2].partition('"')[0]
                + f"/{id_mailru}/{file_name}"
            )

            file_xlsx = requests.get(link).content

            with open(
                f'{self.PATH_TO_FILE}{self.BRAND}.{file_name.split(".")[-1]}', "wb"
            ) as f:
                f.write(file_xlsx)
                return None

        except requests.exceptions.HTTPError as ex:
            logger.error(ex)
            return None

    def get_file_from_yandex(
        self, url: str, file_name: str, format_file_xlsx: str = None
    ) -> None:
        """
        :param url: Ссылка на диск
        :param file_name: Имя файла на диске
        :param format_file_xlsx: Формат файла нужно указать, если есть два файла с одинаковыми названиями
        :return:

        Метод для скачивания файла с yandex диск
        """
        logger.info(f"\n{self.BRAND}")
        format_xlsx = ["xls", "xlsx", "csv"]

        if format_file_xlsx not in format_xlsx and format_file_xlsx is not None:
            logger.error("this format file is not excel")
            raise "this format file is not excel"

        base_url = "https://cloud-api.yandex.net/v1/disk/public/resources?"
        params = {"public_key": url}

        yandex_url = base_url + urlencode(query=params, safe="/", quote_via=quote)

        try:
            response = requests.get(yandex_url)
            data_json = response.json()
            urls = []
            for item in data_json["_embedded"]["items"]:
                name = item["name"]
                if file_name in name and name.split(".")[-1] == format_file_xlsx:
                    urls.append(item["file"])

            for url_file in urls:
                file = requests.get(url_file).content
                path_to_file = f"{self.PATH_TO_FILE}{self.BRAND}.{format_file_xlsx}"
                with open(path_to_file, "wb") as f:
                    f.write(file)

        except Exception as ex:
            logger.error(ex)

    def get_file_from_google(self, url: str, format_file: str) -> None:
        """
        :param url: ссылка на google диск
        :param format_file: формат файла, требуется указывать для params
        :return:

        Метод для скачивания файла с google диск
        """
        logger.info(f"\n{self.BRAND}")
        try:
            params = {
                "format": f"{format_file}",
            }
            response = requests.get(url, params=params)
            response.raise_for_status()

            logger.info(f"status_code: {response.status_code}")

            with open(
                f'{self.PATH_TO_FILE}{self.BRAND}.{params.get("format")}', "wb"
            ) as f:
                f.write(response.content)
        except Exception as ex:
            logger.error(ex)

    def transfer_to_ftp(self) -> None:
        """
        Метод для отправки файла на FTP, откуда потом цены и остатки подхватит 1С
        """
        ftp_server = ftplib.FTP(self.FTP_HOST, self.FTP_USER, self.FTP_PASSWORD)
        ftp_server.encoding = "utf-8"

        error_code = ""
        try:
            ftp_server.cwd(f"{self.FTP_PATH}{self.BRAND}")
        except ftplib.all_errors as ex:
            error_code = str(ex).split(None, 1)[0]
            logger.error(ex)

        if error_code == "550":
            logger.info(f"create new directory: {self.FTP_PATH}{self.BRAND}")
            ftp_server.mkd(f"{self.FTP_PATH}{self.BRAND}")
            ftp_server.cwd(f"{self.FTP_PATH}{self.BRAND}")

        # path_to_file = ""
        files = []
        for file in os.listdir(self.PATH_TO_FILE):
            if self.BRAND == file.split(".")[0] and file.split(".")[-1] != "zip":
                path_to_file = f'{self.PATH_TO_FILE}{self.BRAND}.{file.split(".")[-1]}'
                files.append(path_to_file)

        for i in files:
            try:
                logger.info("transfer file to ftp")
                with open(i, "rb") as file:
                    ftp_server.storbinary(f"STOR {os.path.basename(i)}", file)
                    data = ftplib.FTP.retrlines(ftp_server, "LIST")
                    logger.info(data)
            except Exception as ex:
                logger.error(f"{self.BRAND}: {ex}")

        ftp_server.quit()
