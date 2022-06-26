# 1.	Özet
Bu projede Raspberry Pi Zero W üzerinde, Docker konteynerizasyon ile Nextcloud bulut sistemi ve PostgreSQL veritabanı kullanılarak kişisel bulut sistemi yapılmıştır. Aynı zamanda mobil cihazlarımıza hızla akan verilerde özellikle fotoğraf arşivlerinde düzenleme yapma amacı güdülmüştür. Farklı isimlerde olan veya üzerine çeşitli efektler (Örn; Instagram filtreleri) yapılan fotoğrafların farklı isimlerle kaydolup olmadığını, benzerlik seviyesini ölçen bir sistem de geliştirilmiştir.
<br><br>

# 2.	Neden Nextcloud?
Nextcloud; dosya depolama, sohbet, proje yönetimi, e-posta, takvim ve kişi rehberi gibi çeşitli uygulamaları bünyesinde barındıran, ev kullanıcıları için ücretsiz bir servistir. Masaüstü, mobil ve web arayüzleri bulunmaktadır. Böylece hızlı bir şekilde birçok özelliği barındıran bir bulut sistemi oluşturulabilir.

Piyasada bu işi yapabilen ücretsiz ve açık kaynaklı Owncloud ve Seafile gibi uygulamalar da bulunmaktadır. Ancak Nextcloud ile bu uygulamaları karşılaştırarak kendi ihtiyaçlarıma en uygun olan uygulamanın Nextcloud olduğuna karar verdim. Bu üç uygulamayı inceleyelim:

<p align="center">
  <img alt="NextCloud & ownCloud & Seafile" src="/images/Nextcloud-ownCloud-Seafile.jpg">
</p>

-	İndirme seçenekleri: Nextcloud diğerlerine göre daha fazla indirme seçeneğine sahiptir. Docker container, virtual machine, android ve IOS cihazlar için diğer programlara göre daha fazla indirme seçeneği sunmaktadır. Bunlardan ziyade bazı üreticiler için hazır kurulumları da bulunmaktadır.
-	Dosya paylaşımı: Burada misafir moduna da sahip olan Owncloud önde olsa da Nextcloud da diğerleri gibi bir ekip arasında işbirliği yapabilmek için paylaşım seçenekleri, Collabora Online Office ile entegrasyonu, dosya yorumları, paylaşım bağlantılarına parola koyabilme gibi diğerlerinde de olan özelliklere sahiptir.
-	Desteklenen cihazlar: Üç uygulama da genelde aynı destekleri sunuyor. Nextcloud bir de Windows Mobile cihazlara destek veriyor ancak bu da oran bakımından çok ayırıcı bir nokta değil.
-	Desteklenen uygulamalar: Nextcloud; diğerlerinden farklı olaran ‘Nextcloud Talk’ ve ‘Nextcloud Groupware’ uygulamalarını sunmaktadır. Nextcloud Talk sayesinde kullanıcılar sistem üzerindeki diğer kullanıcılarla text, arama veya web meeting şeklinde konuşmalar gerçekleştirebilir. Nextcloud Groupware sayesinde webmail, takvim ve kişi yönetimi gibi seçenekler sunar.
-	Güvenlik: Her üç uygulama da veri aktarımı sırasında şifreleme, sunucu tarafında şifreleme, uçtan uca şifreleme gibi temel özelliklere sahip olsa da Nextcloud LDAP, SAML, Active Directory ve Kerberos konularında daha da kapsamlı bir güvenlik sunar. Ayrıca Nextcloud scan hizmeti ile sunucunuzun güveliğini analiz eder ve nelerin iyileştirilebileceği konusunda yardım sunar.
-	Enterprise çözümleri: Nextcloud diğer iki sisteme göre maliyet olarak daha düşük, sunduğu özellikler bakımından da daha zengin olmasıyla bu konuda da öne çıkıyor.
<br><br>

# 3.	Kurulum:
Kurulum için bir micro SD karta Raspberry Pi OS kurularak Raspberry Pi Zero W cihazına takılacak ve sistem ayağa kaldırılacaktır. Daha sonra uygulamalarımızı container olarak yüklemek için Docker kurulacak ve ardından Nextcloud imajı indirilerek kurulacaktır. Nextcloud’un verileri saklayabilmesi için Docker Hub’dan PostgreSQL imajı indirilerek kurulacak ve oluşturulan Docker network sayesinde Nextcloud ile haberleştirilecektir. Son olrak Duplicate Image Finder uygulaması da entegre edilerek sistem çalışır hale getirilecektir.
<br>
## &nbsp;&nbsp;&nbsp;&nbsp;3.1.	Raspberry:
-	https://www.raspberrypi.com/software/ adresinden Raspberry Pi Imager indirilir. 
-	Uygulama çalıştırılır ve SD kart formatlanır: SD kart bilgisayara takılıyken Raspberry Pi Imager açılır. Uygulamanın sunduğu iki seçenekten ilkinde işletim sistemi seçimi, ikincisinden de SD kart seçimi yapılır. 

<p align="center">
  <img alt="Raspberry Pi Imager" src="/images/raspberrypi_imager.png">
</p>

-	Pencerenin sağ altında yer alan ayarlar butonuna tıklanarak açılan pencereden ‘Enable SSH’ seçeneği seçilir ve kullanıcı şifresi belirlenir. ‘Configure wifi’ seçeneği işaretlenerek bağlanılacak wifi ağının bilgileri girilir. Bu sayede işletim sistemi kurulduktan sonra klavye, monitör gibi herhangi bir donanıma ihtiyaç duyulmadan sadece Raspberry üzerine SD kart takılıp güç bağlantısı yapılarak uzaktan erişim sağlanabilir.  Bütün ayarlar yapıldıktan sonra ana penceredeki ‘Write’ butonuna tıklanarak işlemin tamamlanması beklenir ve bitti uyarısı verildikten sonra artık SD kart Raspberry üzerine takılabilir.

<p align="center">
  <img alt="Raspberry Pi Imager" src="/images/raspberrypi_imager_settings.png">
</p>

Not: Raspberry Pi’ye SSH ile bağlantı yapabilmek için IP adresini öğrenmenin çeşitli yolları bulunmaktadır. Ben modem arayüzüne bağlanıp ağa bağlı cihazları görüntüleyip oradan IP adresine ulaşmayı tercih ettim.

<br>

## &nbsp;&nbsp;&nbsp;&nbsp;3.2.	Docker:
-	Terminal ekranından komut verilerek güncelleme yapılır.
sudo apt-get update && sudo apt-get upgrade
-	Kolay kurulum için hazırlanmış olan script indirilir.
curl -fsSL https://get.docker.com -o get-docker.sh
-	Script çalıştırılarak kurulum tamamlanır.
sudo sh get-docker.sh
-	Root kullanıcıları konteynerları çalıştırabilir. Bu yüzden ya ‘sudo’ ön eki ile komutlar çalıştırılmalı ya da aşağıdaki kod ile kullanıcı (burada kullanıcı: pi) bu gruba eklenmelidir.
sudo usermod -aG docker [user_name]
-	Artık Docker kullanıma hazırdır. ‘docker version’ ve ‘docker info’ komutları ile durum görüntülenebilir ve hatta ‘docker run hello-world’ komutu ile Docker Hello World konteynerı çalıştırılarak sistemin sorunsuzca kurulduğu gözlemlenebilir.

<p align="center">
  <img alt="Raspberry Pi Imager" src="/images/docker_hello_world.png">
</p>

<br>

## &nbsp;&nbsp;&nbsp;&nbsp;3.3.	Nextcloud ve PostgreSQL kurulumu:
-	 Nextcloud ve PostgreSQL official imajları Docker Hub üzerinden indirilir
docker pull nextcloud
docker pull postgres

-	Docker üzerinde ‘nextcloud-net’ adında bir köprü ağı oluşturulur. Bu sayede bu isimdeki network kullanılarak kurulacak konteynerların birbirleriyle aynı ağda olması ve dolayısıyla birbirlerini görüp konuşmaları sağlanır.
docker network create --driver bridge nextcloud-net
-	PostgreSQL konteyneri ‘nextcloud-net’ ağı üzerinde ayaklandırılır. ‘POSTGRES_PASSWORD’ ortam değişkeni ile parola belirlenir.
docker run --name postgres -e POSTGRES_PASSWORD=123456 --network nextcloud-net -d postgres
-	Nextcloud konteyneri ‘nextcloud-net’ ağı üzerinde ayaklandırılır. ‘-p’ parametresi ile 8080 portu dışarıya açılarak dış dünya ile haberleşmesi sağlanır. ‘-v’ parametresi ile volume oluşturulur ve Nextcloud üzerinde ‘/var/www/html’ yolundaki web arayüzü dosyalarına yerelde ‘/home/pi/nextcloud’ adresinden de ulaşılabilmesi sağlanır. 

Artık kurulum tamamlanmıştır. Son olarak kendi IP adresinizi girerek http://192.168.xx.xx:8080/ web arayüzüne ulaşıp ayarları yapıp işlemleri tamamlamak gerekmektedir. 
-	Açılan sayfada admin hesabı için kullanıcı adı ve şifre oluşturulur.

<p align="center">
  <img alt="Raspberry Pi Imager" src="/images/nextcloud_install_01.png">
</p>

-	Data klasörü default olarak ‘/var/www/html/data’ yolu olarak gelmektedir, istenirse değiştirilebilir.
-	Veritabanları arasından PostgreSQL seçilir. ‘postgres’ kullanıcı adı ile postgres containerını ayaklandırırken kullandığımız ‘123456’ şifresi girilerek veritabanı bağlantı ayarları da tamamlanmış olur.


<p align="center">
  <img alt="Raspberry Pi Imager" src="/images/nextcloud_install_02.png">
</p>

-	Son olarak eğer isteniyorsas ‘Install recommended apps’ kutucuğuna tıklanarak Calendar, Contacts, Talk, Mail & Collaborative editing uygulamalarının da kurulumu onaylanabilir. ‘Finish Setup’ butonuna tıklanarak kurulumun bitmesi ve Nextcloud anasayfasının açılması beklenir.

<p align="center">
  <img alt="Raspberry Pi Imager" src="/images/nextcloud_install_03.png">
</p>


<p align="center">
  <img alt="Raspberry Pi Imager" src="/images/nextcloud_main_page.png">
</p>

<br>

## &nbsp;&nbsp;&nbsp;&nbsp;3.4.	Nextcloud Mobile App
-	https://nextcloud.com/install/ adresinden mobil cihaza uygun olan market linkine tıklanarak uygulama kurulur. Uygulama açılınca IP adresi ve kullanıcı bilgileri yazılarak uygulamaya giriş yapılır.


<p align="center">
  <img alt="Raspberry Pi Imager" src="/images/nextcloud_mobile.png">
</p>

<br>

## &nbsp;&nbsp;&nbsp;&nbsp;3.5.	Nextcloud Sunucusunu İnternet Ortamına Açma
Nextcloud sunucusu sadece iç ağ ortamında kullanılmak isteniyorsa bu haliyle yeterlidir. Ancak dışarı açılmak isteniyorsa statik IP almak, bir domaine bağlamak gibi yöntemler kullanılabilir. Seçilen yönteme göre ya da modem markasına göre izlenecek yollarda farklılıklar oluşabilmektedir. Bu yüzden konu hakkında daha ileri okuma için aşağıdaki link takip edilebilir:

[Make your Nextcloud ready for accessing over the internet | by Chelaru Adrian | Medium](https://che-adrian.medium.com/make-your-nextcloud-ready-for-accessing-over-the-internet-9a17116a44ce)

<br><br>

# 4.	Duplicate Image Finder:
https://github.com/elisemercury/Duplicate-Image-Finder adresinden de ulaşılabilen Duplicate Image Finder (difPy) paketi bir veya iki farklı klasördeki görüntüleri arar, bulduğu görüntüleri karşılaştırır ve bunların kopya olup olmadığını kontrol eder. Daha sonra, kopya olarak sınıflandırılan görüntü dosyalarını ve daha düşük çözünürlüğe sahip yinelenen görüntülerin dosya adlarını çıkarır, böylece yinelenen görüntülerden hangilerinin silinmesinin güvenli olduğunu bildirir. Daha sonra bu fotoğraflar manuel olarak da silinebilir veya difPy’ın otomatik olarak silmesine de izin verilebilir. Kurulumu için aşağıdaki script çalıştırılabilir:
pip install difPy

<br>

# &nbsp;&nbsp;&nbsp;&nbsp;4.1.	Çalışma Mantığı ve Kullanımı
Bir Python paketi olan difPy paketi; OpenCV, NumPy, scikit-image, collections gibi paket ve modülleri kullanır. Görüntü benzerliği için MSE (Mean Squared Error) kullanır. İki görüntü arasındaki ortalama kare hatası, iki görüntü arasındaki kare farkının toplamıdır. Hata ne kadar düşükse, görüntüler o kadar “benzer”olur. Konu hakkında ileri okuma yapmak için kaynak:
[Finding Duplicate Images with Python | by Elise Landman | Towards Data Science]([https://www.google.com](https://towardsdatascience.com/finding-duplicate-images-with-python-71c04ec8051))

difPy ile bir klasördeki fotoğraflar şu komutlarla incelenir:
from difPy import dif
search = dif("C:/Path/to/Folder/")
İki klasör incelemek için şu komutlar kullanılır:
from difPy import dif
search = dif("C:/Path/to/Folder_A/", "C:/Path/to/Folder_B/")

search sınıfının result niteliği kullanılarak sonuçlar yazdırılabilir:
<p align="center">
  <img alt="Raspberry Pi Imager" src="/images/difPy_01.png">
</p>

<br><br>

# 5.	Sonuçlar:
Kurulan bu sistem gerek bireysel gerekse şirket içi depolama çözümleri için düşük maliyetli, güvenlik risklerini aza indiren gayet yeterli bir çözümdür. Dosyalara istenilen yerden ulaşılabilir. Kullanışlı yönlerinden bir tanesi de veriler elimizin altındaki bir cihazda (sd card, flash bellek, hdd, ssd vb.) olduğundan bu cihazın yedeklemesini de hızlı ve güvenli bir şekilde yapabiliriz. Buradaki tek eksi yan, Raspberry Pi Zero W cihazının bu proje için yetersiz kalmasıdır. Karşılaştığım iki büyük problem ise şunlardı:
-	Kopya fotoğrafları bulmak için kullandığım difPy paketi görüntü işleme kütüphanelerinden faydalandığı için yüksek işlem gücü gerektiriyordu ve bu da işlemlerimin çok yavaşlamasına ve Raspberry cihazımın çok ısınmasına sebebiyet veriyordu.
-	Wifi üzerinden yapmış olduğum bağlantıda modemim ve bilgisayarım istediğim yüksek hızları vermesine rağmen Raspberry Pi Zero W bu konuda yetersiz kalıyordu. Bir hız testi yapmak için Raspberry komut satırında sudo apt install speedtest-cli komutu ile hız testi paketini kurdum. Daha sonra speedtest-cli komutuyla hız testini çalıştırdım ve 9.14 Mbit/s hızını aldım. Bu da dosyaların çok geç yedeklenmesine sebebiyet veriyor. Bu yüzden network kartı daha iyi ve işlem gücü daha yüksek bir cihaz kullanımı yapılmalı. 

<p align="center">
  <img alt="Raspberry Pi Imager" src="/images/speedtest_01.png">
</p>

Buraya kadar takip ettiğiniz için çok teşekkür ederim. Konu ile ilgili sorularınız için omeravci@marun.edu.tr mail adresimden iletişime geçebilirsiniz.









<p align="center">
  <img alt="Raspberry Pi Imager" src="/images/.png">
</p>


[I'm an inline-style link](https://www.google.com)


