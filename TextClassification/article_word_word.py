#TODO don't touch

# wektory słów od słów dla każdego artykułu

#print(prepare_dictionary(words_pa,key_anti_words+key_pro_words).keys())

r = 2
words = [w for _,w in key_anti_words+key_pro_words]
slowa = words
bliskie_slowa = set()
for a in words_pa:
    for i, w in enumerate(a):
        if w in slowa:
            for n in range(max(i - r, 0), min(i + r, len(a))):
                if a[n] not in slowa:
                    bliskie_slowa.add(a[n])

bliskie_slowa = list(bliskie_slowa)
matrix_pro = []
matrix_anty = []
for article_index,article in enumerate(words_pa):
    if df_train["label"][article_index] == 0:
        slowa = [sl for _,sl in key_anti_words]
        matrix = matrix_anty
    else:
        slowa = [sl for _,sl in key_pro_words]
        matrix = matrix_pro
    kluczowe_w_artykule = [s for s in slowa if s in article]
    matrix.append([np.zeros(len(bliskie_slowa)) for s in kluczowe_w_artykule])
    for word_index,s in enumerate(article):
        if s in slowa:
            for n in range(max(word_index - r, 0), min(word_index + r, len(article))):
                if article[n] not in words:
                    matrix[-1][kluczowe_w_artykule.index(s)][bliskie_slowa.index(article[n])] += 1

#%%

for i in range(len(matrix_pro)):
    matrix_pro[i] = TfidfTransformer().fit_transform(matrix_pro[i]).toarray()

for i in range(len(matrix_anty)):
    matrix_anty[i] = TfidfTransformer().fit_transform(matrix_anty[i]).toarray()

#%%

slowa = {sl: {s: 0 for s in bliskie_slowa} for _,sl in key_pro_words+key_anti_words}
for article_index,article in enumerate(words_pa):
    for word_index,s in enumerate(article):
        if s in slowa:
            for n in range(max(word_index - r, 0), min(word_index + r, len(article))):
                if article[n] not in words:
                    slowa[s][article[n]] += 1

vectors = TfidfTransformer().fit_transform([list(w.values()) for w in slowa.values()])

#%% raw

from minisom import MiniSom
import os

def zwolennik(wiedza,to_czytania,opis="czlek"):

    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, f'plots/{opis}')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    som_zwolennik = MiniSom(10, 10, len(bliskie_slowa), sigma=3, learning_rate =0.05, neighborhood_function='gaussian')
    learn_articles = np.random.choice(wiedza,size=int(len(wiedza)*0.8),replace=False)
    print("Wiedza")
    for i,article in enumerate(learn_articles):
        som_zwolennik.train_random(article, 1)

    print("Nauka")
    plots = []
    slowa_kluczowe = [s for _,s in key_pro_words+key_anti_words]
    colors = ['r' if i>len(key_pro_words) else 'g' for i,_ in enumerate(slowa_kluczowe)]
    for i,article in enumerate(matrix_pro):
        x = plt.figure(figsize=(20, 20))

        for _, (t, c, vec) in enumerate(zip(slowa_kluczowe, colors, vectors.toarray())):
            winnin_position = som_zwolennik.winner(vec)
            plt.text(winnin_position[0], winnin_position[1]+np.random.rand()*.9,t,fontsize=30,color=c)

        plt.xticks(range(10))
        plt.yticks(range(10))
        plt.grid()
        plt.xlim([0, 10])
        plt.ylim([0, 10])
        plt.plot()
        plt.savefig(f"plots/{opis}/w{i}.png")
        plots.append(f"plots/{opis}/w{i}.png")
        plt.close(x)

        som_zwolennik.train_random(article,1)
    print("Gif")
    with imageio.get_writer(F'plots/{opis}/plots.gif', mode='I') as writer:
        for filename in plots:
            image = imageio.imread(filename)
            writer.append_data(image)


zwolennik(matrix_anty,matrix_pro,"anty_czyta_pro")
zwolennik(matrix_pro,matrix_anty,"pro_czyta_anty")
zwolennik(matrix_anty+matrix_pro,matrix_pro,"random_czyta_pro")
zwolennik(matrix_anty+matrix_pro,matrix_anty,"random_czyta_anty")