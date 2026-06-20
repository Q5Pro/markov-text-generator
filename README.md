# 📝 Markov Chain Text Generator

Verdiğiniz herhangi bir metni (kitap, şarkı sözü, makale, deneme...) analiz
ederek bir Markov zinciri modeli kurar ve o metnin üslubuna benzer ama
tamamen yeni, orijinal metinler üretir.

## Özellikler

- 🔗 Ayarlanabilir "order" (derece) — daha yüksek değer kaynağa daha sadık çıktı verir
- 🌱 Belirli bir kelimeyle başlatma desteği
- 📚 Dosyadan veya stdin'den (pipe) metin okuma
- 🇹🇷 Türkçe karakterleri (ç, ğ, ı, ö, ş, ü) destekler
- 🚫 Harici bağımlılık yok, sadece Python standart kütüphanesi

## Kurulum

```bash
git clone <repo-url>
cd markov-text-generator
```

## Kullanım

```bash
# Bir dosyadan 100 kelimelik metin üret
python3 markov.py --input kitap.txt --length 100

# Daha "sadık" çıktı için order yükselt
python3 markov.py --input kitap.txt --order 3 --length 200

# Belirli bir kelimeyle başlat
python3 markov.py --input kitap.txt --seed-word "Bir"

# Pipe ile kullanım
cat kitap.txt | python3 markov.py --length 50

# Birden fazla varyasyon üret
python3 markov.py --input kitap.txt --count 5
```

| Parametre | Açıklama | Varsayılan |
|---|---|---|
| `--input` | Eğitim metni dosyası | stdin |
| `--order` | Markov zinciri derecesi (n-gram boyutu) | 2 |
| `--length` | Üretilecek kelime sayısı | 100 |
| `--seed-word` | Başlangıç kelimesi | rastgele |
| `--count` | Üretilecek metin sayısı | 1 |

## Nasıl çalışır?

Markov zinciri, bir dizideki her elemanın yalnızca kendinden önceki
*N* elemana bağlı olduğunu varsayan istatistiksel bir modeldir. Bu araç,
kaynak metindeki her N-kelimelik diziyi (n-gram) bir sonraki kelimeyle
ilişkilendirir. Üretim sırasında, mevcut n-gram'a göre kaynak metinde
o n-gram'ı takip eden kelimelerden rastgele biri seçilir.

**İpucu:** Daha doğal sonuçlar için en az birkaç bin kelimelik kaynak
metin kullanın — kısa metinlerde model çok az seçeneğe sahip olur ve
çıktı orijinal metni neredeyse birebir tekrar edebilir.

## Lisans

MIT
