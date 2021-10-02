# GrillBot / Funkce / Narozeniny

Funkcionalita narozenin slouží k oznamování, kdy má kdo narozeniny. Vyhodnocení narozenin probíhá na základě data narození, který si každý uživatel ukldádá sám na pomocí příkazu. Samotné oznámení o narozeninách je možné provést pomocí příkazu, nebo počkat na provedení naplánované úlohy. Ve výchozí konfiguraci se naplánovaná úloha spouští každých 24 hodin.

## Příkazy

_Všechny příkazy počítají s výchozím prefixem `$`. Pokud máte v konfiguraci vlastní prefix, pak jej zohledněte._

Příkazy mají jednotnou skupinu příkazů pojmenovanou jako `$birthday`, případně aliasem `$narozeniny`.

- `$birthday {kdy}` - Uložení data narození k uživateli, který použil příkaz. **Datum narození nelze přiřadit jinému uživateli.**
  - Alias: `$narozeniny {kdy}`
  - Parametry:
    - `kdy` (DateTime) - Datum narození. Pokud si nepřejete uložit věk, pak zadejte rok `0001`.
  - Příklad: `$birthday 1997-06-05`
  - Oprávnění:
    - Vyžadováno, aby bot měl oprávnění přidávat v kanálu reakce.
- `$birthday have?` - Zjištění, zda má uživatel uloženo datum narození. **Není možné zjistit, zda má někdo uloženo datum narození jiného uživatele.**
  - Alias: `$birthday mam?`, `$narozeniny mam?`
  - Příkaz nemá žádné parametry.
- `$birthday remove` - Smazání data narození uživatele. **Není možné smazat datum narození někomu jinému uživateli.**
  - Alias: `$birthday gone`, `$birthday pryc`, `$birthday pryč`, `$birthday smazat`. Stejné aliasy je možné použít i při nahrazení prefixu `$birthday` za `$narozeniny`.
- `$birthday` - Zjišťění, kdo má dnes narozeniny.
  - Alias: `$narozeniny`
