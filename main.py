from octopus import Octopus
from settings import OCTOPUS_SETTINGS
from datetime import date

from for_logger import log_this

if __name__ == '__main__':
    log_this()

    livolo = Octopus("Livolo")
    livolo.get_file_from_mailru("https://cloud.mail.ru/public/1ZWJ/4ncMnVjVa", "Прайс")
    livolo.transfer_to_ftp()

    rocket_socket = Octopus("Rocket_socket")
    rocket_socket.get_file_from_mailru("https://cloud.mail.ru/public/1ZWJ/4ncMnVjVa", "Прайс")
    rocket_socket.transfer_to_ftp()

    welrok = Octopus("Welrok")
    welrok.get_file_from_mailru("https://cloud.mail.ru/public/1ZWJ/4ncMnVjVa", "Прайс")
    welrok.transfer_to_ftp()

    terneo = Octopus("Terneo")
    terneo.get_file_from_mailru("https://cloud.mail.ru/public/1ZWJ/4ncMnVjVa", "Прайс лист")
    terneo.transfer_to_ftp()

    # arlight = Octopus("Arlight")
    # arlight.auth_and_download_from_link(tag_login='loginUser',
    #                                     tag_password='loginPass',
    #                                     login=OCTOPUS_SETTINGS.get('ARLIGHT_LOGIN'),
    #                                     password=OCTOPUS_SETTINGS.get('ARLIGHT_PASSWORD'),
    #                                     base_url='https://assets.transistor.ru/',
    #                                     url_to_file='https://assets.transistor.ru/price/v3/sites/price.xlsx'
    #                                     )
    # arlight.transfer_to_ftp()

    camelion = Octopus("Camelion")
    camelion.find_massage_from_outlook('info@e-s-t.ru', f'Остатки товаров на {date.today().strftime("%d.%m.%Y")}')
    camelion.transfer_to_ftp()

    italline = Octopus("Italline")
    italline.get_file_from_yandex("https://disk.yandex.ru/i/r6i-TCZfuqr2qw", file_name="складские")
    italline.transfer_to_ftp()

    ultraflash = Octopus("Ultraflash")
    ultraflash.find_massage_from_outlook('info@e-s-t.ru', f'Остатки товаров на {date.today().strftime("%d.%m.%Y")}')
    ultraflash.transfer_to_ftp()

    # zortes_stock = Octopus("Zortes_stock")
    # zortes_stock.get_file_from_yandex('https://disk.yandex.ru/i/vPXlChjshCB4hw')
    # zortes_stock.transfer_to_ftp()
    #
    # zortes_price = Octopus("Zortes_price")
    # zortes_price.get_file_from_yandex('https://disk.yandex.ru/i/dOiqAYW3rI5iow')
    # zortes_stock.transfer_to_ftp()

    newport_stock = Octopus("Newport_stocks")
    newport_stock.get_file_from_link("http://178.177.4.229:8087/publ/Остатки NEWPORT.csv")
    newport_stock.transfer_to_ftp()

    newport_price = Octopus("Newport_price")
    newport_price.get_file_from_link("https://newport-light.ru/Down/price-newport-mrc.xlsx")
    newport_price.transfer_to_ftp()

    simple_story = Octopus("Simple story")
    simple_story.get_file_from_yandex('https://disk.yandex.ru/d/hDHeLMp3dW6TRw', file_name='действующий')

    ovivo = Octopus("Ovivo")
    # ovivo.get_file_from_mailru("https://cloud.mail.ru/public/mQqu/XEoebtHtX", 'Остатки Овиво')
    ovivo.get_file_from_yandex(url='https://disk.yandex.ru/d/_YU5JEZnN0oRZQ', file_name='Остатки')
    ovivo.transfer_to_ftp()

    bylectrica = Octopus("Bylectrica")
    bylectrica.get_file_from_yandex(url='https://disk.yandex.ru/d/_YU5JEZnN0oRZQ', file_name='Остатки')
    bylectrica.transfer_to_ftp()

    leek = Octopus("Leek")
    leek.find_massage_from_outlook('1c8@energoco.ru', 'Остатки складов с ценами')
    leek.transfer_to_ftp()

    brizzy = Octopus("Brizzi")
    brizzy.get_file_from_google(
        url='https://docs.google.com/spreadsheets/u/0/d/1o3j5DucKsvX2gPJi21KsZB0sgQEN4J3CB-YzVtSy5YY/export',
        format_file='xlsx'
    )
    brizzy.transfer_to_ftp()

    apeyron = Octopus("Apeyron")
    apeyron.get_file_from_link("http://storage.aeled.ru/feed_apeyron.yml")
    apeyron.transfer_to_ftp()

    # kutek = Octopus("Kutek")
    # kutek.get_file_from_mailru(url='https://cloud.mail.ru/public/FoMy/4Hbh6fNra', name='наличие на')
    # kutek.transfer_to_ftp()

    # sferon_brands = ["Прайс Arti Lampadari", "Прайс Dio D'Arte", "Прайс Lucia Tucci"]
    # sferon = Octopus("Sferon")
    # sferon.get_all_files_from_yandex("https://disk.yandex.ru/d/sa2zN832OAzAUQ", file_names=sferon_brands,
    #                                  format_file='xlsx')
    # sferon.transfer_to_ftp()
