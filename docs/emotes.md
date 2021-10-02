# GrillBot / Správa a statistika kanálů

GrillBot sbírá statistiky použitých emotikonů. Díky tomu lze například snadno zjišťovat, které emotikony jsou nepoužívané, ...

Sbírání statistik se provádí tak, že bot automaticky skenuje každou zprávu a loguje každé použití emotikonu. Každá statistická položka se váže na daný emotikon a uživatele, který emotikon použil.

## Příkazy

_Všechny příkazy počítají s výchozím prefixem `$`. Pokud máte v konfiguraci vlastní prefix, pak jej zohledněte._

Příkazy mají jednotnou skupinu příkazů pojmenovanou jako `$emote`.

- `$emote list [{id/tag/jmeno uzivatele}]` - Jedná se o alias pro `$emote list count desc [{id/tag/jmeno uzivatele}]`.
- `$emote list count desc [{id/tag/jmeno uzivatele}]` - Statistika použití emotikonů podle počtu použití seřazené sestupně.
- `$emote list count asc [{id/tag/jmeno uzivatele}]` - Statistika použití emotikonů podle počtu použití seřazené vzestupně.
- `$emote list lastuse desc [{id/tag/jmeno uzivatele}]` - Statistika použití emotikonů podle data a času posledního použití seřazeno sestupně.
- `$emote list lastuse asc [{id/tag/jmeno uzivatele}]` - Statistika použití emotikonů podle data a času posledního použití seřazeno vzestupně.
  - Parametry:
    - `id/tag/jmeno uzivatele` - Identifikace uživatele. Je možné použít tag, identifikátor, uživatelské jméno případně server alias, pokud nějaký uživatel mám. Volitelný parametr. Pokud není zadán uživatel, pak je statistika za všechny uživatele.
- `$emote get {emote/id/nazev}` - Získání statistiky emotikonu. Vypíše základní informace o emotikonu, datum a čas prvního a posledního výskytu, dobu od posledního použití, počet použití, počet uživatelů, kteří použili emotikon a TOP10 uživatelů, kteří použili emotikon.
  - Parametry:
    - `emote/id/nazev` - Identifikace emotikonu. Je možné použít samotný emotikon v plném formátu, identifikátor nebo název.
