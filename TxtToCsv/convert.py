if __name__ == "__main__":
    index = 0
    output = open('data.csv','w',encoding='utf-8')
    print('id\tlabel\tdata',file=output)
    with open('antyvaccine.txt', encoding='utf-8' ) as file:
        for line in file:
            line = line.rstrip().replace('\t', ' ')
            if line:
                index += 1
                print(index, 0, line,file=output,sep='\t')

    with open('provaccine.txt', encoding='utf-8' ) as file:
        for line in file:
            line = line.rstrip().replace('\t', ' ')
            if line:
                index += 1
                print(index, 1, line,file=output,sep='\t')
    output.close()