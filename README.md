# Görüntü Segmentasyonu

Bu proje; kullanıcı etkileşimli bir görüntü segmentasyonu uygulamasıdır. Tek bir arayüz üzerinden üç farklı popüler algoritmayı (K-means, Watershed ve GrabCut) test etmenize ve sonuçları otomatik olarak kaydetmenize olanak tanır.

# Özellikler

Uygulama, resimdeki nesneleri arka plandan ayırmak için üç farklı yaklaşım sunar:

1. K-means Kümeleme: Pikselleri renk benzerliklerine göre gruplandırır. Karmaşık renk geçişlerini basitleştirmek için idealdir.

2. Watershed Algoritması: Görüntüyü topografik bir harita gibi işleyerek nesne sınırlarını belirler. Özellikle birbirine değen nesneleri ayırmada etkilidir. Sınırları belirginleştirmek için kalınlaştırılmış kırmızı çizgiler kullanır.

3. GrabCut: Kullanıcı tarafından fare ile seçilen bir dikdörtgen alanı temel alarak nesneyi arka plandan akıllıca ayırır.

# Kullanılan Kütüphaneler ve Kurulum

OpenCV

Numpy

pip install numpy opencv

# Kullanım Talimatları

k - Kmeans uygular.

w - Watershed uygular.

g - GrabCut uygular.

r - Görseli sıfırlar.

q - Çıkış

# Otomatik Kayıt

Her segmentasyon işlemi bittiğinde, sonuçlar çalışma dizinine şu isimlerle otomatik olarak kaydedilir.

# Teknik Detaylar

Watershed Geliştirmesi: Güneş ve bulut gibi çok açık renkli nesnelerin kaybolmaması için cv2.threshold değeri 220 olarak optimize edilmiş ve cv2.dilate ile sınır çizgileri görselleştirme için kalınlaştırılmıştır.

GrabCut Etkileşimi: cv2.setMouseCallback fonksiyonu ile farenin tıklama ve bırakma olayları takip edilerek dinamik bir seçim alanı (ROI) oluşturulur.

K-means İşleme: Görüntü verileri float32 formatına dönüştürülerek OpenCV'nin k-means motoruna gönderilir ve sonuçlar tekrar görselleştirme için uint8 formatına geri çekilir.

#Input

![image](https://github.com/user-attachments/assets/a34a4751-b798-43dd-a5bc-5afa643b1a51)


#Output

#GrabCut
![sonuc_grabcut](https://github.com/user-attachments/assets/8726a43a-052a-489b-a873-54d73bc0b096)

#K-means
![sonuc_kmeans](https://github.com/user-attachments/assets/cfa9de61-bf3c-461b-b417-dc95e7c79c47)

#Watershed
![sonuc_watershed](https://github.com/user-attachments/assets/2da3c319-d319-4024-acf3-f5d6ea93363a)
