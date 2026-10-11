# Architektura — ConsumableAlchemy

Jak mod działa i na czym opiera się w vanilli. Pojęcia: słownik w [README.md](../README.md). Powody:
[decisions.md](decisions.md). Dane receptur: [recipes.md](recipes.md). Adresy vanilli to nazwa funkcji plus
`plik:linia` w skryptach instalacji 5.0.0.1044392 (`<gra>\content\content0\scripts\game\...`).

## Klasyfikacja — `CA_IsConsumableItemName` (common.ws)

Consumable = singleton **i** (bomba (`category == petard`) **lub** tag `Potion` — także wywary z tagiem
`Mutagen`), z wyłączeniem: `Snow Ball`, `Tutorial Bomb`, `Village drink`, `Pops Antidote` (q303), `ReinaldsPhiltre` ([rozstrzygnięcie](decisions.md#przedmioty-specjalne-poza-systemem)), tag `Quest`, tag
`NoAdditionalAmmo` (bomby z farbą `q703_paint_bomb_*` z Toussaint), `TAG_INFINITE_AMMO`.
`CA_IsConsumableItem(id)` (`@addMethod` na `CInventoryComponent`) dodatkowo wymaga, by inwentarz należał
do gracza. Limit jest [vanillowy](decisions.md#limit-jak-w-vanilli): mod nie ma własnej stałej ani nie zmienia `SingletonItemGetMaxAmmo`.

## Punkty zaczepienia

| Mechanika | Vanilla | Mod |
|---|---|---|
| Każde odnawianie (medytacja `MeditationRestoring` `playerWitcher.ws:10249`, łóżko, stół, `RecoverGeralt`, NG+ `:1191`, tutorial) przechodzi przez `SingletonItemRefillAmmo` (`inventoryComponent.ws:3575`) | ustawia max | `@wrapMethod`: zainicjalizowany consumable (`is_initialized != 0`) → nic; reszta (nie-consumables, inicjalizacja nowego przedmiotu) → vanilla |
| Inicjalizacja nowego przedmiotu: `OnItemAdded` (`inventoryComponent.ws:4817`) woła odnawianie, potem ustawia `is_initialized = 1` | max | vanilla (po łóżku/stole w Corvo Bianco vanilla daje max + 1) |
| Limit: `SingletonItemGetMaxAmmo` (`:3779`) | atrybut `ammo` + bonusy | bez zmian |
| Nadmiar ponad limit (stary zapis, wygasły bonus) | przycina tylko przy zmianie skilla/zestawu (`SkillReduceBombAmmoBonus`, `r4Player.ws:11743`) | bez zmian; nie przycinać przy odczycie ([powód](decisions.md#nadmiar-ponad-limit-zostaje)) |
| Alkohol i powiadomienia: `SingletonItemsRefillAmmo` (`:3641`) / `NoAlco`, sterowane prywatnym `HasNotFilledSingletonItem` (`:3712`) | | `@replaceMethod HasNotFilledSingletonItem`: pomija consumables |
| Tutorial „uzupełnij alkoholem”: `SingletonItemRemoveAmmo` (`:3749`) dodaje fakt `tut_alch_refill` | | `@replaceMethod`: nie dla consumables |
| Stół w Corvo Bianco: `ManageSingletonItemsBonus` (`:3832`), wołane z `ApplyAlchemyTableBuff` (`quest_function.ws:7927`) | +1 ponad max | `@replaceMethod`: kopia vanilli z pominięciem consumables — premia +1 tylko dla pozostałych mikstur i bomb (questowych), vanillowe powiadomienia |
| Samodzielne starty: `StandaloneEp1_1` / `StandaloneEp2_1` (`playerWitcher.ws:11428` / `:11930`), `ApplyPatchFixes` (`:738`, wołane z `:367` przy wczytaniu zapisu) | czyszczą receptury, dają zestaw startowy | `@wrapMethod` na trzech: po vanilli `CA_LearnRecipesOfOwnedConsumables` ([sekcja niżej](#samodzielne-starty-dodatków-hos--bw)) |
| Loot i zakup: `GiveItemTo` (`:745`) | posiadany singleton → odmowa „already cooked” | bez zmian ([powód](decisions.md#pozyskanie-poza-warzeniem-jak-w-vanilli)) |
| Czy wolno warzyć: `W3AlchemyManager.CanCookRecipe` (`alchemyManager.ws:141`) | `EAE_CannotCookMore` dla posiadanych | `@replaceMethod`: posiadany consumable zablokowany tylko przy pełnej kieszeni |
| Warzenie: `CookItem` (`alchemyManager.ws:208`) | nowy przedmiot dostaje max, posiadany bez zmian | `@wrapMethod`: po vanilli każdy egzemplarz uwarzonego consumable poniżej limitu → `SingletonItemSetAmmo(max)`; nadmiar ponad max nietknięty |
| Powiadomienie przy próbie warzenia: `CR4AlchemyMenu.CreateItem` (`alchemyMenu.ws:332`) | `panel_alchemy_exception_already_cooked` | `@wrapMethod`: przy pełnej kieszeni consumable własny tekst `CA_FullStockText` ([powód](decisions.md#tekst-przy-pełnej-kieszeni)), bez wołania vanilli. `cantCookReason` pozycji menu (`:505`, wewnątrz `PopulateData`) i HUD przy lootcie (`inventoryComponent.ws:777`) bez zmian |
| Składniki receptury: `GetRecipe`, `GetRecipes`, `getAlchemyRecipeFromName`, `CR4AlchemyMenu.CreateItem` | | sekcja niżej |

## Receptury — recipes.ws i tabela

`CA_GetRecipeIngredients(recipe)` zwraca składniki, które gracz płaci teraz:
`CA_GetTableIngredients(recipe.recipeName, isCopy, out ingredients)` z generowanego
`ConsumableAlchemy_recipes_table.ws`. `isCopy` = przedmiot odblokowany (`CA_IsCopyRecipe`: consumable
i `GetItemQuantityByName > 0`, także 0 dawek) → receptura powielania, inaczej pełna. Receptury spoza tabeli
(oleje, questowe, inne) → vanillowe `requiredIngredients` w obu przypadkach. Kluczem jest nazwa receptury
(`name_name` z XML, np. `Recipe for Swallow 1`).

Łańcuch: `tools/recipes/recipes_table.json` (edytowany ręcznie) → `generate.py` (walidacja + generowanie)
→ `.ws`. Budowa generowanego pliku: dyspozytor `CA_GetTableIngredients` → po jednej funkcji ze `switch` na
`name` na rodzaj (`_Potion` / `_Bomb` / `_Decoction`) → po jednej małej funkcji na recepturę
(`CA_TableRecipe_*`, gałąź powielania / pełna) → `CA_AddTableIngredient`. Małe funkcje, bo kompilator
vanilli nie mieści dużych (`HACK_NO_MEMORY_TO_COMPILE_*` w `gameEffectManager.ws:201`,
`OutOfMemoryHack_*` w `quest_function.ws:7369`); `switch` na `name` jak w vanilli (`temp.ws:9197`,
`definitionsManager.ws:76`).

**Każde miejsce, które czyta składniki receptury, idzie przez `CA_GetRecipeIngredients`** — inaczej
rozbieżność list zdradzi moda:
- `W3AlchemyManager.GetRecipe` (`@replaceMethod`) — używają go `CanCookRecipe`, `CookItem`,
  `GetRequiredIngredients`. Receptury z XML ładuje prywatne `LoadRecipesCustomXMLData` (`alchemyManager.ws:46`).
- `W3AlchemyManager.GetRecipes` (`@wrapMethod`) — lista w menu; menu bierze składniki z
  `m_recipeList[id].requiredIngredients` (`alchemyMenu.ws:605`).
- globalna `getAlchemyRecipeFromName` (`alchemyManager.ws:534`; `@wrapMethod` bez klasy i bez nawiasów)
  — tooltip receptury w ekwipunku (`guiBaseInventoryComponent.ws:776`), przypięta receptura
  (`inventoryMenu.ws:4464`, `guiTooltipComponent.ws:714`).
- `CR4AlchemyMenu.CreateItem` (`@wrapMethod`) — po każdym warzeniu przeładowuje `m_recipeList` i panel
  składników. Vanilla odświeża tylko dla `level > 1` (`alchemyMenu.ws:351`), a po odblokowaniu lista musi
  się przeliczyć także dla poziomu 1.
- `guiTooltipComponent.GetRecipeDataFromXML` (`guiTooltipComponent.ws:~2020`) pominięty: szuka
  `'alchemy_recipies'` (literówka w vanilli), więc zawsze zwraca pusto.

Dwa miejsca czytają pełną recepturę wprost z XML (`alchemy_recipes`), z pominięciem moda. Nie łatane, póki
pełna receptura w tabeli = vanilla; zmiana takiej receptury wymaga zaczepienia:
- tutorial alchemii `AddThunderBoltIngredients` (`quests\tutorialManager\UITutorials\alchemy.ws:195`) daje
  składniki pełnej receptury Pioruna 1 — po zmianie tutorialowego warzenia nie da się dokończyć. Metoda
  stanu (`state`), zaczepienie niesprawdzone.
- stół do rozkładania mutagenów (B&W, `gameplay\interactive\mutagenDismantlingTable.ws:17-60`) podświetla
  składniki pełnej receptury wywarów, których gracz nie ma.

W3 nie ma zamienników składników: `CanCookRecipe` sprawdza po nazwie, a uśpione API kategorii składników
(`GetIngredientCategoryElements`, `commonGame.ws:32-35`) nie ma danych w XML.

## Mechanika vanilli istotna dla moda

- **Widoczność receptur:** `GetRecipes` wymusza `forceAll = true` (`alchemyManager.ws:398`) → menu pokazuje
  wszystkie poznane receptury, także niższego poziomu po uwarzeniu wyższego (blokuje je `CanCookRecipe`).
  Kod filtrujący (`ShouldRemoveRecipe`, ukrywanie posiadanych wywarów i poz. 3) jest martwy.
- **Filtry menu** (Flash): `PopulateData` przekazuje `canCookStatusForFilter` (`alchemyMenu.ws:459/514`);
  `EAE_CannotCookMore` → pozycja ukryta pod filtrem „Już wykonane”. Filtry: „Posiadasz składniki / Brak
  składników / Już wykonane”, tylko przez skrót klawiszowy „Filtry”; „Już wykonane” domyślnie wyłączony.
  Mod zachowuje statusy → przy pełnej kieszeni pozycja chowa się jak w vanilli, poniżej limitu jest widoczna.
  Zmiana statusu zmienia, co menu ukrywa; żeby zmienić tylko tekst pozycji, zmieniaj `cantCookReason`.
- **Teksty powodu odmowy:** `AlchemyExceptionToString` (`alchemyTypes.ws:103`) mapuje status na klucz;
  `EAE_CannotCookMore` → `panel_alchemy_exception_already_cooked` (`:111`). Ten klucz trafia do `cantCookReason`
  pozycji menu (`alchemyMenu.ws:505`), do komunikatu przy próbie warzenia (`alchemyMenu.ws:369`), do HUD
  (`inventoryComponent.ws:777`) i do tooltipu (`guiTooltipComponent.ws:1921`). Etykiety filtrów to klucze
  `gui_panel_filter_has_ingredients / _elements_missing / _already_crafted` przekazane ze skryptu
  (`alchemyMenu.ws:90`), ale same trzy przełączniki i ich logika są we Flashu. Pokrewne klucze vanilli:
  `message_common_alchemy_items_refilled` / `_cannot_refill` (`inventoryComponent.ws:3658/3668`, odnawianie przy
  medytacji). Brzmień PL/EN nie ustalono: `*.w3strings` (nagłówek `RTSW`, wersja 164, szyfrowane) nie dają się
  odczytać prostym skryptem; czytać je trzeba narzędziem do w3strings.
- **Przedmioty `Potion` + `SingletonItem` bez tagu `Quest`** (dane z XML): wszystkie mikstury i wywary z recepturą
  w lootcie/sklepach, plus `Killer Whale 1` i feromony Nekker / Utopiec / Niedźwiedź 1 (receptura 1 poz., zwykłe
  składniki) — w modzie zużywalne. Bez receptury: `Village drink`, `ReinaldsPhiltre` (efekt `EET_ReinaldPhiltre`,
  nazwa „signs_enhancement”, bez referencji w skryptach poza efektem). `Trial Potion Kit` ma tag `Quest`, brak
  `SingletonItem`; jego recepturę vanilla usuwa po zadaniu (`playerWitcher.ws:1152`). Martwy filtr `GetRecipes`
  (`alchemyManager.ws:488`) ukrywał posiadane `Killer Whale 1`, `Trial Potion Kit`, `Pops Antidote`, feromony.
- **Receptury od startu nowej gry** (`playerWitcher.ws:260`): Jaskółka 1, Kot 1, Biały Miód 1, Samum 1,
  Kartacz 1, oleje na upiory i trupojady, Alcohest.
- **Walka:** warzenie zablokowane w walce (`EAE_InCombat`, `alchemyManager.ws:156`, `IsInCombat()`);
  medytacja surowiej (`CanMeditate` / `CanMeditateHere` → `IsThreatened()`, `playerWitcher.ws:10093/10157`).
- **Alkohol w medytacji:** 1 sztuka najtańszego `StrongAlcohol` na całą medytację
  (`GetAlcoholForAlchemicalItemsRefill`, `playerWitcher.ws:5621`).
- **Wywar Wodnej Baby** (`EET_Mutagen03`, `mutagen03.ws`): przy nałożeniu +1 dawka każdej miksturze i bombie
  (także z 0 dawek — darmowa dawka), przy wygaśnięciu −1 (także dawka opłacona składnikami, uwarzona ponad
  limit w trakcie działania).
- **Pełne dawki z pominięciem wrappera odnawiania** (zgodne z [pozyskaniem jak w vanilli](decisions.md#pozyskanie-poza-warzeniem-jak-w-vanilli)): `AddItemQuest`, `AddItemQuestExt` itd.
  (`quest_function.ws:2016/2053/2135/5958/6004`) i przedmioty startowe nowej gry (`r4Player.ws:15482`)
  po `AddAnItem` wołają wprost `SingletonItemSetAmmo(max)`. Nie łatać (zasada 4).

## Samodzielne starty dodatków (HoS / B&W)

`StandaloneEp1_1` (HoS, `playerWitcher.ws:11428`; fakt końcowy `standalone_ep1` `:11916`) i `StandaloneEp2_1`
(B&W, `:11930`; fakt `standalone_ep2` `:12488`) czyszczą receptury (`RemoveAllAlchemyRecipes`, `:11595`)
i dają zestaw startowy (HoS `:11662-11709`, B&W `:12090-12207`): kilka receptur poz. 1 i ok. 20 przedmiotów
bez receptury na swój poziom (poz. 2 przy recepturze poz. 1, poz. 1 i wywary bez receptury). W vanilli
medytacja je odnawia; w modzie są jednorazowe. Receptury poz. 2 da się później kupić (Toussaint
`_EP2_store__Alchemist`, zielarze `Oxenfurt_Herbalist` / `Druid_Herbalist`). Przy każdym wczytaniu zapisu
woła się `ApplyPatchFixes` (`private final`, `playerWitcher.ws:738`) — miejsce na poprawkę dla istniejących
zapisów.

Mod owija `StandaloneEp1_1` / `StandaloneEp2_1` i `ApplyPatchFixes` (ta tylko przy fakcie `standalone_ep1` /
`standalone_ep2`). Po vanilli `CA_LearnRecipesOfOwnedConsumables` (`ConsumableAlchemy_standalone.ws`) daje
każdemu posiadanemu consumable bez znanej receptury recepturę po `cookedItem_name` z `alchemy_recipes`
(`AddAlchemyRecipe(r, true, true)`, `playerWitcher.ws:4851`, idempotentne). Nic w save'ie. Przedmiot, którego
jakakolwiek receptura jest już znana, zostaje bez zmian. Skutki jak przy każdej poznanej recepturze:
statystyki i osiągnięcia warzenia, Nabyta Tolerancja, `SEC_AlchemyRecipe`.

## Degradacja

Mod nie zapisuje w save'ie nic własnego (brak klas ze stanem, `saved`, faktów, tagów) — tylko vanillowe
`ammo_current` / `is_initialized`.
- Usunięcie moda: vanilla przy medytacji uzupełnia tylko, gdy dawki < limit (`inventoryComponent.ws:3599`);
  nadmiar zostaje i schodzi przy użyciu. Sprawdzenie w grze: [testing.md](testing.md).
- Dodanie moda w trakcie gry: posiadane przedmioty są od razu odblokowane (receptura powielania).
