import torch
import os
import random
import math
import time
from torch.autograd import Variable

class DataSet:
    def __init__(self, datapath, batch_size):
        self.dictionary = {'<unk>': 0}
        self.sentence = []
        self.batch_size = batch_size


        print('Loading data from %s ...'%datapath)
        start_time = time.time()
        with open(datapath,'r') as f:
            self.num_tokens = 0
            self.num_vocb = 1

            for line in f:
                sequence = []
                tokens = line.split() + ['<eos>']
                self.num_tokens += len(tokens)
                # Build dictionary

                for token in tokens:
                    if token not in self.dictionary:
                        self.dictionary[token] = self.num_vocb 
                        self.num_vocb += 1
                    sequence.append(self.dictionary[token])
                # Add digit sequence
                #self.sentence.append(sentence)
                self.sentence.append(torch.LongTensor(sequence))
        print('Data discription:')
        print('Data name : %s'%datapath)
        print('Number of sentence : %d'%len(self.sentence))
        print('Number of tokens %d'%self.num_tokens)
        print('Finishing loading data in %f s.'%(time.time()-start_time))

        self.num_batch = int(len(self.sentence) / self.batch_size)
        
        self.shuffle = range(self.__len__())
        random.shuffle(self.shuffle)
        

    def shuffle_batch(self):
        self.shuffle(self.shuffle)


    def get_batch(self, batch_idx):
        lengths = [self.sentence[x].size(0) for x in range(self.batch_size * batch_idx, self.batch_size * (batch_idx + 1))]
        max_len = max(lengths)
        lengths = Variable(torch.LongTensor(lengths))
        
        batch_data = torch.zeros(self.batch_size, max_len)
        for i in range(self.batch_size):
            sequence_idx = i + self.batch_size * batch_idx
            batch_data[i].narrow(0, 0, lengths.data[i]).copy_(self.sentence[sequence_idx])

        return Variable(batch_data.t()), lengths


    def __getitem__(self, index):
        return self.get_batch(index) 

    def __len__(self):
        return self.num_batch

#Test
if __name__ == '__main__':
    test_data_path = 'data/penn/test.txt'
    test_dataset = DataSet(test_data_path, batch_size = 64)
    batch_data,_ = test_dataset[0]
    print(batch_data.data)
    for i in range(len(test_dataset)):
        batch_data, lengths = test_dataset[i]
        print(batch_data.size())
        