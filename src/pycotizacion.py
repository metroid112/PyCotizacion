import csv

from re import findall
from requests_html import HTMLSession
from time import sleep
from datetime import datetime


def main():

    session = HTMLSession()
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
    }
    url = 'https://www.brou.com.uy/cotizaciones'
    response = session.get(url, headers=header)

    viejo_cotizacion_brou_compra = 0
    viejo_cotizacion_brou_venta = 0
    viejo_cotizacion_ebrou_compra = 0
    viejo_cotizacion_ebrou_venta = 0
    while True:
        response.html.render(sleep=.5)
        cotizaciones = findall('"valor"> (.+?) <', response.html.html)
        try:
            cotizacion_brou_compra = float(cotizaciones[0].replace(',', '.'))
            cotizacion_brou_venta = float(cotizaciones[1].replace(',', '.'))
            cotizacion_ebrou_compra = float(cotizaciones[4].replace(',', '.'))
            cotizacion_ebrou_venta = float(cotizaciones[5].replace(',', '.'))

            if viejo_cotizacion_brou_compra != 0:
                variacion_cotizacion_brou_compra = round((cotizacion_brou_compra - viejo_cotizacion_brou_compra) / viejo_cotizacion_brou_compra, 2)
            else:
                variacion_cotizacion_brou_compra = 0
            if viejo_cotizacion_brou_venta != 0:
                variacion_cotizacion_brou_venta = round((cotizacion_brou_venta - viejo_cotizacion_brou_venta) / viejo_cotizacion_brou_venta, 2)
            else:
                variacion_cotizacion_brou_venta = 0
            if viejo_cotizacion_ebrou_compra != 0:
                variacion_cotizacion_ebrou_compra = round((cotizacion_ebrou_compra - viejo_cotizacion_ebrou_compra) / viejo_cotizacion_ebrou_compra, 2)
            else:
                variacion_cotizacion_ebrou_compra = 0
            if viejo_cotizacion_ebrou_venta != 0:
                variacion_cotizacion_ebrou_venta = round((cotizacion_ebrou_venta - viejo_cotizacion_ebrou_venta) / viejo_cotizacion_ebrou_venta, 2)
            else:
                variacion_cotizacion_ebrou_venta = 0

            if variacion_cotizacion_brou_compra == 0:
                str_variacion_cotizacion_brou_compra = f'→{variacion_cotizacion_brou_compra}'
            if variacion_cotizacion_brou_compra > 0:
                str_variacion_cotizacion_brou_compra = f'↑{variacion_cotizacion_brou_compra}'
            if variacion_cotizacion_brou_compra < 0:
                str_variacion_cotizacion_brou_compra = f'↓{variacion_cotizacion_brou_compra}'

            if variacion_cotizacion_brou_venta == 0:
                str_variacion_cotizacion_brou_venta = f'→{variacion_cotizacion_brou_venta}'
            if variacion_cotizacion_brou_venta > 0:
                str_variacion_cotizacion_brou_venta = f'↑{variacion_cotizacion_brou_venta}'
            if variacion_cotizacion_brou_venta < 0:
                str_variacion_cotizacion_brou_venta = f'↓{variacion_cotizacion_brou_venta}'

            if variacion_cotizacion_ebrou_compra == 0:
                str_variacion_cotizacion_ebrou_compra = f'→{variacion_cotizacion_ebrou_compra}'
            if variacion_cotizacion_ebrou_compra > 0:
                str_variacion_cotizacion_ebrou_compra = f'↑{variacion_cotizacion_ebrou_compra}'
            if variacion_cotizacion_ebrou_compra < 0:
                str_variacion_cotizacion_ebrou_compra = f'↓{variacion_cotizacion_ebrou_compra}'

            if variacion_cotizacion_ebrou_venta == 0:
                str_variacion_cotizacion_ebrou_venta = f'→{variacion_cotizacion_ebrou_venta}'
            if variacion_cotizacion_ebrou_venta > 0:
                str_variacion_cotizacion_ebrou_venta = f'↑{variacion_cotizacion_ebrou_venta}'
            if variacion_cotizacion_ebrou_venta < 0:
                str_variacion_cotizacion_ebrou_venta = f'↓{variacion_cotizacion_ebrou_venta}'

            now = datetime.now()

            print('------------------------------------------------')
            print(f'\tFecha:\t{now}')
            print(f'Dolar BROU  -> C: ${cotizacion_brou_compra} - {str_variacion_cotizacion_brou_compra}% | V: ${cotizacion_brou_venta} - {str_variacion_cotizacion_brou_venta}%')
            print(f'Dolar eBROU -> C: ${cotizacion_ebrou_compra} - {str_variacion_cotizacion_ebrou_compra}% | V: ${cotizacion_ebrou_venta} - {str_variacion_cotizacion_ebrou_venta}%')

            viejo_cotizacion_brou_compra = cotizacion_brou_compra
            viejo_cotizacion_brou_venta = cotizacion_brou_venta
            viejo_cotizacion_ebrou_compra = cotizacion_ebrou_compra
            viejo_cotizacion_ebrou_venta = cotizacion_ebrou_venta

            with open('log_cotizacion.csv', 'a+', newline='') as log_file:
                log_writer = csv.writer(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                log_writer.writerow([now, cotizacion_brou_compra, cotizacion_brou_venta, cotizacion_ebrou_compra, cotizacion_ebrou_venta])
        except IndexError:
            pass

        sleep(7200)


if __name__ == "__main__":
    main()
