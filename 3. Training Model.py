# importando bibliotecas
import numpy as np
import pandas as pd
import matplotlib.pyplot as ply
import pickle
import re
import string
import time

import tensorflow as tf
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.preprocessing.text import Tokenizer
from keras.callbacks import EarlyStopping, TensorBoard, ModelCheckpoint
from keras.models import Sequential
from tensorflow.keras.utils import to_categorical

from sklearn.model_selection import train_test_split

# ABRINDO E COLOCANDO DADOS NA FORMATAÇÃO CORRETA (DATAFRAME COM COLUNA AUTOR E COLUNA TEXTO)


todos_portais = ['Band', 'BBC', 'Folha de SP', 'Gazeta do Povo', 'Globo',
                 'iG', 'R7', 'UOL', 'Veja', 'Carta Capital', 'Revista Forúm',
                 'Brasil de Fato', 'Pleno News', 'Terça Livre', 'Renova Mídia',
                 'Conexão Política', 'Jornal da Cidade', 'El Pais', 'Deutsche Welle', 'Estadão', 'Isto É']


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


df_textos = juntando_todas_informacoes(todos_portais).drop('data', 1)
df_textos = df_textos.rename(columns={'portal': 'Autor', 'manchete': 'Texto'}, inplace=False)

# df_textos é uma DataFrame com a primeira coluna sendo o autor e a segundo coluna sendo o texto

def filtrando_por_autor(df_original, filtro_autor=''):  # Se filtro do autor for '' serão considerados todos autores

    # Se o filtro inputado não existir na dataframe, serão considerados todos autores
    if filtro_autor not in df_original.Autor.value_counts().index:
        filtro_autor = ''

    # deixando todos textos do mesmo tamanho
    if filtro_autor == '':
        nova_df = df_original.copy()
    else:
        nova_df = df_original.copy()
        nova_df = nova_df[nova_df.Autor == filtro_autor]

    return nova_df


# Formatando a coluna textos da dataframe

def limpar_texto(texto):
    texto = texto.lower()  # padroniza as letras
    texto = re.sub('(:?https?:\/\/[^\s]*)|www.[^\s]*', '', texto)  # remove os links
    texto = re.sub('(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])',
                   '', texto)  # remove emojis
    # texto = re.sub('[%s]' % re.escape(string.punctuation), ' ', texto) # remove as pontuações
    # texto = re.sub('\w*\d\w*', '', texto) # remove as palavras que iniciam com números

    return texto


# =============================================================================================================================#

def formatando_textos(df_original):
    df_original['Texto'] = df_original.Texto.apply(limpar_texto)

    return df_original


# Transformando cada palavra em um número (token) único

def substituindo_palavras_numeros(df_original):
    myTokenizer = Tokenizer()
    myTokenizer.fit_on_texts(df_original.Texto)

    df_nova = df_original[['Autor', 'Texto']]
    df_nova['Texto'] = myTokenizer.texts_to_sequences(df_nova.Texto)

    return df_nova, myTokenizer


# Criando dataframe com enunciados segmentados
# cada texto vai ser dividio em varios pequenos textos

def segmentando_textos(df_original):
    texto_novo = []
    autor_novo = []

    for i, row in df_original.iterrows():
        for j in range(1, len(row.Texto)):
            autor_novo.append(row.Autor)
            texto_novo.append(row.Texto[:j + 1])

    df_segmentada = pd.DataFrame({'Autor': autor_novo, 'Texto': texto_novo})

    return df_segmentada


def ajustes_finais_dataframe(df_original, numero_palavra):
    df_original['Texto'] = pad_sequences(df_original.Texto).tolist()
    tamanho_maximo_seq = len(df_original['Texto'][0])

    df_final = pd.DataFrame()
    df_final['Predictors'] = df_original['Texto'].apply(lambda x: x[:-1])
    df_final['Label'] = df_original['Texto'].apply(lambda x: x[-1])

    nova_label = []
    for i, a in df_final.Label.iteritems():
        nova_label.append(to_categorical(a, num_classes=numero_palavra))
    df_final['Label'] = nova_label

    return df_final, tamanho_maximo_seq


def criar_modelo(tamanho_maximo_sequencia, total_palavras):
    input_tamanho = tamanho_maximo_sequencia - 1
    model = Sequential()

    # Add Input Embedding Layer
    model.add(Embedding(total_palavras, 10, input_length=input_tamanho))

    # Add Hidden Layer 1 - LSTM Layer
    model.add(LSTM(100))
    model.add(Dropout(0.1))

    # Add Output Layer
    model.add(Dense(total_palavras, activation='softmax'))

    opt = tf.keras.optimizers.Adam(lr=0.001, decay=1e-6)

    model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

    return model


def rodando_programa(df_original, autor=''):
    df_filtrada = filtrando_por_autor(df_original, autor)
    df_textos_limpos = formatando_textos(df_filtrada)
    df_tokenizado, myTokenizer = substituindo_palavras_numeros(df_textos_limpos)
    numero_palavras = len(myTokenizer.word_index) + 1
    df_segmentada = segmentando_textos(df_tokenizado)
    df_final, tamanho_sequencia = ajustes_finais_dataframe(df_segmentada, numero_palavras)
    # model = criar_modelo(tamanho_sequencia, numero_palavras)

    X = df_final.Predictors
    y = df_final.Label
    X_corr = np.concatenate(X.apply(lambda x: np.asarray(x))).reshape(X.shape[0], len(X[0]))
    y_corr = np.concatenate(y.apply(lambda x: np.asarray(x))).reshape(y.shape[0], len(y[0]))

    X_train, X_test, y_train, y_test = train_test_split(X_corr, y_corr,
                                                        test_size=0.2,
                                                        random_state=1)

    return myTokenizer, tamanho_sequencia, numero_palavras, X_train, X_test, y_train, y_test

mytoken, tamanho_maximo, numero_palavras, X_train, X_test, y_train, y_test = rodando_programa(df_textos,'UOL')

EPOCHS = 10
BATCH_SIZE = 10

AUTOR = 'UOL'

NOME = f'{AUTOR}-AUTOR -- {EPOCHS}-EPOCHS -- {BATCH_SIZE}-BATCH_SIZE -- {int(time.time())}'

model = criar_modelo(tamanho_maximo,numero_palavras)

#tensorboard = TensorBoard(log_dir=f'logs/{NOME}')

#filepath = 'RNN_Final-{epoch:02d}-{val_acc:.3f}'
#checkpoint = ModelCheckpoint('models/{}.model'.format(filepath,monitor='val_acc',verbose=1, save_best_only=True, mode='max'))

model.fit(X_train, y_train,
          batch_size=BATCH_SIZE,
          epochs=EPOCHS,
          validation_split = 0.2)

model.save('Models/{}/model.h5'.format(AUTOR))

with open('Models/{}/max_size.pickle'.format(AUTOR), 'wb') as f:
    pickle.dump(tamanho_maximo, f)
    f.close()

with open('Models/{}/mytoken.pickle'.format(AUTOR), 'wb') as f:
    pickle.dump(mytoken, f)
    f.close()
