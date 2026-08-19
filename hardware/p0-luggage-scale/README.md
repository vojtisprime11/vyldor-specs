# P0 — verze bez elektroniky, kterou zvládneš dnes

**Nekupuj nic. Nepájej nic. Tenhle test trvá dvacet minut a odpoví na tu jedinou
otázku, na které Vyldor stojí:**

> Mění se napětí v řemenu měřitelně s obvodem pasu?

Když je odpověď ne, nemá smysl kupovat tenzometry — a ušetřil jsi si týden.
Když je ano, máš čísla, která můžeš poslat investorovi ještě dnes.

---

## Proč to jde bez tenzometru

Tenzometr v přezce má měřit sílu v řemenu. **Kufrová váha měří sílu taky** — jen
hůř, pomaleji a musíš ji odečítat očima. Na otázku „je tam vůbec signál?" to stačí.

Kolik čekat: pásek, přezka a vlastní poddajnost těla se chovají jako pružina v sérii.
Při realistickém rozsahu tuhosti vychází na **1 cm obvodu** tohle:

| Tuhost soustavy | ΔF na 1 cm | Na váze |
|---|---|---|
| 200 N/m (měkké) | 2,0 N | **204 g** |
| 500 N/m | 5,0 N | **510 g** |
| 1000 N/m | 10,0 N | **1019 g** |
| 2000 N/m (tuhé) | 20,0 N | **2039 g** |

Běžná kufrová váha rozlišuje 10–20 g. **Signál je nejméně desetkrát nad rozlišením
přístroje** i v tom nejhorším případě. Proto to jde změřit rukou.

---

## Co potřebuješ

- Kufrová váha (digitální, do 50 kg, rozlišení 10–20 g) — nebo pružinový siloměr
- Krejčovský metr
- Kožený pásek
- Kus provázku nebo popruhu, aby šla váha zapojit do smyčky
- Papír a tužka

Když kufrovou váhu nemáš, půjčí ti ji kdokoliv, kdo létá.

---

## Jak to zapojit

Váhu dej **do série s páskem**, ne vedle něj. Cíl je, aby celá síla v řemenu šla
skrz ni.

```
   pas
 ┌─────────────────────────────┐
 │                             │
 └── pásek ──[ VÁHA ]── provázek ──┘
```

Prakticky: pásek si zapni volněji, přeruš smyčku, vlož váhu za háček a provázkem
smyčku dopni. Tah táhne za váhu a ta ukazuje sílu v řemenu.

**Důležité:** mezi jednotlivými měřeními **nepřenastavuj délku smyčky.** Jakmile ji
změníš, měříš něco jiného. Celý test stojí na tom, že délka je konstantní a mění se
jen tvoje tělo.

---

## Co změřit

Napiš si tabulku a u každého řádku odečti sílu **i obvod pasu metrem**.

| # | Stav | Síla (g) | Obvod (cm) |
|---|---|---|---|
| 1 | Klidný stoj, normální výdech | | |
| 2 | Hluboký nádech, zadržet | | |
| 3 | Úplný výdech, zadržet | | |
| 4 | Sed na židli | | |
| 5 | Předklon | | |
| 6 | Před jídlem | | |
| 7 | 20 minut po jídle | | |
| 8 | Klidný stoj **znovu**, po hodině | | |

Řádek 8 je kontrolní. Když se výrazně liší od řádku 1, něco se posunulo nebo se
kůže protáhla — a to je taky výsledek, který stojí za zapsání.

---

## Jak to vyhodnotit

Spočítej dvě čísla:

**1. Kolik gramů na centimetr.** Vezmi dvě měření s nejrozdílnějším obvodem
(nejspíš 2 a 3, nádech vs. výdech) a vyděl rozdíl sil rozdílem obvodů:

```
citlivost = (F₂ − F₃) / (C₂ − C₃)     [g/cm]
```

**2. Je dech vidět?** Rozdíl mezi nádechem a výdechem v gramech porovnej
s rozlišením váhy. Když je nádech desetkrát nad krokem displeje, dech je čitelný.

### Brána

> **GO:** citlivost vyjde alespoň **100 g/cm** a rozdíl nádech/výdech je aspoň
> desetinásobek rozlišení váhy. Pak má smysl kupovat tenzometry — víš, že signál
> existuje a řádově jak je velký.
>
> **NO-GO:** citlivost pod 50 g/cm nebo se hodnoty chovají nahodile. Pak buď je
> pásek moc tuhý a nepřenáší nic, nebo se ti mezi měřeními posouvá smyčka.
> Zkontroluj druhé, než uvěříš prvnímu.

---

## Co tenhle test **neodpoví**

Buď v tom poctivý, až to budeš někomu posílat:

- **Neřekne, jestli to jde měřit při chůzi.** Stojíš na místě a odečítáš očima.
  Šum z pohybu je přesně to, co může celý produkt zabít, a tady ho nevidíš.
- **Neřekne nic o měření přes oblečení.**
- **Neřekne nic o dlouhodobém driftu ani o teplotě.**

Na tohle je potřeba P1 s tenzometrem. P0 je vstupenka — potvrzuje, že signál je
dost velký na to, aby stálo za to ho hledat pořádně.

---

## Až budeš mít čísla

Ta tabulka je první měřená data, která o Vyldoru existují. Patří:

1. Do decku jako slide s reálnými čísly místo tvrzení.
2. Do mailu investorům jednou větou: *„Změřil jsem to: X gramů na centimetr obvodu."*
3. Sem do repozitáře — i když vyjde NO-GO. Zvlášť když vyjde NO-GO.
