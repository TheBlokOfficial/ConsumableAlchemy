# Testy w grze — ConsumableAlchemy

Test robi autor po wdrożeniu (`deploy.ps1`), na **zwykłym zapisie** z poznanymi recepturami (pułapki niżej).
Checklistę bieżącego wycinka aktualizuje gałąź, która zmienia kod; zaliczony punkt, który opisuje trwałe
zachowanie, przechodzi do „Potwierdzone”.

## Test dymny (po każdym wdrożeniu)

- [ ] Gra startuje bez błędów kompilacji moda; zapis się wczytuje.
- [ ] Medytacja nie uzupełnia posiadanej, niepełnej mikstury.
- [ ] Menu alchemii: odblokowana Jaskółka 1 pokazuje recepturę powielania (`Dwarven spirit`, 3× `Celandine`, `Drowner brain`).
- [ ] Uwarzenie niepełnej mikstury daje max.

## Bieżąca checklista: dawki, limity i tabela receptur

Obecny kod, dopracowana tabela receptur, samodzielne starty dodatków i stół w Corvo Bianco.

Receptury:
- [ ] Jaskółka 1 nieodblokowana → pełna receptura (`Dwarven spirit`, 5× `Celandine`, `Drowner brain`); zaraz
  po uwarzeniu prawy panel pokazuje powielenie, bez zamykania menu.
- [ ] Mikstura z 0 dawek → receptura powielania; warzenie zabiera właściwe składniki.
- [ ] Ponowne warzenie poz. 2 i 3 bez przedmiotu niższego poziomu (np. Jaskółka 2: `Alcohest`, 3× `Celandine`,
  2× `Drowner brain`); poz. 3: `Alcohest` zamiast `White Gull 1`.
- [ ] Wywar: medytacja go nie odnawia; po wypiciu można uwarzyć ponownie (alkohol + 1–3 składniki
  z sygnaturą wywaru; mutagen tylko w wywarach południcy i nocnicy);
  przy 1/1 komunikat „Masz już wszystkie dawki” (EN: „Already fully stocked”).
- [ ] Tooltip receptury w ekwipunku i przypięta receptura pokazują tę samą listę co menu.

Dawki i limity:
- [ ] Warzenie przy 0/x i przy części (np. 1/3) daje max.
- [ ] Limity vanilli: Jaskółka 1 x/3, bomby poz. 1 x/2, wywar 1/1 (potwierdza wartości `ammo` z
  [recipes.md](recipes.md#dane-receptur-z-gry)).
- [ ] Optymalizacja (`S_Alchemy_s08`) podnosi limit bomb; warzenie napełnia do nowego limitu.
- [ ] Ulepszenie (np. Jaskółka 2) ma od razu max.
- [ ] Medytacja nie zużywa alkoholu.
- [ ] Zapis z nadmiarem (np. 5/3): pokazuje limit vanilli, nadmiar schodzi przy użyciu, warzenie zablokowane
  do spadku poniżej limitu.

Pozyskanie:
- [ ] Zakup lub loot posiadanej mikstury → vanillowa odmowa „już uwarzono”.
- [ ] Nowy przedmiot z lootu lub sklepu → max.

Degradacja (zasada 5: zapisy po odinstalowaniu zostają sprawne):
- [ ] Po usunięciu moda zapis się wczytuje; mikstura 0/x odnawia się medytacją; bomba ponad max zostaje
  i schodzi przy użyciu.

Samodzielne starty i stół:
- [ ] Nowa gra HoS i B&W: menu alchemii pokazuje receptury startowych przedmiotów (także poz. 1 i wywary);
  da się je uwarzyć ponownie (lista składników krótsza, jak przy powieleniu).
- [ ] Istniejący zapis po starcie dodatku (bez moda przy zapisie): po wczytaniu z modem to samo.
- [ ] Corvo Bianco, stół włączony, medytacja: questowa mikstura lub bomba dostaje +1 ponad max
  (jak w vanilli), consumable nie.

## Potwierdzone w grze

- Podmiana `PopulateData` się kompiluje; mikstura z kompletem dawek pokazuje w prawym panelu i w komunikacie
  „Masz już wszystkie dawki”, przedmiot uwarzony na zawsze w vanilli — „Już masz ten przedmiot”.

- `@addMethod` działa na `CInventoryComponent`; `@wrapMethod` bez klasy na globalnej
  `getAlchemyRecipeFromName` się kompiluje.
- Medytacja nie odnawia mikstur ani bomb (także na starcie HoS: Wzmocniona Jaskółka) i nie pokazuje
  komunikatu o odnowieniu.
- Posiadaną miksturę można uwarzyć ponownie; mikstura z 0 dawek zostaje w ekwipunku.
- Po zdjęciu skilla Optymalizacja vanilla przycina nadmiar bomb.
- Zapis z nadmiarem dawek pokazuje np. `5/3`, nie odnawia się, nadmiar schodzi przy użyciu.

## Pułapki testowe

- **Samodzielny start dodatku (nowa gra z HoS lub B&W):** vanilla czyści receptury, mod dodaje receptury
  startowych consumables; poza nimi gracz zaczyna bez receptur, więc to nie jest stan do ogólnych testów
  alchemii — [architecture.md](architecture.md#samodzielne-starty-dodatków-hos--bw).
- Mod nie pojawia się w zakładce „Mody” w grze — to nie znaczy, że się nie wczytał
  ([powód](decisions.md#mod-poza-listą-modów-w-grze)); znak wczytania to test dymny.
- Wywar Wodnej Baby dodaje i zabiera dawki — vanilla, nie błąd moda; przy teście limitów nie mieć go
  aktywnego ([architecture.md](architecture.md#mechanika-vanilli-istotna-dla-moda)).
