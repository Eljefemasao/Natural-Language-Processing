
# -*- coding: utf-8 -*-


from gensim import models
from tqdm import tqdm
import os
import glob
from sklearn.manifold import TSNE
import pandas as pd
import matplotlib.pyplot as plt


CHAR_DATA_DIR = './test_file/'       # Single Words data which was extract from original data.
INDEX_DATA_DIR = './classify_novel/917.txt'   # Original data's file name which mean title of book. Number is 10.


class LabeledListSentence(object):
    def __init__(self, words_list, labels):
        self.words_list = words_list
        self.labels = labels

    def __iter__(self):
        for i, words in enumerate(self.words_list):
            yield models.doc2vec.LabeledSentence(words, ['%s' % self.labels[i]])


def make_train_file(directory):

    result_text = []
    result_index = []

    # get test_data_file's path and connect the all files.
    file_path = glob.glob(os.path.join(directory, '*.txt'))

    for f_p in file_path:
        pre_text = []
        with open(f_p, 'r') as f:
            for rows in f:
                lines = rows.strip()
                pre_text.append(lines)
            result_text.append(pre_text)

    with open(INDEX_DATA_DIR, 'r') as index:
        for row in index:
            line = row.strip()
            result_index.append(line)

    return result_text, result_index, file_path


def display_result(model, result_index):

    print("\n")

    # detect similar word with its degree of relatedness number.
    char = '僕'
    print("<<Word analyzing about: %s>>" % char)
    print("\n")
    results = model.most_similar(positive=[char])

    for result in results:
        print(result[0])

        with tqdm(total=100) as pbar:
            for i in range(int(result[1] * 1000)):
                pbar.update(0.1)

    print("\n")

    # detect similar document with its degree of relatedness number.
    title = 5
    print("<<Book's title analyzing about: title=%s>>" % result_index[title])
    print("<<Index = %s>>" % result_index)

    print("\n")
    results1 = model.docvecs.most_similar(positive=[title])
    for result1 in results1:
        print(result1[0])

        with tqdm(total=100) as pbar:
            for i in range(int(result1[1] * 1000)):
                pbar.update(0.1)

    print("\n")


def plot_degree_of_relatedness(model):

    # It gets a standalone vocab list for the final dataframe to plot.
    # And for knowing the order of the words.
    vocab = list(model.wv.vocab)
    X = model[vocab]
    print(len(X))
    print(X[0])
    tsne = TSNE(n_components=2)
    X_tsne = tsne.fit_transform(X)

    df = pd.DataFrame(X_tsne, index=vocab, columns=['x', 'y'])
    print(df)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(df['x'], df['y'])
    for word, pos in df.iterrows():
        ax.annotate(word, pos)

    plt.show()


def main():

        result_text, result_index, file_path = make_train_file(CHAR_DATA_DIR)
        sentences = LabeledListSentence(result_text, result_index)
        model = models.Doc2Vec(alpha=0.025, min_count=5,
                               size=100, iter=20, workers=4)

        model.build_vocab(sentences)
        model.train(sentences, total_examples=sum([len(w) for w in file_path]), epochs=model.iter)
        model.save('./data/doc2vec.model')
        model = models.Doc2Vec.load('./data/doc2vec.model')

        display_result(model, result_index)

        plot_degree_of_relatedness(model)


if __name__ == '__main__':

    main()
