"""
Übung: Bibliotheks-Ausleihsystem  (Level: Intermediate)

Ziel: Baue ein System, das Bücher verwaltet, Ausleihen verbucht,
überfällige Leihen findet und Mahngebühren berechnet.

Geübte Konzepte:
- dataclasses (inkl. field(init=False) und __post_init__)
- Enum
- datetime / date / timedelta
- sorted() mit key-Funktion (lambda) + reverse  --> KEIN Bubble Sort!
- collections.Counter und defaultdict
- Generatoren (yield)
- @property
- Eigene Exceptions
- Dict-/List-Comprehensions

Spielregeln der Bibliothek:
- Eine Ausleihe läuft LOAN_DAYS (14) Tage.
- Ein Mitglied darf maximal MAX_ACTIVE_LOANS (3) Bücher gleichzeitig haben.
- Verspätung kostet FEE_PER_DAY (0.50 €) pro Tag, aber maximal MAX_FEE (20.00 €)
  pro einzelner Ausleihe.

Arbeite die TODOs von oben nach unten ab und führe die Datei immer wieder aus.
Der Testblock unten sagt dir, was noch fehlt.
"""

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta
from enum import Enum

LOAN_DAYS = 14
FEE_PER_DAY = 0.50
MAX_FEE = 20.00
MAX_ACTIVE_LOANS = 3


# ---------------------------------------------------------------------------
# 1) Exceptions
# ---------------------------------------------------------------------------

class BookNotAvailableError(Exception):
    """Wird geworfen, wenn kein Exemplar mehr verfügbar ist."""
    pass


class MemberLimitReachedError(Exception):
    """Wird geworfen, wenn ein Mitglied schon MAX_ACTIVE_LOANS Bücher hat."""
    pass


class LoanNotFoundError(Exception):
    """Wird geworfen, wenn eine Rückgabe zu keiner offenen Ausleihe passt."""
    pass


# ---------------------------------------------------------------------------
# 2) Enum
# ---------------------------------------------------------------------------

class Genre(Enum):

    FANTASY = "Fantasy"
    SCIFI = "Sci-fi"
    KRIMI = "Krimi"
    SACHBUCH = "Sachbuch"
# ---------------------------------------------------------------------------
# 3) Datenklassen
# ---------------------------------------------------------------------------

@dataclass
class Book:

    isbn : str
    title : str
    author : str
    genre : Genre
    copies_total : int
    copies_available : int = field(init=False)

    def __post_init__(self):
        self.copies_available = self.copies_total

    @property
    def is_available(self):
        if self.copies_available <= 0:
            return False
        return True



@dataclass
class Loan:
    """Eine einzelne Ausleihe.

    TODO 4: Definiere die Felder:
        isbn: str
        member_id: str
        loaned_on: date
        due_on: date          -> field(init=False), in __post_init__ berechnen:
                                 loaned_on + timedelta(days=LOAN_DAYS)
        returned_on: date | None = None

    TODO 5: Schreibe die Property `is_open`  -> True, solange returned_on None ist.

    TODO 6: Schreibe die Methode `days_late(self, today)`:
            - Ist das Buch zurückgegeben, zählt returned_on, sonst today.
            - Gib die Anzahl Tage NACH due_on zurück, minimal 0.
            - Tipp: (a - b).days liefert dir die Differenz in Tagen.

    TODO 7: Schreibe die Methode `fee(self, today)`:
            days_late * FEE_PER_DAY, gedeckelt auf MAX_FEE, auf 2 Stellen gerundet.
            Tipp: min() ist hier dein Freund.
    """
    pass


# ---------------------------------------------------------------------------
# 4) Die Bibliothek
# ---------------------------------------------------------------------------

class Library:
    def __init__(self):
        self.books: dict[str, Book] = {}
        self.loans: list[Loan] = []

    def add_book(self, book):
        """TODO 8: Lege das Buch unter seiner ISBN in self.books ab."""
        pass

    def borrow(self, isbn, member_id, today):
        """Verbucht eine Ausleihe und gibt das erzeugte Loan-Objekt zurück.

        TODO 9: In dieser Reihenfolge prüfen:
            1. Unbekannte ISBN            -> KeyError (passiert von selbst)
            2. Mitglied hat schon MAX_ACTIVE_LOANS offene Leihen
                                          -> MemberLimitReachedError
            3. Buch nicht verfügbar       -> BookNotAvailableError
            Sonst: copies_available um 1 verringern, Loan bauen,
                   an self.loans anhängen und zurückgeben.
            Tipp: Die Anzahl offener Leihen bekommst du mit
                  sum(1 for ... ) oder len(list(self.active_loans(member_id))).
        """
        pass

    def return_book(self, isbn, member_id, today):
        """Nimmt ein Buch zurück und gibt die fällige Gebühr zurück.

        TODO 10:
            - Suche die erste OFFENE Ausleihe mit passender isbn + member_id.
              Findest du keine -> LoanNotFoundError.
            - Setze returned_on = today.
            - Erhöhe copies_available wieder um 1.
            - Gib loan.fee(today) zurück.
            Tipp: next((l for l in self.loans if ...), None) ist elegant.
        """
        pass

    def active_loans(self, member_id=None):
        """GENERATOR: liefert alle offenen Ausleihen.

        TODO 11: Nutze `yield` (kein return einer Liste!).
                 Ist member_id gesetzt, nur die Leihen dieses Mitglieds liefern.
        """
        pass

    def overdue_loans(self, today):
        """Alle offenen und überfälligen Ausleihen.

        TODO 12: Gib eine Liste zurück, sortiert nach days_late ABSTEIGEND.
                 Nutze sorted() mit key=lambda ... und reverse=True.
        """
        pass

    def total_fees(self, member_id, today):
        """TODO 13: Summe aller Gebühren dieses Mitglieds über ALLE Ausleihen
                    (offen wie zurückgegeben), auf 2 Stellen gerundet.
        """
        pass

    def genre_stats(self):
        """TODO 14: Wie oft wurde je Genre ausgeliehen (über alle Loans)?
                    Gib einen collections.Counter zurück, der Genre -> Anzahl mappt.
                    Tipp: Counter(...) frisst direkt einen Generator-Ausdruck.
        """
        pass

    def loans_per_member(self):
        """TODO 15: Gib ein defaultdict(list) zurück: member_id -> Liste der ISBNs,
                    die dieses Mitglied jemals ausgeliehen hat (Reihenfolge = Ausleih-
                    Reihenfolge).
        """
        pass

    def top_authors(self, n=3):
        """TODO 16: Die n meistausgeliehenen Autor:innen.

        Gib eine Liste von (autor, anzahl)-Tupeln zurück, sortiert nach
        Anzahl ABSTEIGEND, bei Gleichstand alphabetisch nach Name AUFSTEIGEND.
        Tipp: key=lambda t: (-t[1], t[0]) erledigt beides auf einmal.
        """
        pass


# ---------------------------------------------------------------------------
# Testblock — hier prüfst du deine Lösung. Nicht verändern, nur ausführen.
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    TODAY = date(2026, 9, 15)

    lib = Library()
    lib.add_book(Book('978-1', 'Der Hobbit', 'J.R.R. Tolkien', Genre.FANTASY, 2))
    lib.add_book(Book('978-2', 'Herr der Ringe', 'J.R.R. Tolkien', Genre.FANTASY, 1))
    lib.add_book(Book('978-3', 'Dune', 'Frank Herbert', Genre.SCIFI, 1))
    lib.add_book(Book('978-4', 'Clean Code', 'Robert C. Martin', Genre.SACHBUCH, 3))
    lib.add_book(Book('978-5', 'Der Schwarm', 'Frank Schätzing', Genre.KRIMI, 1))

    # Anna: ein stark überfälliges Buch, ein frisches
    lib.borrow('978-1', 'M1', TODAY - timedelta(days=30))   # 16 Tage zu spät
    lib.borrow('978-3', 'M1', TODAY - timedelta(days=5))    # noch im Rahmen

    # Ben: extrem überfällig (Gebühr läuft in den Deckel) + zwei frische
    lib.borrow('978-1', 'M2', TODAY - timedelta(days=60))   # 46 Tage zu spät
    lib.borrow('978-2', 'M2', TODAY - timedelta(days=2))
    lib.borrow('978-4', 'M2', TODAY - timedelta(days=1))

    print('--- Verfügbarkeit ---')
    print('Hobbit verfügbar?', lib.books['978-1'].is_available, '(erwartet: False)')
    print('Clean Code verfügbar?', lib.books['978-4'].is_available, '(erwartet: True)')

    print('\n--- Grenzen ---')
    try:
        lib.borrow('978-5', 'M2', TODAY)
    except MemberLimitReachedError as e:
        print('Limit korrekt geblockt:', e)

    try:
        lib.borrow('978-2', 'M3', TODAY)
    except BookNotAvailableError as e:
        print('Ausverkauft korrekt geblockt:', e)

    print('\n--- Offene Leihen von M1 ---')
    for loan in lib.active_loans('M1'):
        print(f'  {loan.isbn} faellig am {loan.due_on} | {loan.days_late(TODAY)} Tage zu spaet')

    print('\n--- Ueberfaellig (absteigend) ---')
    for loan in lib.overdue_loans(TODAY):
        print(f'  {loan.member_id} {loan.isbn}: {loan.days_late(TODAY)} Tage -> {loan.fee(TODAY):.2f} EUR')

    print('\n--- Gebuehren ---')
    print('M1:', lib.total_fees('M1', TODAY), '(erwartet: 8.0)')
    print('M2:', lib.total_fees('M2', TODAY), '(erwartet: 20.0 — Deckel greift)')

    print('\n--- Rueckgabe ---')
    gebuehr = lib.return_book('978-3', 'M1', TODAY)
    print('Dune zurueck, Gebuehr:', gebuehr, '(erwartet: 0.0)')
    print('Dune wieder verfuegbar?', lib.books['978-3'].is_available, '(erwartet: True)')
    print('Offene Leihen M1 jetzt:', len(list(lib.active_loans('M1'))), '(erwartet: 1)')

    try:
        lib.return_book('978-3', 'M1', TODAY)
    except LoanNotFoundError as e:
        print('Doppelte Rueckgabe korrekt geblockt:', e)

    print('\n--- Statistiken ---')
    print('Genres:', dict(lib.genre_stats()))
    print('  erwartet: FANTASY 3, SCIFI 1, SACHBUCH 1')
    print('Pro Mitglied:', dict(lib.loans_per_member()))
    print('Top-Autoren:', lib.top_authors(3))
    print("  erwartet: [('J.R.R. Tolkien', 3), ('Frank Herbert', 1), ('Robert C. Martin', 1)]")

    print('\n--- Selbstcheck ---')
    assert lib.books['978-1'].copies_available == 0
    assert lib.total_fees('M1', TODAY) == 8.00
    assert lib.total_fees('M2', TODAY) == 20.00
    assert [l.member_id for l in lib.overdue_loans(TODAY)] == ['M2', 'M1']
    assert lib.top_authors(1) == [('J.R.R. Tolkien', 3)]
    assert lib.genre_stats()[Genre.FANTASY] == 3
    print('Alle Checks bestanden. Sauber!')
