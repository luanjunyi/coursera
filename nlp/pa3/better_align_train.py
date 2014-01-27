import cPickle as pickle
import ibm1_train
import ibm2_train
from ibm1_train import load_corpus, IBM1

# We assume Spanish to English IBM2 model has been trained and is pickled as 'ibm2.model'
if __name__ == "__main__":
    en2es_ibm1 = ibm1_train.IBM1("corpus.en", "corpus.es")
    en2es_ibm1.train()
    with open("en2es.ibm1.model", "w") as outfile:
        pickle.dump(en2es_ibm1, outfile)
        

    en2es_ibm2 = ibm2_train.IBM2("corpus.en", "corpus.es")
    en2es_ibm2.train("en2es.ibm1.model")
    with open("en2es.ibm2.model", "w") as outfile:
        pickle.dump(en2es_ibm2, outfile)
