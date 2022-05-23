# GrillBot / Funkce / Narozeniny

Funkcionalita narozenin slouží k oznamování, kdy má kdo narozeniny. Vyhodnocení narozenin probíhá na základě data narození, který si každý uživatel ukldádá sám na pomocí příkazu. Samotné oznámení o narozeninách je možné provést pomocí příkazu, nebo počkat na provedení naplánované úlohy. Ve výchozí konfiguraci se naplánovaná úloha spouští každých 24 hodin (v 8:00 AM).

## Příkazy

*Všechny příkazy mají jednotnou skupinu `/narozeniny` a jsou integrovány jako "slash commands".*

- `/narozeniny pridat {kdy}` - Uložení data narození k uživateli, který použil příkaz. **Datum narození nelze přiřadit jinému uživateli.**
  - Parametry:
    - `kdy` (DateTime) - Datum narození. Pokud si nepřejete uložit věk, pak zadejte rok `0001`.
  - Příklad: `/narozeniny pridat 1997-06-05`
- `/narozeniny mam` - Zjištění, zda má uživatel uloženo datum narození. **Není možné zjistit, zda má někdo uloženo datum narození jiného uživatele.**
  - Příkaz nemá žádné parametry.
- `/narozeniny smazat` - Smazání data narození uživatele. **Není možné smazat datum narození někomu jinému uživateli.**
- `/narozeniny dnes` - Zjišťění, kdo má dnes narozeniny.
