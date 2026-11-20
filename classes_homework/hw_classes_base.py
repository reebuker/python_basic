from math import log

import numpy as np

NGRAM_SIZE_DEFAULT = 1
LOWERCASE_DEFAULT = True
NGRAM_SIZE_ALLOWED = [1, 2]

USE_IDF_DEFAULT = True
DEFAULT_IDF = np.array([])

TOP_N_DEFAULT = 3


class CountVectorizer:
    def __init__(self, lowercase=LOWERCASE_DEFAULT, ngram_size=NGRAM_SIZE_DEFAULT):
        self._vocabulary = {}
        self.lowercase = lowercase
        assert ngram_size in NGRAM_SIZE_ALLOWED
        self.ngram_size = ngram_size

    @property
    def vocabulary(self):
        return self._vocabulary.copy()

    @vocabulary.deleter
    def vocabulary(self):
        self._vocabulary = {}

    @vocabulary.setter
    def vocabulary(self, value):
        if not isinstance(value, dict):
            raise TypeError("Use only dict for vocabulary.setter")
        self._vocabulary = value

    def add_word(self, word):
        if word in self._vocabulary:
            return self._vocabulary[word]
        else:
            self._vocabulary[word] = len(self._vocabulary)
            return self._vocabulary[word]

    def tokenize(self, text: str) -> list[str]:
        tokenized = []
        if self.ngram_size == 1:
            if self.lowercase:
                text = text.lower()
            tokenized = text.split()

        if self.ngram_size == 2:
            if self.lowercase:
                text = text.lower()
            tokens = text.split()
            for i in range(1, len(tokens)):
                tokenized.append(tokens[i - 1] + " " + tokens[i])

        return tokenized

    def fit(self, docs: list[str]) -> None:
        # проверка
        docs_clean = []
        for doc in docs:
            if doc.strip() != "":
                docs_clean.append(doc)

        if not docs_clean:
            raise ValueError("В fit передали пустой корпус")

        # основная функция
        self._vocabulary = {}
        for doc in docs_clean:
            tokens = self.tokenize(doc)
            for token in tokens:
                self.add_word(token)

    # Порядок первого появления, как в задании
    # (На картинке ожидаемого поведения)
    def get_feature_names(self) -> list[str]:
        return list(self._vocabulary.keys())

    def transform(self, docs: list[str]) -> list[list[int]]:
        # проверка
        if not self._vocabulary:
            raise RuntimeError("Словарь пуст")

        # основная функция
        doc_words_count = []
        for doc in docs:
            counts = []
            tokens = self.tokenize(doc)

            for feature in self.get_feature_names():
                counts.append(tokens.count(feature))

            doc_words_count.append(counts)

        return doc_words_count

    def fit_transform(self, docs: list[str]) -> list[list[int]]:
        self.fit(docs)
        return self.transform(docs)

    def to_dict(self) -> dict:
        return {
            "lowercase": self.lowercase,
            "ngram_size": self.ngram_size,
            "vocabulary": self.vocabulary,
        }

    @classmethod
    def from_dict(cls, state):
        obj = cls(lowercase=state["lowercase"], ngram_size=state["ngram_size"])
        obj.vocabulary = state["vocabulary"]
        return obj


class BinaryVectorizer(CountVectorizer):
    def transform(self, docs: list[str]) -> list[list[int]]:
        # основная функция
        result = []
        for doc in docs:
            binary = []
            tokens = self.tokenize(doc)

            for feature in self.get_feature_names():
                binary.append(1 if feature in tokens else 0)

            result.append(binary)

        return result


class TfidfVectorizer(CountVectorizer):
    def __init__(
        self,
        lowercase=LOWERCASE_DEFAULT,
        ngram_size=NGRAM_SIZE_DEFAULT,
        use_idf=USE_IDF_DEFAULT,
    ):
        super().__init__(lowercase=lowercase, ngram_size=ngram_size)
        self._idf = DEFAULT_IDF
        self.use_idf = use_idf

    def get_idf(self, vectors) -> np.ndarray:
        # IDF = log(кол-во документов / кол-во документов, где есть слово t)
        idf = []
        num_of_docs = len(vectors)
        for index in self._vocabulary.values():
            word_occurs = 0
            for vec in vectors:
                word_occurs += 1 if vec[index] > 0 else 0
            # Формула со сглаживанием, как на картинке в ДЗ
            idf.append(log((num_of_docs + 1) / (word_occurs + 1)) + 1)
        return np.array(idf)

    def fit(self, docs: list[str]):
        # в задании словарь строится по порядку вхождения новых слов
        super().fit(docs)
        if not self.use_idf:
            self._idf = DEFAULT_IDF
            return self

        vectors = super().transform(docs)
        self._idf = self.get_idf(vectors)
        return self

    def transform(self, test_texts: list[str]) -> list[list[float]]:
        doc_words_count = super().transform(test_texts)
        tokenized_docs = [self.tokenize(doc) for doc in test_texts]

        # Tf = кол-во вхождений слова t в документ / кол-во слов в документе
        vecs = []
        for doc in range(len(doc_words_count)):
            # clean_doc - только известные слова
            clean_doc = [w for w in tokenized_docs[doc] if w in self._vocabulary]

            if clean_doc:
                vecs.append(np.array(doc_words_count[doc]) / len(clean_doc))
            else:
                vecs.append(np.zeros(len(self._vocabulary)))

        tf = np.array(vecs)
        if self.use_idf:
            return (tf * self._idf).tolist()
        else:
            return (tf).tolist()

    def fit_transform(self, docs: list[str]) -> list[list[float]]:
        self.fit(docs)
        return self.transform(docs)

    # Задание 2
    @classmethod
    def from_config(cls, config):
        obj = cls(
            lowercase=config.get("lowercase", LOWERCASE_DEFAULT),
            use_idf=config.get("use_idf", USE_IDF_DEFAULT),
        )
        return obj

    @property
    def idf(self):
        idf = []
        if len(self._idf) == 0:
            return idf

        for feature_name in self.get_feature_names():
            idf.append(float(self._idf[self._vocabulary[feature_name]]))
        return idf


class KeywordExtractor:
    def __init__(self, vectorizer, top_n=TOP_N_DEFAULT):
        self.vectorizer = vectorizer
        if top_n <= 0:
            raise ValueError
        self._top_n = top_n

    @property
    def top_n(self):
        return self._top_n

    @top_n.setter
    def top_n(self, value):
        if value <= 0:
            raise ValueError
        self._top_n = value

    def fit(self, corpus: list[str]) -> "KeywordExtractor":
        self.vectorizer.fit(corpus)
        return self

    def extract(self, corpus: list[str]) -> list[list[tuple]]:
        weights = self.vectorizer.transform(corpus)
        vocab_words = self.vectorizer.get_feature_names()

        top_n_for_doc = []
        for d in range(len(weights)):
            word_weights = []
            for w in range(len(vocab_words)):
                if weights[d][w] > 0:
                    word_weights.append((vocab_words[w], weights[d][w]))

            word_weights.sort(key=lambda x: (-x[1], x[0]))

            top_n_for_doc.append(word_weights[: self._top_n])

        return top_n_for_doc


def demo():
    # Обучающие сообщения
    TRAIN_CORPUS = [
        "Марс сигнал сигнал",
        "Марс пыль",
        "Марс сигнал антенна",
    ]

    # Сообщения для проверки
    CHECK_CORPUS = [
        "СИГНАЛ шум сигнал",
        "антенна пыль",
        "марс марс марс",
        "комета",
        "",
    ]

    # Сценарий 1
    print("Сценарий 1")
    tfidf_vec = TfidfVectorizer.from_config({})
    matrix = tfidf_vec.fit_transform(TRAIN_CORPUS)

    print("Слова:")
    print(tfidf_vec.get_feature_names())

    print("Idf:")
    print(tfidf_vec.idf)

    print("Tf:")
    print(matrix)
    print()

    # Сценарий 2
    print("Сценарий 2")
    tf_vec = TfidfVectorizer.from_config({"lowercase": False, "use_idf": False})
    CORPUS_2 = ["Марс марс", "МАРС сигнал"]

    tf_vec.fit_transform(CORPUS_2)
    print("Слова:")
    print(tf_vec.get_feature_names())

    print("Idf:")
    print(tf_vec.idf)

    print("Tf:")
    print(tf_vec.transform(CORPUS_2))

    tfidf_vec.fit(["Венера собака"])
    print("Слова:")
    print(tfidf_vec.get_feature_names())

    print("Idf:")
    print(tfidf_vec.idf)

    print("Tf:")
    print(tfidf_vec.transform(["Марс Венера облака"]))
    print()

    # Сценарий 3
    print("Сценарий 3")
    tfidf_vec = TfidfVectorizer()
    kv_ext = KeywordExtractor(tfidf_vec, top_n=2)
    kv_ext.fit(TRAIN_CORPUS)

    print("top_n = 2:")
    print(kv_ext.extract(CHECK_CORPUS))

    print("top_n = 1:")
    kv_ext.top_n = 1
    print(kv_ext.extract(CHECK_CORPUS))

    print("top_n = 0:")
    try:
        kv_ext.top_n = 0
    except ValueError:
        print("Top_n не может быть меньше или равен 0")


if __name__ == "__main__":
    demo()
