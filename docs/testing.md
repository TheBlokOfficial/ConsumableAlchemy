# Testy w grze — Consumable Alchemy

Test robi autor po wdrożeniu (`deploy.ps1`), na **zwykłym zapisie** z poznanymi recepturami — nie na
samodzielnym starcie dodatku (pułapki niżej). Kompilacja: błędy moda pokazuje okno przy starcie gry;
ostrzeżenia `[content0] ... not marked as abstract` / `has no autostate` są z vanilli. Checklistę bieżącego
wycinka aktualizuje gałąź, która zmienia kod; zaliczony punkt, który opisuje trwałe zachowanie, przechodzi
do „Potwierdzone”.

## Test dymny (po każdym wdrożeniu)

- [ ] Gra startuje bez błędów kompilacji moda; zapis się wczytuje.
- [ ] Medytacja nie uzupełnia posiadanej, niepełnej mikstury.
- [ ] Menu alchemii: odblokowana Jaskółka 1 pokazuje recepturę powielania (`Dwarven spirit`, 3× `Celandine`).
- [ ] Uwarzenie niepełnej mikstury daje max.

## Bieżąca checklista: dawki, limity i tabela receptur

Kod v0.4 i tabela receptur (tabela odtwarza poprzednią regułę 1:1, rozgrywka bez zmian).

Receptury:
- [ ] Jaskółka 1 nieodblokowana → pełna receptura (`Dwarven spirit`, 5× `Celandine`, `Drowner brain`); zaraz
  po uwarzeniu prawy panel pokazuje powielenie, bez zamykania menu.
- [ ] Mikstura z 0 dawek → receptura powielania; warzenie zabiera właściwe składniki.
- [ ] Ponowne warzenie poz. 2 i 3 bez przedmiotu niższego poziomu (np. Jaskółka 2: `Alcohest`, 3× `Celandine`,
  2× `White myrtle`); poz. 3: `Alcohest` zamiast `White Gull 1`.
- [ ] Wywar: medytacja go nie odnawia; po wypiciu można uwarzyć ponownie (alkohol + zioła, bez mutagenu);
  przy 1/1 komunikat „Już masz ten przedmiot”.
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

Degradacja (README obiecuje, że zapisy po odinstalowaniu zostają sprawne):
- [ ] Po usunięciu moda zapis się wczytuje; mikstura 0/x odnawia się medytacją; bomba ponad max zostaje
  i schodzi przy użyciu.

## Potwierdzone w grze

- Adnotacje działają na metodach `private`/`final`; `@addMethod` działa na `CInventoryComponent`;
  `@wrapMethod` bez klasy na globalnej `getAlchemyRecipeFromName` się kompiluje.
- Kod v0.4 się kompiluje i wczytuje.
- Medytacja nie odnawia mikstur ani bomb (także na starcie HoS: Wzmocniona Jaskółka) i nie pokazuje
  komunikatu o odnowieniu.
- Posiadaną miksturę można uwarzyć ponownie; mikstura z 0 dawek zostaje w ekwipunku.
- Po zdjęciu skilla Optymalizacja vanilla przycina nadmiar bomb.
- Zapis z nadmiarem dawek pokazuje np. `5/3`, nie odnawia się, nadmiar schodzi przy użyciu.

## Pułapki testowe

- **Samodzielny start dodatku (nowa gra z HoS lub B&W) nie nadaje się do testów alchemii.** Czyści receptury
  i daje przedmioty bez receptury na swój poziom; poziomu 1 nie można warzyć, bo posiadany jest wyższy (tak
  samo w vanilli) — [architecture.md](architecture.md#samodzielne-starty-dodatków-hos--bw).
- Mod nie pojawia się na liście modów w menu gry — to nie znaczy, że się nie wczytał.
- Wywar Wodnej Baby dodaje i zabiera dawki — przy teście limitów nie mieć go aktywnego
  ([architecture.md](architecture.md#mechanika-vanilli-istotna-dla-moda)).
