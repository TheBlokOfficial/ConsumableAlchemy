# Archiwum: reguły powielania liczone w grze

Nieobowiązujące. Reguły z czasów, gdy recepturę powielania liczył skrypt w grze; zastąpione ręcznie
dopracowaną tabelą (D19 w [decisions.md](../decisions.md)). Obecna tabela odtwarza regułę v2 z dzielnikiem
([recipes.md](../recipes.md#obecna-tabela)).

## v1

Zostaje alkohol i każdy składnik o cenie bazowej ≤ 16; wypada przedmiot niższego poziomu i wszystko droższe;
ilości bez zmian. Wynik `rule.py 16`: mikstury poz. 1–2 → alkohol + zioła (Jaskółka 1: 60 → 30, Jaskółka 2:
180 → 30); poz. 3 → wypada tylko rzadki minerał (`White Gull 1` zostaje). Odrzucona: poz. 3 był pułapką
kosztową, część bomb poz. 3 tańsza od poz. 1 (Dimeritium 3: 12 vs Dimeritium 1: 50); bez zmian ceny m.in.
Tańcząca Gwiazda 1, Smoczy Sen 1, Kartacz 1/2, Biały Miód 1/2.

## v2 + dzielnik

Opis: [recipes.md](../recipes.md#obecna-tabela). Strojenie miało iść dwiema liczbami (próg, dzielnik).
Dzielnik 1 odrzucony: psuje bomby poz. 1 (powielenie = pełna receptura; Dimeritium 1 = 5× `Saltpetre`, droższe
od poz. 2/3).

## v3: reguła powszechności

W powieleniu zostają tylko składniki powszechne: alkohol, roślina zbierana w świecie albo składnik z ≥ 7 sklepów
(dane: [recipes.md](../recipes.md#dostępność-składników)). Odrzucona: powielenie nie tanieje dla receptur
złożonych wyłącznie z powszechnych składników — Kot 1/2 (152/210), Dimeritium 1/2 (150/123), Biały Szron 1/2,
Srebrny Pył 1/2, Smoczy Sen 2. W grze byłaby stałą listą rzadkich składników (skrypty nie widzą asortymentu
sklepów). Pozostałość: dostępność zamiast ceny (zachowuje `Quicksilver solution`, `Optima mater`,
`Water essence`) może posłużyć jako generator szkicu.

## „Wyrzuć najdroższy składnik”

`compare.py`. Odrzucona: zostawia rzadkie składniki (perła, Nigredo, Rebis, mniejsze mutageny, szpik alghula)
i daje nierówne oszczędności (Dimeritium 3: 272 → 172, wywar 28: 385 → 305).
