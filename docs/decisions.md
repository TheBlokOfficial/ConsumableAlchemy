# Rozstrzygnięcia — Consumable Alchemy

Rozstrzygnięcia autora z powodem. Odrzucone warianty są tu po to, żeby do nich nie wracać bez nowego
argumentu. Numer nie zmienia się i nie wraca (wycofane: D24 — sposób pracy, jest w CLAUDE.md; D25 — scalone
z D18). Pytania otwarte (D22, D23, D26, D27 i inne): [roadmap.md](roadmap.md#do-decyzji-autora).
Mechanizm: [architecture.md](architecture.md), receptury: [recipes.md](recipes.md).

## Cel

Wzorzec: Wiedźmin 1 — każda butelka to składniki, a składniki są tanie i powszechne. Kryterium: wypicie
mikstury i rzucenie bomby nie może boleć ani irytować przy powielaniu (nie żal rzucić, nawet przy pudle),
a całość ma być bardziej immersyjna niż vanilla, w której medytacja odnawia wszystko. Bez odblokowania
i powielenia (D11) mod nie miałby sensu: każde warzenie za pełną recepturę byłoby kilkukrotnie droższe niż
jednorazowe warzenie w vanilli.

## Twarde wymogi

- **D1. Vanillowość.** Zero mod-smellu i własnego renderowania (nakładki, własne okna i przyciski). Wolno
  dodać element do istniejącego systemu gry, jeśli wygląda jak vanilla: nowy wpis lokalizacji w istniejącym
  miejscu UI, nowa pozycja filtra. Komunikat: najpierw istniejący klucz lokalizacji (obecnie reużywany
  `panel_alchemy_exception_already_cooked`). Powód: mod ma nie wyglądać jak mod; granica dotyczy wyglądu,
  nie tego, czy tekst jest nowy.
- **D2. Języki PL + EN** — każdy nowy tekst w grze w obu.
- **D3. Zgodność z innymi modami nie jest wymogiem** — autor gra bez innych modów.
- **D4. README = strona dla gracza** (PL, bez technikaliów, styl Nexusa, lista zmian wersji); technikalia
  w CLAUDE.md i `docs/`.

## Mechanika

- **D5. Nic poza warzeniem nie uzupełnia** mikstur, bomb ani wywarów: medytacja, łóżko, stół, alkohol.
- **D6. Warzenie napełnia do limitu**; uwarzony przedmiot można warzyć ponownie, gdy brakuje choć jednej
  dawki. Powody: dolewka przy 2/3 kosztuje tyle co przy 0/3 — tak samo jak medytacja w vanilli, to nie wada;
  skille limitu zyskują sens (większa pojemność = tańsza dawka); nowy poziom od razu ma max, więc nie ma
  przenoszenia dawek przy ulepszaniu. Odrzucone: 1 warzenie = 1 dawka; uzysk kilku sztuk (nadwyżka ponad limit).
- **D7. Limit = vanilla:** atrybut `ammo` wg poziomu + bonusy vanilli (skill Optymalizacja `S_Alchemy_s08`,
  buff `EET_Mutagen03`, zestaw `EISB_RedWolf_2`, perk `S_Perk_20`); wywary 1, bonusy ich nie dotyczą.
  Powód: spójność z D6 i z opisami skilli w grze. Odrzucone: stałe 3 (psuło opisy skilli); baza 3 + bonusy.
- **D8. Poziomy jak w vanilli:** wyższy poziom usuwa niższy, niższego nie można warzyć, mając wyższy.
- **D9. Zakres: mikstury, bomby, wywary.** Wywary w systemie, bo medytacja nie ma odnawiać niczego
  alchemicznego. Oleje — vanilla: przedmiot oleju się nie zużywa, medytacja go nie dotyczy, więc nie łamie
  spójności. Przedmioty z tagiem `Quest` poza systemem.
- **D10. Alkohol jest wyłącznie składnikiem**, w recepturze stały, ×1. Skutek: zużywa się szybciej niż
  w vanilli ([recipes.md](recipes.md#alkohol)).
- **D11. Odblokowanie i powielenie:** pierwsze warzenie za pełną recepturę, każde kolejne za krótszą.
  1. Sygnałem jest sama lista składników w prawym panelu menu — precedens vanilli: poziomy 1/2/3 mają różne
     listy bez wyjaśnień.
  2. Odblokowanie = posiadanie przedmiotu w ekwipunku, także z 0 dawek. Bez nowych danych w zapisie;
     mikstur i bomb nie da się sprzedać ani wyrzucić, więc odblokowania nie da się stracić (poza wymianą na
     wyższy poziom, który ma własne odblokowanie). Pozyskanie poza warzeniem też odblokowuje.
  3. Odrzucone: znacznik `isNew` na liście — menu alchemii go nie rysuje.
- **D12. Mikstura z 0 dawek zostaje w ekwipunku** (jak w vanilli) — to znacznik odblokowania.
- **D13. Warzenie tylko w menu alchemii.** Odrzucone: medytacja warzy z zapasu składników — ciche zabieranie
  składników jest niejawne i myli.
- **D14. Pozyskanie poza warzeniem = vanilla:** nowy przedmiot z lootu, zakupu, questu czy startu dostaje max,
  posiadany jest odrzucany komunikatem „already cooked”. Powód: w świecie i tak nie ma gotowych mikstur do
  podniesienia (poz. 2/3 na pewno nie ma w lootcie ani u kupców; poz. 1 niesprawdzone w danych). Odrzucone:
  nowy z lootu = 1 dawka, posiadany +1.
- **D15. Blokada warzenia jak w vanilli** (`IsInCombat`), łagodniejsza niż medytacji (`IsThreatened`); nie
  zrównywać — warzyć można przy wrogach w pobliżu, zanim zacznie się walka. Skille limitu nie są psute:
  decydują o liczbie bomb na jedną walkę, a dodatkowe dawki trzeba opłacić składnikami.
- **D16. Nadmiaru ponad limit nie przycinamy przy odczycie** — przy wczytywaniu zapisu bonusy limitu mogą być
  jeszcze nieprzywrócone → trwała utrata dawek. Nadmiar schodzi przy użyciu; warzenie zablokowane do spadku
  poniżej limitu.
- **D17. Stół alchemiczny w Corvo Bianco bez premii:** `ManageSingletonItemsBonus` tylko odmawia, warzenie
  przy stole też bez premii. Powód: vanillowa premia (+1 ponad max) działa przy odnawianiu, czyli dawałaby
  dawkę bez warzenia (D5). Pomysł na inną rolę stołu: [roadmap.md](roadmap.md#odłożone).
- **D18. Dwa poziomy naraz na liście menu zostają:** posiadana niepełna Jaskółka 1 (dolewka) i znana receptura
  Jaskółki 2 (ulepszenie) widoczne obok siebie; w ekwipunku nigdy obie (ulepszenie zużywa poz. 1, a poz. 1 jest
  zablokowany przy posiadanym poz. 2). Odrzucone: ukrywanie niższego poziomu przy znanej wyższej recepturze
  albo gdy wyższy da się uwarzyć.

## Receptury

- **D19. Receptury ręcznie dopracowane w tabeli**, nie liczone regułą w grze. Skrypt tworzy szkic; każdą
  recepturę poprawiamy pod kątem spójności między poziomami rodziny, unikatowości (brak kolizji) i oryginalności
  (sygnaturowy składnik). Do moda trafia generowany `.ws`. Powód: reguła dawała kolizje i odbierała miksturom
  symbolikę ([recipes.md](recipes.md#znane-wady-obecnej-tabeli)). Odrzucone: strojenie reguły progiem
  i dzielnikiem, reguła powszechności, „wyrzuć najdroższy składnik”
  ([archive/recipe-rules.md](archive/recipe-rules.md)).
- **D20. Podmiany składników dozwolone, a nawet zalecane**, jeśli zachowują unikatowość; receptura powielania
  nie musi być podzbiorem pełnej. Odrzucone: dynamiczna podmiana składników wg ekwipunku — mod-smell.
- **D21. Pełna receptura też może się zmienić:** obie receptury projektujemy razem, by powielenie było spójnym
  okrojeniem pełnej. Tabela = pełna + powielenie dla każdego consumable.
- **D28. Receptura powielania nie zawiera przedmiotu niższego poziomu.** Powód: pełna receptura poz. 2/3
  zużywa przedmiot niższego poziomu, a niższego nie wolno warzyć, mając wyższy (D8) — z nim w powieleniu
  ponowne warzenie poz. 2/3 byłoby niemożliwe.
