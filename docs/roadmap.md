# Roadmapa — ConsumableAlchemy

Co dalej: to, czego jeszcze nie zbudowano, i pytania czekające na autora. Rozstrzygnięcia:
[decisions.md](decisions.md).

## Stan

v0.4 czyta receptury z generowanej tabeli; kompiluje się i wczytuje, reszta checklisty
([testing.md](testing.md)) czeka na test. Tabela nie jest szlifowana ([recipes.md](recipes.md#obecna-tabela)).

## Następne kroki

- [ ] **1. Test v0.4 w grze** według [testing.md](testing.md), z degradacją (zasada 5). Idzie pierwszy:
  etap receptur buduje na tym stanie. Gotowe, gdy: checklista odhaczona, wyniki w „Potwierdzone w grze”.
- [ ] **2. Szlif receptur: mikstury.** Zmiana pełnej receptury Pioruna 1 wymaga zaczepienia tutorialu
  ([architecture.md](architecture.md#receptury--recipesws-i-tabela)).
- [ ] **3. Szlif receptur: bomby.**
- [ ] **4. Szlif receptur: wywary.** Zmiana pełnej receptury wywaru wymaga zaczepienia stołu mutagenów.
- [ ] **5. Zamknięcie etapu receptur:** reguła `collision` jako błąd (D30), progi wysiłku powielenia
  `COPY_EFFORT_MAX` (2 / 4 / 6) sprawdzone na danych.

Każda partia (kroki 2–4) według D19–D22, D28–D31: propozycja per rodzina (pełna + powielenie + uzasadnienie
+ wynik walidatora) na gałęzi → autor przegląda `report.py --base main` → akceptacja → `generate.py` →
wdrożenie → test. Gotowe, gdy: autor zaakceptował, test w grze przeszedł.

## Do decyzji autora

Żadne nie blokuje kolejnego kroku.
- **D23. Samodzielne starty dodatków (HoS / B&W): receptury dla całego zestawu startowego czy tylko poz. 2?**
  Ok. 20 przedmiotów startowych jest w modzie jednorazowych
  ([architecture.md](architecture.md#samodzielne-starty-dodatków-hos--bw)). Rekomendacja: wrapper na
  `StandaloneEp1_1` / `StandaloneEp2_1`, dla istniejących zapisów `ApplyPatchFixes` przy fakcie
  `standalone_ep1` / `_ep2`: każdy posiadany consumable bez znanej receptury → `AddAlchemyRecipe(r, true, true)`
  (`playerWitcher.ws:4851`, idempotentne; receptura po `cookedItem_name`, jak `alchemyManager.ws:69`). Bez
  zapisu w save'ie, ok. 40 linii. Skutki jak przy każdej poznanej recepturze: statystyki i osiągnięcia
  `EA_BreakingBad` / `EA_Bombardier`, Nabyta Tolerancja (`S_Alchemy_s18`), `SEC_AlchemyRecipe`.
  Niesprawdzone: czy quest startu woła owiniętą metodę. Odrzucone: receptura przy inicjalizacji przedmiotu
  poz. ≥ 2 (nie pokrywa poz. 1 i wywarów); warzenie bez receptury (niespójność menu i tooltipów).
- **Wywar Wodnej Baby — zostawić czy zmienić?** Darmowa dawka przy nałożeniu, utrata opłaconej przy
  wygaśnięciu ([architecture.md](architecture.md#mechanika-vanilli-istotna-dla-moda)).
- **Stół w Corvo Bianco a mikstury questowe.** Wyłączony stół zabiera premię +1 także questowym miksturom
  i bombom (zasada 4: vanilla), a gracz słyszy tylko dźwięk odmowy. Warianty: zostaje; premia dla questowych;
  istniejący komunikat (D17).
- **Alkohol** zużywa się szybciej niż w vanilli ([recipes.md](recipes.md#alkohol)). Zostaje czy powielenie
  podstawia najtańszy posiadany alkohol, jak medytacja?

## Do zbadania przed pytaniem do autora

- **D26. Dwuznaczny komunikat „Już masz ten przedmiot”** (`panel_alchemy_exception_already_cooked`): w vanilli
  „uwarzone na zawsze”, w modzie także „pełna kieszeń”. Zbadać: `EAlchemyExceptions`,
  `AlchemyExceptionToString`, kandydaci kluczy z brzmieniem PL/EN z `*.w3strings`, czy etykiety filtrów
  przychodzą ze skryptu, czy z Flasha. Potem pytanie z wariantami: (0) zostaje; (i) inny tekst tylko przy pełnej
  kieszeni przez `cantCookReason` (status i filtr bez zmian, [architecture.md](architecture.md#mechanika-vanilli-istotna-dla-moda));
  (ii) dodatkowo filtr „Uzupełniono”.
- **Inne przedmioty specjalne bez tagu `Quest`** (feromony, `Killer Whale 1`, `Trial Potion Kit`) — sprawdzić
  w XML, czy powinny zostać vanillowe jak `Pops Antidote` (D27).

## Odłożone

- **Widoczność moda na liście modów w menu gry** — znak, że mod się wczytał. Założenie: mod z samych skryptów
  nie ma manifestu ani metadanych. Do ustalenia: z czego gra buduje listę (manifest, `metadata.store`,
  bundle), czy da się bez RedKitu, skutki uboczne (osiągnięcia, ostrzeżenia).
- **Oleje jako zużywalne** — przedmiot oleju ma dawki = liczba nałożeń, nałożenie zużywa 1, warzenie
  uzupełnia, medytacja nie. W vanilli przedmiot oleju się nie zużywa, a powłoka ma ładunki na ciosy
  (`W3Effect_Oil.ReduceAmmo`, `r4Player.ws:1009`; nieskończona ze skillem `S_Alchemy_s06` poz. 3) — to
  zostaje. Do ustalenia: czy olej jest singletonem z `ammo`, funkcja nakładania, UI (tooltip x/y, blokada
  przy 0), limit, oleje questowe i auto-nakładanie, koszt. Oleje są vanilla (D9).
- **Stół alchemiczny w Corvo Bianco** — inna rola niż premia przy odnawianiu (D17), np. warzenie przy stole
  → max + `QUANTITY_INCREASED_BY_ALCHEMY_TABLE` (vanillowa stała, +1).
- **Tańsze zioła u kupców, więcej ziół w lootcie** (wymaga zmian w XML).
- **Paczka do wydania** — archiwum zip dla Nexusa, numer wersji w paczce, strona moda dla gracza (dlaczego,
  co robi, instalacja, lista zmian; z zasad produktu i rozstrzygnięć).
