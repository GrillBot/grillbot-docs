# GrillBot / Návrhy

GrillBot umožňuje uživatelům podat návrh na následjící:

- Nový emotikon na serveru.
- Novou funkcionalitu bota.

## Návrhy emotikonů

Uživatel může navrhnout nový emote, který mu na serveru chybí a nemá možnosti vlastnit nitro, aby měl emotikon k dispozici z jiného serveru.

Návrhy je možné podávat v období, které určí oprávněná osoba. Období se nastavuje v nastavení serveru v soukromé administraci GrillBot.

Když nastane období pro podávání návrhů, tak se uživatelům zpřístupní příkaz `/suggestion emote`, kde buď pomocí přílohy, nebo použitého emote vloží daný emote. Poté se uživateli otevře nové modálové okno, kam vyplní název emotu a důvod proč by měl být na daném serveru. Důvod je nepovinný. Název emotu se předvyplní automaticky.

Následně, když uživatel pošle návrh na nový emotikon, tak se pošle do kanálu pro tzv. "Emote komisi", která určí, zda se emote může zúčastnit hlasování, či nikoliv (pomocí tlačítek Schválit/Zamítnout).

Jakmile se oprávněná osoba rozhodne, že nastal čas, tak může pomocí příkazu `/process_emote_suggestions` spustit hlasování o nových emotikonech. To znamená, že všechny schválené návrhy se pošlou do hlasovacího kanálu, kde mohou ostatní uživatelé o emotikonu hlasovat. Hlasovací doba je 1 týden (7 dní od provedení příkazu pro spuštění hlasování) a nelze ji zkrátit.

Bot automaticky kontroluje veškerá hlasování a u emotů, kterým uběhla hlasovací doba, tak vyhodnotí výsledky a pošle informaci o vyhodnocení do kanálu pro komisi.

### Webová administrace

Oprávněné osoby mohou seznam všech návrhů (schválených i zamítnutých) vidět v sekci "Návrhy na emoty".

## Návrhy funkcionality bota

Uživatel může novou funkcionalitu navrhnout pomocí příkazu `/suggestion feature`. Po spuštění příkazu se uživateli otevře nové modálové okno, do kterého uživatel zadá název funkcionality a co nejpodrobněji funkcionalitu popíše.

Následně, jak uživatel potvrdí odeslání, tak se návrh pošle na email administrátorovi bota. Email administrátora a konfiguraci použitého SMTP serveru musí administrátor nastavit v souboru `appsettings.json`.
