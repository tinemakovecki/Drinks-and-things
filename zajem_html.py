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


def izloci_podatke_piv(imenik, regex):
    '''Iz html datotek izloči podatke vin'''
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
            pod['Description'] = str(pod['Description']).replace('\n', '')

            podatki.append(pod)
        else:
            print(datoteka)
    return podatki


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


def csv_vina():
    '''Podatke vin zapiše v csv datoteko'''
    vina = izloci_podatke_vin('vina', regex_vino)
    orodja.zapisi_tabelo(vina, ['id', 'Name', 'ShortDes', 'Color', 'Varietal', 'Price', 'Size', 'ABV', 'Country',
                                'Region', 'Closure', 'Taste', 'Smell', 'Description'], 'CSV/vina.csv')


def csv_piva():
    piva = izloci_podatke_piv('beer', regex_pivo)
    orodja.zapisi_tabelo(piva, ['id', 'Name', 'Country', 'Brewery', 'Bottler', 'Style', 'Price', 'Volume', 'ABV',
                                'Description'], 'CSV/piva.csv')

