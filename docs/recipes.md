# Receptury i balans — Consumable Alchemy

Dane receptur z gry, narzędzia `tools/recipes/` i kryteria balansu kosztu warzenia. Decyzje: D10, D11,
D19–D21, D28 w [decisions.md](decisions.md). Jak mod czyta tabelę:
[architecture.md](architecture.md#receptury--recipesws-i-tabela). Plan szlifowania:
[roadmap.md](roadmap.md#następne-kroki).

Problem: w vanilli jedno warzenie daje praktycznie nieskończony zapas (odnawiany alkoholem). W modzie każde
warzenie kosztuje składniki, więc bez zmian w recepturach mikstura byłaby kilkukrotnie droższa (części
potworów, rzadkie minerały, mutageny). Rozwiązanie: odblokowanie za pełną recepturę, powielenie za krótszą.

## Narzędzia (`tools/recipes/`, Python)

- `bundle.py list|extract <bundle> <wzorzec> [katalog]` — czytnik bundli `POTATO70` (wpis TOC 0x130 B: nazwa
  0x100, hash 16, offset/0/size/zsize/crc/kompresja; 0 = brak, 1 = zlib). Pliki trafiają do
  `tools\recipes\x\`. `xml.bundle` → `gameplay\items\*.xml` (baza + wersje `items_plus` dla NG+);
  `ep1.bundle` / `bob.bundle` → `dlc\ep1|bob\data\gameplay\items\*.xml`.
- `recipes.py` → `data.json` (przedmioty + receptury).
- `table.py` → tabela receptur mikstur i bomb z cenami.
- `availability.py` — bez argumentu: źródła składników (sklepy, świat); `copies`: koszt powielenia wg dostępności.
- `rule.py [próg] [dzielnik]` → reguła powielania, z której powstała obecna tabela; używa jej `draft.py`.
- `compare.py` → porównanie reguły z wariantem „wyrzuć najdroższy składnik” (odrzucony, D19).
- **`recipes_table.json` — tabela receptur, źródło prawdy dla moda** (D19), edytowana ręcznie, commitowana
  (same nazwy przedmiotów i ilości). Klucz = nazwa receptury (`Recipe for Swallow 1`); pola: `item`, `family`,
  `level` (1–3), `kind` (`potion` / `bomb` / `decoction`), `full` i `copy` (listy `[nazwa, ilość]`), `note`.
  Sortowanie: rodzaj → rodzina → poziom. Obejmuje każdą recepturę, której przedmiot jest consumable
  (93: 41 mikstur, 24 bomby, 28 wywarów).
- `draft.py` → szkic tabeli z danych vanilli: `full` = receptura z XML, `copy` = `rule.py 16 2`. Bez `--force`
  nie nadpisuje istniejącej tabeli; `--diff` porównuje tabelę ze świeżym szkicem (pokazuje ręczne zmiany).
- `generate.py` → waliduje tabelę (pola, ilości > 0, niepuste listy, brak duplikatu składnika i klucza,
  bezpieczne nazwy) i generuje `src/.../consumableAlchemy_recipes_table.ws`.
- `x/` i `data.json` są w `.gitignore` (dane CDPR) — odtwarzać przez `bundle.py extract` + `recipes.py`.

## Dane receptur z gry

- Receptury: `def_item_alchemy_recipes_potions.xml` / `_petards.xml` / `_mutagens.xml`
  (+ `dlc\ep1|bob\...potions.xml`: Killer Whale, feromony), węzeł `<custom><alchemy_recipes>`.
- Mikstury i bomby nie używają mutagenów (to wywary). Wywar = `Dwarven spirit` + 1 mutagen potwora + 1–2 zioła.
- Poziom 1 mikstury: `Dwarven spirit`; poz. 2: `Alcohest` + **przedmiot poz. 1**; poz. 3: `White Gull 1` +
  **przedmiot poz. 2**. Bomby analogicznie, bez alkoholu.
- Drogie składniki: części potworów (30–60), `Optima mater` 50, `Powdered pearl` 50 (składnik rzemieślniczy),
  na poz. 3 rzadkie minerały (`Rebis`, `Vitriol`, `Quebrith`, `Aether`, `Nigredo`, `Rubedo`, `Vermilion`,
  `Alchemists powder`: 18–35) i `White Gull 1` (cena 100; da się go uwarzyć, ok. 110 w składnikach).
- Tagi: alkohole `StrongAlcohol`; zioła `HerbGameplay` (nie wszystkie — `Buckthorn` bez tagu); części
  potworów i minerały bez rozróżniającego tagu (oba `AlchemyIngredient, mod_alchemy`); mutageny
  `MutagenIngredient`.
- Ceny w XML są bazowe — w sklepie wielokrotnie wyższe (np. `Optima mater` 50 w XML, 124 u zielarza); do
  porównań względnych wystarczą.
- Limity `ammo` (`def_item_alchemy_potion.xml` / `_petards.xml` / `_mutagens.xml`; NG+ `items_plus` bez
  `ammo`): mikstury 3/4/5 — wyjątki: Zamieć (Blizzard) 2/3/4, Biały Miód 1/2/5, Odwar Raffarda 2/2/3, Orka 3,
  feromony 2; bomby 2/3/4; wywary 1 (`CommonMutagenAbility`). Abilities poz. 2/3 zagnieżdżają się
  cyklicznie, więc wartości potwierdza test w grze ([testing.md](testing.md)).
- Mikstur poz. 2/3 nie ma w tabelach lootu ani u kupców (tylko w zestawach samodzielnych startów dodatków).

## Dostępność składników

Z `availability.py`:
- Wszystko o cenie bazowej ≤ 16 to zioła (14–17 sklepów + krzaki w świecie) i minerały (16–31 sklepów).
  `Buckthorn` nie jest w sklepach, ale rośnie w świecie.
- Rzadkie minerały poz. 3 (`Quebrith` 18, `Aether`, `Vitriol`, `Rebis`, `Rubedo`, `Vermilion`, `Nigredo`)
  sprzedaje tylko 1 sklep (`_EP2_store__Alchemist`).
- Powszechne mimo ceny > 16: `Optima mater` (32 sklepy), `Powdered pearl` (29), `Quicksilver solution` (18),
  `Water essence` (11, zielarze); pół-powszechny `Specter dust` (5 sklepów, głównie z potworów).
- Części potworów i mutageny: 0 sklepów, tylko z potworów i gniazd.
- Gra nie daje skryptom dostępu do asortymentu sklepów — dostępność może być tylko kryterium przy
  projektowaniu tabeli.

## Obecna tabela

Pełna receptura = vanilla (kolejność składników z XML). Powielenie = reguła z `rule.py 16 2`: zostaje baza
(alkohol `StrongAlcohol`; w bombach proszek bazowy `Saltpetre` / `Stammelfords dust` / `Alchemists powder`)
i składniki o cenie ≤ 16; wypada przedmiot niższego poziomu (D28), części potworów, mutageny, rzadkie
minerały, perła; `White Gull 1` → `Alcohest` (inaczej poz. 3 byłby pułapką kosztową); ilości / 2 w górę,
alkohol zawsze 1. Koszt powielenia (ceny bazowe): poz. 1 ok. 30, poz. 2 ok. 30, poz. 3 ok. 35–65, wywary
ok. 25. Przykład: Jaskółka 1 — pełna `Dwarven spirit`, 5× `Celandine`, `Drowner brain`; powielenie
`Dwarven spirit`, 3× `Celandine`.

## Znane wady obecnej tabeli

- **Kolizje** (ten sam zbiór składników): Kot 1 = Maribor 1 = wywar Mutagen 5; Zamieć 1 = wywar Mutagen 2;
  Zamieć 2 = Jaskółka 2; Dimeritium 1 = Księżycowy Pył (Silver Dust) 1 (sam `Saltpetre`); ok. 40 par różni się
  1 składnikiem (poz. 1 = alkohol lub proszek + 1 zioło).
- **Utrata symboliki:** mikstury poz. 1–2 tracą jedyny unikalny składnik (Czarna Krew — `Ghoul blood`,
  Zamieć — `Golem heart`, Puszczyk — `Arachas venom`, Grom — `Endriag embryo` …); Księżycowy Pył traci
  `Quicksilver solution` (18 sklepów), Dimeritium 1 — `Optima mater` (32 sklepy). Wywary tracą mutagen.
  Jaskółka i Biały Miód bez zarzutu.
- **Puste lub dziwne:** Mutagen 28 = sam alkohol; Biały Miód 1 i Feromon Niedźwiedzia: powielenie = pełna
  receptura. Poz. 2 tańszy od poz. 1 w 11 rodzinach (`Alcohest` 10 < `Dwarven spirit` 20) — nieszkodliwe.

## Kryteria balansu

- **Odwrócenie trudności:** mikstura z pospolitą częścią potwora (Jaskółka — mózg topielca) byłaby trudniejsza
  w powieleniu niż zaawansowana, której rzadka część wypada i zostają same zioła. Dlatego każda receptura
  powielania ma **składnik wysiłku** dobrany do rangi mikstury: rzadka część potwora podmieniona na osiągalny,
  tematycznie bliski zamiennik (np. esencje upiorów → `Specter dust`; drogie minerały ze sklepów `Optima mater`
  / `Quicksilver solution` / `Powdered pearl`; części średnio pospolitych potworów).
- Mikstury podstawowe nie mogą być droższe w powieleniu od zaawansowanych — walidator ma pokazywać poziom
  wysiłku.
- Każda receptura ma sygnaturowy składnik i różni się od innych o więcej niż 1 składnik (D19).

## Części potworów

Dane do D22 ([roadmap.md](roadmap.md#do-decyzji-autora)).
- **W3:** pospolite — `Ghoul blood` (ghul, zawsze 1), `Drowner brain` (ok. 0,5 na zabicie), `Drowned dead
  tongue` (topielec ok. 0,5, gniazdo zawsze), `Nekker heart` (nekker ok. 0,3, duże i gniazda zawsze); średnie —
  `Endriag heart` / `embryo`; rzadkie (bez sensu w powieleniu) — esencje południcy i nocnicy, `Golem heart`,
  `Fogling teeth`, `Arachas venom`, `Specter dust`. Brak tagu rozróżniającego → lista nazw. Wędrowne grupy
  potworów odradzają się po ok. 2–4 dniach gry (źródło: poradniki, niesprawdzone w kodzie); nazwane i questowe nie.
- **W1:** receptury na substancje (dowolny składnik z daną substancją, z ziół lub potworów), 1 alkohol =
  1 mikstura, warzenie tylko w medytacji, limit tylko stosami po 10; części potworów wymagały wpisu
  w bestiariuszu; potwory (utopce, ghule, barghesty) odradzały się → składniki tanie i zalegające, barierą była
  logistyka, nie koszt. Punkt odniesienia autora: zdobycie części ≈ zebranie zioła.

## Alkohol

Stały z receptury, ×1 (D10). Vanilla zużywa 1 sztukę najtańszego `StrongAlcohol` na całą medytację
(w praktyce `Mahakam Spirit` 8 / `Alcohest` 10); mod — 1 na każde warzenie (np. 4 mikstury + 1 wywar = 5).
Podaż dobra: `Dwarven spirit` w 20 sklepach, `Alcohest` w 21.
