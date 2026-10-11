# Roadmapa — ConsumableAlchemy

Co dalej: to, czego jeszcze nie zbudowano, i pytania czekające na autora. Rozstrzygnięcia:
[decisions.md](decisions.md).

## Stan

Obecny kod (warzenie napełnia do limitu, limity vanilli, receptury z generowanej tabeli) kompiluje się
i wczytuje, reszta checklisty ([testing.md](testing.md)) czeka na test. Przed wydaniem mod nie ma numeru wersji. Tabela nie jest szlifowana ([recipes.md](recipes.md#obecna-tabela)).

## Następne kroki

- [ ] **1. Test obecnego kodu w grze** według [testing.md](testing.md), z degradacją (zasada 5). Idzie pierwszy:
  etap receptur buduje na tym stanie. Gotowe, gdy: checklista odhaczona, wyniki w „Potwierdzone w grze”.
- [ ] **2. Szlif receptur: mikstury.** Zmiana pełnej receptury Pioruna 1 wymaga zaczepienia tutorialu
  ([architecture.md](architecture.md#receptury--recipesws-i-tabela)).
- [ ] **3. Szlif receptur: bomby.**
- [ ] **4. Szlif receptur: wywary.** Zmiana pełnej receptury wywaru wymaga zaczepienia stołu mutagenów.
- [ ] **5. Zamknięcie etapu receptur:** reguła `collision` jako błąd ([składnik sygnaturowy](decisions.md#składnik-sygnaturowy)), progi wysiłku powielenia
  `COPY_EFFORT_MAX` (2 / 4 / 6) sprawdzone na danych.

Każda partia (kroki 2–4) według [rozstrzygnięć o recepturach](decisions.md#receptury): propozycja per rodzina (pełna + powielenie + uzasadnienie
+ wynik walidatora) na gałęzi → autor przegląda `report.py --base main` → akceptacja → `generate.py` →
wdrożenie → test. Gotowe, gdy: autor zaakceptował, test w grze przeszedł.

## Do decyzji autora

Żadne nie blokuje kolejnego kroku.
- **Starty dodatków (HoS / B&W): receptury dla całego zestawu startowego czy tylko poz. 2?**
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
  istniejący komunikat ([stół bez premii](decisions.md#stół-w-corvo-bianco-bez-premii)).
- **Alkohol** zużywa się szybciej niż w vanilli ([recipes.md](recipes.md#alkohol)). Zostaje czy powielenie
  podstawia najtańszy posiadany alkohol, jak medytacja?
- **Komunikat „Już masz ten przedmiot” przy pełnej kieszeni.** Ten sam status `EAE_CannotCookMore` znaczy
  w vanilli „uwarzone na zawsze”, w modzie także „komplet dawek” ([szczegóły](architecture.md#mechanika-vanilli-istotna-dla-moda)).
  Warianty: (0) zostaje; (i) osobny tekst tylko przy pełnej kieszeni, status i filtr „Już wykonane” bez zmian
  (nowy klucz PL + EN, brzmienie do uzgodnienia); (ii) dodatkowo filtr „Uzupełniono” — wymaga zmian we Flashu
  (trzy stałe przełączniki), poza zakresem moda. Rekomendacja: (i).
- **Przedmioty specjalne: system moda czy vanilla?** Bez tagu `Quest` zostały: feromony (3) i `Killer Whale 1`
  — zwykłe mikstury z recepturą z lootu i sklepów; rekomendacja: system moda. `ReinaldsPhiltre` — bez receptury,
  jak `Village drink`; rekomendacja: vanilla, wyłączenie po nazwie w `CA_IsConsumableItemName` i `draft.py`
  ([wzór](decisions.md#antidotum-popsa-poza-systemem)). `Trial Potion Kit` ma tag `Quest` — już vanilla.
  Dane: [architecture.md](architecture.md#mechanika-vanilli-istotna-dla-moda).

## Odłożone

- **Widoczność moda na liście modów w menu gry** — znak, że mod się wczytał. Założenie: mod z samych skryptów
  nie ma manifestu ani metadanych. Do ustalenia: z czego gra buduje listę (manifest, `metadata.store`,
  bundle), czy da się bez RedKitu, skutki uboczne (osiągnięcia, ostrzeżenia).
- **Oleje jako zużywalne** — przedmiot oleju ma dawki = liczba nałożeń, nałożenie zużywa 1, warzenie
  uzupełnia, medytacja nie. W vanilli przedmiot oleju się nie zużywa, a powłoka ma ładunki na ciosy
  (`W3Effect_Oil.ReduceAmmo`, `r4Player.ws:1009`; nieskończona ze skillem `S_Alchemy_s06` poz. 3) — to
  zostaje. Do ustalenia: czy olej jest singletonem z `ammo`, funkcja nakładania, UI (tooltip x/y, blokada
  przy 0), limit, oleje questowe i auto-nakładanie, koszt. Oleje są vanilla ([zakres systemu](decisions.md#zakres-systemu)).
- **Stół alchemiczny w Corvo Bianco** — inna rola niż premia przy odnawianiu ([stół bez premii](decisions.md#stół-w-corvo-bianco-bez-premii)), np. warzenie przy stole
  → max + `QUANTITY_INCREASED_BY_ALCHEMY_TABLE` (vanillowa stała, +1).
- **Tańsze zioła u kupców, więcej ziół w lootcie** (wymaga zmian w XML).
- **Paczka do wydania** — wersja **1.0**: archiwum zip dla Nexusa z numerem wersji, tag `v1.0` w gicie,
  strona moda dla gracza (dlaczego, co robi, instalacja, lista zmian; z zasad produktu i rozstrzygnięć).
  Numery wersji dopiero od wydania.
