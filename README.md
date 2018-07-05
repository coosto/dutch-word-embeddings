<h1> <a href="https://www.coosto.com/en"><img align="right" src="https://www.coosto.com/themes/coosto/assets/images/misc/logo-coosto.png" width="180px"></a> Dutch Word2Vec Model </h1>

This repository contains a Word2Vec model trained on a large Dutch corpus, comprised of social media messages and posts from Dutch news, blog and fora. Finding pre-trained Dutch models online can often be quite difficult, especially since most online models are trained on neatly written texts like Wikipedia or newspaper archives. When working with noisy text sources these models usually underperform due to the large number of out-of-vocabulary words used on social platforms and their short-message writing style. By training on a combination of both large and short texts from multiple online sources we've tried to create a model more suited for these types of texts.

We are sharing this model to help research using Dutch data sources, so feel free to use it for your projects! If you would like a more up-to-date model, or a model with specific preprocessing steps, we'd be happy to help! Please contact the current maintainer ([*@Alexander Nieuwenhuijse*](https://github.com/severun)) if you'd like to use this model for commercial products.

## Installation
The model can be downloaded using the provided utils script
```sh
$ git clone https://github.com/severun/dutch-word2vec-model.git
$ cd dutch-word2vec-model
$ python3 utils.py download
```
Or directly as an asset from [release page](https://github.com/coosto/dutch-word-embeddings/releases).

## Usage
To run a demo (using [gensim](https://github.com/RaRe-Technologies/gensim)) for the downloaded model run following command. It will first output some example analogies and afterward present an interactive prompt to query for nearest neighbour terms.
```sh
$ python3 utils.py demo --model model.bin
Loading model...
Model loaded
...
````

## Examples
If we query for "tomaat" (Dutch for tomato) we get a lot of Dutch vegetables:  
<pre>
Enter word or sentence: tomaat
     Term     |      Distance
-----------------------------------
paprika       |0.8452869653701782   (Bell pepper)
komkommer     |0.7932491898536682   (Cucumber)
courgette     |0.771128237247467    (Zucchini)
spinazie      |0.7697550058364868   (Spinach)
aubergine     |0.7646535634994507   (Eggplant)
rucola        |0.7631270885467529   (Arugula)
avocado       |0.7610437273979187   (Avocado)
radijs        |0.7554484605789185   (Radish)
tomaatjes     |0.7549760341644287   (Tomatoes)
tomaten       |0.7525067925453186   (Tomatoes)
</pre>

Another interesting case is "lidl" (A supermarket chain), which returns a list of other supermarkets:
<pre>
Enter word or sentence: lidl
      Term     |      Distance
------------------------------------
aldi           |0.9053274989128113
jumbo          |0.7790680527687073
<b>albert_heijn   |0.7582876086235046</b>
supermarkt     |0.7522222995758057
#lidl          |0.7320866584777832
<b>albert_hein    |0.7161234617233276</b>
<b>albert_heyn    |0.7076783180236816</b>
ekoplaza       |0.6897568702697754
vomar          |0.6830324530601501
nettorama      |0.6739382147789001
</pre>
This example shows some common typographical errors for a supermarket chain called Albert Heijn. This type of errors would not be in the model is it was trained only on neatly written text, like the Dutch Wikipedia data or newspaper articles, but is included in this model because these errors are made a lot on social media.

<hr>

# Data selection & Modeling
The model was trained using ~600 million individual messages, comprised of Dutch social media messages (624 million messages) and Dutch news, blog and fora posts (36 million messages). All messages were published between 01/01/2017 and 31/12/2017. To improve the quality of the model some basic preprocessing was applied to all the messages, described below.

### Splitting sentences
Every individual message was split into separate sentences by searching for punctuation marks, which are only considered to be an end-of-line character if it is not used in the following exceptions:
* (Roman) Numerals
* Single letters
* Abbriviations

### Clean up
Given that social media messages are usually not neatly formatted some cleaning of the text is applied:
1. Converting to lowercase
2. Removing HTML/XML tags
3. Replacing *URLs* with the *\<url\>* token
4. Replacing *@-mentions* with the *\<mention\>* token
5. Removing punctuation marks, emojis and unwanted unicode characters
7. Removing sentences with less than 5 tokens.

The URLs and @-mentions are removed for both privacy and performance reasons. The last step is applied to remove very small text messages, since they usually do not provide enough relevant context to learn from.

### Deduplication
Lastly the entire set of cleaned up sentences is removed from any duplicate training examples and shuffeled into a random order. This results in a training set of 490 million unique preprocessed sentences.

### Training
The model was trained using [Google's Word2Vec implementation](https://code.google.com/p/word2vec/). We've selected the Continuous Bag-of-Words (CBOW) model and generate vectors of size 300. The min-count parameter was chosen based on manual inspection of the vocabulary and to limit the size of the model.
```sh
word2vec -train input.txt -output model.bin -size 300 -window 10 -negative 10 -hs 0 -cbow 1 -sample 1e-5 -iter 5 -min-count 300
```
The resulting model contains 250479 vectors and was not pruned or altered in any way.

License
----
This work is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International License ](https://creativecommons.org/licenses/by-nc/4.0/).

Please contact the current maintainer ([*@Alexander Nieuwenhuijse*](https://github.com/severun)) if you wish to use this model with a different license.
