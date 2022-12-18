import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pickle
import pandas as pd

'''
This script gets the headlines in the front page from the biggest news portals in Brazil
Each portal has its own scrapping script
After being scrapped, the dataframe is appended to the historical data
'''

######################################################################################
#########                                                                   ##########
#########             1. Portals we will retrieve the data from             ##########
#########                                                                   ##########
######################################################################################

# SITES
todos_portais = ['Band','BBC','Folha de SP','Gazeta do Povo','Globo',
                 'iG','R7','UOL','Veja','Carta Capital','Revista Forúm',
                 'Brasil de Fato','Pleno News','Terça Livre','Renova Mídia',
                'Conexão Política','Jornal da Cidade','El Pais', 'Deutsche Welle','Estadão','Isto É']

# Band  -- OK
band = 'https://www.band.uol.com.br'
# BBC  -- OK
bbc = 'https://www.bbc.com/portuguese'
# Folha de SP  -- OK
folha = 'https://www.folha.uol.com.br/'
# Gazeta do Povo  -- OK
gazeta = 'https://www.gazetadopovo.com.br/'
# Globo  -- OK
globo = 'https://www.globo.com/'
# iG  -- OK
ig = 'https://www.ig.com.br/'
# R7 -- OK
r7 = 'https://www.r7.com/'
# UOL  -- OK
uol = 'https://www.uol.com.br/'
# Veja  -- OK
veja = 'https://veja.abril.com.br/'
# Carta Capital  -- OK
carta_capital = 'https://www.cartacapital.com.br/'
# Revista Forúm  -- OK
forum = 'https://revistaforum.com.br/'
# Brasil de Fato  -- OK
brasil_fato = 'https://www.brasildefato.com.br/'
# Pleno News  -- OK
pleno = 'https://pleno.news/'
# Terça Livre  -- OK
terca_livre = 'https://tercalivre.com.br/'
# Renova Mídia  -- OK
renova = 'https://renovamidia.com.br/?utm_source=rfrsh'
# Conexão Política  -- OK
conexao = 'https://www.conexaopolitica.com.br/'
# Jornal da Cidade  -- OK
jornal_cidade = 'https://www.jornaldacidadeonline.com.br/'
# El Pais  -- OK
elpais = 'https://brasil.elpais.com/'
# Deutsche Welle  -- OK
dw = 'https://www.dw.com/pt-br/not%C3%ADcias/s-7111'
# Estadão  -- OK
estadao = 'https://www.estadao.com.br/'
# Isto É  -- OK
istoe = 'https://istoe.com.br/'


######################################################################################
#########                                                                   ##########
#########           2. Functions to get headlines for each portal           ##########
#########                                                                   ##########
######################################################################################

def coletando_infos_band():
    infos = []
    hora_dia = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    frases_comuns = ['Em Alta', 'Tóquio no Bandsports', 'Notícias', 'Entretenimento', 'Esporte', 'Receitas',
                     'Web Stories', 'Nosso Time', 'Mais Vistos', '1', '2', '3', '4', '5', '6', 'Programas']

    r = requests.get(band)
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('h2'):
        manchete = a.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    infos_completas = [[hora_dia, 'Band', x] for x in infos]
    return infos_completas

# --------------------------------------------------------------------------------------------------#

def coletando_infos_bbc():
    infos = []
    hora_dia = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    frases_comuns = []

    r = requests.get(bbc)
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('h3'):
        manchete = a.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    infos_completas = [[hora_dia, 'BBC', x] for x in infos]
    return infos_completas

# --------------------------------------------------------------------------------------------------#

def coletando_infos_folha():
    infos = []
    hora_dia = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    frases_comuns = ['Mais lidas', 'editoriais o que a folha pensa', 'tendências / debates', 'painel do leitor',
                     'TV Folha', 'Fotografia']

    r = requests.get(folha)
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('h2'):
        manchete = a.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for b in soup.find_all('span', class_='c-list-links__title'):
        manchete = b.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for c in soup.find_all('p', class_='c-rotate-headlines__description'):
        manchete = c.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete.split(' -')[0])

    infos_completas = [[hora_dia, 'Folha de SP', x] for x in infos]
    return infos_completas

# --------------------------------------------------------------------------------------------------#

def coletando_infos_gazeta():
    infos = []
    hora_dia = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    frases_comuns = ['Quero receber', 'Gazeta do Povo', 'Notícias', 'Opinião', 'Mais', 'Informações', 'Notificações',
                     'NOTÍCIAS', 'LINHA DO TEMPO', 'PODCAST', 'KIT ANTICORRUPÇÃO', 'SaibaAgora', 'Ideias',
                     'Família e Bem-estar']

    r = requests.get(gazeta)
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('h2'):
        manchete = a.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for b in soup.find_all('a', class_='trigger-gtm'):
        manchete = b.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    infos_completas = [[hora_dia, 'Gazeta do Povo', x] for x in infos]
    return infos_completas

# --------------------------------------------------------------------------------------------------#

def coletando_infos_globo():
    infos = []
    hora_dia = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    frases_comuns = ['MEGAPIX AO VIVO', 'OFF', 'SPORTV AO VIVO']

    r = requests.get(globo)
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('h3'):
        manchete = a.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for b in soup.find_all('h4'):
        manchete = b.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    infos_completas = [[hora_dia, 'Globo', x] for x in infos]
    return infos_completas

# --------------------------------------------------------------------------------------------------#

def coletando_infos_ig():
    infos = []
    hora_dia = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    frases_comuns = [' ']

    r = requests.get(ig)
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('a', {'data-tb-region-item': 'taboola-region'}):
        manchete = a.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for b in soup.find_all('a', {'class': 'title'}):
        manchete = b.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for c in soup.find_all('h2', {'class': 'sliderV5_container_desc_titulo'}):
        manchete = c.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for d in soup.find_all('li', {'class': 'secondary-calling'}):
        manchete = d.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for e in soup.find_all('li', {'class': 'chamada-secundaria'}):
        manchete = e.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for f in soup.find_all('h2', {'class': 'componenteDestaqueSecao-contentText-titulo'}):
        manchete = f.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for g in soup.find_all('h2', {'class': 'componenteDestaqueSecao-horizontal-flex-contentText-titulo'}):
        manchete = g.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for h in soup.find_all('h2', {'class': 'componenteDestaqueSecao-horizontal-contentText-titulo'}):
        manchete = h.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for i in soup.find_all('li', {'class': 'segunda-chamada'}):
        manchete = i.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    infos_completas = [[hora_dia, 'iG', x] for x in infos]
    return infos_completas

# --------------------------------------------------------------------------------------------------#

def coletando_infos_r7():
    infos = []
    hora_dia = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    frases_comuns = []

    r = requests.get(r7)
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('h3', {
        'class': ['r7-flex-title-h1', 'r7-flex-title-h2', 'r7-flex-title-h3', 'r7-flex-title-h4', 'r7-flex-title-h5',
                  'r7-flex-title-h6']}):
        manchete = a.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for b in soup.find_all('h4', {
        'class': ['r7-flex-title-h1', 'r7-flex-title-h2', 'r7-flex-title-h3', 'r7-flex-title-h4', 'r7-flex-title-h5',
                  'r7-flex-title-h6']}):
        manchete = b.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    infos_completas = [[hora_dia, 'R7', x] for x in infos]
    return infos_completas

# --------------------------------------------------------------------------------------------------#

def coletando_infos_uol():
    infos = []
    hora_dia = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    frases_comuns = []

    r = requests.get(uol)
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('h1', {'class': 'titulo color2'}):
        manchete = a.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for b in soup.find_all('span', {'class': ['linha font1 cor2-hover cor2-p4-hover cor-transition', 'color2',
                                              'title cor-transition cor2-hover cor2-p4-hover',
                                              'chamada corb cor2-hover cor2-p4-hover cor-transition',
                                              'chamada cor2-hover cor2-p4-hover cor-transition',
                                              'chamada cor2-hover cor-transition']}):
        manchete = b.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for c in soup.find_all('h2', {'class': 'titulo color2'}):
        manchete = c.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for d in soup.find_all('p', {'class': ['subtitle titulo', 'texto color2']}):
        manchete = d.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    infos_completas = [[hora_dia, 'UOL', x] for x in infos]
    return infos_completas

# --------------------------------------------------------------------------------------------------#

def coletando_infos_veja():
    infos = []
    hora_dia = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    frases_comuns = []

    r = requests.get(veja)
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('h2', {'class': ['title']}):
        manchete = a.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for b in soup.find_all('a', {'class': ['link related-article']}):
        manchete = b.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for c in soup.find_all('h3', {'class': ['title']}):
        manchete = c.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for d in soup.find_all('h4', {'class': ['title']}):
        manchete = d.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    infos_completas = [[hora_dia, 'Veja', x] for x in infos]
    return infos_completas

# --------------------------------------------------------------------------------------------------#

def coletando_infos_carta_capital():
    infos = []
    hora_dia = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    frases_comuns = [
        'Jornalismo crítico e transparente. Notícias sobre política, economia e sociedade com olhar progressista - Carta Capital',
        'O que pensam os políticos do campo progressista']

    r = requests.get(carta_capital)
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('h1'):
        manchete = a.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for b in soup.find_all('li', {'class': ['li_meta_related_matters']}):
        manchete = b.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for c in soup.find_all('div', class_='wpb_wrapper'):
        for d in c.find_all('ul'):
            for e in d.find_all('li'):
                manchete = e.text.strip()
                if manchete != '' and manchete not in infos and manchete not in frases_comuns:
                    infos.append(manchete)

    for f in soup.find_all('h3'):
        manchete = f.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for g in soup.find_all('h4'):
        manchete = g.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for h in soup.find_all('h5'):
        manchete = h.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for i in soup.find_all('div', class_='txt'):
        for j in i.find_all('a'):
            manchete = j.text.strip()
            if manchete != '' and manchete not in infos and manchete not in frases_comuns:
                infos.append(manchete)

    infos_completas = [[hora_dia, 'Carta Capital', x] for x in infos]
    return infos_completas

# --------------------------------------------------------------------------------------------------#

def coletando_infos_forum():
    infos = []
    hora_dia = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    frases_comuns = []

    r = requests.get(forum)
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('a', {'class': ['rf_item', 'rf-post-title']}):
        manchete = a.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for b in soup.find_all('div', {'class': ['rf_blog_destaque_item_content']}):
        for c in b.find_all('h3'):
            manchete = c.text.strip()
            if manchete != '' and manchete not in infos and manchete not in frases_comuns:
                infos.append(manchete)

    infos_completas = [[hora_dia, 'Revista Forúm', x] for x in infos]
    return infos_completas

# --------------------------------------------------------------------------------------------------#

def coletando_infos_brasil_fato():
    infos = []
    hora_dia = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    frases_comuns = []

    r = requests.get(brasil_fato)
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('h3', {'class': ['big-title', 'title']}):
        manchete = a.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for b in soup.find_all('h2', {'class': ['title']}):
        manchete = b.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    infos_completas = [[hora_dia, 'Brasil de Fato', x] for x in infos]
    return infos_completas

# --------------------------------------------------------------------------------------------------#

def coletando_infos_pleno():
    infos = []
    hora_dia = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    frases_comuns = []

    r = requests.get(pleno)
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('div', {'class': ['text', 'holder-box']}):
        for b in a.find_all('h2'):
            manchete = b.text.strip()
            if manchete != '' and manchete not in infos and manchete not in frases_comuns:
                infos.append(manchete)

    for c in soup.find_all('div', {'class': ['post-block small', 'post-block small height-1', 'holder-box']}):
        for d in c.find_all('h3'):
            manchete = d.text.strip()
            if manchete != '' and manchete not in infos and manchete not in frases_comuns:
                infos.append(manchete)

    infos_completas = [[hora_dia, 'Pleno News', x] for x in infos]
    return infos_completas

# --------------------------------------------------------------------------------------------------#

def coletando_infos_terca_livre():
    infos = []
    hora_dia = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    frases_comuns = []

    r = requests.get(terca_livre)
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('h2', class_='entry-title h6'):
        manchete = a.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    infos_completas = [[hora_dia, 'Terça Livre', x] for x in infos]
    return infos_completas

# --------------------------------------------------------------------------------------------------#

def coletando_infos_renova():
    infos = []
    hora_dia = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    frases_comuns = []

    r = requests.get(renova)
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('h3', {'class': ['elementor-post__title']}):
        manchete = a.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    infos_completas = [[hora_dia, 'Renova Mídia', x] for x in infos]
    return infos_completas

# --------------------------------------------------------------------------------------------------#

def coletando_infos_conexao():
    infos = []
    hora_dia = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    frases_comuns = []

    r = requests.get(conexao)
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('div', {'class': ['mvp-feat1-sub-text', 'mvp-widget-feat1-top-text left relative',
                                             'mvp-widget-feat1-bot-text left relative',
                                             'mvp-feat1-feat-text left relative',
                                             'mvp-widget-feat2-right-text left relative', 'mvp-feat1-list-text',
                                             'mvp-blog-story-text left relative']}):
        for b in a.find_all('h2'):
            manchete = b.text.strip()
            if manchete != '' and manchete not in infos and manchete not in frases_comuns:
                infos.append(manchete)

    infos_completas = [[hora_dia, 'Conexão Política', x] for x in infos]
    return infos_completas

# --------------------------------------------------------------------------------------------------#

def coletando_infos_jornal_cidade():
    infos = []
    hora_dia = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    frases_comuns = []

    r = requests.get(jornal_cidade)
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('a', {'class': ['widget__title', 'widget__title font-bold block']}):
        manchete = a.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    infos_completas = [[hora_dia, 'Jornal da Cidade', x] for x in infos]
    return infos_completas

# --------------------------------------------------------------------------------------------------#

def coletando_infos_elpais():
    infos = []
    hora_dia = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    frases_comuns = []

    r = requests.get(elpais)
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('h2'):
        manchete = a.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for b in soup.find_all('a', {'class': ['c_r_s_h related_story_headline']}):
        manchete = b.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    infos_completas = [[hora_dia, 'El Pais', x] for x in infos]
    return infos_completas

# --------------------------------------------------------------------------------------------------#

def coletando_infos_dw():
    infos = []
    hora_dia = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    frases_comuns = ['Temas recorrentes', 'Boletim de notícias em áudio']

    r = requests.get(dw)
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('h2'):
        if a.span is None:
            manchete = a.text.strip()
        else:
            a.span.decompose()
            manchete = a.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    infos_completas = [[hora_dia, 'Deutsche Welle', x] for x in infos]
    return infos_completas

# --------------------------------------------------------------------------------------------------#

def coletando_infos_estadao():
    infos = []
    hora_dia = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    frases_comuns = []

    r = requests.get(estadao)
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('h3', {'class': ['title']}):
        manchete = a.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    for b in soup.find_all('h4', {'class': ['bullets-title']}):
        manchete = b.text.strip()
        if manchete != '' and manchete not in infos and manchete not in frases_comuns:
            infos.append(manchete)

    infos_completas = [[hora_dia, 'Estadão', x] for x in infos]
    return infos_completas

# --------------------------------------------------------------------------------------------------#

def coletando_infos_istoe():
    infos = []
    hora_dia = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    frases_comuns = []

    r = requests.get(istoe)
    soup = BeautifulSoup(r.content, 'html.parser')

    for a in soup.find_all('div', {'class': ['titulo-destaque-chamadas', 'bloco-noticias', 'wrapper-title']}):
        for b in a.find_all('h1'):
            manchete = b.text.strip()
            if manchete != '' and manchete not in infos and manchete not in frases_comuns:
                infos.append(manchete)

    infos_completas = [[hora_dia, 'Isto É', x] for x in infos]
    return infos_completas

# --------------------------------------------------------------------------------------------------#

######################################################################################
#########                                                                   ##########
#########                       3. Auxiliar functions                       ##########
#########                                                                   ##########
######################################################################################

def abrir_pickle(nome_portal): # to open pickle file
    with open('Manchetes/{}.pickle'.format(nome_portal), 'rb') as f:
        df = pickle.load(f)
        f.close()

    return df


def salvar_pickle(df, nome_portal): # to save pickle file
    with open('Manchetes/{}.pickle'.format(nome_portal), 'wb') as f:
        pickle.dump(df, f)
        f.close()


def adicionar_infos_novas(df_antigo, infos_novas): # Appeding historical headlines with new headlines
    df_final = df_antigo.append(infos_novas).drop_duplicates(subset='manchete', ignore_index=True)

    return df_final

def coletando_infos(nome_portal): # calling the portal scrapper for each portal
    if nome_portal == 'Band':
        lista_manchetes = coletando_infos_band()
    elif nome_portal == 'BBC':
        lista_manchetes = coletando_infos_bbc()
    elif nome_portal == 'Folha de SP':
        lista_manchetes = coletando_infos_folha()
    elif nome_portal == 'Gazeta do Povo':
        lista_manchetes = coletando_infos_gazeta()
    elif nome_portal == 'Globo':
        lista_manchetes = coletando_infos_globo()
    elif nome_portal == 'iG':
        lista_manchetes = coletando_infos_ig()
    elif nome_portal == 'R7':
        lista_manchetes = coletando_infos_r7()
    elif nome_portal == 'UOL':
        lista_manchetes = coletando_infos_uol()
    elif nome_portal == 'Veja':
        lista_manchetes = coletando_infos_veja()
    elif nome_portal == 'Carta Capital':
        lista_manchetes = coletando_infos_carta_capital()
    elif nome_portal == 'Revista Forúm':
        lista_manchetes = coletando_infos_forum()
    elif nome_portal == 'Brasil de Fato':
        lista_manchetes = coletando_infos_brasil_fato()
    elif nome_portal == 'Pleno News':
        lista_manchetes = coletando_infos_pleno()
    elif nome_portal == 'Terça Livre':
        lista_manchetes = coletando_infos_terca_livre()
    elif nome_portal == 'Renova Mídia':
        lista_manchetes = coletando_infos_renova()
    elif nome_portal == 'Conexão Política':
        lista_manchetes = coletando_infos_conexao()
    elif nome_portal == 'Jornal da Cidade':
        lista_manchetes = coletando_infos_jornal_cidade()
    elif nome_portal == 'El Pais':
        lista_manchetes = coletando_infos_elpais()
    elif nome_portal == 'Deutsche Welle':
        lista_manchetes = coletando_infos_dw()
    elif nome_portal == 'Estadão':
        lista_manchetes = coletando_infos_estadao()
    elif nome_portal == 'Isto É':
        lista_manchetes = coletando_infos_istoe()

    df = pd.DataFrame(lista_manchetes, columns=['data', 'portal', 'manchete'])
    return df

######################################################################################
#########                                                                   ##########
#########                       4. Colleting the data                       ##########
#########                                                                   ##########
######################################################################################

def coletando_todas_infos(todos_portais): # Call the other functions to scrap and save the headlines
    for portal in todos_portais:
        df_antigo = abrir_pickle(portal)
        tamanho_anterior = df_antigo.shape[0]

        novo_df = coletando_infos(portal)

        df_final = adicionar_infos_novas(df_antigo, novo_df)
        tamanho_novo = df_final.shape[0]

        salvar_pickle(df_final, portal)

        print('{} --- Before: {} - After: {} --- Difference: {}'.format(portal, tamanho_anterior, tamanho_novo,
                                                                       tamanho_novo - tamanho_anterior))


if __name__ == '__main__':
    coletando_todas_infos(todos_portais)