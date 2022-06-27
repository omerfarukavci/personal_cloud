from difPy import dif

def test1(): #Tek klasordeki fotograflari karsilastirir.
    search = dif('folder1/', delete=True)
    print(search.result)

def test2(): #Iki klasordeki fotograflari karsilastirir.
    search = dif('folder1/', 'folder2/')
    print(search.result)


if __name__ == '__main__':
    test1()
    print('*' * 70)
    test2()