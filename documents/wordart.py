import os

from os import path
from wordcloud import WordCloud

# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()


# Read the whole text.
# text = open(path.join(d, 'input.txt')).read()


def generate_word_art(inputfile, outputfile):
    text = open(inputfile, 'r', encoding='UTF-8').read()
    # Generate a word cloud image
    # print(text)
    wordcloud = WordCloud(width=800,height=400).generate(text)

    # Display the generated image:
    # the matplotlib way:
    import matplotlib.pyplot as plt

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    # lower max_font_size
    # wordcloud = WordCloud(max_font_size=40).generate(text)
    # plt.autoscale()
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    # plt.show()
    plt.savefig(str(outputfile) + '.png', bbox_inches='tight', pad_inches=0, facecolor='k')
