import csv

from re import findall
from requests_html import HTMLSession
from datetime import datetime
from dateutil import parser


def main():

    session = HTMLSession()
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
    }
    url = 'https://www.brou.com.uy/cotizaciones'
    response = session.get(url, headers=header)

    response.html.render(sleep=.5)
    cotizaciones = findall('"valor"> (.+?) <', response.html.html)
    try:
        cotizacion_brou_compra = float(cotizaciones[0].replace(',', '.'))
        cotizacion_brou_venta = float(cotizaciones[1].replace(',', '.'))
        cotizacion_ebrou_compra = float(cotizaciones[4].replace(',', '.'))
        cotizacion_ebrou_venta = float(cotizaciones[5].replace(',', '.'))

        now = datetime.date(datetime.now())

        print('------------------------------------------------')
        print(f'\tFecha:\t{now}')
        print(f'\tDolar BROU  -> C: ${cotizacion_brou_compra} | V: ${cotizacion_brou_venta}')
        print(f'\tDolar eBROU -> C: ${cotizacion_ebrou_compra} | V: ${cotizacion_ebrou_venta}')

        with open('log_cotizacion.csv', mode='r', newline='') as log_file:
            csv_list = list(csv.reader(log_file, delimiter=','))
            last_register_date = csv_list[-1][0]
            update_log = last_register_date == now

        if update_log:
            print('\tRegistrando nueva fecha')
            with open('log_cotizacion.csv', 'a+', newline='') as log_file:
                log_writer = csv.writer(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                log_writer.writerow([now, cotizacion_brou_compra, cotizacion_brou_venta, cotizacion_ebrou_compra, cotizacion_ebrou_venta])
    except IndexError:
        pass


if __name__ == "__main__":
    main()
