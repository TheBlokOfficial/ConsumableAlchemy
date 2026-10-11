# Roadmapa — ConsumableAlchemy

Co dalej: to, czego jeszcze nie zbudowano, i pytania czekające na autora. Rozstrzygnięcia:
[decisions.md](decisions.md).

## Stan

Kod (warzenie napełnia do limitu, limity vanilli, receptury z tabeli, receptury startów dodatków, stół
w Corvo Bianco, tekst przy pełnej kieszeni) działa w grze. Dopracowana tabela receptur
([recipes.md](recipes.md#obecna-tabela)) czeka na ocenę autora w zwykłej grze. Poza tym nic nie jest
zaplanowane; pomysły spoza zakresu i wydanie są odrzucone w [decisions.md](decisions.md).

## Następne kroki

- [ ] **1. Receptury w praktyce:** autor gra z modem i ocenia receptury i koszt powielenia. Pomoc:
  `report.py` (pole `note` uzasadnia każdą recepturę). Najpierw sprawdzić wyzwalacze powrotu w rozstrzygnięciach
  ([alkohol](decisions.md#alkohol-tylko-jako-składnik), [części potworów](decisions.md#części-potworów-według-wysiłku)).
  Uwagi wracają do tabeli jednym przejściem. Gotowe, gdy: autor zaakceptował receptury.
- [ ] **2. Pozostałe punkty checklisty** z [testing.md](testing.md), sprawdzane przy okazji grania (degradacja,
  nowa gra HoS i B&W). Gotowe, gdy: checklista odhaczona, wyniki w „Potwierdzone w grze”.

## Do decyzji autora

Brak otwartych pytań.

## Szlif

Brak.
