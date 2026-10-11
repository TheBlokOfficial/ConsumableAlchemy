# Roadmapa — ConsumableAlchemy

Co dalej: to, czego jeszcze nie zbudowano, i pytania czekające na autora. Rozstrzygnięcia:
[decisions.md](decisions.md).

## Stan

Kod (warzenie napełnia do limitu, limity vanilli, receptury z tabeli, receptury startów dodatków, stół
w Corvo Bianco) i dopracowana tabela receptur ([recipes.md](recipes.md#obecna-tabela)) czekają na test
w grze ([testing.md](testing.md)) i ręczny przegląd receptur przez autora. Przed wydaniem mod nie ma numeru
wersji.

## Następne kroki

- [ ] **1. Przegląd receptur przez autora:** `report.py --base main` (pole `note` uzasadnia każdą recepturę).
  Uwagi wracają do tabeli jednym przejściem. Gotowe, gdy: autor zaakceptował.
- [ ] **2. Test w grze** według [testing.md](testing.md), z degradacją (zasada 5), w tym nowa gra HoS i B&W.
  Gotowe, gdy: checklista odhaczona, wyniki w „Potwierdzone w grze”.

## Do decyzji autora

Brak otwartych pytań.

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
