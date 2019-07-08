#!/usr/bin/env python

from wordcloud import WordCloud
import numpy as np

# https://amueller.github.io/word_cloud/auto_examples/index.html#example-gallery
x, y = np.ogrid[:300, :300]
mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
mask = 255 * mask.astype(int)


def get_word_cloud_by_freq(freq):
    # apt install fonts-wqy-microhei
    font = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
    # Generate a word cloud image
    wc = WordCloud(background_color="white",  mask=mask, font_path=font)
    return wc.generate_from_frequencies(freq)


if __name__ == "__main__":
    from collections import defaultdict
    import matplotlib.pyplot as plt
    import pandas as pd

    df = pd.read_csv("../key_info.csv", index_col=0, dtype=str)
    freq = defaultdict(int)
    for index, row in df.iterrows():
        if row["primary_key"]:
            freq[row["primary_key"]] += 8
        if row["secondary_key"]:
            freq[row["secondary_key"]] += 4
        if row["ternary_key"]:
            freq[row["ternary_key"]] += 2
        if row["quartus_key"]:
            freq[row["quartus_key"]] += 1
        if row["fifth_key"]:
            freq[row["fifth_key"]] += 1
    print(freq)
    # Display the generated image:
    # the matplotlib way:
    wordcloud = get_word_cloud_by_freq(freq)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    # The pil way (if you don't have matplotlib)
    # image = wordcloud.to_image()
    # image.show()
