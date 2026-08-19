# P1 — je v napětí řemenu čitelný signál?

Tohle je celý ten test, na kterém stojí v0.8. Nic jiného v projektu nemá smysl,
dokud tenhle nedopadne. Stojí zhruba **500 Kč a jedno odpoledne.**

Není to prototyp pásku. Je to donor pásek, jeden tenzometr a záznam do souboru.
Cílem je jediný graf, na který se dá ukázat.

---

## Proč to rozhoduje o penězích, ne jen o technice

StartupYard i většina akcelerátorů chtějí „aspoň funkční prototyp". Fondy říkají
totéž jinými slovy. Dokud je Vyldor koncept, každá odpověď zní „ozvěte se, až něco
budete mít".

Tenhle test není prototyp pásku, ale je to **měřená data**. Graf, na kterém je vidět
dech vyčtený z napětí opasku, mění větu „myslím, že to půjde" na „tady to je".
To je rozdíl mezi konceptem a důkazem, a je to rozdíl za pět set korun.

---

## Nákupní seznam

| Díl | Kolik | Orientačně | Poznámka |
|---|---|---|---|
| Tenzometr **BF350-3AA** (350 Ω, fóliový) | 4 ks | ~80 Kč | Kupuj víc, první dva zničíš při lepení |
| Modul **HX711** (24bit ADC pro můstek) | 1 ks | ~50 Kč | Zelená destička, běžně skladem |
| **ESP32** DevKit (nebo Arduino Nano) | 1 ks | ~200 Kč | ESP32 kvůli rychlosti a USB |
| Rezistory **350 Ω, tolerance 0,1 %** | 2 ks | ~40 Kč | **Metalizované, ne uhlíkové** — uhlík se s teplotou hýbe víc než měřený signál |
| Vteřinové lepidlo (kyanoakrylát) | 1 | ~40 Kč | Na lepení tenzometru |
| Kožený pásek, který nelituješ | 1 | — | Donor. Bude zničený. |
| Krejčovský metr | 1 | ~30 Kč | **Referenční pravda.** Bez něj celý test nic neznamená. |

Zdroje: LaskaKit, Drátek.cz, GM Electronic, Arduino-shop, nebo AliExpress (levnější,
2–3 týdny dodání).

### Pozor při objednávání tenzometru — tady se dá snadno koupit špatná věc

Pod názvem „tenzometr BF350" se prodávají **dvě různé věci** a jen jedna z nich funguje
se zapojením níže:

| | Co to je | Použitelné? |
|---|---|---|
| **Holý tenzometr** | Kousek oranžové fólie s mřížkou a dvěma drátky. Žádná destička. Změříš na něm ohmmetrem ~350 Ω. | **Ano, tenhle chceš** |
| **Modul / „senzor ohýbání"** | Malá plošňák s trimrem, LED a piny VCC/GND/OUT. Napájí se 5 V a dává analogové napětí. | **Ne.** Má vlastní zesilovač a s HX711 se pere. |

Rozpoznávací znak: **jestli to má napájecí pin, není to tenzometr, ale hotový obvod.**
Modul se dá použít, ale pak potřebuješ úplně jiné zapojení a jinou analýzu — a přijdeš
o teplotní kompenzaci, která je na těle to hlavní.

Když si nejsi jistý, hledej v popisu „350 Ω" a „foil strain gauge" a v obrázku fólii
bez plošného spoje. Cena holého tenzometru je pod stovku za kus.

---

## Zapojení — a proč zrovna takhle

**Jeden tenzometr do HX711 nezapojuj.** HX711 měří rozdíl napětí ve Wheatstoneově
můstku. Když mu dáš jediný odpor, vrátí ti `8388607` — saturaci — a strávíš večer
hledáním chyby v kódu, která je v zapojení. Tohle je nejčastější způsob, jak tenhle
test skončí předčasně.

**Půlmůstek se dvěma tenzometry**, protože pásek bude na těle:

```
        E+ (červený, ~4,3 V z HX711)
         │
    ┌────┴────┐
    │         │
 R_aktivní  R1 350Ω 0,1 %
    │         │
    ├── A+    ├── A-        ← rozdíl mezi A+ a A- je měřený signál
    │         │
 R_slepý    R2 350Ω 0,1 %
    │         │
    └────┬────┘
         │
        E- (černý)
```

- **R_aktivní** — nalepený na řemenu, natahuje se s ním.
- **R_slepý** — nalepený na kousku **stejné kůže vedle**, ale nezatížený.

Ten slepý je celý smysl. Tenzometr reaguje na teplotu skoro stejně jako na napětí.
Na těle se ohřeje z 20 °C na 32 °C a ten drift je větší než dech, který hledáš.
Protože jsou oba ve stejné větvi a ve stejné teplotě, teplota se odečte a zbude
jen mechanika.

**HX711 → ESP32:**

| HX711 | ESP32 |
|---|---|
| VCC | 3V3 |
| GND | GND |
| DT | GPIO 16 |
| SCK | GPIO 4 |

**Nalepení tenzometru:** odmasti kůži lihem, tenká vrstva vteřinového lepidla,
tenzometr přitlač prstem přes fólii 60 sekund. Mřížka musí ležet **podél** řemenu —
ve směru, kterým se natahuje. Otočený o 90° neuvidíš skoro nic. Vývody odlehči
kapkou lepidla kousek vedle, jinak je při prvním zatažení utrhneš.

---

## Postup měření

Firmware posílá CSV na sériovou linku, 80 vzorků za sekundu. Nahraj si každý blok
zvlášť a k **jídlu a pasu si vždy zapiš obvod krejčovským metrem** — to je jediná
reference, proti které se dá cokoliv tvrdit.

| Blok | Trvání | Co dělat |
|---|---|---|
| `klid` | 2 min | Stát rovně, dýchat normálně |
| `dech` | 2 min | 10 pomalých hlubokých nádechů, počítej je nahlas |
| `sed` | 2 min | Sednout si, zůstat |
| `chuze` | 3 min | Chodit normálním tempem |
| `schody` | 1 min | Do schodů |
| `kasel` | 1 min | 5× zakašlat s odstupem |
| `jidlo_pred` | 1 min | Před jídlem + změř metrem |
| `jidlo_po` | 1 min | 20 min po jídle + změř metrem |
| `pres_tricko` | 2 min | Zopakuj `klid` a `dech` přes tenké tričko |
| `pres_mikinu` | 2 min | Zopakuj přes mikinu |

Ty poslední dva bloky jsou ty, které to nejspíš zabijí. Dělej je taky.

---

## Vyhodnocení

```bash
python3 analyse.py zaznam.csv
```

Skript vykreslí surový průběh, vytáhne dechovou frekvenci a vysloví verdikt podle
brány z `Vyldor Belt/TESTING.md`:

> **GO:** změna obvodu o 1 cm je odlišitelná od šumu při chůzi, a dechová frekvence
> jde vyčíst z toho samého signálu.
> **NO-GO:** pokud signál utopí pohyb nebo poloha, padá obvod i dech zároveň — a
> produkt se musí předefinovat znovu, ne přemalovat render.

---

## Když to vyjde

Graf z `analyse.py` jde rovnou do decku jako slide 4 a do mailu investorům jako
věta „tady je dech vyčtený z napětí opasku". Tím přestává být Vyldor koncept.

## Když to nevyjde

Zveřejni to. Je to nejcennější věc, kterou v tu chvíli budeš mít — protože to bude
změřené, a protože skoro nikdo to nedělá. Padá s tím obvod i dech, ale nepadá s tím
tvoje důvěryhodnost; tu to naopak postaví.
