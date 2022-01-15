# GrillBot / Hledání

Zjednodušená forma inzerce, kdy uživatel v kanálu něco hledá. Může to být cokoliv. Od nějakého produktu, až po týmy.

Data se v databázi ukládají do tabulky `SearchItems` a jsou mapována na entitu [SearchItem](https://gitlab.com/grillbot/grillbot/-/blob/master/src/GrillBot/GrillBot.Database/Entity/SearchItem.cs). 

## Příkazy

_Všechny příkazy počítají s výchozím prefixem `$`. Pokud máte v konfiguraci vlastní prefix, pak jej zohledněte._

Příkazy mají jednotnou skupinu příkazů pojmenovanou jako `$hledam`;

- `$hledam [{kanal}]` - Vypíše seznam hledání v daném kanálu. Součástí každé položky seznamu bude informace o tom, kdo něco hledá a samotná zpráva od uživatele.
  - Parametry
    - `kanal` - Identifikace kanálu ze kretého se chce vypsat hledání. Volitelný parametr. Pokud není zadán, tak se vypíše hledání v kanálu, kde byl příkaz zavolán.
- `$hledam {obsah}` - Vytvoření hledání v kanálu, ve kterém byl příkaz zavolán..
  - Parametry
    - `obsah` - Obsah zprávy hledání. Maximální délka zprávy může být 1024 znaků.
- `$hledam remove {id}` - Odebrání hledání. Odebrat hledání je omezeno pouze na autora daného hledání nebo uživatele s vyššími právy (Administrator nebo Manage Messages).
  - Parametry
    - `id` - ID hledání. Lze zjistit pomocí příkazu `$hledam`

## Administrace

Oprávnění uživatelé mají možnost vidět všechna hledání formou webové administrace. Také mnou hromadně mazat hledání.

