# Receptury — ConsumableAlchemy

Dane receptur z gry, narzędzia `tools/recipes/` i obecna tabela. Decyzje: [decisions.md](decisions.md#receptury).
Jak mod czyta tabelę: [architecture.md](architecture.md#receptury--recipesws-i-tabela).

## Narzędzia (`tools/recipes/`, Python)

Szczegóły (formaty, reguły, progi) są w docstringach skryptów; tu tylko do czego służą.
- `bundle.py list|extract <bundle> <wzorzec> [katalog]` — czytnik bundli gry; pliki trafiają do
  `tools\recipes\x\`. `xml.bundle` → `gameplay\items\*.xml` (baza + `items_plus` dla NG+);
  `ep1.bundle` / `bob.bundle` → `dlc\ep1|bob\data\gameplay\items\*.xml`.
- `recipes.py` → `data.json` (przedmioty + receptury).
- `loot.py` — wspólny czytnik tabel lootu z `x/` (sklepy, zioła, potwory, kontenery).
- `ingredients.py` → `ingredient_catalog.json` (commitowany): każdy składnik tabeli z ceną, typem, sklepami,
  światem, potworami i **wysiłkiem 1–5** liczonym wyłącznie regułami skryptu; progi kopiuje do `_meta`.
- `rules.py` — reguły walidatora i raportu (lista `RULES`, wagi `error` / `warn` / `info`) i [wysiłek receptury](decisions.md#wysiłek-receptury).
  `error` blokuje bramkę (w tym kolizja, [składnik sygnaturowy](decisions.md#składnik-sygnaturowy));
  `warn` — do przejrzenia przy zmianie tabeli.
- `validate.py [--errors-only] [--table <plik>]` — uruchamia `rules.py` na tabeli; kod wyjścia 1 tylko przy
  błędach. `tools/check.ps1` uruchamia go z `--errors-only`.
- `report.py [--base <ref>]` → `report.html` (gitignorowany): vanilla, `full` i `copy` obok siebie, koszt,
  wysiłek, wyniki reguł; z `--base` pokazuje też stan tabeli w danym ref-ie git. Wymaga katalogu składników.
- `generate.py [--check]` → waliduje tabelę i generuje `ConsumableAlchemy_recipes_table.ws`; `--check` niczego
  nie zapisuje i kończy się błędem, gdy plik na dysku jest nieaktualny.
- **`recipes_table.json` — tabela receptur, źródło prawdy dla moda** ([receptury ręcznie w tabeli](decisions.md#receptury-ręcznie-w-tabeli)), edytowana ręcznie, commitowana
  (same nazwy przedmiotów i ilości). Klucz = nazwa receptury (`Recipe for Swallow 1`); pola: `item`, `family`,
  `level` (1–3), `kind` (`potion` / `bomb` / `decoction`), `full` i `copy` (listy `[nazwa, ilość]`), `note`.
  Sortowanie: rodzaj → rodzina → poziom. Obejmuje każdą recepturę, której przedmiot jest consumable
  (92: 40 mikstur, 24 bomby, 28 wywarów).
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
- W1 jako punkt odniesienia ([części potworów](decisions.md#części-potworów-według-wysiłku)): receptury na substancje, części potworów z odradzających się potworów były
  tanie i zalegały — barierą była logistyka, nie koszt.

## Obecna tabela

Pełna receptura = vanilla (kolejność składników z XML). Powielenie dopracowane ręcznie według
[rozstrzygnięć](decisions.md#receptury): baza (alkohol ×1; w bombach proszek bazowy `Saltpetre` /
`Stammelfords dust` / `Alchemists powder`) + 1–3 składniki, w tym sygnaturowy wspólny dla poziomów rodziny;
`White Gull 1` → `Alcohest`; mutagen zostaje tylko w wywarach południcy i nocnicy. Uzasadnienie każdej
receptury jest w polu `note`. `validate.py`: 0 błędów i 0 ostrzeżeń. Wyjątki: powielenie Białego Miodu 1 =
pełna receptura (pełna ma tylko dwa składniki); wywar 15 ma jeden składnik poza alkoholem (próg wysiłku).

## Alkohol

Stały z receptury, ×1 ([alkohol tylko jako składnik](decisions.md#alkohol-tylko-jako-składnik)): mod zużywa 1 sztukę na każde warzenie (np. 4 mikstury + 1 wywar = 5), vanilla
1 na całą medytację ([architecture.md](architecture.md#mechanika-vanilli-istotna-dla-moda)). Podaż dobra:
`Dwarven spirit` w 20 sklepach, `Alcohest` w 21.
