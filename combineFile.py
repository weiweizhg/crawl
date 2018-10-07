# -*- coding: utf-8 -*-


def save_message(proxy):
    with open('D:\\pyPractice\\crawling\\message.csv','a') as f:
        f.write(proxy[0]+','+proxy[1]+','+proxy[2]+','+proxy[3]+','+proxy[4]+','+proxy[5]+'\n')

def combine_file(file):
    with open(file,'r') as fr:
        for line in fr.readlines():
            res = line.strip().split(',')
            save_message(res)


def main():
    save_message(['ISSN', 'Name', 'ImpactFactor', 'Partition', 'MajorSubject', 'SmallSubject'])
    for id in range(1,21):
        fileAdd = 'D:\\pyPractice\\crawling\\message'+str(id)+'.csv'
        combine_file(fileAdd)


if __name__ == '__main__':
    main()