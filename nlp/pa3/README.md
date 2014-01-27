This is the implementatoin of PA3(machine translation) of the NLP course in Coursera.

### Caveate

1. There are different number of lines in the training data. More specifically, there are blink lines in the files. This takes me one day to find out.

2. The training can take quite some time. More so if you didn't calcuate the denominator in advance.

3. The models trained can be large, so I removed the model files.

### Usage

#### Task 1: IBM1 model

1. Training
```
python ibm1_train.py
```
The training files, **corpus.es** and **corpus.en**, are hard coded in the source code. It will pickle the model to local file **ibm1.model**.

2. Decoding
```
python ibm1_decode.py dev.es dev.en > dev.p1.out
```

#### Task 2: IBM2 model

1. Training
```
python ibm2_train.py
```
Like task 1, the paths of training files are hard coded. Besides it assumes IBM1 model has been trained and stored at **./ibm1.model**. The calculation t(f|e) will begine from that model in the first iteration of EM algorithm. It will pickle the trained model to **./ibm2.model**.

2. Decoding
```
python ibm2_decode.py dev.es dev.en > dev.p2.out
```
My score in the dev data reached 0.461 in F1 score. It exceeds the solution provided by TA. I've not time to find out the reason for now.

### Task 3: Growing alignments

1. Training
```
python better_align_train.py
```
It will train English to Spanish IBM1 model and IBM2 model.

2. Decoding
```
python better_align_decode.py dev.es dev.en > dev.p3.out
```
Both my code and TA's code ended up only output the alignments that are intersection of the two models. Mine got a F1 score of 0.498 with precision of 0.774. Again it beat the benchmark provided on dev data but I don't know why. Completing the suggested heuristics will improve recall in expense of precision and the F1 score will be worsen.
