This is the solution to programming assignment 4.

### Caveate
1. The original `tag.model` file uses ':' for delimiter. ':' will interfere with the contents, making parsing the model file hard. This is especially true when adding custom features in task 2 and 3. So I wrote a awk script that will convert tag.model to tag.model.converted by running
```
cat tag.model | awk -f convert_model.awk > tag.model.converted
```

2. I used a home made logger lib for logging. You'll probably fail running my python file for lacking the lib. Just remove all lines containing _logger if you need to.

### Usage

#### Task 1: Viterbi algorithm
```
python viterbi.py tag.model.converted gene.dev > gene.dev.p1.out
python eval_gene_tagger.py gene.key gene.dev.p1.out
```
It will read model file from `tag.model.converted`. For the corpus in gene.dev, it will output to gene.dev.p1.out 

#### Task 2 and task 3: Perceptron algorithm with custom features

```
python train.py p3.model
python viterbi.py p3.model gene.dev suf > gene.dev.p3.out
python eval_gene_tagger.py gene.key gene.dev.p3.out
```

Task 2 and 3 will use same code because task 3 only added prefix features and having separate files for them doesn't make sense.

Above command will train a model and write to p3.model. Ten use it to predict tags in gene.dev.

For task 2. I tried to train the GLM myself using only trigram tag feature and tag-token feature. It should be identical to tag.model. However, I got 0.438 F1 score on it.

My best F1 so far is 0.56. Someone from the discussion forum claim to reach 0.6 plus F1.

