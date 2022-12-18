import pickle
import numpy as np
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Model
from tensorflow.keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

portal_model = 'Globo'

model = load_model('Models/{}/model.h5'.format(portal_model))

with open('Models/{}/max_size.pickle'.format(portal_model), 'rb') as f:
    tamanho_maximo = pickle.load(f)
    f.close()

with open('Models/{}/mytoken.pickle'.format(portal_model), 'rb') as f:
    mytoken = pickle.load(f)
    f.close()


def gerando_texto(seed_text, next_words, model, max_sequence_len, tokenizer):
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len - 1, padding='pre')
        # predicted = model.predict_classes(token_list, verbose=0)

        predict_x = model.predict(token_list)
        classes_x = np.argmax(predict_x, axis=1)

        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == classes_x:
                output_word = word
                break
        seed_text += " " + output_word
    return seed_text.title()

gerando_texto('Bolsonaro',10,model,tamanho_maximo,mytoken)