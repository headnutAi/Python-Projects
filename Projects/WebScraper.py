import re
import requests
from bs4 import BeautifulSoup
import spacy


class SimpleScraper:
    """
    Ein einfacher Web-Scraper, der Inhalte von einer URL abruft,
    sie parst und zusätzliche Analyse-Funktionen bietet.
    """

    def __init__(self, user_agent="MyResearchBot/1.0"):
        self.headers = {"User-Agent": user_agent}

    def fetch(self, url):
        """Ruft den HTML-Inhalt der gegebenen URL ab."""
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.text

    def parse(self, html, selector):
        """Parst den HTML-Inhalt und gibt die Elemente zurück, die dem CSS-Selektor entsprechen."""
        soup = BeautifulSoup(html, "html.parser")
        return soup.select(selector)

    def scrape(self, url, selector):
        """Führt das Abrufen und Parsen durch und gibt eine Liste des bereinigten Textes zurück."""
        html = self.fetch(url)
        elements = self.parse(html, selector)
        return [el.get_text(strip=True) for el in elements]

    def find_sentences(self, text, keyword):
        """
        Sucht in einem gegebenen Text nach Sätzen, die das Schlüsselwort enthalten.
        """
        sentences = text.split(".")

        found_sentences = []
        for sentence in sentences:
            if keyword in sentence:
                clean_sentence = sentence.strip()
                if clean_sentence:
                    found_sentences.append(clean_sentence + ".")

        return found_sentences

    def extract_persons(self, text, nlp_model):
        """
        Extrahiert Personen (PER-Entities) aus dem Text mit dem bereitgestellten spaCy-Modell.
        Filtert Duplikate und Namen mit mehr als zwei Wörtern.
        """
        doc = nlp_model(text)

        persons = [ent.text for ent in doc.ents if ent.label_ == "PER"]

        persons = list(dict.fromkeys(persons))

        persons = [name for name in persons if len(name.split()) <= 2]

        return persons


if __name__ == "__main__":
    scraper = SimpleScraper()
    url = "https://de.wikipedia.org/wiki/Wikipedia:Hauptseite"
    selector = "li"

    try:
        nlp = spacy.load("de_core_news_sm")
    except OSError:
        print("Das 'de_core_news_sm' Modell ist nicht installiert.")
        print("Bitte führen Sie 'python -m spacy download de_core_news_sm' in Ihrer Konsole aus.")
        exit()

    paragraphs = scraper.scrape(url, selector)
    text = " ".join(paragraphs)

    # Suche nach Sätzen mit einem Schlüsselwort
    keyword = "Berlin"
    print("\n" + "=" * 50)
    print(f"Suche nach Sätzen mit dem Schlüsselwort: **{keyword}**")
    print("=" * 50)

    sentences_with_keyword = scraper.find_sentences(text, keyword)
    counterBerlin = len(sentences_with_keyword)

    for sentence in sentences_with_keyword:
        print(sentence)

    print(f"\nEs wurden **{counterBerlin}** Sätze gefunden, die '{keyword}' enthalten.")

    # Extraktion von Personen
    print("\n" + "=" * 50)
    print("Extrahiere Personen mit spaCy")
    print("=" * 50)

    persons = scraper.extract_persons(text, nlp)

    namecounter = len(persons)

    print("Gefundene Personen (max. 2 Wörter):")
    print(persons)
    print(f"Anzahl der gefundenen eindeutigen Personen: **{namecounter}**")