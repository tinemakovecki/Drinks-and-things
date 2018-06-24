import re
import orodja
import os


def zajemi_strani_vino():
    '''Zajame podatke iz spletne strani'''
    osnova1 = 'https://winelibrary.com/search?page='
    osnova2 = '&search=&sort_by=popular&varietal%5B%5D=Cabernet+Sauvignon&varie' \
             'tal%5B%5D=Chardonnay&varietal%5B%5D=Pinot+Noir&varietal%5B%5D=Merlot&varietal%5B%5D=Syrah+%2F+Shiraz&v' \
             'arietal%5B%5D=Grenache+%2F+Garnacha&varietal%5B%5D=Cabernet+Franc&varietal%5B%5D=Sauvignon+Blanc&varie' \
             'tal%5B%5D=Sangiovese&varietal%5B%5D=Riesling&varietal%5B%5D=Mourvedre+%2F+Mataro+%2F+Monastrell+%2F+Ga' \
             'rrut&varietal%5B%5D=Petit+Verdot&varietal%5B%5D=Tempranillo+%2F+Tinto+Fino+%2F+Tinta+Roriz&varietal%5B' \
             '%5D=Malbec&varietal%5B%5D=Pinot+Gris+%2F+Pinot+Grigio&varietal%5B%5D=Cinsault&varietal%5B%5D=Gamay&var' \
             'ietal%5B%5D=Nebbiolo&varietal%5B%5D=Zinfandel&varietal%5B%5D=Carignan+%2F+Carinena&varietal%5B%5D=Peti' \
             'te+Sirah&varietal%5B%5D=Port+Varieties&varietal%5B%5D=Chenin+Blanc&varietal%5B%5D=Muscat&varietal%5B%5' \
             'D=Pinot+Meunier&varietal%5B%5D=Roussanne&varietal%5B%5D=Pinot+Bianco+%2F+Pinot+Blanc&varietal%5B%5D=Ma' \
             'lvasia&varietal%5B%5D=Sherry+Varieties&varietal%5B%5D=Refosco'
    for stran in range(72, 74):
        naslov = osnova1 + str(stran) + osnova2
        ime_datoteke = 'strani_vina/{}.html'.format(stran)
        orodja.shrani(naslov, ime_datoteke)


def zajemi_strani_pivo():
    '''Zajame podatke iz spletne strani'''
    osnova = 'https://www.masterofmalt.com/country/'
    drzave = [("american-beer", 8),("australian-beer", 1), ("belgian-beer",5), ("danish-beer",4), ("dutch-beer",2),
              ("english-beer",17), ("german-beer",2), ("icelandic-beer",1), ("japanese-beer",2), ("kiwi-beer",2),
              ("scotch-beer",5)]
    for drzava, strani in drzave:
        for i in range(1,strani+1):
            naslov = osnova + drzava + "/" + str(i) + "/"
            ime_datoteke = 'beer/{}-{}.html'.format(drzava,i)
            orodja.shrani(naslov, ime_datoteke)


regex_url = re.compile(
    r'</div>.*?'
    r'<div id="product_id_(?P<id>\d{4,8})" class="search-item">.*?'
    r'<div class="search-item-inner clearfix">.*?'
    r'<div class="search-item-img col-xs-\d{1,3} col-sm-\d{1,3}  col-lg-\d{1,3} text-center">.*?'
    r'<a href="(?P<url>.*?)"><img alt="(?P<Ime>.*?)" class="img-full-responsive" .*?',
    flags=re.DOTALL)

regex_url_beer = re.compile(
    r' <div id=".*?" class=".*?" data-product-url="https://www.masterofmalt.*?'
    r'.com/beer/(?P<url>.*?)" data-productid="(?P<id>\d{4,8})">.*?',
    flags=re.DOTALL
)


def izloci_url(imenik, regex):
    '''Vrne seznam s slovarji podatkov iz imenika'''
    podatki = []
    for datoteka in orodja.datoteke(imenik):
        for podatek in re.finditer(regex, orodja.vsebina_datoteke(datoteka)):
            pod = podatek.groupdict()
            pod['id'] = int(pod['id'])
            podatki.append(pod)
    return podatki


def zajemi_vina():
    '''Pregleda celotne strani in zajame posamezna vina'''
    vina = izloci_url('strani_vina/', regex_url)
    for vino in vina:
        ime_datoteke = 'vina/{}.html'.format(vino['id'])
        orodja.shrani(vino['url'], ime_datoteke)


def zajemi_piva():
    '''Pregleda celotne strani in zajame posamezna piva'''
    piva = izloci_url('beerpages/', regex_url_beer)
    for pivo in piva:
        ime_datoteke = 'beer/{}.html'.format(pivo['id'])
        url = "https://www.masterofmalt.com/beer/" + pivo['url']
        orodja.shrani(url, ime_datoteke)


regex_vino = re.compile(
    r'<h1 itemprop=\'name\'.*?title">(?P<Name>.*?)((\$|&).*)?<small>(?P<ShortDes>.*?)</small></h1>.*?'
    r'<span itemprop=\'price\'>(?P<Price>.*?)</span>.*?'
    r'title="Show (bottle|front) graphic for this product." data-index="0" href="(?P<Image>.*?)"><img src=.*?'
    r'<p itemprop=\'(description|reviewBody(?!(.*?itemprop=\'description)))\'>"?(?P<Description>.*?)"?(</p>|<br>).*?'
    r'<td class=\'label\'>Item #</td>.*?'
    r'<td class=\'data\'>(?P<id>\d{4,8})</td>.*?'
    r'<td class="label">Country</td>.*?'
    r'<td class="data"><a href="/search\?country%.*?">(?P<Country>.*?)</a></td>.*?'
    r'<td class="label">Region</td>.*?'
    r'<td class="data"><a href="/search\?country%.*?">(?P<Region>.*?)</a></td>.*?'
    r'<td class="label">Color</td>.*?'
    r'<td class="data"><a href="/search\?color%.*?">(?P<Color>.*?)</a></td>.*?'
    r'<td class="label">ABV</td>.*?'
    r'<td class="data">(?P<ABV>.*?)%?</td>.*?'
    r'<td class="data"><a href="/search\?varietal%5B%5D.*?"(?P<Varietal>.*?)</td>.*?'
    r'<td class="label">Size</td>.*?'
    r'<td class="data">(?P<Size>.*?)</td>.*?'
    r'<td class="label">Closure</td>.*?'
    r'<td class="data">(?P<Closure>.*?)</td>.*?'
    r'<td class="label">Taste</td>.*?'
    r'<td class="data">(?P<Taste>.*?)</td>.*?'
    r'<td class="label">Nose</td>.*?'
    r'<td class="data">(?P<Smell>.*?)</td>.*?',
    flags=re.DOTALL)

regex_vrsta = re.compile(r'>(?P<vrsta>.*?)</a>')


regex_pivo = re.compile(
    r'<div class="productImageWrap">.*?'
    r'<img src="(?P<Image>.*?)".*?'
    r'(<meta itemprop=\'price\' content=\'(?P<Price>.*?)\'/>|Discontinued).*?'
    r'<span id="ContentPlaceHolder1_ctl00_ctl00_wdItemNameCountry" class="kv-key gold">Country</span>.*?'
    r'<span class="kv-val">(?P<Country>.*?)</span>.*?'
    r'<span id="ContentPlaceHolder1_ctl00_ctl00_wdItemNameDistillery" class="kv-key gold">Brewery</span>.*?'
    r'<span class="kv-val" itemprop="brand"><a href="https://www.masterofmalt.com/distilleries/.*?/">(?P<Brewery>.*?)</a></span>.*?'
    r'<span id="ContentPlaceHolder1_ctl00_ctl00_wdItemNameBottler" class="kv-key gold">Bottler</span>.*?'
    r'<span class="kv-val" itemprop="manufacturer">(?P<Bottler>.*?)</span>.*?'
    r'<span id="ContentPlaceHolder1_ctl00_ctl00_wdItemNameStyle" class="kv-key gold">Style</span>.*?'
    r'<span class="kv-val">(?P<Style>.*?)</span>.*?'
    r'<span id="ContentPlaceHolder1_ctl00_ctl00_wdItemNameAlcohol" class="kv-key gold">Alcohol</span>.*?'
    r'<span class="kv-val">(?P<ABV>.*?)%</span>.*?'
    r'<span id="ContentPlaceHolder1_ctl00_ctl00_wdItemNameVolume" class="kv-key gold">Volume</span>.*?'
    r'<span class="kv-val">(?P<Volume>.*?)</span>.*?'
    r'var isProductPage = true,.*?lastViewedProductID = \d{4,8},.*?productID = (?P<id>\d{4,8});.*?'
    r'"name": "(?P<Name>.*?)",.*?"description": "(?P<Description>.*?)",.*?',
    flags=re.DOTALL)


def izloci_podatke_vin(imenik, regex):
    '''Iz html datotek izloči podatke vin'''
    podatki = []
    for datoteka in orodja.datoteke(imenik):
        vino = re.search(regex, orodja.vsebina_datoteke(datoteka))
        if vino is not None:
            pod = vino.groupdict()
            pod['Price'] = float(pod['Price'])
            pod['id'] = int(pod['id'])
            vrste = regex_vrsta.findall(pod['Varietal'])
            pod['Varietal'] = vrste
            pod['Description'] = str(pod['Description']).replace('\n', '')
            if pod['ABV'] != 'N/A':
                pod['ABV'] = float(pod['ABV'])
            else:
                pod['ABV'] = None
            podatki.append(pod)
        else:
            print(datoteka)
            os.remove(datoteka)
    return podatki


def izloci_podatke_piv(imenik, regex):
    '''Iz html datotek izloči podatke piv'''
    podatki = []
    for datoteka in orodja.datoteke(imenik):
        pivo = re.search(regex, orodja.vsebina_datoteke(datoteka))
        if pivo is not None:
            pod = pivo.groupdict()
            if pod['Price'] is None:
                pod['Price'] = 'Discontinued'
            else:
                pod['Price'] = float(pod['Price'])
            pod['id'] = int(pod['id'])
            pod['Description'] = str(pod['Description']).replace('\\"', '')
            pod['Description'] = str(pod['Description']).replace(';', ',')
            podatki.append(pod)
        else:
            print(datoteka)
    return podatki


def csv_vina():
    '''Podatke vin zapiše v csv datoteko'''
    vina = izloci_podatke_vin('vina', regex_vino)
    wines = []
    for vino in vina:
        ime = vino['Name']
        barva = vino['Color']
        cena = vino['Price']
        stopnja_alkohola = vino['ABV']
        drzava = vino['Country']
        regija = vino['Region']
        # TODO: filter the descriptions for nonsense!
        opis = vino['Description']
        okus = vino['Taste']
        vonj = vino['Smell']
        slika = vino['Image']

        # velikost:
        velikost = ""

        if "mL" in str(vino['Size']):
            for sign in str(vino['Size']):
                if sign not in " mL":
                    velikost += sign
            velikost = float(velikost) / 1000
        else:
            for sign in str(vino['Size']):
                if sign != "l":
                    velikost += sign
            velikost = float(velikost)

        # vrsta:
        # parsing the strings
        sorts = vino['Varietal']
        if len(sorts) == 1:
            vrsta = sorts[0]
        else:
            vrsta = 'blend'

        # write a dictionary for each wine
        entry = {'ime': ime,
                 'vrsta': vrsta,
                 'barva': barva,
                 'velikost': velikost,
                 'stopnja_alkohola': stopnja_alkohola,
                 'drzava': drzava,
                 'regija': regija,
                 'cena': cena,
                 'okus': okus,
                 'vonj': vonj,
                 'opis': opis,
                 'slika': slika}
        wines.append(entry)
    column_names = wines[0].keys()
    orodja.zapisi_tabelo(wines, column_names, 'wines.csv')


def csv_piva():
    piva = izloci_podatke_piv('beer', regex_pivo)
    beers = []
    country_dic = {'Scotch Beer': 'Scotland',
                   'English Beer': 'England',
                   'Belgian Beer': 'Belgium',
                   'American Beer': 'United States',
                   'Japanese Beer': 'Japan',
                   'Dutch Beer': 'Netherlands',
                   'Danish Beer': 'Denmark',
                   'Kiwi Beer': 'New Zealand',
                   'Australian Beer': 'Australia',
                   'German Beer': 'Germany',
                   'Icelandic Beer': 'Iceland'}
    for pivo in piva:
        ime = pivo['Name']
        pivovarna = pivo['Brewery']
        opis = pivo['Description']
        drzava = country_dic[pivo['Country']]
        slika = pivo['Image']

        # velikost:
        velikost = ""
        for sign in str(pivo['Volume']):
            if sign not in "cl":
                velikost += sign
        velikost = float(velikost) / 100

        # stopnja_alkohola:
        stopnja_alkohola = ""
        for sign in str(pivo['ABV']):
            if sign == ',':
                stopnja_alkohola += '.'
            else:
                stopnja_alkohola += sign
        stopnja_alkohola = float(stopnja_alkohola)

        # cena:
        if pivo['Price'] == 'Discontinued':
            cena = None
        else:
            cena = pivo['Price']

        # vrsta:
        # some types are doubled, we need to join them together
        if pivo['Style'] == 'Cask Aged Beer':
            vrsta = 'Cask-Aged Beer'
        elif pivo['Style'] == 'Spiced Beer':
            vrsta = 'Herb / Spice Beer'
        elif pivo['Style'] == 'Spiced Beer':
            vrsta = 'Herb / Spice Beer'
        elif pivo['Style'] == 'Wheat Beer':
            vrsta = 'Wheat / Wit / White Beer'
        else:
            vrsta = pivo['Style']

        # write a dictionary for each beer
        entry = {'ime': ime,
                 'pivovarna': pivovarna,
                 'vrsta': vrsta,
                 'velikost': velikost,
                 'stopnja_alkohola': stopnja_alkohola,
                 'drzava': drzava,
                 'cena': cena,
                 'opis': opis,
                 'slika': slika}
        beers.append(entry)


    column_names = ['ime', 'pivovarna', 'vrsta', 'velikost',
                'stopnja_alkohola', 'drzava', 'cena', 'opis', 'slika']

    # write a new file with the adjusted data
    orodja.zapisi_tabelo(beers, column_names, 'beers.csv')


csv_piva()
csv_vina()


