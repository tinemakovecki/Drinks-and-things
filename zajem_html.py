import re
import orodja

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
    vina = izloci_url('strani_vina/', regex_url)
    for vino in vina:
        ime_datoteke = 'vina/{}.html'.format(vino['id'])
        orodja.shrani(vino['url'], ime_datoteke)


regex_vino = re.compile(
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
    r'<td class="data">(?P<ABV>.*?)%</td>.*?'
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


def izloci_podatke_vin(imenik, regex):
    podatki = []
    for datoteka in orodja.datoteke(imenik):
        for vino in re.finditer(regex, orodja.vsebina_datoteke(datoteka)):
            pod = vino.groupdict()
            pod['id'] = int(pod['id'])
            vrste = regex_vrsta.findall(pod['Varietal'])
            pod['Varietal'] = vrste
            pod['Description'] = str(pod['Description']).replace('\n', '')
            pod['ABV'] = float(pod['ABV'])
            podatki.append(pod)
    return podatki

podatki = izloci_podatke_vin('vina_manjsa', regex_vino)
print(podatki)
print(len(podatki))

