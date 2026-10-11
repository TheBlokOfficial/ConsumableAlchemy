# ConsumableAlchemy — współpraca

Jak pracujemy nad projektem. Czym jest projekt (słownik, zasady produktu, środowisko, konwencje, pułapki
kompilatora): @README.md. Stan prac i następny krok: [docs/roadmap.md](docs/roadmap.md).

## Role

- **Autor** (właściciel projektu) **mówi, co ma powstać, i sprawdza wynik w grze.** Pytaj go wyłącznie
  o decyzje projektowe: mechanika, balans, co widzi gracz. Implementację wybierasz sam i krótko raportujesz.
- **Architekt** (główna sesja) rozmawia z autorem, czyta kod potrzebny do decyzji i zlecenia, przegląda
  diffy, scala i wdraża. Drobne, lokalne zmiany (dokumenty, kilka linii kodu) robi sam. Długich plików nie
  czyta w całości (skrypty vanilli, XML-e gry, generowana tabela): Grep z wąskim wzorcem albo agent Explore,
  który zwraca wniosek z `plik:linia`. Autorowi pokazuje wynik, który sam by przyjął.
- **Wykonawca** (Agent `wykonawca`, deklaracja w `.claude/agents/wykonawca.md`: sonnet, w tle, własny
  worktree; zasady pracy i format raportu są tam, zlecenie ich nie powtarza) dostaje
  zamkniętą część pracy. Zlecenie z adresami: cel, nazwa gałęzi, pliki i miejsca w nich (także `plik:linia`
  w vanilli), znane fakty i pułapki, kryteria odbioru, czego nie robić, punkt zatrzymania.
  Przed zleceniem commit: worktree powstaje z bieżącego HEAD (`worktree.baseRef` w `.claude/settings.json`),
  agent sam nadaje gałęzi nazwę ze zlecenia. Opus (`model: "opus"`) tylko do zadania bez gotowego
  projektu albo szukania nieznanej przyczyny. Niezależne obszary — równolegle.
- **Research** (kod vanilli, dane z bundli) zlecasz tak samo, z poleceniem zapisu wyników do pliku
  w trakcie pracy — przerwany agent nie może zabrać wyników ze sobą. Wniosek trafia do właściwego
  dokumentu, zanim sesja się skończy.

## Przebieg pracy

- **Wycinek** — zmiana widoczna w grze albo zamknięty etap narzędzi — to jednostka planu i scalenia; sesja
  może mieć kilka. Plan od razu, bez pytania, czy go przygotować: 5–10 linii — co autor zobaczy w grze,
  zakres zmian, pytania — i czekasz na zielone światło. Szczegóły wykonania idą do zlecenia, nie do autora.
  To, co zobaczy gracz (receptury, teksty komunikatów), uzgadniasz z autorem na piśmie, w tabeli albo
  z brzmieniem PL/EN, zanim powstanie kod.
- **Kolejna runda:** pracę przyjętą po przeglądzie scalasz; drobne poprawki robisz sam w worktree wykonawcy
  (ścieżki bezwzględne i `git -C`, bez `cd` — sesja przeniosłaby się do worktree), dłuższą listę dostaje
  nowy wykonawca ze ścieżkami i hashami. Wykonawcy z dużym kontekstem nie wznawiaj — każdy jego krok
  wysyła cały dotychczasowy kontekst.
- **Test w grze:** architekt uruchamia `deploy.ps1` — z worktree, żeby sprawdzić gałąź przed scaleniem
  (skrypt wgrywa `src/` z własnego katalogu), albo z głównego katalogu po scaleniu. Autor testuje według
  [docs/testing.md](docs/testing.md); błędy kompilacji przepisuje z okna gry.
- **Uwagi autora** po teście poprawiasz od razu, gdy to błąd; szlif (działa, ale mogłoby być lepiej) idzie
  jednym zdaniem do sekcji „Szlif” w roadmapie (utwórz ją, gdy jej nie ma).
- **Dokumenty przy pracy:** roadmapę i rozstrzygnięcia aktualizujesz raz na wycinek, przy scaleniu, jednym
  commitem; `docs/architecture.md` i checklistę w `docs/testing.md` — w gałęzi, która zmienia kod.
- **Git:** każdy wykonawca pracuje we własnej gałęzi i worktree; główny katalog stoi zawsze na `main`.
  Scalenie do `main`: zmiany samych narzędzi i dokumentów — po przeglądzie i zielonej bramce, bez pytania;
  zmiany kodu moda — po potwierdzeniu autora (co najmniej: kompiluje się w grze). Potem usunięcie worktree
  i gałęzi. **Push tylko na wyraźne polecenie autora** — repo jest publiczne
  (https://github.com/TheBlokOfficial/ConsumableAlchemy), wszystko, co commitujesz, jest jawne. Commity
  małe i logiczne, po angielsku. Autor commitów: `TheBlokOfficial <tomasznosal.mail@proton.me>` (lokalny
  config repo, wspólny dla worktree).
- **Ustawienia sesji** (`.claude/settings.json`): worktree z HEAD, wyłączone zbędne narzędzia, bez auto-memory.

## Komunikacja

Długość odpowiedzi zależy od sytuacji, nie od tego, ile się wydarzyło:
- **pytanie autora** → odpowiedź od pierwszego zdania, tak długa, jak wymaga pytanie;
- **zielone światło, zlecenie** → jedno zdanie, bez powtarzania planu;
- **wrócił jeden z kilku agentów, autor zatrzymał agenta** → bez wiadomości; jeden raport, gdy wrócą wszyscy;
- **raport po pracy** → wyniki, odstępstwa od planu, decyzje do podjęcia. Bez powtarzania planu i tego, co już
  padło. Stanu domyślnego nie potwierdzasz (bez pusha, bramka zielona, diff przejrzany) — piszesz tylko
  o odstępstwie;
- **pytania do autora** → numerowane, każde z rekomendacją (albo wprost: „bez rekomendacji”), tak żeby dało
  się odpowiedzieć „1 tak, 2 tak”. Tylko to, co blokuje albo należy do autora;
- **koniec sesji** → tylko to, czego nie było w raportach, 2–4 rzeczy do sprawdzenia w grze (gdzie pójść, co
  uwarzyć, na co patrzeć) i następny krok. Prostym językiem, bez nazw funkcji. Na „bez odbioru” — jedna linia.

## Dokumenty

| Plik | Co zawiera | Zalecana długość |
|---|---|---|
| `CLAUDE.md` | współpraca: role, przebieg pracy, komunikacja, zasady dokumentów | ok. 90 linii |
| `README.md` | projekt: słownik, zasady produktu, środowisko, struktura, konwencje, pułapki kompilatora | ok. 100 linii |
| `docs/architecture.md` | jak mod działa: punkty zaczepienia, mechanika vanilli, degradacja | ok. 100 linii |
| `docs/decisions.md` | rozstrzygnięcia z powodem, zwłaszcza odrzucone kierunki | wpis ok. 6 linii |
| `docs/recipes.md` | dane receptur z gry, narzędzia `tools/recipes/`, obecna tabela | ok. 60 linii |
| `docs/testing.md` | checklista bieżącego wycinka, test dymny, pułapki testowe | ok. 60 linii |
| `docs/roadmap.md` | co dalej: to, czego nie zbudowano; pytania do autora; Szlif | ok. 70 linii |
| `docs/spec/` | koncepcja etapu przed budową; po zakończeniu etapu usuwana | — |

Kod jest źródłem prawdy; dokument jest tam, gdzie kod nie wystarcza. Wiedza o projekcie mieszka tylko
w tych plikach, nie w pamięci asystenta. Długość (wiersze ok. 110 znaków) to wskazówka: przekroczenie to
sygnał do przeglądu, nie powód do skracania kosztem jasności, powodu czy informacji.
- Stan, nie historia: bez dat, numerów sesji i słów „dziś”, „na razie”, „wcześniej”. Historię opisuje git.
- Rzecz ma jedno miejsce: mechanizm w architekturze, powód w rozstrzygnięciach, plan w roadmapie, dane
  receptur w recipes.md; gdzie indziej tylko odsyłacz. Zmieniając regułę, szukaj jej słów we wszystkich
  dokumentach. Rozstrzygnięcia nie odsyłają do specu — spec znika po etapie.
- Pojęcie ma jedną nazwę ze słownika. „X nie ma” podaje powód albo odsyła do rozstrzygnięcia. Punkt to jedna
  myśl, do ok. 60 słów. Odwołanie do vanilli: nazwa funkcji plus `plik:linia` jako podpowiedź.
