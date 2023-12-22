import ftplib
import json
import os
import shutil
from datetime import date
from pathlib import Path
from urllib.parse import urlencode
from zipfile import ZipFile

import requests
from loguru import logger
from settings import OCTOPUS_SETTINGS

import win32com.client as win32


class Octopus:
    def __init__(self, brand):
        self.BRAND = brand
        self.FTP_HOST = '5.188.156.224'
        self.FTP_USER = OCTOPUS_SETTINGS.get('FTP_USER')
        self.FTP_PASSWORD = OCTOPUS_SETTINGS.get('FTP_PASSWORD')
        self.FTP_PATH = '/input/b85f50c4-b985-11ec-a5fc-020017000b7b/'
        self.PATH_TO_FILE = 'C:/Users/grinev.TL/PycharmProjects/octopus/files/'

    def auth_and_download_from_link(self, tag_login, tag_password, login, password, base_url, url_to_file):
        logger.info(f'\n{self.BRAND}')

        session = requests.Session()

        user = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0'
        headers = {
            'user-agent': user
        }

        data = {
            tag_login: login,
            tag_password: password,
        }
        try:
            logger.info('authorization...')

            session.post(base_url, data=data, headers=headers)

            logger.info('authorization completed')

            logger.info('request to file')

            get_file = session.get(url_to_file, headers=headers)

            with open(f'{self.PATH_TO_FILE}{self.BRAND}.xlsx', 'wb') as f:
                f.write(get_file.content)

            logger.info(f'status code: {get_file.status_code} {self.BRAND}: download is complete')
        except Exception as ex:
            logger.error(f'{self.BRAND}: {ex}')

    def get_file_from_link(self, url):
        logger.info(f'\n{self.BRAND}')
        logger.info('request to file')
        try:
            get_file = requests.get(url)

            with open(f'{self.PATH_TO_FILE}{self.BRAND}.{url.split(".")[-1]}', 'wb') as f:
                f.write(get_file.content)

            logger.info(f'status code: {get_file.status_code} {self.BRAND}: download is complete')
        except Exception as ex:
            logger.error(f'{self.BRAND}: {ex}')

    def find_massage_from_outlook(self, sender, theme_of_message):
        logger.info(f'\n{self.BRAND}')
        outlook = win32.Dispatch('Outlook.Application').GetNamespace('MAPI')

        main_folder = outlook.Folders.Item(2)
        sub_folder = main_folder.Folders('Входящие').Folders('ОСТАТКИ')
        # folder = outlook.GetDefaultFolder(6)

        messages = sub_folder.Items
        today_now = date.today()
        found = 0
        try:
            for message in messages:
                if message.SenderEmailAddress == sender and message.Subject == f'{theme_of_message}{today_now.strftime("%d.%m.%Y")}':
                    found += 1

                    logger.info('Message found')
                    logger.info('get attachments')

                    for att in message.Attachments:
                        att.SaveAsFile(f'{self.PATH_TO_FILE}{self.BRAND}.{str(att).split(".")[-1]}')
                    logger.info(f'{self.BRAND}: file saved')
            if found == 0:
                return logger.error(f'{self.BRAND}: file not found')
        except Exception as ex:
            logger.error(f'{self.BRAND}: {ex}')

    def get_file_from_mailru(self, url, name):
        logger.info(f'\n{self.BRAND}')
        id_mailru = f'{url.split("/")[-2]}/{url.split("/")[-1]}'
        api_mailru = f'https://cloud.mail.ru/api/v4/public/list?weblink={id_mailru}'

        file_name = ''

        try:
            response = requests.get(api_mailru)
            response.raise_for_status()

            logger.info(f'status_code: {response.status_code}')

            response = response.text
            data = json.loads(response)

            check = False
            for item in data['list']:
                data_name = item['name']
                if name.lower() in data_name.lower():
                    check = True
                    file_name = item['weblink'].split('/')[-1]
                    logger.info(f'"{name}" found')
                    break

            if check is False:
                return logger.error(f'"{name}" not found')

        except requests.exceptions.HTTPError as ex:
            logger.error(ex)

        try:
            temp = requests.get(url)
            temp.raise_for_status()

            logger.info(f'status_code: {temp.status_code}')

            temp = temp.text

            link = temp.partition('"weblink_get":')[2].partition(',"weblink_thumbnails"')[0]
            link = link.partition('"url":"')[2].partition('"')[0] + f'/{id_mailru}/{file_name}'

            file_xlsx = requests.get(link).content

            with open(f'{self.PATH_TO_FILE}{self.BRAND}.{file_name.split(".")[-1]}', 'wb') as f:
                f.write(file_xlsx)

        except requests.exceptions.HTTPError as ex:
            logger.error(ex)

    def get_file_from_yandex(self, url, file_name=None):
        logger.info(f'\n{self.BRAND}')
        format_xlsx = ['xls', 'xlsx', 'csv']

        base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
        public_key = url

        yandex_url = base_url + urlencode(dict(public_key=public_key))

        try:
            response = requests.get(yandex_url)
            download_url = response.json()['href']
            format_file = response.json()["href"].split('&')[1].split('.')[-1]

            download_response = requests.get(download_url).content

            fln = f'{self.PATH_TO_FILE}{self.BRAND}.{format_file}'
            with open(fln, 'wb') as f:
                f.write(download_response)

            if format_file not in format_xlsx:
                zip_file = ZipFile(fln)
                with ZipFile(zip_file.filename, 'r') as zip_file:
                    list_of_file_names = zip_file.namelist()

                    logger.info(f'files from zip: {list_of_file_names}')

                    for member in list_of_file_names:
                        if file_name in member:
                            name = os.path.basename(member)

                            logger.info(f'name is found: {name}')

                            source = zip_file.open(member)
                            target = open(os.path.join(f'{self.PATH_TO_FILE}', f'{self.BRAND}.{name.split(".")[-1]}'), 'wb')
                            with source, target:
                                shutil.copyfileobj(source, target)
        except Exception as ex:
            logger.error(ex)


    def transfer_to_ftp(self):
        ftp_server = ftplib.FTP(self.FTP_HOST, self.FTP_USER, self.FTP_PASSWORD)
        ftp_server.encoding = 'utf-8'

        error_code = ''
        try:
            ftp_server.cwd(f'{self.FTP_PATH}{self.BRAND}')
        except ftplib.all_errors as ex:
            error_code = str(ex).split(None, 1)[0]
            logger.error(ex)

        if error_code == "550":
            logger.info(f"create new directory: {self.FTP_PATH}{self.BRAND}")
            ftp_server.mkd(f'{self.FTP_PATH}{self.BRAND}')
            ftp_server.cwd(f'{self.FTP_PATH}{self.BRAND}')

        path_to_file = ''
        files = []
        for file in os.listdir(self.PATH_TO_FILE):
            if self.BRAND == file.split(".")[0] and file.split(".")[-1] != 'zip':
                path_to_file = f'{self.PATH_TO_FILE}{self.BRAND}.{file.split(".")[-1]}'
                files.append(path_to_file)

        for i in files:
            try:
                logger.info('transfer file to ftp')
                with open(path_to_file, "rb") as file:
                    ftp_server.storbinary(f'STOR {os.path.basename(i)}', file)
                    data = ftplib.FTP.retrlines(ftp_server, 'LIST')
                    logger.info(data)
            except Exception as ex:
                logger.error(f'{self.BRAND}: {ex}')

        ftp_server.quit()

