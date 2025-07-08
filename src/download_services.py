import json

from urllib.parse import urlencode, quote

from exchangelib import Credentials, Account, DELEGATE, FileAttachment, EWSTimeZone

from datetime import datetime

from file_service import FileDownloader
from logger import logger
import requests
from settings import settings


class DownloaderFromLinkAuth(FileDownloader):
    def __init__(self, brand: str):
        super().__init__(brand)

    def download(
        self,
        tag_login: str,
        tag_password: str,
        login: str,
        password: str,
        base_url: str,
        url_to_file: str,
    ) -> None:
        logger.info(f"\n{self.brand}")

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
            with open(
                f"{settings.octopus_settings.path_to_file}{self.brand}.xlsx", "wb"
            ) as f:
                f.write(get_file.content)

            logger.info(
                f"status code: {get_file.status_code} {self.brand}: download is complete"
            )
        except Exception as ex:
            logger.error(f"{self.brand}: {ex}")


class DownloaderFromLink(FileDownloader):
    def __init__(self, brand: str):
        super().__init__(brand)

    def download(self, url: str) -> None:

        logger.info(f"\n{self.brand}")
        logger.info("request to file")
        try:
            get_file = requests.get(url)

            with open(
                f'{settings.octopus_settings.path_to_file}{self.brand}.{url.split(".")[-1]}',
                "wb",
            ) as f:
                f.write(get_file.content)

            logger.info(
                f"status code: {get_file.status_code} {self.brand}: download is complete"
            )
        except Exception as ex:
            logger.error(f"{self.brand}: {ex}")


class DownloaderFromOutlookExchange(FileDownloader):
    def __init__(self, brand: str):
        super().__init__(brand)

    def download(self, sender: str, theme_of_message: str) -> None:

        logger.info(f"\n{self.brand}")

        credentials = Credentials(
            settings.octopus_settings.email, settings.octopus_settings.email_password
        )
        account = Account(
            primary_smtp_address=settings.octopus_settings.email,
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
                            f"{settings.octopus_settings.path_to_file}/{self.brand}.{str(att.name).split('.')[-1]}",
                            "wb",
                        ) as f:
                            f.write(att.content)
                        logger.info(f"file is saved")
                    else:
                        logger.info("file not found")
                break
        except Exception as ex:
            logger.error(f"{self.brand}: {ex}")


class DownloaderFromMailRu(FileDownloader):
    def __init__(self, brand: str):
        super().__init__(brand)

    def download(self, url: str, name: str) -> None:
        logger.info(f"\n{self.brand}")
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
                f'{settings.octopus_settings.path_to_file}{self.brand}.{file_name.split(".")[-1]}',
                "wb",
            ) as f:
                f.write(file_xlsx)
                return None

        except requests.exceptions.HTTPError as ex:
            logger.error(ex)
            return None


class DownloaderFromYandex(FileDownloader):
    def __init__(self, brand: str):
        super().__init__(brand)

    def download(self, url: str, file_name: str, format_file_xlsx: str) -> None:

        logger.info(f"\n{self.brand}")
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
                path_to_file = f"{settings.octopus_settings.path_to_file}/{self.brand}.{format_file_xlsx}"
                with open(path_to_file, "wb") as f:
                    f.write(file)

        except Exception as ex:
            logger.error(ex)


class DownloaderFromGoogle(FileDownloader):
    def __init__(self, brand: str):
        super().__init__(brand)

    def download(self, url: str, format_file: str) -> None:

        logger.info(f"\n{self.brand}")
        try:
            params = {
                "format": f"{format_file}",
            }
            response = requests.get(url, params=params)
            response.raise_for_status()

            logger.info(f"status_code: {response.status_code}")

            with open(
                f'{settings.octopus_settings.path_to_file}{self.brand}.{params.get("format")}',
                "wb",
            ) as f:
                f.write(response.content)
        except Exception as ex:
            logger.error(ex)
