#	difPy Örnek Kullanım:

Bu örneğimizde **folder1** ve **folder2** olmak üzere iki klasörümüz bulunmakta. Örnek olması açısından iki klasörde de orjinal fotoğraf, bu fotoğrafın Gaussian Blur, Lens Blur uygulanmış halleri ve farklı yüzdelere sahip düşük kalitelerde kaydedilmiş versiyonları bulunmaktadır. **difPy_example.py** dosyasını çalıştırdığımızda, dosyada iki fonksiyon bulunmaktadır. Sırayla inceleyelim:

###	test1 fonksiyonu:
```python3
def test1(): #Tek klasordeki fotograflari karsilastirir.
    search = dif('folder1/', delete=True)
    print(search.result)
```
Çıktısı ise şöyledir:

<p align="center">
  <img alt="test1 fonksiyonu çıktısı" src="/images/output1.png">
  <br><em>test1 fonksiyonu çıktısı</em>
</p>

**folder1** incelenmiş, 7 fotoğraftan orjinal olanı bulunmuş ve diğerleri ```python3 delete=True ``` parametresi ile kullanıcıya sorularak silinmiştir. Silinen fotoğrafların hangilerinin olduğu ekrana yazılmıştır. Son olarak da hangi fotoğrafın hangi fotoğrafa benzediği, hangi klasörde bulunduğu gibi bilgiler gösterilmiştir. Klasörün kod çalışmadan önceki hali ve sonraki hali ise şöyledir:

<p align="center">
  <img alt="Kod çalışmadan önce ve sonra klasörün durumları" src="/images/output3.PNG">
  <br><em>Kod çalışmadan önce ve sonra klasörün durumları</em>
</p>

###	test2 fonksiyonu:
```python3
def test2(): #Iki klasordeki fotograflari karsilastirir.
    search = dif('folder1/', 'folder2/')
    print(search.result)
```
Çıktısı ise şöyledir:

<p align="center">
  <img alt="test2 fonksiyonu çıktısı" src="/images/output2.PNG">
  <br><em>test2 fonksiyonu çıktısı</em>
</p>

İlk fonksiyondan sonra **folder1**  klasöründe sadece orjinal fotoğraf kalmıştır. Bu sefer **folder1** ve **folder2** klasörleri karşılaştırılmış ve ilk klasördeki orjinal fotoğrafa benzeyen diğer fotoğraflar bulunup listelenmiştir.
