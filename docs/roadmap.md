# Roadmapa — Consumable Alchemy

Co dalej: to, czego jeszcze nie zbudowano, i pytania czekające na autora. Rozstrzygnięcia:
[decisions.md](decisions.md). Co już działa: kod i [README.md](../README.md#lista-zmian).

## Stan

Mod w wersji v0.4 czyta receptury z generowanej tabeli (= poprzednia reguła 1:1). Kompiluje się i wczytuje;
reszta checklisty ([testing.md](testing.md)) czeka na test.

## Następne kroki

1. **Test v0.4 i tabeli w grze** według [testing.md](testing.md), razem z degradacją (obietnica w README).
   Etap receptur buduje na tym stanie, więc idzie pierwszy.
2. **Walidator** `validate.py` (dane z `ingredient_catalog.json`, flagi także w kolumnie raportu `report.py`): kolizje (identyczne zbiory i różnica 1 składnika), brak
   sygnatury, monotoniczność wysiłku w rodzinie, wysiłek wg rangi (podstawowe ≤ zaawansowane), powielenie
   tańsze od pełnej, składniki istnieją, alkohol w miksturach i wywarach, proszek w bombach, brak niższego
   poziomu w powieleniu (D28).
3. **Spec szlifowania receptur** — [spec/receptury.md](spec/receptury.md) uzupełniony wynikami katalogu
   i walidatora, do akceptacji autora; wymaga rozstrzygnięcia D22 i pytania o mutagen w wywarach.
4. **Szlifowanie receptur partiami** (mikstury → bomby → wywary): propozycja per rodzina (pełna + powielenie
   + uzasadnienie + wynik walidatora) na gałęzi, autor przegląda `report.py --base main` → akceptacja autora → `generate.py` → wdrożenie → test. README (opis
   krótszej receptury i przykład) zmienia się razem z tabelą. Zmiana pełnej receptury Pioruna 1 albo wywaru
   wymaga zaczepienia tutorialu / stołu mutagenów ([architecture.md](architecture.md#receptury--recipesws-i-tabela)).

## Do decyzji autora

- **D22. Części potworów w powieleniu.** Zależy od łatwości zdobycia (odradzanie, drop); dane:
  [spec/receptury.md](spec/receptury.md#części-potworów), `ingredient_catalog.json`. Rekomendacja: części
  z wysiłkiem 3 w katalogu (`Ghoul blood`, `Drowner brain`, `Drowned dead tongue`, `Nekker heart`, także
  `Arachas venom`, `Alghoul bone marrow`, mutageny południcy i nocnicy) zostają jako składnik wysiłku;
  wysiłek 4–5 → tematyczny zamiennik.
- **Wysiłek receptury** w raporcie = suma poziomów składników, bez ilości. Do ustalenia przed walidatorem.
- **Mutagen w powieleniu wywaru** — zostaje czy wypada (dziś wypada; wywar = alkohol + zioła).
- **D23. Samodzielne starty dodatków (HoS / B&W)** — ok. 20 przedmiotów startowych jest w modzie jednorazowych
  ([architecture.md](architecture.md#samodzielne-starty-dodatków-hos--bw)). Rekomendacja: wrapper na
  `StandaloneEp1_1` / `StandaloneEp2_1`, a dla istniejących zapisów na `ApplyPatchFixes` przy fakcie
  `standalone_ep1` / `_ep2`: każdy posiadany consumable bez znanej receptury → `AddAlchemyRecipe(r, true, true)`
  (`playerWitcher.ws:4851`, idempotentne; przedmiot → receptura przez iterację `alchemy_recipes` po
  `cookedItem_name`, jak `alchemyManager.ws:69`). Mod dalej nic nie zapisuje; ok. 40 linii. Skutki jak przy
  każdej poznanej recepturze, także cichej: statystyki i osiągnięcia `EA_BreakingBad` / `EA_Bombardier`,
  ability Nabytej Tolerancji (`S_Alchemy_s18`), zdarzenie `SEC_AlchemyRecipe`. Niesprawdzone: czy quest
  startu woła owiniętą metodę. Odrzucone: receptura przy inicjalizacji przedmiotu poz. ≥ 2 (nie pokrywa poz. 1
  i wywarów); warzenie bez receptury (niespójność menu i tooltipów). Pytanie: cały zestaw czy tylko poz. 2.
- **D26. Dwuznaczny komunikat „Już masz ten przedmiot”** (`panel_alchemy_exception_already_cooked`):
  w vanilli „uwarzone na zawsze”, w modzie także „pełna kieszeń”. Warianty: (0) zostaje; (i) inny tekst
  tylko przy pełnej kieszeni przez `cantCookReason` (istniejący klucz albo nowy wpis PL + EN; status i filtr
  bez zmian, pułapka 4); (ii) dodatkowo filtr „Uzupełniono” (pomysł autora) — tani, jeśli etykiety filtrów
  przychodzą ze skryptu, drogi i ryzykowny, jeśli są we Flashu. Przed decyzją zbadać: `EAlchemyExceptions`,
  `AlchemyExceptionToString`, kandydaci kluczy z brzmieniem PL/EN z `*.w3strings`, źródło etykiet filtrów.
- **D27. `Pops Antidote`** (q303) nie ma tagu `Quest`, więc jest consumable (jest w tabeli). Rekomendacja:
  wyłączyć z systemu (vanilla). Przy okazji sprawdzić w XML inne zwykłe mikstury/bomby bez tagu `Quest`
  i przedmioty specjalne (feromony, `Killer Whale 1`, `Trial Potion Kit`).
- **Wywar Wodnej Baby** — darmowa dawka przy nałożeniu, utrata opłaconej przy wygaśnięciu
  ([architecture.md](architecture.md#mechanika-vanilli-istotna-dla-moda)). README opisuje to jako zachowanie
  gry; zostawić czy zmienić.
- **Stół w Corvo Bianco a mikstury questowe** — wyłączony stół zabiera premię +1 także questowym miksturom
  i bombom (zasada 4: vanilla), a gracz słyszy tylko dźwięk odmowy, bez tekstu. Zostawić czy przywrócić
  premię dla questowych / dodać istniejący komunikat (D17).
- **Alkohol** zużywa się szybciej niż w vanilli ([recipes.md](recipes.md#alkohol)). Pomysł: w powieleniu
  podstawiać najtańszy posiadany alkohol, jak medytacja.

## Odłożone

- **Widoczność moda na liście modów w menu gry** — znak, że mod się wczytał. Założenie: mod z samych skryptów
  nie ma manifestu ani metadanych. Do ustalenia: z czego gra buduje listę (manifest, `metadata.store`,
  bundle), czy da się bez RedKitu, skutki uboczne (osiągnięcia, ostrzeżenia).
- **Oleje jako zużywalne** — przedmiot oleju ma dawki = liczba nałożeń, nałożenie zużywa 1, warzenie
  uzupełnia, medytacja nie. W vanilli przedmiot oleju się nie zużywa, a powłoka ma ładunki na ciosy
  (`W3Effect_Oil.ReduceAmmo`, `r4Player.ws:1009`; nieskończona ze skillem `S_Alchemy_s06` poz. 3) — to
  zostaje. Do ustalenia: czy olej jest singletonem z `ammo`, funkcja nakładania, UI (tooltip x/y, blokada
  przy 0), limit, oleje questowe i auto-nakładanie, koszt. Dziś oleje są vanilla (D9).
- **Stół alchemiczny w Corvo Bianco** — inna rola niż premia przy odnawianiu (D17), np. warzenie przy stole
  → max + `QUANTITY_INCREASED_BY_ALCHEMY_TABLE` (vanillowa stała, +1).
- **Tańsze zioła u kupców, więcej ziół w lootcie** (wymaga zmian w XML).
- **Paczka do wydania** — archiwum zip dla Nexusa, numer wersji w paczce.

## Szlif

(pusto)
