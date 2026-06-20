"""
Markov Chain Text Generator
============================
Verilen bir metin örneğini (kitap, şarkı sözü, makale vb.) analiz ederek
Markov zinciri modeli kurar ve bu modele dayanarak yeni, orijinal ama
benzer üsluplu metinler üretir.

Kullanım:
    python markov.py --input ornek.txt --length 100
    python markov.py --input ornek.txt --order 3 --length 200 --seed-word "Bir"
    echo "metin..." | python markov.py --length 50

Hiçbir harici kütüphane gerekmez, sadece standart kütüphane kullanılır.
"""

import argparse
import random
import re
import sys
from collections import defaultdict


class MarkovChain:
    """
    N-gram tabanlı Markov zinciri. `order` parametresi, bir sonraki kelimeyi
    tahmin etmek için kaç önceki kelimeye bakılacağını belirler.
    Daha yüksek order -> kaynak metne daha sadık ama daha az "yaratıcı" çıktı.
    """

    def __init__(self, order: int = 2):
        self.order = order
        self.model = defaultdict(list)
        self.starts = []  # Cümle başlangıcı olarak kullanılabilecek n-gramlar

    def train(self, text: str):
        words = self._tokenize(text)
        if len(words) <= self.order:
            raise ValueError("Eğitim metni, seçilen order için çok kısa.")

        for i in range(len(words) - self.order):
            key = tuple(words[i:i + self.order])
            next_word = words[i + self.order]
            self.model[key].append(next_word)

            # Büyük harfle başlayan kelimeler cümle başlangıcı olabilir
            if words[i][0:1].isupper():
                self.starts.append(key)

        if not self.starts:
            self.starts = list(self.model.keys())

    def _tokenize(self, text: str):
        # Noktalama işaretlerini kelimelerden ayırarak basit bir tokenizasyon
        text = re.sub(r"\s+", " ", text.strip())
        tokens = re.findall(r"[\wÇĞİÖŞÜçğıöşü]+|[.,!?;:]", text)
        return tokens

    def generate(self, length: int = 100, seed_word: str = None) -> str:
        if not self.model:
            raise RuntimeError("Önce train() ile model eğitilmeli.")

        if seed_word:
            candidates = [k for k in self.model if k[0].lower() == seed_word.lower()]
            current = random.choice(candidates) if candidates else random.choice(self.starts)
        else:
            current = random.choice(self.starts)

        result = list(current)

        for _ in range(length - self.order):
            choices = self.model.get(current)
            if not choices:
                # Tıkanırsa rastgele yeni bir başlangıç seç
                current = random.choice(list(self.model.keys()))
                choices = self.model[current]

            next_word = random.choice(choices)
            result.append(next_word)
            current = tuple(result[-self.order:])

        return self._detokenize(result)

    def _detokenize(self, tokens) -> str:
        text = ""
        for i, token in enumerate(tokens):
            if i == 0:
                text += token
            elif re.match(r"^[.,!?;:]$", token):
                text += token  # Noktalama öncesi boşluk yok
            else:
                text += " " + token

        # İlk harfi büyüt ve sonuna nokta ekle (yoksa)
        text = text[0].upper() + text[1:] if text else text
        if text and text[-1] not in ".!?":
            text += "."
        return text


def main():
    parser = argparse.ArgumentParser(
        description="Markov zinciri ile bir metin örneğinden yeni metin üretir"
    )
    parser.add_argument("--input", type=str, help="Eğitim metni dosyası (.txt). Verilmezse stdin okunur.")
    parser.add_argument("--order", type=int, default=2, help="Markov zinciri derecesi (varsayılan: 2)")
    parser.add_argument("--length", type=int, default=100, help="Üretilecek kelime sayısı")
    parser.add_argument("--seed-word", type=str, default=None, help="Üretimin başlayacağı kelime")
    parser.add_argument("--count", type=int, default=1, help="Kaç farklı metin üretilsin")
    args = parser.parse_args()

    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        if sys.stdin.isatty():
            print("Hata: --input verilmedi ve stdin'den okunacak bir şey yok.")
            print("Örnek: python markov.py --input kitap.txt --length 100")
            sys.exit(1)
        text = sys.stdin.read()

    chain = MarkovChain(order=args.order)
    chain.train(text)

    for i in range(args.count):
        output = chain.generate(length=args.length, seed_word=args.seed_word)
        if args.count > 1:
            print(f"--- Metin {i + 1} ---")
        print(output)
        if args.count > 1:
            print()


if __name__ == "__main__":
    main()
