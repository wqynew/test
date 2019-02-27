# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 14:06:42 2019

@author: wuqia
"""
import argparse
import sys
import os
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=os.path.basename(__file__))
    parser.add_argument('ite',type=int,default=5)
    args = parser.parse_args()
    args.ite=args.ite+1
    sys.stdout.write(args.ite)
    print (args.ite)
