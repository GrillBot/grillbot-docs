# GrillBot / Hledání

Zjednodušená forma inzerce, kdy uživatel v kanálu něco hledá. Může to být cokoliv. Od nějakého produktu, až po týmy.

Data se v databázi ukládají do tabulky `SearchItems` a jsou mapována na entitu [SearchItem](https://gitlab.com/grillbot/grillbot/-/blob/master/src/GrillBot/GrillBot.Database/Entity/SearchItem.cs).

## Příkazy

*Všechny příkazy mají jednotnou skupinu `/hledam` a jsou integrovány jako "slash commands".*

- `/hledam list [{kanal}] [{vyhledavani}]` - Vypíše seznam hledání v daném kanálu. Součástí každé položky seznamu bude informace o tom, kdo něco hledá a samotná zpráva od uživatele.
  - Parametry
    - `kanal` - Identifikace kanálu ze kretého se chce vypsat hledání. Volitelný parametr. Pokud není zadán, tak se vypíše hledání v kanálu, kde byl příkaz zavolán.
    - `vyhledavani` - Textové vyhledávání ve zprávě. Volitelný parametr. Pokud není zadán, tak se nezohlední.
- `/hledam nove {zprava}` - Vytvoření hledání v kanálu, ve kterém byl příkaz zavolán.
  - Parametry
    - `zprava` - Obsah zprávy hledání. Maximální délka zprávy může být 1024 znaků.
- `/hledam smazat {ident}` - Odebrání hledání. Odebrat hledání je omezeno pouze na autora daného hledání nebo uživatele s vyššími právy (Administrator, ManageMessages nebo BotAdmin).
  - Parametry
    - `ident` - Identifikace hledání. Je možné použít záznam z automaticky doplněné nápovědy (autocomplete), která se automaticky generuje, nebo zadat ID samotného záznamu. Automaticky doplněná nápověda nabízí pouze prvních 25 položek v daném kanálu.

*Může se stát, že některá hledání zničeho-nic zmizí. K tomu může dojít pokud bude kanál smazán, bot opustí server nebo uživatel opustí server.*

## Administrace

Oprávnění uživatelé mají možnost vidět všechna hledání formou webové administrace. Také mnou hromadně mazat hledání.
Všichni uživatelé mají možnost vidět svá hledání pomocí veřejné webové administrace.
