- [X] html de sidebar ve main content height goreceli , icerige gore degisiyor
- [X] kullanici listesi pagination olmalimi (transatiton table kaldi , filtre ile cakisiyor)
- [X] modelde ayri bir model olusturulcak dovizler icin birde kullanci baglantisi yapilcak
- [X] doviz modeli olusturulduktan sonra kullanici duzenleme bolumune eklenecek
- [X] sayfada yetkiliyse goster,  misafirler edit yapamasin
- [X] admin sayfasi tammi olmasi lazim
- [ ] para birimleri interger double mi olmali
- [X] sifre degisiminde yanlis sifrede uyari vermedi
- [ ] pdf yukleme
- [X] how to fine grain form.as_p customization
- [ ] kullanicilarda duzenle deyince ustteki admin degisiyor,
- [X] kullanicilarda duzenlemeyi sadece yetkililere ac
- [X] islemler silinebilir mi olucak , editlenebilirmi
- [X] transaction list 2 tanemi olucak bi tanesi her user kendininkine bakcak digeri admin hepsine
- [X] islem tarihi dendiginde tarih aylar ingilizce
- [X] admin disi loginde problem var passwordlarda haslenmiyor
- [ ] her login sayfasinda o kisim bos degil admin yaziyor duzelt
- [ ] islemlerde id belki iyi olurdu her islemin kendi istmi
- [X] margin top consistency
- [X] 404 page customized
- [X] on delete CASCADE mi olsun hepsi sonra sorun olmasin
- [ ] djangoda geri alma varmi bak bu islemleri
- [X] admin sayfasindan olustururken islem tag secmek zorunlu dedi
- [X] kimden geldi kimden gitti nasil olcak bak
- [ ] bakiye de belki select2 kullanilabilir kullanici secimi icin
- [X] islemlerde tarih filtrelenmesi yapilcak
- [X] islem silme yok eklensin mi, adminler bile islemi degistiremiyor nasil olsun
- [X] cok onemli silinen gruplar taglar silinmesin mi
- [X] olusturulan grubu sil yok
- [ ] web sayfasinin iconu yok 
- [ ] sayfalarda titller bos
- [X] linkler consistent degil users vs sayfa linkleri
- [ ] islemler duzenlenince , son duzenlenme tarihi yok
- [X] transactions daki filtreler tam degil
- [X] butun viewlere login required yapilcak
- [X] sayfada login olmadan yan bar olmicak
- [ ] kullanici duzenle kisminda sifre kismi olmicak
- [ ] tablolarda dinamiklik olucak , sort yani
- [ ] islem olusturmada miktar 0 , bunu place holder yapilabilir
- [X] gruplar mesela MuUSer a entegre edilmedi foreign key ile ona bak
- [ ] islemler active passive yapilsa daha iyi silinmeyi kalksa , recovery icin
- [ ] resim yukleme , PDf yukleme su an sadece 1 er tane yuklenebiliyorlar galiba
- [ ] etkinlik taglari vs ayri olcak 3 tane mi ?
- [ ] banka fisleri ve evraklar ayri olcak
- [ ] islemler picture and pdf fieldleri eklendi , tum codda guncellenme lazim , ayri model yerine boyle cunku normal bakkal fisi bile eklenebilir
- [ ] yeni kullanicilar modeli daha basit olur direk MuUser a eklemektense
- [ ] yeni viewlere login required koyulcak
- [ ] transaction olustururken para birimi secmek zorunlu diyor, daha dogrusu demiyor
- [ ] ispatli tabloda % cok kusuratli 99999 gidiyor
- [ ] yetkililer sadece login yapabilirler cunku normallerin username ve password olmicak
- [ ] createuser sayfasinda ayrica yetkili diye tik atmayi unutma front endden ayarlancak
- [ ] username uniqu false ve null=True yapildi , yani create user derken username varmi kontrol edilsin hata gostersin varsa,yani unique database kurali olmasada backendde kural olsun 
- [ ] first_name ad-soyad icin ortak kullanilsin, fron endden ayarlansin
- [ ] isim aramalari nasil fuzzy searcmi arastirilsin
- [ ] kayit edilirken kullanci adi olsun ad soyad olsun hepsi kucuk harfle kayit olsun
- [ ] isim ve soysisim yerine sadece isim fieldinde olsun hepsi
- [ ] adminler birbirlerinin sifrelerini felan silebiliyorlar
- [ ] update yaparken vs olmazsa uyarisi ile goster



sorular
*********
exel den kullanicilar baska bir modeldemi tutulsun
kisisel islemler kismi silinsinmi, onun icin tablo var cunku
formlarda olmayinca uyari ver eksik mesela telefon nosu

ii 


pagination ===
kullanicilar works
kullnici gruplari works
exelkullanicilari works
bakiye table works , / bakiye tablosu kaymis , cok para biriminden kaynakli galiba
harcama kalemi works
para birimleri sadece liste cunku az para birimi var
gecmis islemler tanblosu works
Kişisel İşlemler Listesi , works
----Etkinlik Listesi   , yoktu eklendi
Evrak Listesi var


Yeni İşlem Oluştur , uyari vermiyor mesela title ve yazi giriyorum gerisini istemiyor ama uyari yok , front endden currency secimi zorunlu yapilcak



//////
+ islemler tipi creationa eklenecek , 
+ detailse eklenecek , 
+ update ye eklenecek , 
+ tabloya eklenecek ,
+ filtreye eklenecek,

/////
 belgeli islemler sayfasi tamamlanacak