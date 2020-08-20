import pandas as pd
import pickle
import nltk
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from joblib import dump
stemmer = SnowballStemmer('spanish')




class CleanTools():
    """Limpieza y steamming de nuevos textos"""

    def __init__(self):
        self.s_ = None
        self.df_ = None

    def clean_str_series(self, s):
        """
        Convierte caracteres de utf8 a ascii y elimina errores


        Parameters:
        -----------
        s: string


        Returns:
        --------
        s: string
        """

        s = s.str.normalize('NFKD').str.encode(
            'ascii', errors='ignore').str.decode('utf-8') \
            .str.capitalize().str.strip().str.replace('[^\w\s]', '')

        return s

    def text_cleaner(self, df,
                     columns_to_clean,
                     columns_not_na):
        """
        Elimina filas de un df en caso de ser vacías y aplica la función
        clean_str_series


        Parameters:
        -----------
        df: dataframe a limpiar
        columns_to_clean: columnas a aplicar clean_str_series
        columns_not_na: columnas a deshechar en caso de que sean NA


        Returns:
        --------
        df: dataframe con columnas limpias
        """

        print("...text_cleaner")
        # Quitar registros no validos
        df[columns_to_clean] = df[columns_to_clean].apply(str)
        df = df.dropna(subset=[columns_not_na], axis=0)

        # Formato texto
        for d in [columns_to_clean]:
            if df[d].dtype == object:
                df[d] = self.clean_str_series(df[d])
         
        df[columns_to_clean] = df[columns_to_clean].str.lower()

        self.df_ = df

    def stem_sentence(self, sentence, min_len=4):
        """
        Aplica steamming a un string


        Parameters:
        -----------
        sentence: string a aplicar steamming
        min_len: mínimo de caracteres en palabras


        Returns:
        --------
        stem_sentence: string con steamming
        """
        token_words = word_tokenize(sentence)
        stem_sentence = []

        for word in token_words:
            if len(word) > min_len:

                stem_sentence.append(stemmer.stem(
                    WordNetLemmatizer().lemmatize(word, pos='v')))

                stem_sentence.append(" ")

        return "".join(stem_sentence)
    
    def stop_words_remover(self, sentence):
        """
        Aplica steamming a un string


        Parameters:
        -----------
        sentence: string a aplicar steamming
        min_len: mínimo de caracteres en palabras


        Returns:
        --------
        stem_sentence: string con steamming
        """
        token_words = word_tokenize(sentence)
        
        stop_words = open("./recursos/stop_words_español.txt", "r")
        stop_words = stop_words.readlines()
        stop_words = [item.replace('\n', "") for item in stop_words]

        filtered_sentence = [w for w in token_words if not w in stop_words] 

        return " ".join(filtered_sentence)

    def stem_sentence_apply(self, limpiar, columns_not_duplicate, columns_to_clean):

        print("...stop words")
    
        text_data = self.df_[columns_to_clean]

        if limpiar:
            self.df_[columns_to_clean] = text_data.apply(
                                                self.stop_words_remover)
            
        return self.df_[columns_to_clean]
