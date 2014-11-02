Proverb Generator
=================

Depends on
----------

- the python library nltk : http://www.nltk.org/
- the C++ library lttoolbox : http://wiki.apertium.org/wiki/Lttoolbox

Building
--------

Execute the ``build.sh`` script to build the ``libltpy.so`` library, which will be used to interface our python program with lttoolbox.

It may require some adjustments to the location of your lttoolbox installation.

Using
-----

All functions are defined in the ``main.py`` file. To use them, start a python shell in this folder and import them with ``from main import *``.

### Building the background graph

We cannot provide the background graph as it is quite heavy (the fie is around 100MB). To build it, we provide two functions :

```
add_file_to_background_graph(graph_file, input_file)
```

This function inputs the whole ``input_file`` into the graph stored in ``graph_file``. If the graph file doesn't exist, it is created.

```
add_words_to_background_graph(graph_file, words)
```

This function add a list of words to the background graph in ``graph_file``. The word list is expected to be in the same format as the output of ``nltk.word_tokenize()``. If the graph file doesn't exist, it is created.

In order to build the same graph as the one we used, run :

```
add_file_to_background_graph("proverbs.bgraph", "proverbsList.txt")
import nltk
add_words_to_background_graph("proverbs.bgraph", nltk.corpus.brown.words())
add_words_to_background_graph("proverbs.bgraph", nltk.corpus.gutenberg.words())
```

### Using the generator

Once the background graph is created, you can make a generator object using it :

```
g = ProverbGenerator("proverbs.bgraph")
```

This will take some time to create it : the graph is normalized during the loading.

Then, you can generate proverbs by giving the generator an input word :

```
g.generate("darkness")
```

It will output the proverb used as a gramatical basis, as well as the generated proverb.

Note : if the input word is not in the graph, or is linked to too few words, the generated proverb will likely be the same as the one used as a basis.

