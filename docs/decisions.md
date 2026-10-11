# Rozstrzygnięcia — ConsumableAlchemy

Rozstrzygnięcia autora z powodem. Odrzucone warianty są tu po to, żeby do nich nie wracać bez nowego
argumentu. Rozstrzygnięcie ma nazwę, nie numer; odwołanie to link do nagłówka. Wymogi ogólne (vanillowość,
PL + EN, zgodność z modami, nic poza warzeniem nie uzupełnia) są zasadami produktu w [README.md](../README.md).
Pytania otwarte: [roadmap.md](roadmap.md#do-decyzji-autora). Mechanizm: [architecture.md](architecture.md),
receptury: [recipes.md](recipes.md).

## Mechanika

### Warzenie napełnia do limitu
Uwarzony przedmiot można warzyć ponownie, gdy brakuje choć jednej dawki. Powody: dolewka przy 2/3 kosztuje
tyle co przy 0/3 — tak samo jak medytacja w vanilli, to nie wada; skille limitu zyskują sens (większa
pojemność = tańsza dawka); nowy poziom od razu ma max, więc nie ma przenoszenia dawek przy ulepszaniu.
Odrzucone: 1 warzenie = 1 dawka; uzysk kilku sztuk (nadwyżka ponad limit).

### Limit jak w vanilli
Atrybut `ammo` wg poziomu + bonusy vanilli (skill Optymalizacja `S_Alchemy_s08`, buff `EET_Mutagen03`, zestaw
`EISB_RedWolf_2`, perk `S_Perk_20`); wywary 1, bonusy ich nie dotyczą. Powód: spójność z
[warzeniem do limitu](#warzenie-napełnia-do-limitu) i z opisami skilli w grze. Odrzucone: stałe 3 (psuło
opisy skilli); baza 3 + bonusy.

### Poziomy jak w vanilli
Wyższy poziom usuwa niższy, niższego nie można warzyć, mając wyższy.

### Zakres systemu
Mikstury, bomby, wywary. Wywary w systemie, bo medytacja nie ma odnawiać niczego alchemicznego. Oleje —
vanilla: przedmiot oleju się nie zużywa, medytacja go nie dotyczy, więc nie łamie spójności. Przedmioty
z tagiem `Quest` poza systemem.

### Alkohol tylko jako składnik
W recepturze stały, ×1. Skutek: zużywa się szybciej niż w vanilli ([recipes.md](recipes.md#alkohol)) —
autor to przyjmuje. Wyzwalacz powrotu: w grze zdobywanie alkoholu staje się trudne albo irytujące. Odrzucone
(do czasu wyzwalacza): powielenie podstawia najtańszy posiadany alkohol, jak medytacja.

### Odblokowanie i powielenie
Pierwsze warzenie za pełną recepturę, każde kolejne za krótszą. Powód: bez tego każde warzenie za pełną
recepturę (części potworów, rzadkie minerały) byłoby kilkukrotnie droższe niż jednorazowe warzenie w vanilli,
a powielenie ma nie boleć.
1. Sygnałem jest sama lista składników w prawym panelu menu — precedens vanilli: poziomy 1/2/3 mają różne
   listy bez wyjaśnień.
2. Odblokowanie = posiadanie przedmiotu, także z 0 dawek (zostaje w ekwipunku, jak w vanilli): bez nowych
   danych w zapisie, a mikstur i bomb nie da się sprzedać ani wyrzucić, więc odblokowania nie da się stracić
   (poza wymianą na wyższy poziom, który ma własne odblokowanie). Pozyskanie poza warzeniem też odblokowuje.
3. Odrzucone: znacznik `isNew` na liście — menu alchemii go nie rysuje.

### Warzenie tylko w menu alchemii
Odrzucone: medytacja warzy z zapasu składników — ciche zabieranie składników jest niejawne i myli.

### Pozyskanie poza warzeniem jak w vanilli
Nowy przedmiot z lootu, zakupu, questu czy startu dostaje max, posiadany jest odrzucany komunikatem „already
cooked”. Powód: w świecie i tak nie ma gotowych mikstur do podniesienia (poz. 2/3 na pewno nie ma w lootcie
ani u kupców; poz. 1 niesprawdzone w danych). Odrzucone: nowy z lootu = 1 dawka, posiadany +1.

### Blokada warzenia w walce
Jak w vanilli (`IsInCombat`), łagodniejsza niż medytacji (`IsThreatened`); nie zrównywać — warzyć można przy
wrogach w pobliżu, zanim zacznie się walka. Skille limitu nie są psute: decydują o liczbie bomb na jedną
walkę, a dodatkowe dawki trzeba opłacić składnikami.

### Nadmiar ponad limit zostaje
Nie przycinamy go przy odczycie — przy wczytywaniu zapisu bonusy limitu mogą być jeszcze nieprzywrócone →
trwała utrata dawek. Nadmiar schodzi przy użyciu; warzenie zablokowane do spadku poniżej limitu.

### Stół w Corvo Bianco bez premii
Consumables nie dostają premii stołu, warzenie przy stole też bez premii; mikstury i bomby spoza systemu
(questowe) dostają ją jak w vanilli, z vanillowymi komunikatami. Powód: vanillowa premia (+1 ponad max)
działa przy odnawianiu, czyli dawałaby dawkę bez warzenia (zasada 1); przedmioty questowe są vanilla
(zasada 4). Odrzucone: stół wyłączony dla wszystkich. Pomysł na inną rolę stołu: [roadmap.md](roadmap.md#odłożone).

### Wywar Wodnej Baby jak w vanilli
Darmowa dawka przy nałożeniu i utrata opłaconej przy wygaśnięciu zostają
([architecture.md](architecture.md#mechanika-vanilli-istotna-dla-moda)). Powód: zasada 4 — mechanika
wywaru to vanilla, mod zmienia tylko źródło dawek.

### Starty dodatków z recepturami
Samodzielny start HoS / B&W daje recepturę każdego startowego consumable bez znanej receptury; bez tego
zestaw startowy byłby jednorazowy. Odrzucone: receptura tylko dla poz. ≥ 2 przy inicjalizacji przedmiotu
(nie pokrywa poz. 1 i wywarów); warzenie bez receptury (niespójność menu i tooltipów).

### Przedmioty specjalne poza systemem
`Pops Antidote` i `ReinaldsPhiltre` zostają vanilla, jak `Snow Ball` / `Village drink`: `Pops Antidote` to
przedmiot zadania q303 bez tagu `Quest` i bez alkoholu w recepturze, `ReinaldsPhiltre` nie ma receptury.
Wyłączenie po nazwie w `CA_IsConsumableItemName`. Feromony i `Killer Whale 1` (zwykłe
mikstury z recepturą z lootu i sklepów) zostają w systemie.

### Tekst przy pełnej kieszeni
Consumable z kompletem dawek przy próbie warzenia dostaje „Masz już wszystkie dawki” / „Already fully
stocked”. Powód: w vanilli ten sam tekst („Już masz ten przedmiot”) znaczy „uwarzone na zawsze”. Status
i filtr „Już wykonane” bez zmian. Tekst daje funkcja wg języka gry (PL, reszta EN), bo nie ma narzędzia do
`.w3strings`. Odrzucone: filtr „Uzupełniono” — wymaga zmian we Flashu.

### Dwa poziomy naraz na liście
Posiadana niepełna Jaskółka 1 (dolewka) i znana receptura Jaskółki 2 (ulepszenie) widoczne obok siebie
w menu; w ekwipunku nigdy obie (ulepszenie zużywa poz. 1, a poz. 1 jest zablokowany przy posiadanym poz. 2).
Odrzucone: ukrywanie niższego poziomu przy znanej wyższej recepturze albo gdy wyższy da się uwarzyć.

## Receptury

### Receptury ręcznie w tabeli
Receptury ręcznie dopracowane w tabeli, nie liczone regułą w grze. Tabela powstała ze szkicu liczonego
z danych vanilli; każdą recepturę poprawiono pod kątem spójności między poziomami rodziny, unikatowości (brak kolizji) i oryginalności
(sygnaturowy składnik). Do moda trafia generowany `.ws`. Powód: reguła dawała kolizje i odbierała miksturom
symbolikę (kolizje i brak sygnatury pokazuje `validate.py`). Odrzucone reguły:
1. Próg ceny bez dzielnika ilości — poz. 3 był pułapką kosztową (zostawał `White Gull 1`), część bomb poz. 3
   tańsza od poz. 1; dzielnik 1 — powielenie bomb poz. 1 = pełna receptura.
2. Reguła powszechności (zostają składniki z ≥ 7 sklepów albo zbierane) — nie tanieją receptury złożone
   wyłącznie z powszechnych składników (Kot, Dimeritium, Biały Szron); w grze wymagałaby stałej listy.
3. „Wyrzuć najdroższy składnik” — zostawia rzadkie składniki, nierówne oszczędności.

### Podmiany składników
Dozwolone, a nawet zalecane, jeśli zachowują unikatowość; receptura powielania nie musi być podzbiorem
pełnej. Odrzucone: dynamiczna podmiana składników wg ekwipunku — mod-smell.

### Pełna receptura też może się zmienić
Obie receptury projektujemy razem, by powielenie było spójnym okrojeniem pełnej. Tabela = pełna + powielenie
dla każdego consumable.

### Części potworów według wysiłku
Część z wysiłkiem 3 z katalogu (`Ghoul blood`, `Drowner brain`, `Drowned dead tongue`, `Nekker heart`,
`Arachas venom`, `Alghoul bone marrow`, mutageny południcy i nocnicy) zostaje w powieleniu jako składnik
wysiłku; wysiłek 4–5 → tematyczny zamiennik ([podmiany](#podmiany-składników)). Powód: pospolita część to
logistyka jak zebranie zioła (punkt odniesienia W1), rzadka byłaby osobnym polowaniem przy każdym powieleniu;
bez części mikstura podstawowa byłaby droższa od zaawansowanej.

### Powielenie bez przedmiotu niższego poziomu
Powód: pełna receptura poz. 2/3 zużywa przedmiot niższego poziomu, a niższego nie wolno warzyć, mając wyższy
([poziomy](#poziomy-jak-w-vanilli)) — z nim w powieleniu ponowne warzenie poz. 2/3 byłoby niemożliwe.

### Wysiłek receptury
Σ (wysiłek składnika − 1) × ilość, obok maksimum. Wysiłek składnika 1–5 liczy skrypt z danych gry
(`ingredients.py`), bez ręcznych wyjątków. Powód: składnik z każdego sklepu nie kosztuje wysiłku niezależnie
od ilości, a każda sztuka części potwora to kolejne zabicie. Odrzucone: suma poziomów bez ilości.

### Składnik sygnaturowy
Unikatowość = powielenie każdej rodziny ma składnik, którego nie ma w powieleniu żadnej innej rodziny tego
rodzaju (alkohol i proszek się nie liczą); identyczny zestaw dwóch rodzin jest błędem. Różnica o jeden
składnik — tylko informacja. Powód: wymóg różnicy > 1 składnika wydłużałby powielenie do alkoholu + 3
składników, a powielenie ma nie boleć.

### Mutageny w wywarach według wysiłku
Jak [części potworów](#części-potworów-według-wysiłku): mutageny południcy i nocnicy (wysiłek 3) zostają,
pozostałe (wysiłek 4–5) → tematyczny zamiennik, który jest [składnikiem sygnaturowym](#składnik-sygnaturowy)
wywaru. Powód: wywar z samego alkoholu i ziół nie ma sygnatury i traci symbolikę, a rzadki mutagen przy
każdym powieleniu to kolejna walka z rzadkim potworem. Odrzucone: mutagen zawsze wypada; mutagen zawsze
zostaje.
