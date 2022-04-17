# GrillBot / Správa a statistika kanálů

GrillBot sbírá statistiky použitých emotikonů. Díky tomu lze například snadno zjišťovat, které emotikony jsou nepoužívané, ...

Sbírání statistik se provádí tak, že bot automaticky skenuje každou zprávu a loguje každé použití emotikonu. Každá statistická položka se váže na daný emotikon a uživatele, který emotikon použil.

## Příkazy

*Všechny příkazy mají jednotnou skupinu `/emote` a jsou integrovány jako "slash commands".*

- `/emote list {order} {direction} [{user}]`
  - Statistika použití emotikonů.
  - Parametry:
    - `order` - Podle kterého kritéria se má řadit. Na výběr jsou možnosti podle počtu použití daného emote, nebo podle data a času posledního použití.
    - `direction` - Zda se má použít vzestupné nebo sestupné řazení.
    - `user` - Identifikace uživatele. Je možné použít tag, identifikátor, uživatelské jméno případně server alias, pokud nějaký uživatel mám. Volitelný parametr. Pokud není zadán uživatel, pak je statistika za všechny uživatele.
- `/emote get {emote/id/nazev}` - Získání statistiky emotikonu. Vypíše základní informace o emotikonu, datum a čas prvního a posledního výskytu, dobu od posledního použití, počet použití, počet uživatelů, kteří použili emotikon a TOP10 uživatelů, kteří použili emotikon.
  - Parametry:
    - `emote/id/nazev` - Identifikace emotikonu. Je možné použít samotný emotikon v plném formátu, identifikátor nebo název.
