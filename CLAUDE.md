# Consumable Alchemy

Mod do Wiedźmina 3 (Remastered, gra 5.0): alchemia zużywalna zamiast singletonów odnawianych medytacją.
Mikstury, bomby i wywary uzupełnia wyłącznie warzenie, za składniki. Opis dla gracza: [README.md](README.md).
Stan prac i następny krok: [docs/roadmap.md](docs/roadmap.md).

## Słownik

- **Consumable** — przedmiot objęty systemem: mikstura, bomba albo wywar, singleton, bez tagu `Quest`
  (pełne kryterium: `CA_IsConsumableItemName`). Wszystko inne jest vanilla.
- **Dawki** i **limit** — vanillowe `ammo_current` i `SingletonItemGetMaxAmmo`. **Pełna kieszeń** = dawki ≥ limit.
- **Odblokowanie** — pierwsze warzenie przedmiotu, za **recepturę pełną**. Przedmiot odblokowany = posiadany
  w ekwipunku, także z 0 dawek.
- **Powielenie** — każde kolejne warzenie, za krótszą **recepturę powielania** (w kodzie `copy` / `isCopy`).
- **Poziom** — 1–3 jak w vanilli (np. Jaskółka → Wzmocniona → Doskonała).
- **Tabela receptur** — `tools/recipes/recipes_table.json`, źródło prawdy obu receptur każdego consumable.

## Zasady produktu

Mod zmienia jedno: skąd biorą się dawki. Resztę gracz ma dostać taką, jaką zna z vanilli. Czytaj według
intencji (alchemia jako rzemiosło, jak w Wiedźminie 1; powielenie nie boli, nie żal rzucić bomby, która
chybi); gdy litera i intencja się rozjeżdżają, powiedz to autorowi.

1. **Dawki daje tylko warzenie.** Medytacja, łóżko, stół, alkohol ani nic innego nie odnawia consumables.
   Warzenie napełnia do limitu. Alkohol jest wyłącznie składnikiem.
2. **Odblokowanie i powielenie.** Jedynym sygnałem dla gracza jest lista składników w menu alchemii — po
   odblokowaniu krótsza. Każde miejsce, które pokazuje albo pobiera składniki receptury (menu, warzenie,
   tooltip, przypięta receptura), daje tę samą listę.
3. **Wygląda jak vanilla.** Zero własnego renderowania i nakładek. Wolno dodać element do istniejącego
   systemu gry, jeśli wygląda jak vanilla (nowy wpis lokalizacji PL + EN w istniejącym miejscu UI, nowa
   pozycja filtra) — ale najpierw szukaj istniejącego klucza lokalizacji.
4. **Poza dawkami — vanilla.** Limity i ich bonusy, pozyskanie poza warzeniem (loot, zakup, questy), poziomy,
   blokada w walce, oleje, przedmioty questowe.
5. **Save bez śladu moda.** Mod nie zapisuje nic własnego (tylko vanillowe `ammo_current` / `is_initialized`);
   po usunięciu moda gra działa. Mechanizm: [docs/architecture.md](docs/architecture.md).
6. **Zgodność z innymi modami nie jest wymogiem** (autor gra bez innych modów).

## Jak pracujemy

- **Autor** (właściciel projektu) **mówi, co ma powstać, i sprawdza wynik w grze.** Pytaj go wyłącznie
  o decyzje projektowe: mechanika, balans, co widzi gracz. Implementację wybierasz sam i krótko raportujesz.
- **Jedna sesja to jeden wycinek** (zmiana widoczna w grze albo zamknięty etap narzędzi), od planu do
  scalenia. Najpierw 5–10 linii planu: co autor zobaczy w grze, co się zmieni w kodzie — i czekasz na
  zielone światło. To, co zobaczy gracz (receptury, teksty komunikatów), uzgadniasz z autorem na piśmie,
  w tabeli albo z brzmieniem PL/EN, zanim powstanie kod.
- **Architekt** (główna sesja) rozmawia z autorem, czyta kod potrzebny do decyzji i zlecenia, przegląda
  diffy, scala i wdraża. Drobne, lokalne zmiany (dokumenty, kilka linii kodu) robi sam. Długich plików nie
  czyta w całości (skrypty vanilli, XML-e gry, generowana tabela): Grep z wąskim wzorcem albo agent Explore,
  który zwraca wniosek z `plik:linia`. Autorowi pokazuje wynik, który sam by przyjął.
- **Wykonawca** (Agent `general-purpose`, `model: "sonnet"`, w tle, `isolation: "worktree"`) dostaje
  zamkniętą część pracy. Zlecenie z adresami: cel, nazwa gałęzi, pliki i miejsca w nich (także `plik:linia`
  w vanilli), znane fakty i pułapki (sekcja niżej), kryteria odbioru, czego nie robić, punkt zatrzymania.
  Przed zleceniem commit — worktree powstaje z HEAD. Opus (`model: "opus"`) tylko do zadania bez gotowego
  projektu albo szukania nieznanej przyczyny. Niezależne obszary — równolegle.
- **Research** (kod vanilli, dane z bundli) zlecasz tak samo, z poleceniem zapisu wyników do pliku
  w trakcie pracy — przerwany agent nie może zabrać wyników ze sobą. Wniosek trafia do właściwego
  dokumentu, zanim sesja się skończy.
- **Kolejna runda:** pracę przyjętą po przeglądzie scalasz; drobne poprawki robisz sam w worktree wykonawcy
  (ścieżki bezwzględne i `git -C`, bez `cd` — sesja przeniosłaby się do worktree), dłuższą listę dostaje
  nowy wykonawca ze ścieżkami i hashami. Wykonawcy z dużym kontekstem nie wznawiaj — każdy jego krok
  wysyła cały dotychczasowy kontekst.
- **Test w grze:** architekt uruchamia `deploy.ps1` — z worktree, żeby sprawdzić gałąź przed scaleniem
  (skrypt wgrywa `src/` z własnego katalogu), albo z głównego katalogu po scaleniu. Autor testuje według
  [docs/testing.md](docs/testing.md); błędy kompilacji przepisuje z okna gry.
- **Uwagi autora** po teście poprawiasz od razu, gdy to błąd; szlif (działa, ale mogłoby być lepiej) idzie
  jednym zdaniem do „Szlif” w roadmapie.
- **Dokumenty przy pracy:** roadmapę i rozstrzygnięcia aktualizujesz raz na wycinek, przy scaleniu, jednym
  commitem; `docs/architecture.md` i checklistę w `docs/testing.md` — w gałęzi, która zmienia kod. Zmiana
  tego, co widzi gracz, aktualizuje `README.md` w tym samym wycinku.
- **Git:** każdy wykonawca pracuje we własnej gałęzi i worktree; główny katalog stoi zawsze na `main`.
  Scalenie do `main` po potwierdzeniu autora (co najmniej: kompiluje się w grze), potem usunięcie worktree
  i gałęzi. **Push tylko na wyraźne polecenie autora** — repo jest publiczne
  (https://github.com/TheBlokOfficial/consumable-alchemy), wszystko, co commitujesz, jest jawne. Commity
  małe i logiczne, po angielsku. Autor commitów: `TheBlokOfficial <tomasznosal.mail@proton.me>` (lokalny
  config repo, wspólny dla worktree). Danych gry nie commituj (`tools/recipes/x/`, `data.json`).
- **Odpowiedzi w trakcie:** po zielonym świetle i po zleceniu — tylko jedno zdanie potwierdzenia, bez
  powtarzania planu. Raport dopiero, gdy jest coś nowego (wynik agenta, błąd, decyzja do podjęcia); przy kilku
  agentach naraz — jeden raport, gdy wrócą wszyscy.
- **Raport na koniec:** 3–6 zdań prostym językiem, co się zmieniło i dlaczego, plus 2–4 rzeczy do
  sprawdzenia w grze (gdzie pójść, co uwarzyć, na co patrzeć). Bez nazw funkcji, chyba że autor zapyta.

## Środowisko, wdrożenie, narzędzia

- **Gra:** `D:\gry\steam\steamapps\common\the witcher 3` — Steam, Remastered, `bin\x64_dx12\witcher3.exe`
  w wersji **5.0.0.1044392**. Nowsza niż next-gen 4.0 — wiedzy o 4.x nie zakładaj, sprawdzaj w skryptach
  vanilli tej instalacji: `<gra>\content\content0\scripts\game\...` (tylko do odczytu; `plik:linia`
  w dokumentach dotyczą tej instalacji). Dodatki są w `content0`, katalogu `dlc` nie ma.
- **Kompilacja:** kompilatora poza grą nie ma. Gra kompiluje skrypty przy starcie i pokazuje błędy w oknie.
  Ostrzeżenia `[content0] ... not marked as abstract` / `has no autostate` są z vanilli — ignoruj.
- **Wdrożenie:** `powershell -ExecutionPolicy Bypass -File deploy.ps1 [-GameDir <ścieżka>]` (albo
  `deploy.bat`) → `<gra>\mods\modConsumableAlchemy`.
- **Receptury:** zmieniasz `tools/recipes/recipes_table.json`, potem `python tools/recipes/generate.py`
  (waliduje i generuje `consumableAlchemy_recipes_table.ws`). Wygenerowanego pliku nie edytuj ręcznie.
- **Dane gry (XML):** wyciągane z bundli przez `tools/recipes/bundle.py` + `recipes.py` — opis narzędzi
  w [docs/recipes.md](docs/recipes.md).
- Pliki czytaj i zmieniaj narzędziami Read/Edit/Write — PowerShell 5.1 psuje polskie znaki
  (`Set-Content` zapisuje w ANSI).

## Struktura

```text
src/modConsumableAlchemy/content/scripts/local/
  consumableAlchemy_common.ws        klasyfikacja consumables
  consumableAlchemy_inventory.ws     blokada odnawiania, alkohol i powiadomienia, stół w Corvo Bianco
  consumableAlchemy_alchemy.ws       menedżer i menu alchemii (warzenie, blokada, odświeżanie listy)
  consumableAlchemy_recipes.ws       wybór receptury: pełna albo powielania
  consumableAlchemy_recipes_table.ws GENEROWANY z tabeli receptur — nie edytować
tools/recipes/                       Python: bundle → dane → tabela receptur → generator .ws
docs/                                dokumentacja techniczna (tabela niżej)
deploy.bat / deploy.ps1              instalacja do folderu gry
README.md                            strona moda dla gracza
```

## Konwencje

- Adnotacje kompilatora (`@wrapMethod`, `@replaceMethod`, `@addMethod`; działają też na metodach `private`
  i `final`) tylko w **nowych** plikach w `content\scripts\local\`. Plików vanilli nie nadpisujemy — mod
  nie wymaga Script Mergera.
- Wszystko własne ma prefiks `CA_`. Styl vanilli: taby, `if(...)`.
- Każdy punkt zaczepienia w vanilli ma wiersz w tabeli „Punkty zaczepienia” w `docs/architecture.md`.
- **Komentarz mówi, dlaczego kod jest taki. Nigdy nie mówi, skąd się wziął** (sesja, wersja, „wcześniej
  było…”) — historia jest w gicie.
- Kod, komentarze i commity po angielsku; dokumenty i README po polsku. Tekst w grze: istniejący klucz
  lokalizacji albo nowy wpis PL + EN.
- Nie kasuj danych, których nie rozumiesz.

## Pułapki, których nie widać w kodzie

1. W funkcji z `@wrapMethod` słowo `wrappedMethod` może wystąpić tylko raz — każde kolejne daje „Could not
   find function 'wrappedMethod'”. Najpierw ustal, co robić, potem jedno wywołanie.
2. Zmienne deklaruje się na początku funkcji — deklaracja po instrukcji to błąd kompilacji.
3. Kompilator vanilli nie mieści dużych funkcji (vanilla obchodzi to `HACK_NO_MEMORY_TO_COMPILE_*`) — stąd
   generator tnie tabelę na jedną małą funkcję na recepturę.
4. Status z `CanCookRecipe` steruje też filtrem menu („Już wykonane”, `canCookStatusForFilter`). Zmiana
   statusu zmienia, co menu ukrywa; żeby zmienić tylko tekst pozycji, zmieniaj `cantCookReason`.
5. Nadmiaru dawek ponad limit nie przycinaj przy odczycie — powód: D16 w [docs/decisions.md](docs/decisions.md).
6. Nagrody questowe i przedmioty startowe dostają pełne dawki z pominięciem wrappera odnawiania
   (`SingletonItemSetAmmo` wprost) — zgodne z zasadą 4, nie łataj.
7. Pułapki testowe (samodzielne starty dodatków, brak moda na liście modów, Wywar Wodnej Baby):
   [docs/testing.md](docs/testing.md#pułapki-testowe).

## Dokumenty

| Plik | Co zawiera | Zalecana długość |
|---|---|---|
| `CLAUDE.md` | słownik, zasady produktu, sposób pracy, pułapki | ok. 140 linii |
| `README.md` | strona dla gracza (PL, bez technikaliów, styl Nexusa), lista zmian wersji | ok. 60 linii |
| `docs/architecture.md` | jak mod działa: punkty zaczepienia, mechanika vanilli, degradacja | ok. 100 linii |
| `docs/decisions.md` | rozstrzygnięcia z powodem, zwłaszcza odrzucone kierunki | wpis ok. 6 linii |
| `docs/recipes.md` | dane receptur z gry, narzędzia `tools/recipes/`, obecna tabela | ok. 70 linii |
| `docs/testing.md` | checklista bieżącego wycinka, test dymny, pułapki testowe | ok. 60 linii |
| `docs/roadmap.md` | co dalej: to, czego nie zbudowano; pytania do autora; Szlif | ok. 70 linii |
| `docs/spec/` | koncepcja etapu przed budową: materiał, potem wersja uzgodniona z autorem | — |
| `docs/archive/` | nieobowiązujące; tylko przez odsyłacz z decisions.md albo roadmapy | — |

Kod jest źródłem prawdy; dokument jest tam, gdzie kod nie wystarcza. Wiedza o projekcie mieszka tylko
w tych plikach, nie w pamięci asystenta. Długość (wiersze ok. 110 znaków) to wskazówka: przekroczenie to
sygnał do przeglądu, nie powód do skracania kosztem jasności, powodu czy informacji.
- Stan, nie historia: bez dat, numerów sesji i słów „dziś”, „na razie”, „wcześniej”. Zmiany wersji opisuje
  lista zmian w README, resztę — git.
- Rzecz ma jedno miejsce: mechanizm w architekturze, powód w rozstrzygnięciach, plan w roadmapie, dane
  receptur w recipes.md; gdzie indziej tylko odsyłacz. Zmieniając regułę, szukaj jej słów we wszystkich
  dokumentach. Materiał etapu (spec) po jego zakończeniu idzie do archiwum.
- Pojęcie ma jedną nazwę ze słownika. „X nie ma” podaje powód albo odsyła do rozstrzygnięcia. Punkt to jedna
  myśl, do ok. 60 słów. Odwołanie do vanilli: nazwa funkcji plus `plik:linia` jako podpowiedź.
