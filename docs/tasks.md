# GrillBot / Plánované úlohy

Cílem plánovaných úloh je provádění automatických operací bez interakce uživatele.

GrillBot má aktuálně integrovány následující plánované úlohy:

- Archivace a mazání starých záznamů z audit logu (každé 2 týdny).
- Upozorňování na narozeniny uživatele (každý den v 8:00).
- Čištění statistik emotikonů, které se již na serverech nenachází (každou hodinu).
- Údržba cache zpráv v paměti (každých 5 minut).
- Údržba informace o přihlášených uživatelích do webových administrací (každých 15 minut).
- Rozesílání upozornění (Reminder) v termínu (každých 5 minut).
- Vrácení přístupu po skončení unverify/selfunverify (každých 30 vteřin).

Kromě výše uvedených časů se úlohy, které nejsou definovány pomocí cron expression, spouští ještě při startu aplikace. Tyto úlohy se nastavují v konfiguračním souboru (`appsettings.json`).

## Vytvoření nové naplánované úlohy

- Je třeba nadefinovat v konfiguračním souboru `appsettings.json`, jak často (nebo kdy) se má úloha spouštět. Je možné zadat hodnotu ve formátu pro objekt typu [TimeSpan](https://docs.microsoft.com/cs-cz/dotnet/api/system.timespan?view=net-6.0), nebo jako cron expression specifický přímo pro Quartz.NET. [Cron examples](https://www.quartz-scheduler.net/documentation/quartz-3.x/tutorial/crontriggers.html#example-cron-expressions).
- Implementovat příslušnou úlohu. Příkladem může být soubor [AuditLogClearingJob.cs](https://gitlab.com/grillbot/grillbot/-/blob/master/src/GrillBot/GrillBot.App/Services/AuditLog/AuditLogClearingJob.cs), případně kód níže:

```cs
using Quartz;

[DisallowConcurrentExecution]
public class YourJob : IJob 
{
    public async Task Execute(IJobExecutionContext context)
    {
        // Implement.
    } 
}
```

Doporučuje se na úlohy atribut `DisallowConcurrentExecution`, aby nedošlo k paralelnímu spuštění jedné úlohy. 
Do úlohy je možné vkládat závislosti pomocí konstruktoru z DI kontejneru. Např.:

```cs
using Quartz;

[DisallowConcurrentExecution]
public class YourJob : IJob 
{
    private IConfiguration Configuration { get; }

    public YourJob(IConfiguration configuration)
    {
        Configuration = configuration;
    }

    public async Task Execute(IJobExecutionContext context)
    {
        // Implement.
    } 
}
```

- Nakonec je třeba úlohu registrovat v souboru [Startup.cs](https://gitlab.com/grillbot/grillbot/-/blob/master/src/GrillBot/GrillBot.App/Startup.cs). V tomto souboru nalezněte volání funkce `AddQuartz(...)`. Do této funkce po vzoru ostatních úloh doplňte odkaz na úlohu. Přepis funkce je `q.AddTriggeredJob<YourJob>(Configuratin, "Your:Path:To:Time:Configuration", bool)`. Pokud chcete ve vaší funkci použít cron expressions, tak jako poslední parametr zadejte hodnotu `true`. Jinak `false`.
