# Receptury — Consumable Alchemy

Dane receptur z gry, narzędzia `tools/recipes/` i obecna tabela. Decyzje: D10, D11, D19–D21, D28
w [decisions.md](decisions.md). Jak mod czyta tabelę: [architecture.md](architecture.md#receptury--recipesws-i-tabela).
Materiał do szlifowania receptur (dostępność składników, wady tabeli, kryteria balansu, części potworów):
[spec/receptury.md](spec/receptury.md).

## Narzędzia (`tools/recipes/`, Python)

- `bundle.py list|extract <bundle> <wzorzec> [katalog]` — czytnik bundli `POTATO70` (wpis TOC 0x130 B: nazwa
  0x100, hash 16, offset/0/size/zsize/crc/kompresja; 0 = brak, 1 = zlib). Pliki trafiają do
  `tools\recipes\x\`. `xml.bundle` → `gameplay\items\*.xml` (baza + wersje `items_plus` dla NG+);
  `ep1.bundle` / `bob.bundle` → `dlc\ep1|bob\data\gameplay\items\*.xml`.
- `recipes.py` → `data.json` (przedmioty + receptury).
- `table.py` → tabela receptur mikstur i bomb z cenami.
- `availability.py` — bez argumentu: źródła składników (sklepy, świat); `copies`: koszt powielenia wg dostępności.
- `loot.py` — wspólny czytnik tabel lootu z `x/` (sklepy, zioła, potwory, kontenery; region = `base` / `ep1` / `bob`).
- `ingredients.py` → `ingredient_catalog.json` (commitowany): każdy składnik z list `full` / `copy` tabeli
  (poza przedmiotami niższego poziomu, wymienionymi w `_meta`) z ceną, typem, sklepami (liczba, regiony),
  światem (krzaki, kontenery), potworami (tabela lootu, szansa, ilość) i **poziomem wysiłku 1–5**. Wysiłek liczą
  wyłącznie reguły w skrypcie (bez ręcznych wyjątków, najłatwiejsze źródło); progi i uzasadnienia są stałymi
  w skrypcie i kopią w `_meta`. Respawn nie jest modelowany. Deterministyczny: drugie uruchomienie nie zmienia pliku.
- `report.py [--base <ref>]` → `report.html` (gitignorowany): raport HTML do porównania receptur — vanilla, `full`
  i `copy` z tabeli (różnice względem vanilli podświetlone), koszt, wysiłek (suma i maksimum), flagi. Z `--base`
  pod zmienionymi wierszami pokazuje wersję z tabeli w danym ref-ie git. Wymaga `ingredient_catalog.json`.
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
  bezpieczne nazwy) i generuje `src/.../consumableAlchemy_recipes_table.ws`. `--check` niczego nie zapisuje:
  kończy się błędem, gdy plik na dysku różni się od wygenerowanego (końce linii CRLF/LF są pomijane).
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

## Obecna tabela

Pełna receptura = vanilla (kolejność składników z XML). Powielenie = reguła z `rule.py 16 2`: zostaje baza
(alkohol `StrongAlcohol`; w bombach proszek bazowy `Saltpetre` / `Stammelfords dust` / `Alchemists powder`)
i składniki o cenie ≤ 16; wypada przedmiot niższego poziomu (D28), części potworów, mutageny, rzadkie
minerały, perła; `White Gull 1` → `Alcohest` (inaczej poz. 3 byłby pułapką kosztową); ilości / 2 w górę,
alkohol zawsze 1. Koszt powielenia (ceny bazowe): poz. 1 ok. 30, poz. 2 ok. 30, poz. 3 ok. 35–65, wywary
ok. 25. Przykład: Jaskółka 1 — pełna `Dwarven spirit`, 5× `Celandine`, `Drowner brain`; powielenie
`Dwarven spirit`, 3× `Celandine`.

## Alkohol

Stały z receptury, ×1 (D10): mod zużywa 1 sztukę na każde warzenie (np. 4 mikstury + 1 wywar = 5), vanilla
1 na całą medytację ([architecture.md](architecture.md#mechanika-vanilli-istotna-dla-moda)). Podaż dobra:
`Dwarven spirit` w 20 sklepach, `Alcohest` w 21.
