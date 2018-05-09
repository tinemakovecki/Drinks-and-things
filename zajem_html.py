import re
import orodja

def zajemi_strani():
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


regex_url = re.compile(
    r'</div>.*?'               # a je treba dat .*? nakonc vsake vrstice?
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


zajemi_vina()