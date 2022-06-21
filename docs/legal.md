# GrillBot / Ustanovení

GrillBot je aplikace s vyhrazenými právy. Zdrojový kód aplikace je veřejný ke čtení a je umožněno do něj přispívat bez omezení. Použití částí kódu z aplikace je umožněno za podmínky uvedení autora u zdrojového kódu.

Administrátor discord serveru je oprávněn přidat běžící instanci aplikace až po písemném povolení vlastníkem aplikace. Současně také spuštění vlastní instance za jiným účelem, než vývoj aplikace je možné až po písemném povolení vlastníkem.

Vlastníkem aplikace je skupina osob, kteří jsou členy skupiny [GrillBot](https://gitlab.com/groups/grillbot/-/group_members) v systému GitLab. Tyto osoby mohou udělit povolení k užívání aplikace.

Uživatel, který se připojí na Discord server, kde se také nachází bot automaticky souhlasí se sběrem dat popsaných v tomto dokumentu.

## Sběr a uchovávání dat

Za účelem správného chodu GrillBot musí uchovávat v databázi informace o uživatelích na discord serveru, záznamy (logy) a další.

Data jsou v databázi uchovávany na základě jejich potřeby po různou dobu.

- Záznamy z logování provozu starší, než 12 měsíců jsou zálohovány na diskové úložiště a z databáze smazány. Na disku jsou data uchovány po dobu minimálně dalšího jednoho měsíce. Po uplynutí této doby si provozovatel aplikace vyhrazuje právo data nenávratně smazat.
- Ostatní výše nezmíněné data jsou v databázi uchovány po dobu existence discord serveru na kterém se bot nachází a to i po opuštění bota ze serveru.

Administrátor serveru je oprávněn provádět pravidelné zálohy celé databáze (kromě výše uvedené automatizované archivace) za účelem zajištění provozuschopnosti služby. Administrátor serveru na kterém běží instance aplikace sám rozhodne, jak dlouho bude držet zálohy.

### Unverify (dočasné odebrání přístupu)

Unverify uchovává k uživateli jeho aktuální stav, pokud má uživatel zrovna odebraný přístup. K aktuálnímu stavu jsou uchovány následující data:

- Povinné identifikátory (identifikátor serveru, uživatele, ...)
- Datum a čas odebrání a konce odebrání přístupu.
- Důvod odebrání přístupu.
- Seznam rolí, které mají být uživateli navráceny.
- Seznam kanálů, do kterých má být uživateli navrácen přístup.

Aktuální stav unverify je po jeho skončení automaticky smazán.

#### Logování unverify

Kromě aktuálního stavu unverify je také uchováván log provedených operací nad unverify. Tyto záznamy jsou uchovávány v databázi k tomu určené tabulce. Uchovávají se tyto typy záznamů:

- Odebrání přístupu (Oprávněná osoba provedla odebrání přístupu).
- Vlastní odebrání přístupu (Uživatel sám sobě odebral přístup).
- Automatické vrácení přístupu (Uživateli skončila doba odebrání přístupu).
- Předčasné vrácení přístupu (Uživateli oprávněná osoba vrátila přístup).
- Aktualizace doby odebrání přístupu (Oprávněná osoba změnila uživateli dobu odebrání přístupu).
- Obnovení původního stavu (Oprávněná osoba obnovila uživateli původní stav před odebráním přístupu).

Každý záznam bez ohledu na jeho typ (z výše uvedených) obsahuje následující data:

- Unikátní identifikátor operace.
- Identifikace uživatele, který operaci provedl.
- Identifikace uživatele nad kterým byla operace provedena.
- Identifikace serveru ve kterém byla tato operace provedena.
- Typ záznamu
- Datum a čas zaevidování operace
- Data konkrétní operace

Mezi konkrétní data se řadí následující:

- Odebrání přístupu a vlastní odebrání přístupu
  - Počáteční a koncové datum odebrání přístupu.
  - Důvod odebrání přístupu
  - Seznam kanálů, které nebyly procesem odebrání přístupu v danou chvíli ovlivněny.
  - Seznam kanálů, ke kterým uživatel ztratil přístup.
  - Seznam rolí, které byly uživateli ponechány.
  - Seznam rolí, které byly uživateli odebrány.
- Automatické vrácení přístupu, předčasné vrácení přístupu a obnovení původního stavu
  - Seznam kanálů, které uživatel obdržel zpět.
  - Seznam rolí, které uživatel obdržel zpět.
- Aktualizace doby odebrání přístupu
  - Nový čas začátku a konce odebrání přístupu.

K záznamům o odebrání přístupu je možné přistoupit pomocí rozhraní REST API, případně pomocí uživatelského rozhraní, které využívá tohoto REST API. Uživatelé mají přístup k těm záznamům, které ukazují provedení nad jeho účtem. Oprávněné osoby mohou vidět všechny záznamy.

### Obecné informace o uživateli

GrillBot v databázi o samotném uživateli eviduje následující:

- Jednoznačný identifikátor ve službě Discord
- Pomocné příznaky (bitová maska)
  - Bit 1 (`1`): Umožňuje uživateli hned po vlastníkovi bota mít nejvyšší oprávnění a může obsluhovat všechny metody dostupné pomocí příkazů ve službě Discord.
  - Bit 2 (`2`): Umožňuje uživateli přístup do webové administrace, kam se přihlašuje pomocí OAuth2 přihlášení služby Discord.
  - Bit 3 (`4`): Pomocný bit rozlišující uživatele a boty.
  - Bit 4 (`8`): Informační bit, že je uživatel přihlášen v privátní webové administraci.
  - Bit 5 (`16`): Uživatel má zablokovaný přístup k veřejné administraci.
  - Bit 6 (`32`): Informační bit, že je uživatel přihlášen ve veřejné webové administraci.
  - Bit 7 (`64`): Veškeré příkazy pro daného uživatele jsou zablokovány.
- Datum a čas narození uživatele. Jedná se o datum s volitelnou specifikací roku. Datum narození si zadává a odebírá uživatel sám. Ostatní osoby nemohou s datem narození jiného uživatele vůbec manipulovat. Oprávněné osoby mají přístup pouze k informaci o tom, zda má uživatel datum narození uloženo (ANO/NE). Žádný uživatel nevidí konkrétní datum. Uložením data narození dává uživatel souhlas k nakládání s datem narození za účelem prezentace ke dni narozenin prostřednictvím příkazu a automatizovaného upozornění.
- Interní poznámka, kterou si mohou oprávněné osoby k uživateli napsat pomocí webové administrace.
- Aktuální uživatelské jméno, diskriminátor a stav přihlášení (Online, Offline, ...) ze služby Discord.
- Agregované informace o použitých emotikonech.
- Interní poznámka nastavitelná v privátní administraci. Vidí ji všechny oprávněné osoby. Poznámka není dostupná ve veřejné administraci.
- Minimální doba, na kterou si uživatel může dát selfunverify. Pokud není nastaveno, tak se na něj vztahuje výchozí nastavení.

Každý uživatel má přístup ke svým informacím pomocí příkazu `/me`, nebo pomocí veřejné administrace. Oprávněné osoby mají přístup ke všem údajům o uživatelích a to pomocí příkazu `$user info`, nebo pomocí webové administrace.

### Statistika používání emotikonů

Statistika o používání různých emotikonů. Vytváří se statistika pouze k emotikonům, ke kterým má bot přístup. Tato statistika se sbírá ze zpráv i reakcí. Neuchovávají se unicode emoji. U každé statistiky je uchováno:

- Jednoznačný identifikátor emotikonu ve formátu `<:nazev:id>`.
- Identifikace uživatele. Který emoji použil.
- Identifikace serveru, ve kterém se emote nachází.
- Počet použití emotikonu.
- Datum a čas prvního výskytu emotikonu, který bot zaznamenal.
- Datum a čas posledního výskytu emotikonu, který bot zaznamenal.

### Upozorňování

Aby bylo možné provádět upozornění uživatele k určitému datu za pomocí feature "Remind", pak musí bot ukládat následující:

- Jednoznačný identifikátor v databázové tabulce.
- Identifikace uživatele, který zprávu k upozornění založil.
- Identifikace uživatele, který zprávu k upozornění má obdržet.
- Identifikace původní zprávy za účelem možnosti vytvářet kopie tohoto upozornění za pomocí reakcí.
- Identifikace zprávy upozornění za účelem odložení.
- Datum a čas, kdy se má upozornění odeslat.
- Obsah zprávy.
- Počet odložení.

### Informace o serveru

K zajištění konzistence dat je zapotřebí pro každý discord server uchovávat:

- Identifikátor serveru.
- Název serveru
- Identifikátor role, která obsahuje oprávnění, které uzamkne psaní ve všech textových kanálech a nepovolí připojení do hlasových kanálů (Volitelně).
- Identifikátor administrátorského/systémového kanálu (Volitelně).
- Identifikátor role, kterou mají "Server booster" uživatelé. Nastavuje se automaticky při startu aplikace.
- Identifikátor kanálu pro návrhy emotů.

#### Informace o uživateli na serveru

Pro každého uživatele na serveru je nutné evidovat (kromě výše uvedených informací o uživateli jako takovém):

- Povinné identifikátory (Serveru, uživatele, ...)
- Kód použité pozvánky
- Počet bodů, které uživatel obdržel svojí aktivitou.
- Počet reakcí, které uživatel obdržel a udělali.
- Datum a čas poslední inkrementace bodů z reakce a ze zprávy (dvě hodnoty data a času).
- Přezdívka (pokud ji má nastavenou).

#### Kanály

Pro každý textový kanál, který se nachází na serveru a byla na něm provedena nějaká aktivita se ukládá:

- Povinné identifikátory (serveru a kanálu, případně nadřazeného kanálu).
- Název kanálu
- Typ kanálu

_Identifikátor nadřazeného kanálu se uchovává pouze v případě, že se jedná o vlákno._

Za každého uživatele jsou pak u kanálu uloženy následující data:

- Povinné identifikátory (kanálu, serveru, uživatele)
- Počet zpráv v kanálu.
- Datum a čas první zaznamenané zprávy v kanálu.
- Datum a čas poslední zaznamenané zprávy v kanálu.

#### Pozvánky

Když se uživatel připojí na server, tak se automaticky provede detekce, kterou pozvánku použil. Tato pozvánka je poté uložena v databázi. K této pozvánce se uchovává:

- Jednoznačné identifikátory
  - Unikátní kód pozvánky.
  - Serveru, ke kterému pozvánka patří.
  - Uživatele, který pozvánku založil.
- Datum a čas vytvoření pozvánky.

Pokud se uživatel připojí pomocí tzv. `Vanity url` (speciální pozvánky s vlastním (nevygenerovaným) kódem), pak se u takové pozvánky neukládá kdo takovou pozvánku založil a kdy ji založil.

### Logování provozu

Logování provozu se provádí za účelem zabezpečení bezproblémového chodu serveru a případného dohledávání nepovolených aktivit.

Logování probíhá formou událostí různých typů. Tyto události jsou:

| Typ                  | Popis                                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------------ |
| `Info`               | Textová zpráva informačního charakteru. Zapisuje se zde informace o načtených pozvánek při startu.           |
| `Warning`            | Varování, že došlo k nějaké události, které by měla být věnována pozornost, ale nemá destruktivní charakter. |
| `Error`              | Při běhu aplikace došlo k chybě.                                                                             |
| `Command`            | Provedení příkazu.                                                                                           |
| `ChannelCreated`     | Vytvoření kanálu                                                                                             |
| `ChannelDeleted`     | Smazání kanálu                                                                                               |
| `ChannelUpdated`     | Úprava kanálu                                                                                                |
| `EmojiDeleted`       | Smazání emotikonu ze serveru.                                                                                |
| `OverwriteCreated`   | Vytvoření přístupové výjimky do kanálu.                                                                      |
| `OverwriteDeleted`   | Smazání přístupové výjimky do kanálu.                                                                        |
| `OverwriteUpdated`   | Aktualizace přístupové výjimky do kanálu.                                                                    |
| `Unban`              | Odblokování uživatele a umožnění se připojit na server.                                                      |
| `MemberUpdated`      | Uživatel na serveru byl aktualizován (přezdívka, nebo umlčení v hlasovém kanálu).                            |
| `MemberRoleUpdated`  | Role uživatele byly aktualizovány.                                                                           |
| `GuildUpdated`       | Vlastnosti serveru byly upraveny.                                                                            |
| `UserLeft`           | Uživatel opustil server.                                                                                     |
| `MessageEdited`      | Obsah nějaké zprávy byl upraven.                                                                             |
| `MessageDeleted`     | Zpráva byla na serveru smazána.                                                                              |
| `InteractionCommand` | Provedení integrovaného příkazu (Slash command, Message command, User command).                              |
| `ThreadDeleted`      | Smazání vlákna.                                                                                              |
| `JobCompleted`       | Dokončení automaticky naplánované úlohy.                                                                     |
| `API`                | Požadavek na REST API.                                                                                       |

U všech událostí se evidují tyto společné vlastnosti:

- Povinné identifikátory
  - Unikátní identifikátor záznamu.
  - Identifikátor serveru, na kterém událost vznikla.
  - Identifikátor uživatele, který událost vyvolal.
  - Identifikátor záznamu z audit logu služby discord (pokud odtamtud pochází).
  - Identifikátor kanálu, ke kterému se vztahuje záznam.
- Datum a čas zaevidování záznamu.
- Typ události (viz tabulka výše).
- Seznam souborů, které k události náleží.

#### Popis jednotlivých událostí

Většina událostí obsahuje v záznamu také data specifické k určitému typu události. Ve většině případů se jedná o JSON data.

- Informační zprávy, varování a chyby obsahují textový řetězec s obsahem zprávy. Neobsahují JSON data.
- Provedení příkazu:
  - Identifikaci příkazu, který byl prováděn.
  - Obsah zprávy, který vyvolal příkaz.
  - Příznak, zda příkaz byl proveden úspěšně.
  - Typ chyby, který vznikl při provádění příkazu, pokud se neprovedl správně.
  - Textovou reprezentaci chyby, která vznikla při prováděné příkazu. Pokud se příkaz neprovedl správně.
- Vytvoření a smazání kanálu:
  - Identifikátor kanálu
  - Název kanálu.
  - Typ kanálu (Text, Hlasový, Kategorie).
  - Příznak NSFW (**N**ot **S**afe **T**o **W**ork) - Pouze u textových kanálů.
  - Bitrate - Pouze u hlasových kanálů.
  - Časové omezení mezi posíláním zpráv (SlowMode) - Pouze u textových kanálů.
  - Popis kanálu.
- Úprava kanálu:
  - V případě změny kanálu se uchovávají stejné informace jako u vytvoření a smazání, jen se drží verze před a po úpravě.
- Smazání emotikonu ze serveru:
  - Identifikátor emotikonu.
  - Název emotikonu.
- Vytvoření a smazání přístupové výjimky do kanálu:
  - Typ přístupové výjimky (Role, Uživatel).
  - Identifikátor cíle výjimky.
  - Hodnota reprezentující povolené možnosti.
  - Hodnota reprezentující zakázané možnosti.
- Aktualizace přístupové výjimky do kanálu:
  - Drží se stejné informace jako u vytvoření a smazání, jen se navíc drží verze před a po úpravě.
- Odblokování uživatele a umožnění se připojit na server:
  - Základní informace o uživateli, který byl odblokován:
    - Jednoznačný identifikátor.
    - Uživatelské jméno
    - Zjednodušený identifikátor.
- Uživatel na serveru byl aktualizován (přezdívka, nebo umlčení v hlasovém kanálu):
  - Přezdívka před a po změně.
  - Stav umlčení v hlasovém kanálu před a po změně.
  - Položky měněné z webové administrace (přes API):
    - Interní poznámka.
    - Příznaky (Administrátor, přístup do webové administrace).
    - Minimální čas při SelfUnverify.
- Role uživatele byly aktualizovány:
  - Seznam rolí, které byly uživateli přidány nebo odebrány.
- Vlastnosti serveru byly upraveny:
  - Všechny změny se drží v páru (před a po změně).
  - Výchozí nastavení upozornění.
  - Popis serveru.
  - Název univerzální pozvánky (Vanity URL).
  - Zda byla změněna grafika serveru (banner, ikona, ...).
  - Identifikátor hlasového regionu.
  - Vlastník serveru.
  - Kanál pro veřejná oznámení.
  - Kanál pro pravidla.
  - Systémový kanál.
  - Hlasový kanál pro neaktivní uživatele.
  - Časový limit po kterém bude uživatel přesunut do kanálu pro neaktivní.
  - Název serveru.
  - Dvoufázové ověřování.
- Uživatel opustil server:
  - Počet členů na serveru po tom, co uživatel opustil server.
  - Zda bylo opuštění serveru způsobeno vyhozením (s nebo bez možnosti návratu) a důvod.
  - Základní informace o uživateli.
- Obsah nějaké zprávy byl upraven:
  - Obsah zprávy před a po.
  - Odkaz na zprávu.
- Zpráva byla na serveru smazána:
  - Příznak, zda byla zpráva nalezena v cache.
  - Obsah zprávy
    - Autor zprávy. Základní informace o uživateli.
    - Datum a čas vytvoření zprávy.
    - Textový obsah zprávy.
- Integrovaný příkaz
  - Název příkazu, modulu a metody svázané s příkazem.
  - Seznam parametrů
    - V každém parametru se ukládá: Název parametru, typ (Bool, Int, Double, String, Kanál, Role, Uživatel a Zpráva) a hodnota.
  - Příznak, že bot odpověděl.
  - Příznak, že bot měl k dispozici platný token ke službě Discord.
  - Příznak, zda příkaz byl proveden úspěšně.
  - Typ chyby, který vznikl při provádění příkazu, pokud se neprovedl správně.
  - Textovou reprezentaci chyby, která vznikla při prováděné příkazu. Pokud se příkaz neprovedl správně.
- Smazání vlákna
  - Identifikátor kanálu
  - Název kanálu.
  - Časové omezení mezi posíláním zpráv (SlowMode) - Pouze u textových kanálů.
  - Typ vlákna (Veřejné/Soukromé)
  - Příznak, že kanál byl archivován.
  - Časové období pro archivaci.
  - Příznak, že kanál byl uzamknut.
- Dokončení naplánované úlohy
  - Název úlohy.
  - Výsledek úlohy - Úlohy, které nemají zapsány výsledek se nelogují.
  - Datum a čas začátku běhu.
  - Datum a čas konce běhu.
  - Příznak, že došlo k chybě.
- API požadavek
  - Název kontroléru na který směřoval požadavek.
  - Název akce na který směřoval požadavek.
  - Datum a čas začátku požadavku.
  - Datum a čas konce požadavku.
  - HTTP metoda (GET, POST, ...).
  - Šablona URL.
  - Skutečná URL.
  - Role aktuálně přihlášeného uživatele (není vyplněno, pokud se jedná o nepřihlášený přístup).
  - Výsledný stavový kód.
  - Seznam parametrů v URL (QueryString).
  - Serializovaná data v těle požadavku (pokud byly přítomna).

### Zpřístupnění

Ke všem výše uvedeným informacím mají přístup pouze oprávněné osoby. Všechny informace jsou čitelné pomocí webové administrace. Oprávněná osoba může provést smazání záznamu pokud k tomu má patřičný důvod.

Uživatel má nárok k výmazu pouze informací o sobě samém. K výmazu dojde formou anonymizace. Z technických důvodů není možné provést ostré smazání dat. Smazání všech informací může provést pouze oprávněná osoba a na základě písemné žádosti.
