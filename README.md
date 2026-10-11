# ConsumableAlchemy

Mod do Wiedźmina 3 (Remastered, gra 5.0): alchemia zużywalna zamiast singletonów odnawianych medytacją.
Mikstury, bomby i wywary uzupełnia wyłącznie warzenie, za składniki. Ten dokument opisuje projekt: pojęcia,
zasady produktu, środowisko i konwencje. Sposób pracy: [CLAUDE.md](CLAUDE.md). Stan prac i następny krok:
[docs/roadmap.md](docs/roadmap.md).

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

## Środowisko, wdrożenie, narzędzia

- **Gra:** `D:\gry\steam\steamapps\common\the witcher 3` — Steam, Remastered, `bin\x64_dx12\witcher3.exe`
  w wersji **5.0.0.1044392**. Nowsza niż next-gen 4.0 — wiedzy o 4.x nie zakładaj, sprawdzaj w skryptach
  vanilli tej instalacji: `<gra>\content\content0\scripts\game\...` (tylko do odczytu; `plik:linia`
  w dokumentach dotyczą tej instalacji). Dodatki są w `content0`, katalogu `dlc` nie ma.
- **Kompilacja:** kompilatora poza grą nie ma. Gra kompiluje skrypty przy starcie i pokazuje błędy w oknie.
  Ostrzeżenia `[content0] ... not marked as abstract` / `has no autostate` są z vanilli — ignoruj.
- **Wdrożenie:** `powershell -ExecutionPolicy Bypass -File deploy.ps1 [-GameDir <ścieżka>]` (albo
  `deploy.bat`) → `<gra>\mods\modConsumableAlchemy`.
- **Bramka przed grą:** przed każdym `deploy.ps1` uruchom `powershell -ExecutionPolicy Bypass -File
  tools/check.ps1` — sprawdza, czy wygenerowana tabela receptur jest aktualna, błędy reguł receptur, lint `.ws`
  (pułapki 1 i 2) i brak danych gry w gicie.
- **Receptury:** zmieniasz `tools/recipes/recipes_table.json`, potem `python tools/recipes/generate.py`
  (waliduje i generuje `ConsumableAlchemy_recipes_table.ws`). Wygenerowanego pliku nie edytuj ręcznie.
- **Dane gry (XML):** wyciągane z bundli przez `tools/recipes/bundle.py` + `recipes.py` — opis narzędzi
  w [docs/recipes.md](docs/recipes.md). Danych gry nie commituj (`tools/recipes/x/`, `data.json`).
- Pliki czytaj i zmieniaj narzędziami Read/Edit/Write — PowerShell 5.1 psuje polskie znaki
  (`Set-Content` zapisuje w ANSI).

## Struktura

```text
src/modConsumableAlchemy/content/scripts/local/
  ConsumableAlchemy_common.ws        klasyfikacja consumables
  ConsumableAlchemy_inventory.ws     blokada odnawiania, alkohol i powiadomienia, stół w Corvo Bianco
  ConsumableAlchemy_alchemy.ws       menedżer i menu alchemii (warzenie, blokada, odświeżanie listy)
  ConsumableAlchemy_recipes.ws       wybór receptury: pełna albo powielania
  ConsumableAlchemy_standalone.ws    receptury startowych consumables przy samodzielnym starcie HoS / B&W
  ConsumableAlchemy_recipes_table.ws GENEROWANY z tabeli receptur
tools/recipes/                       Python: bundle → dane → tabela receptur → generator .ws
tools/check.ps1                      bramka przed grą
tools/lint_ws.py                     lint .ws: pułapki 1 i 2 kompilatora
docs/                                dokumentacja techniczna (spis w CLAUDE.md)
deploy.bat / deploy.ps1              instalacja do folderu gry
```

## Konwencje

- Adnotacje kompilatora (`@wrapMethod`, `@replaceMethod`, `@addMethod`; działają też na metodach `private`
  i `final`) tylko w **nowych** plikach w `content\scripts\local\`. Plików vanilli nie nadpisujemy — mod
  nie wymaga Script Mergera.
- Wszystko własne ma prefiks `CA_`. Styl vanilli: taby, `if(...)`.
- Każdy punkt zaczepienia w vanilli ma wiersz w tabeli „Punkty zaczepienia” w `docs/architecture.md`.
- **Komentarz mówi, dlaczego kod jest taki. Nigdy nie mówi, skąd się wziął** (sesja, wersja, „wcześniej
  było…”) — historia jest w gicie.
- Kod, komentarze i commity po angielsku; dokumenty po polsku. Tekst w grze: istniejący klucz lokalizacji
  albo nowy wpis PL + EN.
- Nie kasuj danych, których nie rozumiesz.

## Pułapki kompilatora

1. W funkcji z `@wrapMethod` słowo `wrappedMethod` może wystąpić tylko raz — każde kolejne daje „Could not
   find function 'wrappedMethod'”. Najpierw ustal, co robić, potem jedno wywołanie.
2. Zmienne deklaruje się na początku funkcji — deklaracja po instrukcji to błąd kompilacji.
3. Kompilator vanilli nie mieści dużych funkcji (vanilla obchodzi to `HACK_NO_MEMORY_TO_COMPILE_*`) — stąd
   generator tnie tabelę na jedną małą funkcję na recepturę.

Pułapki mechaniki vanilli (status warzenia a filtr menu, nadmiar dawek ponad limit, pełne dawki z pominięciem
odnawiania): [docs/architecture.md](docs/architecture.md). Pułapki testowe:
[docs/testing.md](docs/testing.md#pułapki-testowe).
