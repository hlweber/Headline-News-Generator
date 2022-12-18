import re
from PIL import Image
import regex
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import emoji
from collections import Counter
import datetime
import plotly.express as px
import nltk
import unidecode
import string
import math
import pickle
from scipy import stats
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer

## Informações básicas

todos_portais = ['Band','BBC','Folha de SP','Gazeta do Povo','Globo',
                 'iG','R7','UOL','Veja','Carta Capital','Revista Forúm',
                 'Brasil de Fato','Pleno News','Terça Livre','Renova Mídia',
                'Conexão Política','Jornal da Cidade','El Pais', 'Deutsche Welle','Estadão','Isto É']

def ler_pickle(nome_portal):
    with open('Manchetes/{}.pickle'.format(nome_portal), 'rb') as f:
        df = pickle.load(f)
        f.close()
    return df


def juntando_todas_informacoes(todos_portais):
    df_completo = pd.DataFrame(columns=['data', 'portal', 'manchete'])
    for portal in todos_portais:
        df_completo = df_completo.append(ler_pickle(portal))

    return df_completo.reset_index(drop=True)


dfss = juntando_todas_informacoes(todos_portais)

df_conversa = juntando_todas_informacoes(todos_portais)
nltk.download('stopwords')
STOPWORDS = nltk.corpus.stopwords.words('portuguese')

stopwords = list(STOPWORDS)
extra = ['sao', 'paulo', 'duration', 'sobre', 'apos', 'haha', 'k', 'eh', 'ce', 'voce', 'pra', 'vc', 'q', 'ia', 'aqui',
         'tá', 'pro', 'uns', 'oq', 'so', 'umas', 'mt', 'lá', 'sim', 'ai', 'vou', 'vai', 'tava', 'nao', 'ta', 'tbm',
         'mto', 'msm', 'to', 'pq', 'ja', 'sei', 'aí', 'ter', 'ser', 'bem', 'aqui']
palavras_deletar = ['videos', 'video', 'veja', 'diz', 'r', 'b']
stopwords = stopwords + extra + palavras_deletar


def limpar_texto(texto):
    texto = unidecode.unidecode(texto)  # remove os acentos
    texto = texto.lower()  # padroniza as letras
    texto = re.sub('(:?https?:\/\/[^\s]*)|www.[^\s]*', '', texto)  # remove os links
    texto = re.sub('(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])',
                   '', texto)  # remove emojis
    texto = re.sub('[%s]' % re.escape(string.punctuation), '', texto)  # remove as pontuações
    texto = re.sub('\w*\d\w*', '', texto)  # remove palavras que tem digitos no meio
    texto = re.sub(r'([^s|r])\1+', r'\1', texto)  # remove letras duplas exceto quando a letra é 's' ou 'r'
    texto = re.sub(r'\s(a?ha)+h?\s', ' haha ', texto)  # padroniza as risadas

    return texto


df_palavras = df_conversa.groupby('portal')['manchete'].agg(' '.join).reset_index()
df_palavras['manchete'] = df_palavras.manchete.apply(limpar_texto)

cv = CountVectorizer(stop_words=stopwords, token_pattern=r'\b\w\w*\b')
data_cv = cv.fit_transform(df_palavras.manchete)
data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
data_dtm.index = df_palavras.portal
df_tokenizado = data_dtm.transpose()


def mostrar_palavras_comuns():
    qtda_palavras_max = 200
    csfont = {'fontname': 'Avenir'}

    for pessoa in df_tokenizado.columns:
        wc = WordCloud(font_path='FontsFree-Net-Avenir-Light.ttf', stopwords=stopwords, background_color="white",
                       colormap='Greys',
                       random_state=6, width=800, height=400)
        wc.generate_from_frequencies(df_tokenizado[pessoa].sort_values(ascending=False).head(qtda_palavras_max))

        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation="bilinear")
        plt.title('{} - Top {} palavras mais usadas'.format(pessoa, qtda_palavras_max), fontsize=20, **csfont)
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.show()

    wc = WordCloud(font_path='FontsFree-Net-Avenir-Light.ttf', stopwords=stopwords, background_color="white",
                   colormap='Greys',
                   random_state=6, width=800, height=400)
    wc.generate_from_frequencies(df_tokenizado.sum(axis=1).sort_values(ascending=False).head(qtda_palavras_max))

    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.title('Top {} palavras mais usadas em todas manchetes'.format(qtda_palavras_max), fontsize=20)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()


def mostrar_qtda_palavras_diferentes():
    plt.figure(figsize=(20, 10))
    g = gridspec.GridSpec(10, 10)

    ax1 = plt.subplot(g[:, :])
    # ax2= plt.subplot(g[:,6:])
    axes = [ax1]

    pessoas = []
    palavras_unicas = []
    for pessoa in df_tokenizado.columns:
        pessoas.append(pessoa)
        palavras_unicas.append(df_tokenizado[df_tokenizado[pessoa] > 0].shape[0])
    qtd_palavras_pessoa = dict(zip(pessoas, palavras_unicas))
    pessoas.append('Todos')
    palavras_unicas.append(df_tokenizado.shape[0])
    pessoas.append('Comum')
    palavras_unicas.append(df_tokenizado[(df_tokenizado > 0).all(1)].shape[0])
    axes[0].axvline(20.5, 0, 1, ls=':', color='gray')
    axes[0].set_xticklabels(pessoas, rotation=45)
    sns.barplot(x=pessoas, y=palavras_unicas, palette="Greys_r", ax=axes[0])

    # print(pd.DataFrame(palavras_unicas,index=pessoas))
    relacao_vocabulario = []
    for pessoa in df_tokenizado.columns:
        df_auxiliar = df_tokenizado[df_tokenizado[pessoa] > 0]
        relacao_pessoa = []
        for pessoa2 in df_tokenizado.columns:
            relacao_pessoa.append((df_auxiliar[df_auxiliar[pessoa2] > 0].shape[0] / qtd_palavras_pessoa[pessoa]))
        relacao_vocabulario.append(relacao_pessoa)
    df_mapa_calor = pd.DataFrame(relacao_vocabulario, columns=df_tokenizado.columns, index=df_tokenizado.columns)
    # sns.heatmap(df_mapa_calor, annot=True,cmap="Greys",cbar=False,ax=axes[1])
    # plt.xlabel("Comparado Com:")
    # plt.ylabel("Comparado De:")
    # plt.title("Relação de vocabulário utilizado (DE x COM)")
    plt.show()


def similariedade_falas(normalizar=0):
    plt.figure(figsize=(20, 10))
    df_proporcoes = pd.DataFrame()
    for pessoa in df_tokenizado.columns:
        df_proporcoes[pessoa] = df_tokenizado[pessoa] / df_tokenizado[pessoa].sum()

    similariedade = []
    maior_valor = 0
    for pessoa in df_tokenizado.columns:
        sim_pessoa = []
        for pessoa2 in df_tokenizado.columns:
            grau_similariedade = math.sqrt((((df_proporcoes[pessoa] - df_proporcoes[pessoa2]) ** 2)).sum())
            if grau_similariedade > maior_valor:
                maior_valor = grau_similariedade
            sim_pessoa.append(grau_similariedade)
        similariedade.append(sim_pessoa)

    if normalizar == 0:
        similariedade_normalizada = [[(j) for j in i] for i in similariedade]
        plt.suptitle('Grau de similariedade')
        plt.title('Quanto maior, menos similar')
    else:
        similariedade_normalizada = [[(j / maior_valor) for j in i] for i in similariedade]
        # plt.suptitle('Grau de similariedade normalizado')
        # plt.title('0 - Mais Similar | 1 - Menos Similar')
    df_mapa_calor_similiriedade = pd.DataFrame(similariedade_normalizada, columns=df_tokenizado.columns,
                                               index=df_tokenizado.columns)
    sns.heatmap(df_mapa_calor_similiriedade, cmap="Greys", cbar=False, annot=True)
    plt.show()


similariedade_falas(1)
mostrar_palavras_comuns()