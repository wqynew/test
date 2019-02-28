# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 14:04:07 2019

@author: wuqia
"""

import os,random,math,re,sys,subprocess
from shutil import copyfile
import numpy as np
import argparse

#from itertools import imap

def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print(proc_stdout)


def anyTrue(predicate, sequence):
    #return True in imap(predicate, sequence)
    for s in sequence:
        if predicate(s):
            return True
    return False    


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
       os.makedirs(path)


def filterFiles(folder, exts, list):
    for fileName in os.listdir(folder):
        if os.path.isdir(folder + '/' + fileName):
            filterFiles(folder + '/' + fileName, exts, list)
        elif anyTrue(fileName.endswith, exts):
            list.append(folder + '/' + fileName)


def find_running():
    username = subprocess.check_output(['whoami']).decode().splitlines()[0].replace('\"', '').replace(' ', '')
    running = []
    lines = subprocess.check_output(['squeue', '-u', username, '--format=\"%.100j\"']).decode().splitlines()
    for l in lines:
        running.append(l.replace('\"', '').replace(' ', ''))
    return running


def gen_script_for_each_xml(ite,root_path, built_binary_path, gen_scripts_path, result_path):

    # print(elements[len(elements)-1])
    sub_path = gen_scripts_path + '/' + str(ite)
    mkdir(root_path + '/' + sub_path)

    
    print('Generating Script: ' + root_path + '/' + sub_path + '/run.sh')

    f = open(root_path + '/' + sub_path + '/run.sh', 'w')

    script = '#!/bin/bash\n'
    script += '#SBATCH --job-name=' + str(ite) + '\n'
    script += '#SBATCH --output=%x.out\n'
    #script += '#SBATCH --cpus-per-task=2\n'
    #script += '#SBATCH --time=10-00:00:00\n'
    #script += '#SBATCH --output=%x.out\n'
    #script += '#SBATCH --error=%x.err\n'
    #script += '#SBATCH --ntasks=1\n'
    #script += '#SBATCH --mem=1G\n'
    script += '#SBATCH -t 2\n'
    script += '#SBATCH -n 2\n'
    script+='#SBATCH --mem-per-cpu=128\n'
    script+='#SBATCH --share\n'
    script+='#SBATCH --gres=gpu\n'
    script+='. ~/.profile\n'
    script+='module load python/3.5.1\n'
    script+='module load cuDNN/v7.2.1\n'
    script+='module load cuda/9.1.85\n'
    script+='module load pytorch/0.4.1\n'
    script+='module load tensorflow/1.11.0/cuda\n'
    #script += '#SBATCH --mem-per-cpu=128\n'
    script += 'python3 ' + root_path +'/' + built_binary_path + ' '
    script += str(ite) + '\n'

    f.write(script)
    f.close()

    running = find_running()

    print(root_path + '/' + sub_path)

    if os.path.exists(root_path + '/' + result_path + str(ite)):
        print('Dataset Generated!')
    elif str(ite) in running:
        print('Running Script ' + str(ite) + '!')
    else:
        subprocess_cmd('cd ' + root_path + '/' + sub_path + '; sbatch run.sh;')

    # print(sub_path)



def gen_all_scripts( root_path, built_binary_path, gen_scripts_path, final_result_path):

    if not os.path.exists(root_path + '/' + gen_scripts_path):
        os.mkdir(root_path + '/' + gen_scripts_path)

    if not os.path.exists(root_path + '/' + final_result_path):
        os.mkdir(root_path + '/' + final_result_path)

    # for i in range(len(xml_file_list)):
    for i in range(2):
        gen_script_for_each_xml(i, root_path,built_binary_path,
                                gen_scripts_path, final_result_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=os.path.basename(__file__))
    parser.add_argument('--root_path',default=os.path.dirname(os.path.realpath(__file__)))
    parser.add_argument('--built_binary_path',default='test.py')
    parser.add_argument('--gen_scripts_path',default='batch')
    parser.add_argument('--final_result_path',default='output')
    args = parser.parse_args()
    gen_all_scripts(
                    args.root_path,  
                    args.built_binary_path, 
                    args.gen_scripts_path, 
                    args.final_result_path)

