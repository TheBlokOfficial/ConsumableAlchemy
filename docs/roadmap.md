# Roadmapa — ConsumableAlchemy

Co dalej: to, czego jeszcze nie zbudowano, i pytania czekające na autora. Rozstrzygnięcia:
[decisions.md](decisions.md).

## Stan

Kod (warzenie napełnia do limitu, limity vanilli, receptury z tabeli, receptury startów dodatków, stół
w Corvo Bianco) i dopracowana tabela receptur ([recipes.md](recipes.md#obecna-tabela)) czekają na test
w grze ([testing.md](testing.md)) i ręczny przegląd receptur przez autora. Poza tymi dwoma krokami nic nie
jest zaplanowane; pomysły spoza zakresu i wydanie są odrzucone w [decisions.md](decisions.md).

## Następne kroki

- [ ] **1. Przegląd receptur przez autora:** `report.py --base main` (pole `note` uzasadnia każdą recepturę).
  Uwagi wracają do tabeli jednym przejściem. Gotowe, gdy: autor zaakceptował.
- [ ] **2. Test w grze** według [testing.md](testing.md), z degradacją (zasada 5), w tym nowa gra HoS i B&W.
  Gotowe, gdy: checklista odhaczona, wyniki w „Potwierdzone w grze”.

## Do decyzji autora

Brak otwartych pytań.

## Szlif

- Prawy panel menu przy pełnej kieszeni nadal pokazuje „Już masz ten przedmiot” (`cantCookReason` w prywatnej
  `PopulateData`); nowy tekst daje tylko komunikat przy próbie warzenia.
