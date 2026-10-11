# Rozstrzygnięcia — ConsumableAlchemy

Rozstrzygnięcia autora z powodem. Odrzucone warianty są tu po to, żeby do nich nie wracać bez nowego
argumentu. Numer nie zmienia się i nie wraca. Wymogi ogólne (vanillowość, PL + EN, zgodność z modami, nic
poza warzeniem nie uzupełnia) są zasadami produktu w [README.md](../README.md) — stąd brak D1–D5; D12
włączone do D11, D24, D25 wycofane. Pytania otwarte: [roadmap.md](roadmap.md#do-decyzji-autora). Mechanizm:
[architecture.md](architecture.md), receptury: [recipes.md](recipes.md).

## Mechanika

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
- **D11. Odblokowanie i powielenie:** pierwsze warzenie za pełną recepturę, każde kolejne za krótszą. Powód:
  bez tego każde warzenie za pełną recepturę (części potworów, rzadkie minerały) byłoby kilkukrotnie droższe
  niż jednorazowe warzenie w vanilli, a powielenie ma nie boleć.
  1. Sygnałem jest sama lista składników w prawym panelu menu — precedens vanilli: poziomy 1/2/3 mają różne
     listy bez wyjaśnień.
  2. Odblokowanie = posiadanie przedmiotu, także z 0 dawek (zostaje w ekwipunku, jak w vanilli): bez nowych
     danych w zapisie, a mikstur i bomb nie
     da się sprzedać ani wyrzucić, więc odblokowania nie da się stracić (poza wymianą na wyższy poziom, który
     ma własne odblokowanie). Pozyskanie poza warzeniem też odblokowuje.
  3. Odrzucone: znacznik `isNew` na liście — menu alchemii go nie rysuje.
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
  dawkę bez warzenia (zasada 1). Pomysł na inną rolę stołu: [roadmap.md](roadmap.md#odłożone).
- **D27. `Pops Antidote` poza systemem** (vanilla), jak `Snow Ball` / `Village drink`: przedmiot zadania q303
  bez tagu `Quest` i bez alkoholu w recepturze. Wyłączenie po nazwie w `CA_IsConsumableItemName` i w `draft.py`.
- **D18. Dwa poziomy naraz na liście menu zostają:** posiadana niepełna Jaskółka 1 (dolewka) i znana receptura
  Jaskółki 2 (ulepszenie) widoczne obok siebie; w ekwipunku nigdy obie (ulepszenie zużywa poz. 1, a poz. 1 jest
  zablokowany przy posiadanym poz. 2). Odrzucone: ukrywanie niższego poziomu przy znanej wyższej recepturze
  albo gdy wyższy da się uwarzyć.

## Receptury

- **D19. Receptury ręcznie dopracowane w tabeli**, nie liczone regułą w grze. Skrypt tworzy szkic; każdą
  recepturę poprawiamy pod kątem spójności między poziomami rodziny, unikatowości (brak kolizji) i oryginalności
  (sygnaturowy składnik). Do moda trafia generowany `.ws`. Powód: reguła dawała kolizje i odbierała miksturom
  symbolikę (kolizje i brak sygnatury pokazuje `validate.py`). Odrzucone reguły:
  1. Próg ceny bez dzielnika ilości — poz. 3 był pułapką kosztową (zostawał `White Gull 1`), część bomb poz. 3
     tańsza od poz. 1; dzielnik 1 — powielenie bomb poz. 1 = pełna receptura.
  2. Reguła powszechności (zostają składniki z ≥ 7 sklepów albo zbierane) — nie tanieją receptury złożone
     wyłącznie z powszechnych składników (Kot, Dimeritium, Biały Szron); w grze wymagałaby stałej listy.
  3. „Wyrzuć najdroższy składnik” (`compare.py`) — zostawia rzadkie składniki, nierówne oszczędności.
- **D20. Podmiany składników dozwolone, a nawet zalecane**, jeśli zachowują unikatowość; receptura powielania
  nie musi być podzbiorem pełnej. Odrzucone: dynamiczna podmiana składników wg ekwipunku — mod-smell.
- **D21. Pełna receptura też może się zmienić:** obie receptury projektujemy razem, by powielenie było spójnym
  okrojeniem pełnej. Tabela = pełna + powielenie dla każdego consumable.
- **D22. Części potworów w powieleniu według wysiłku z katalogu:** część z wysiłkiem 3 (`Ghoul blood`,
  `Drowner brain`, `Drowned dead tongue`, `Nekker heart`, `Arachas venom`, `Alghoul bone marrow`, mutageny
  południcy i nocnicy) zostaje jako składnik wysiłku; wysiłek 4–5 → tematyczny zamiennik (D20). Powód:
  pospolita część to logistyka jak zebranie zioła (punkt odniesienia W1), rzadka byłaby osobnym polowaniem
  przy każdym powieleniu; bez części mikstura podstawowa byłaby droższa od zaawansowanej.
- **D28. Receptura powielania nie zawiera przedmiotu niższego poziomu.** Powód: pełna receptura poz. 2/3
  zużywa przedmiot niższego poziomu, a niższego nie wolno warzyć, mając wyższy (D8) — z nim w powieleniu
  ponowne warzenie poz. 2/3 byłoby niemożliwe.
- **D29. Wysiłek receptury = Σ (wysiłek składnika − 1) × ilość**, obok maksimum. Wysiłek składnika 1–5 liczy
  skrypt z danych gry (`ingredients.py`), bez ręcznych wyjątków. Powód: składnik z każdego sklepu nie kosztuje
  wysiłku niezależnie od ilości, a każda sztuka części potwora to kolejne zabicie. Odrzucone: suma poziomów bez
  ilości.
- **D30. Unikatowość = składnik sygnaturowy:** powielenie każdej rodziny ma składnik, którego nie ma
  w powieleniu żadnej innej rodziny tego rodzaju (alkohol i proszek się nie liczą); identyczny zestaw dwóch
  rodzin jest błędem. Różnica o jeden składnik — tylko informacja. Powód: wymóg różnicy > 1 składnika
  wydłużałby powielenie do alkoholu + 3 składników, a powielenie ma nie boleć.
- **D31. Mutagen w powieleniu wywaru według D22:** mutageny południcy i nocnicy (wysiłek 3) zostają, pozostałe
  (wysiłek 4–5) → tematyczny zamiennik, który jest składnikiem sygnaturowym wywaru (D30). Powód: wywar z samego
  alkoholu i ziół nie ma sygnatury i traci symbolikę, a rzadki mutagen przy każdym powieleniu to kolejna walka
  z rzadkim potworem. Odrzucone: mutagen zawsze wypada; mutagen zawsze zostaje.
