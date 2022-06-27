# 1.	Özet
Bu proje Marmara Üniversitesi lisansüstü eğitimim kapsamında Sayın [Dr. Öğr. Üyesi Serkan Aydın](https://avesis.marmara.edu.tr/serkan.aydin)'ın Gömülü Sistemler ve Mobil Uygulamalar dersi için geliştirilmiştir. Projede Raspberry Pi Zero W üzerinde, Docker konteynerizasyon ile Nextcloud bulut sistemi ve PostgreSQL veritabanı kullanılarak kişisel bulut sistemi yapılmıştır. Aynı zamanda mobil cihazlarımıza hızla akan verilerde özellikle fotoğraf arşivlerinde düzenleme yapma amacı güdülmüştür. Farklı isimlerde olan veya üzerine çeşitli efektler (Örn; Instagram filtreleri) yapılan fotoğrafların farklı isimlerle kaydolup olmadığını, benzerlik seviyesini ölçen bir sistem de geliştirilmiştir.

<p align="center">
  <img width="600" height="653" alt="Personal Cloud System" src="/images/personal_cloud_system.png">
  <br><em>Personal Cloud System</em>
</p>

<br><br>

# 2.	Neden Nextcloud?
Nextcloud; dosya depolama, sohbet, proje yönetimi, e-posta, takvim ve kişi rehberi gibi çeşitli uygulamaları bünyesinde barındıran, ev kullanıcıları için ücretsiz bir servistir. Masaüstü, mobil ve web arayüzleri bulunmaktadır. Böylece hızlı bir şekilde birçok özelliği barındıran bir bulut sistemi oluşturulabilir.

Piyasada bu işi yapabilen ücretsiz ve açık kaynaklı Owncloud ve Seafile gibi uygulamalar da bulunmaktadır. Ancak Nextcloud ile bu uygulamaları karşılaştırarak kendi ihtiyaçlarıma en uygun olan uygulamanın Nextcloud olduğuna karar verdim. Bu üç uygulamayı inceleyelim:

<p align="center">
  <img alt="NextCloud & ownCloud & Seafile" src="/images/Nextcloud-ownCloud-Seafile.jpg">
  <br><em>NextCloud & ownCloud & Seafile</em>
</p>

-	İndirme seçenekleri: Nextcloud diğerlerine göre daha fazla indirme seçeneğine sahiptir. Docker container, virtual machine, android ve IOS cihazlar için diğer programlara göre daha fazla indirme seçeneği sunmaktadır. Bunlardan ziyade bazı üreticiler için hazır kurulumları da bulunmaktadır.
-	Dosya paylaşımı: Burada misafir moduna da sahip olan Owncloud önde olsa da Nextcloud da diğerleri gibi bir ekip arasında işbirliği yapabilmek için paylaşım seçenekleri, Collabora Online Office ile entegrasyonu, dosya yorumları, paylaşım bağlantılarına parola koyabilme gibi diğerlerinde de olan özelliklere sahiptir.
-	Desteklenen cihazlar: Üç uygulama da genelde aynı destekleri sunuyor. Nextcloud bir de Windows Mobile cihazlara destek veriyor ancak bu da oran bakımından çok ayırıcı bir nokta değil.
-	Desteklenen uygulamalar: Nextcloud; diğerlerinden farklı olaran ‘Nextcloud Talk’ ve ‘Nextcloud Groupware’ uygulamalarını sunmaktadır. Nextcloud Talk sayesinde kullanıcılar sistem üzerindeki diğer kullanıcılarla text, arama veya web meeting şeklinde konuşmalar gerçekleştirebilir. Nextcloud Groupware sayesinde webmail, takvim ve kişi yönetimi gibi seçenekler sunar.
-	Güvenlik: Her üç uygulama da veri aktarımı sırasında şifreleme, sunucu tarafında şifreleme, uçtan uca şifreleme gibi temel özelliklere sahip olsa da Nextcloud LDAP, SAML, Active Directory ve Kerberos konularında daha da kapsamlı bir güvenlik sunar. Ayrıca Nextcloud scan hizmeti ile sunucunuzun güveliğini analiz eder ve nelerin iyileştirilebileceği konusunda yardım sunar.
-	Enterprise çözümleri: Nextcloud diğer iki sisteme göre maliyet olarak daha düşük, sunduğu özellikler bakımından da daha zengin olmasıyla bu konuda da öne çıkıyor.

<br><br>

# 3.	Kurulum:
Kurulum için bir micro SD karta Raspberry Pi OS kurularak Raspberry Pi Zero W cihazına takılacak ve sistem ayağa kaldırılacaktır. Daha sonra uygulamalarımızı container olarak yüklemek için Docker kurulacak ve ardından Nextcloud imajı indirilerek kurulacaktır. Nextcloud’un verileri saklayabilmesi için Docker Hub’dan PostgreSQL imajı indirilerek kurulacak ve oluşturulan Docker network sayesinde Nextcloud ile haberleştirilecektir. Burada Docker konteynerlarının kullanılmasının en büyük faydası; sistemin direkt hazır paket şeklinde ayağa kaldırılabilir olmasıdır. Böylece sistem çökmelerinde süre ve veri kaybı yaşanmayacak, konteyner otomatik olarak ayağa kalkacaktır. Son olarak Duplicate Image Finder uygulaması da entegre edilerek sistem çalışır hale getirilecektir. 

<br>

## &nbsp;&nbsp;&nbsp;&nbsp;3.1.	Raspberry:
-	*https://www.raspberrypi.com/software/* adresinden **Raspberry Pi Imager** indirilir. 
-	Uygulama çalıştırılır ve SD kart formatlanır: SD kart bilgisayara takılıyken Raspberry Pi Imager açılır. Uygulamanın sunduğu iki seçenekten ilkinde işletim sistemi seçimi, ikincisinden de SD kart seçimi yapılır. 

<p align="center">
  <img alt="Raspberry Pi Imager" src="/images/raspberrypi_imager.png">
  <br><em>Raspberry Pi Imager</em>
</p>

-	Pencerenin sağ altında yer alan ayarlar butonuna tıklanarak açılan pencereden **Enable SSH** seçeneği seçilir ve kullanıcı şifresi belirlenir. **Configure wifi** seçeneği işaretlenerek bağlanılacak wifi ağının bilgileri girilir. *Bu sayede işletim sistemi kurulduktan sonra klavye, monitör gibi herhangi bir donanıma ihtiyaç duyulmadan* sadece Raspberry üzerine SD kart takılıp güç bağlantısı yapılarak uzaktan erişim sağlanabilir.  Bütün ayarlar yapıldıktan sonra ana penceredeki **Write** butonuna tıklanarak işlemin tamamlanması beklenir ve bitti uyarısı verildikten sonra artık SD kart Raspberry üzerine takılabilir.

<p align="center">
  <img alt="Raspberry Pi Imager" src="/images/raspberrypi_imager_settings.png">
  <br><em>Raspberry Pi Imager ayarları</em>
</p>

<br>

**Not:** Raspberry Pi’ye SSH ile bağlantı yapabilmek için IP adresini öğrenmenin çeşitli yolları bulunmaktadır. Ben modem arayüzünden ağa bağlı cihazları görüntüleyip, bu şekilde IP adresine ulaşmayı tercih ettim. Alternatif yöntemler için [bağlantıya](https://raspberrytips.com/find-current-ip-raspberry-pi/) tıklayabilirsiniz.

<p align="center">
  <img alt="Learn Raspberry Pi IP address" src="/images/modem_devices.png">
  <br><em>Modem arayüzünden bağlı olan cihazları görüntüleme</em>
</p>
<br>

## &nbsp;&nbsp;&nbsp;&nbsp;3.2.	Docker:
-	Terminal ekranından komut verilerek sistem & repo güncellemesi yapılır:
```sh
sudo apt-get update && sudo apt-get upgrade
```
-	Kurulum için hazırlanmış olan script indirilir:
```sh
curl -fsSL https://get.docker.com -o get-docker.sh
```
-	Script çalıştırılarak kurulum tamamlanır:
```sh
sudo sh get-docker.sh
```
-	Root kullanıcıları konteynerları çalıştırabilir. Bu yüzden ya ***sudo*** ön eki ile komutlar çalıştırılmalı ya da aşağıdaki kod ile kullanıcı (burada kullanıcı: **pi**) bu gruba eklenmelidir:
```sh
sudo usermod -aG docker [user_name]
```
-	Artık Docker kullanıma hazırdır. docker version ve ```sh docker info``` komutları ile durum görüntülenebilir ve hatta ```sh docker run hello-world``` komutu ile Docker Hello World konteynerı çalıştırılarak sistemin sorunsuzca kurulduğu gözlemlenebilir.

<p align="center">
  <img alt="Docker hello-world" src="/images/docker_hello_world.png">
  <br><em>Docker hello-world</em>
</p>

<br>

## &nbsp;&nbsp;&nbsp;&nbsp;3.3.	Nextcloud ve PostgreSQL kurulumu:
-	 Nextcloud ve PostgreSQL official imajları Docker Hub üzerinden indirilir:
```sh
docker pull nextcloud
docker pull postgres
```
-	Docker üzerinde **nextcloud-net** adında bir köprü ağı oluşturulur. Bu sayede bu isimdeki network kullanılarak kurulacak konteynerların birbirleriyle aynı ağda olması ve dolayısıyla birbirlerini görüp konuşmaları sağlanır:
```sh
docker network create --driver bridge nextcloud-net
```
-	PostgreSQL konteyneri **nextcloud-net** ağı üzerinde ayaklandırılır. ***‘POSTGRES_PASSWORD’*** ortam değişkeni ile parola belirlenir:
```sh
docker run --name postgres -e POSTGRES_PASSWORD=123456 --network nextcloud-net -d postgres
```
-	Nextcloud konteyneri **nextcloud-net** ağı üzerinde ayaklandırılır. ***-p*** parametresi ile **8080** portu dışarıya açılarak dış dünya ile haberleşmesi sağlanır. ***-v*** parametresi ile volume oluşturulur ve Nextcloud üzerinde ***/var/www/html*** yolundaki web arayüzü dosyalarına yerelde ***/home/pi/nextcloud*** adresinden de ulaşılabilmesi sağlanır. 

Artık kurulum tamamlanmıştır. Son olarak kendi IP adresinizi girerek **http://192.168.xx.xx:8080/** web arayüzüne ulaşıp, ayarları yapıp işlemleri tamamlamak gerekmektedir. 
-	Açılan sayfada admin hesabı için kullanıcı adı ve şifre oluşturulur.

<p align="center">
  <img alt="Creating an admin account" src="/images/nextcloud_install_01.png">
  <br><em>Admin hesabı oluşturma</em>
</p>

-	Data klasörü default olarak ***/var/www/html/data*** yolu olarak gelmektedir, istenirse değiştirilebilir.
-	Veritabanları arasından **PostgreSQL** seçilir. ***postgres*** kullanıcı adı ile postgres konteynerini ayaklandırırken kullandığımız ***123456*** şifresi girilerek veritabanı bağlantı ayarları da tamamlanmış olur.


<p align="center">
  <img alt="Configure data folder and database" src="/images/nextcloud_install_02.png">
  <br><em>Data klasörü ve veritabanı ayarları</em>
</p>

-	Son olarak eğer isteniyorsas **Install recommended apps** kutucuğuna tıklanarak **Calendar, Contacts, Talk, Mail & Collaborative editing** uygulamalarının da kurulumu onaylanabilir. ***Finish Setup*** butonuna tıklanarak kurulumun bitmesi ve Nextcloud anasayfasının açılması beklenir.

<p align="center">
  <img alt="Finish setup" src="/images/nextcloud_install_03.png">
  <br><em>Finish setup</em>
</p>


<p align="center">
  <img alt="Nextcloud Home Page" src="/images/nextcloud_main_page.png">
  <br><em>Nextcloud Home Page</em>
</p>

<br>

## &nbsp;&nbsp;&nbsp;&nbsp;3.4.	Nextcloud Mobile App
-	https://nextcloud.com/install/ adresinden mobil cihaza uygun olan market linkine tıklanarak uygulama kurulur. Uygulama açılınca IP adresi ve kullanıcı bilgileri yazılarak uygulamaya giriş yapılır.


<p align="center">
  <img alt="Configure Nextcloud mobile" src="/images/nextcloud_mobile.png">
  <br><em>Nextcloud mobile ayarları</em>
</p>

<br>

## &nbsp;&nbsp;&nbsp;&nbsp;3.5.	Nextcloud Sunucusunu İnternet Ortamına Açma
Nextcloud sunucusu sadece iç ağ ortamında kullanılmak isteniyorsa bu haliyle yeterlidir. Kullanıcı; wifi ağına bağlandığında otomatik olarak cihazındaki veriler buluta depolanacaktır. Ancak dışarı açılmak isteniyorsa statik IP almak, bir domaine bağlamak gibi yöntemler kullanılabilir. Seçilen yönteme göre ya da modem markasına göre izlenecek yollarda farklılıklar oluşabilmektedir. Bu yüzden konu hakkında daha ileri okuma için [link](https://che-adrian.medium.com/make-your-nextcloud-ready-for-accessing-over-the-internet-9a17116a44ce) takip edilebilir:



<br><br>

# 4.	Duplicate Image Finder:
https://github.com/elisemercury/Duplicate-Image-Finder adresinden de ulaşılabilen **Duplicate Image Finder (difPy)** paketi bir veya iki farklı klasördeki görüntüleri arar, bulduğu görüntüleri karşılaştırır ve bunların kopya olup olmadığını kontrol eder. Daha sonra, kopya olarak sınıflandırılan görüntü dosyalarını veya daha düşük çözünürlüğe sahip yinelenen görüntülerin dosya adlarını çıkarır, böylece yinelenen görüntülerden hangilerinin silinmesinin güvenli olduğunu bildirir. Daha sonra bu fotoğraflar manuel olarak da silinebilir veya difPy’ın otomatik olarak silmesine de izin verilebilir. Kurulumu için aşağıdaki script çalıştırılır:
```sh
pip install difPy
```

<br>

# &nbsp;&nbsp;&nbsp;&nbsp;4.1.	Çalışma Mantığı ve Kullanımı
Bir Python paketi olan difPy paketi; **OpenCV, NumPy, scikit-image, collections** gibi paket ve modülleri kullanır. Görüntü benzerliği için **MSE (Mean Squared Error)** kullanır. İki görüntü arasındaki ortalama kare hatası, iki görüntü arasındaki kare farkının toplamıdır. Hata ne kadar düşükse, görüntüler o kadar **“benzer”** olur. Konu hakkında ileri okuma için kaynak:
[Finding Duplicate Images with Python | by Elise Landman | Towards Data Science]([https://www.google.com](https://towardsdatascience.com/finding-duplicate-images-with-python-71c04ec8051))

difPy ile bir klasördeki fotoğraflar şu komutlarla incelenir:
```sh
from difPy import dif
search = dif("C:/Path/to/Folder/")
```
İki klasör incelemek için şu komutlar kullanılır:
```sh
from difPy import dif
search = dif("C:/Path/to/Folder_A/", "C:/Path/to/Folder_B/")
```

**search** sınıfının **result** niteliği kullanılarak sonuçlar yazdırılabilir:
<p align="center">
  <img alt="difPy example usage" src="/images/difPy_01.png">
  <br><em>difPy örnek kullanımı</em>
</p>

<br><br>

# 5.	Sonuçlar:
Kurulan bu sistem gerek bireysel gerekse şirket içi depolama çözümleri için düşük maliyetli, güvenlik risklerini aza indiren, yeterli bir çözümdür. Dosyalara istenilen yerden de ulaşılabilir. Kullanışlı yönlerinden bir tanesi de veriler elimizin altındaki bir cihazda (sd card, flash bellek, hdd, ssd vb.) olduğundan bu cihazın yedeklemesini de hızlı ve güvenli bir şekilde yapabiliriz. Buradaki tek eksik taraf; Raspberry Pi Zero W cihazının bu proje için yetersiz kalmasıdır. Karşılaştığım iki büyük problem ise şunlardı:
-	Kopya fotoğrafları bulmak için kullandığım difPy paketi görüntü işleme kütüphanelerinden faydalandığı için yüksek işlem gücü gerektiriyordu ve bu da işlemlerimin çok yavaşlamasına ve Raspberry cihazımın çok ısınmasına sebebiyet veriyordu. Çözüm; daha yüksek işlem gücüne sahip bir cihaz kullanmak veya depolamayı burada yapıp hesaplamayı merkezi, işlem gücü yüksek bir cihazda yapmak.
-	Wifi üzerinden yapmış olduğum bağlantıda modemim ve bilgisayarım istediğim yüksek hızları vermesine rağmen Raspberry Pi Zero W bu konuda yetersiz kalıyordu. Bir hız testi yapmak için Raspberry komut satırında ```sh sudo apt install speedtest-cli``` komutu ile hız testi paketini kurdum. Daha sonra ```sh speedtest-cli``` komutuyla hız testini çalıştırdım ve **9.14 Mbit/s** hızını aldım. Bu da dosyaların çok geç yedeklenmesine sebebiyet veriyor. Bu yüzden network kartı daha iyi ve işlem gücü daha yüksek bir cihaz kullanımı yapılmalı. Çözüm; kablolu bağlantı yapmak veya daha yüksek donanımlı bir cihaz kullanmak.

<p align="center">
  <img alt="Speedtest CLI" src="/images/speedtest_01.png">
  <br><em>Speedtest CLI</em>
</p>

Buraya kadar takip ettiğiniz için size, ders içeriğinde bize kattıklarından dolayı da Sayın Serkan Aydın hocama çok teşekkür ederim. Konu ile ilgili sorularınız için ***[omeravci@marun.edu.tr](mailto:omeravci@marun.edu.tr?subject=[GitHub]%20Personal%20Cloud)*** mail adresimden iletişime geçebilirsiniz.



