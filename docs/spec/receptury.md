# Spec: szlifowanie receptur — materiał

Materiał wejściowy etapu szlifowania receptur ([roadmap.md](../roadmap.md#następne-kroki), kroki 2–6); nie
jest jeszcze uzgodnioną koncepcją. Po zakończeniu etapu idzie do archiwum. Dane z gry i narzędzia:
[recipes.md](../recipes.md); decyzje D19–D21, D28: [decisions.md](../decisions.md).

## Wady obecnej tabeli

- **Kolizje** (ten sam zbiór składników, 6 par): Kot 1 = Maribor 1 = wywar Mutagen 5; Zamieć 1 = wywar Mutagen 2;
  Zamieć 2 = Jaskółka 2; Dimeritium 1 = Księżycowy Pył (Silver Dust) 1 (sam `Saltpetre`); ok. 40 par różni się
  1 składnikiem (poz. 1 = alkohol lub proszek + 1 zioło).
- **Utrata symboliki:** mikstury poz. 1–2 tracą jedyny unikalny składnik (Czarna Krew — `Ghoul blood`,
  Zamieć — `Golem heart`, Puszczyk — `Arachas venom`, Grom — `Endriag embryo` …); Księżycowy Pył traci
  `Quicksilver solution`, Dimeritium 1 — `Optima mater`. Wywary tracą mutagen. Jaskółka i Biały Miód bez zarzutu.
  Walidator: 46 receptur bez składnika sygnaturowego (D30).
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
- Każda receptura ma sygnaturowy składnik; identyczny zestaw dwóch rodzin jest błędem (D30).

## Dostępność składników

Z `availability.py`. Gra nie daje skryptom dostępu do asortymentu sklepów — dostępność jest tylko kryterium
przy projektowaniu tabeli.
- Wszystko o cenie bazowej ≤ 16 to zioła (14–17 sklepów + krzaki w świecie) i minerały (16–31 sklepów).
  `Buckthorn` nie jest w sklepach, ale rośnie w świecie.
- Rzadkie minerały poz. 3 (`Quebrith`, `Aether`, `Vitriol`, `Rebis`, `Rubedo`, `Vermilion`, `Nigredo`)
  sprzedaje tylko `_EP2_store__Alchemist`.
- Powszechne mimo ceny > 16: `Optima mater` (32 sklepy), `Powdered pearl` (29), `Quicksilver solution` (18),
  `Water essence` (11, zielarze); pół-powszechny `Specter dust` (5 sklepów, głównie z potworów).
- Części potworów i mutageny: 0 sklepów, tylko z potworów i gniazd.

## Części potworów

Dane do D22 ([roadmap.md](../roadmap.md#do-decyzji-autora)).
- **W3:** pospolite — `Ghoul blood` (ghul, zawsze 1), `Drowner brain` (ok. 0,5 na zabicie), `Drowned dead
  tongue` (topielec ok. 0,5, gniazdo zawsze), `Nekker heart` (nekker ok. 0,3, duże i gniazda zawsze), także
  `Arachas venom` i `Alghoul bone marrow` (wysiłek 3 w katalogu); rzadsze (wysiłek 4) — `Endriag heart` /
  `embryo`, `Golem heart`, `Fogling teeth`; esencje południcy i nocnicy. `Specter dust` (wysiłek 2) jest
  w sklepach. Brak tagu rozróżniającego → lista nazw. Wędrowne grupy
  potworów odradzają się po ok. 2–4 dniach gry (poradniki, niesprawdzone w kodzie); nazwane i questowe nie.
- **W1:** receptury na substancje (dowolny składnik z daną substancją), 1 alkohol = 1 mikstura, warzenie
  w medytacji, stosy po 10; części potworów wymagały wpisu w bestiariuszu, a odradzające się potwory dawały
  tanie, zalegające składniki — barierą była logistyka, nie koszt. Punkt odniesienia autora: zdobycie części
  ≈ zebranie zioła.
