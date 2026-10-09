# Roadmapa — Consumable Alchemy

Co dalej: to, czego jeszcze nie zbudowano, i pytania czekające na autora. Rozstrzygnięcia:
[decisions.md](decisions.md). Co już działa: kod i [README.md](../README.md#lista-zmian).

## Stan

Mod w wersji v0.4 czyta receptury z generowanej tabeli (= poprzednia reguła 1:1). Kompiluje się i wczytuje;
reszta checklisty ([testing.md](testing.md)) czeka na test.

## Następne kroki

1. **Test v0.4 i tabeli w grze** według [testing.md](testing.md), razem z degradacją (obietnica w README).
   Etap receptur buduje na tym stanie, więc idzie pierwszy.
2. **`tools/check.ps1`** — szybka bramka przed grą: `generate.py` w trybie sprawdzania (tabela zgodna
   z wygenerowanym `.ws`), lint pułapek kompilatora z CLAUDE.md (drugie `wrappedMethod` w funkcji, deklaracja
   zmiennej po instrukcji), dane gry (`tools/recipes/x/`, `data.json`) poza commitem.
3. **Katalog składników** `tools/recipes/ingredients.py` → `ingredient_catalog.json`: dla każdego składnika
   cena, typ, sklepy (liczba, region), zbieranie w świecie, **drop z potworów** (tabele lootu potworów w XML,
   szansa, potwór, odradzanie) i poziom wysiłku 1–5 (kryteria w `_meta`). Dane do D22 i walidatora. Bez zmian
   w `draft.py`, `generate.py` i tabeli.
4. **Walidator** `validate.py` (po katalogu): kolizje (identyczne zbiory i różnica 1 składnika), brak
   sygnatury, monotoniczność wysiłku w rodzinie, wysiłek wg rangi (podstawowe ≤ zaawansowane), powielenie
   tańsze od pełnej, składniki istnieją, alkohol w miksturach i wywarach, proszek w bombach, brak niższego
   poziomu w powieleniu (D28).
5. **Spec szlifowania receptur** (`docs/spec/receptury.md`) — kryteria z [recipes.md](recipes.md#kryteria-balansu)
   i wyniki katalogu zebrane w jedną koncepcję do akceptacji autora; wymaga rozstrzygnięcia D22 i pytania
   o mutagen w wywarach.
6. **Szlifowanie receptur partiami** (mikstury → bomby → wywary): propozycja per rodzina (pełna + powielenie
   + uzasadnienie + wynik walidatora) → akceptacja autora → `generate.py` → wdrożenie → test. README (opis
   krótszej receptury i przykład) zmienia się razem z tabelą.

## Do decyzji autora

- **D22. Części potworów w powieleniu.** Zależy od łatwości zdobycia (odradzanie, drop); punkt odniesienia:
  W1 ([recipes.md](recipes.md#części-potworów)). Rekomendacja architekta: pospolite części (`Ghoul blood`,
  `Drowner brain`, `Drowned dead tongue`, `Nekker heart`) zostają jako składnik wysiłku, jeśli katalog
  potwierdzi drop; rzadkie → tematyczny zamiennik.
- **Mutagen w powieleniu wywaru** — zostaje czy wypada (dziś wypada; wywar = alkohol + zioła).
- **D23. Samodzielne starty dodatków (HoS / B&W)** — ok. 20 przedmiotów startowych jest w modzie jednorazowych
  (dane: [architecture.md](architecture.md#samodzielne-starty-dodatków-hos--bw)). Rekomendacja:
  `@wrapMethod(W3PlayerWitcher)` na `StandaloneEp1_1` / `StandaloneEp2_1` → po oryginale dla każdego
  posiadanego consumable bez znanej receptury `AddAlchemyRecipe(r, true, true)`; dla istniejących zapisów to
  samo w wrapperze `ApplyPatchFixes` przy `FactsQuerySum('standalone_ep1' / 'standalone_ep2') > 0` (odczyt
  vanillowych faktów, idempotentne, mod dalej nic nie zapisuje). Ok. 40 linii; zwykła gra i NG+ bez zmian.
  Skutki: osiągnięcia za znane receptury, Nabyta Tolerancja — jak przy każdej poznanej recepturze.
  Niesprawdzone: czy quest startu woła owiniętą metodę. Odrzucone: poznawanie receptury przy inicjalizacji
  przedmiotu poz. ≥ 2 (nie pokrywa poz. 1 i wywarów); warzenie bez znajomości receptury (zmienia projekt,
  ryzyko niespójności menu i tooltipów, mod-smell). Pytanie: cały zestaw (także poz. 1 i wywary) czy tylko poz. 2.
- **D26. Dwuznaczny komunikat „Już masz ten przedmiot”** (`EAE_CannotCookMore` →
  `panel_alchemy_exception_already_cooked`): w vanilli znaczy „uwarzone na zawsze”, w modzie także „pełna
  kieszeń — uwarzysz po zużyciu”. Warianty: (0) zostaje; (i) inny tekst pozycji tylko przy pełnej kieszeni —
  istniejący klucz lokalizacji albo nowy wpis PL + EN, przez `cantCookReason` w skrypcie (filtr „Już wykonane”
  bez zmian — jego nazwa pasuje do obu znaczeń); (ii) dodatkowo nowy filtr „Uzupełniono” (pomysł autora), jeśli
  etykiety filtrów przychodzą ze skryptu — jeśli są zaszyte we Flashu menu, to edycja `.redswf`, duży koszt
  i ryzyko przy aktualizacjach gry. Do zbadania przed decyzją: enum `EAlchemyExceptions`,
  `AlchemyExceptionToString`, kandydaci kluczy (crafting, ekwipunek, medytacja) z brzmieniem PL/EN
  z `*.w3strings`, źródło etykiet filtrów. Status pozycji się nie zmienia (pułapka 4 w CLAUDE.md).
- **D27. `Pops Antidote`** (q303) nie ma tagu `Quest`, więc jest consumable (jest w tabeli). Rekomendacja:
  wyłączyć z systemu (vanilla). Przy okazji sprawdzić w XML inne zwykłe mikstury/bomby bez tagu `Quest`
  i przedmioty specjalne (feromony, `Killer Whale 1`, `Trial Potion Kit`).
- **Wywar Wodnej Baby** — darmowa dawka przy nałożeniu, utrata opłaconej przy wygaśnięciu
  ([architecture.md](architecture.md#mechanika-vanilli-istotna-dla-moda)). README opisuje to jako zachowanie
  gry; zostawić czy zmienić.
- **Alkohol** zużywa się szybciej niż w vanilli ([recipes.md](recipes.md#alkohol)). Pomysł: w powieleniu
  podstawiać najtańszy posiadany alkohol, jak medytacja.

## Odłożone

- **Widoczność moda na liście modów w menu gry** — znak, że mod się wczytał. Założenie: mod z samych skryptów
  nie ma manifestu ani metadanych. Do ustalenia: z czego gra buduje listę (manifest, `metadata.store`,
  bundle), czy da się bez RedKitu, skutki uboczne (osiągnięcia, ostrzeżenia).
- **Oleje jako zużywalne** — przedmiot oleju ma dawki = liczba nałożeń, nałożenie zużywa 1, warzenie
  uzupełnia, medytacja nie; ładunki powłoki na ciosy bez zmian (`W3Effect_Oil.ReduceAmmo`). Do ustalenia: czy
  olej jest singletonem z `ammo`, funkcja nakładania, UI (tooltip x/y, blokada przy 0), limit, oleje questowe
  i auto-nakładanie, koszt. Dziś oleje są vanilla (D9).
- **Stół alchemiczny w Corvo Bianco** — inna rola niż premia przy odnawianiu (D17), np. warzenie przy stole
  → max + `QUANTITY_INCREASED_BY_ALCHEMY_TABLE` (vanillowa stała, +1).
- **Tańsze zioła u kupców, więcej ziół w lootcie** (wymaga zmian w XML).
- **Paczka do wydania** — archiwum zip dla Nexusa, numer wersji w paczce.

## Szlif

(pusto)
