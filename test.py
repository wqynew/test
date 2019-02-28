# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 14:06:42 2019

@author: wuqia
"""
import argparse
import sys
import os

    
import multiprocessing as mp
import threading as td
import time
import tensorflow as tf


def job(q,c):
    res = c
    for i in range(2):
        res += i+i**2+i**3
    q.put(res)
    
def multcore(c):
    q = mp.Queue()
    p1 = mp.Process(target=job,args=(q,c,))
    p2 = mp.Process(target=job,args=(q,c,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    res1 = q.get()
    res2 = q.get()
    print('multicore:',res1+res2)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description=os.path.basename(__file__))
    parser.add_argument('ite',type=int,default=5)
    args = parser.parse_args()
    args.ite=args.ite+1
    sys.stdout.write(str(args.ite))
    
    print (args.ite)

    print('tensorflow:', tf.add(1, 2))

    st = time.time()
    multcore(args.ite)
    st3 = time.time()
    print('multicode time:',st3 - st)
    



