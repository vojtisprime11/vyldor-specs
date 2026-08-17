#!/usr/bin/env python3
"""Vyldor P1 — turn a strain-gauge recording into the one chart that decides v0.8.

Usage:  python3 analyse.py zaznam.csv  [--tape klid=82.0,jidlo_po=83.5]

The `--tape` values are the tape-measure readings in centimetres for the blocks where
you took them. They are the only ground truth in this experiment: without them the
recording shows that *something* changed, not that circumference did.

The verdict at the end is the gate written in `Vyldor Belt/TESTING.md`, applied
mechanically so the answer does not depend on how much you want it to pass.
"""
import argparse
import csv
import math
import sys


def load(path):
    rows, bad = [], 0
    with open(path, newline="", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("ms,"):
                continue
            parts = line.split(",")
            if len(parts) != 3:
                bad += 1
                continue
            try:
                rows.append((int(parts[0]), parts[1], int(parts[2])))
            except ValueError:
                bad += 1
    if bad:
        print(f"  (preskoceno {bad} poskozenych radku — u seriove linky normalni)")
    return rows


def blocks(rows):
    out = {}
    for ms, name, raw in rows:
        out.setdefault(name, []).append((ms, raw))
    return out


def stats(samples):
    values = [v for _, v in samples]
    n = len(values)
    mean = sum(values) / n
    sd = math.sqrt(sum((v - mean) ** 2 for v in values) / n) if n > 1 else 0.0
    return mean, sd, n


def rate_hz(samples):
    """Sampling rate implied by the timestamps, not by what we asked the HX711 for."""
    if len(samples) < 2:
        return 0.0
    span = (samples[-1][0] - samples[0][0]) / 1000.0
    return (len(samples) - 1) / span if span > 0 else 0.0


def detrend(values):
    """Remove a straight line. Body temperature and creep both drift slowly; breathing
    does not, so the trend is the thing standing between you and the breathing peak."""
    n = len(values)
    xs = list(range(n))
    mx, my = sum(xs) / n, sum(values) / n
    denom = sum((x - mx) ** 2 for x in xs) or 1.0
    slope = sum((xs[i] - mx) * (values[i] - my) for i in range(n)) / denom
    return [values[i] - (my + slope * (xs[i] - mx)) for i in range(n)]


def dominant_band(samples, lo, hi):
    """Strongest frequency in [lo, hi] Hz, by direct DFT.

    A full FFT is not worth a dependency here: we test a few hundred candidate
    frequencies over a band we care about, which is both fast enough and much easier
    to check by hand than a library call.
    """
    fs = rate_hz(samples)
    if fs <= 0 or len(samples) < 64:
        return None, 0.0, fs
    values = detrend([v for _, v in samples])
    n = len(values)
    best_f, best_mag = 0.0, 0.0
    steps = 400
    for i in range(steps + 1):
        f = lo + (hi - lo) * i / steps
        w = 2 * math.pi * f / fs
        re = sum(values[k] * math.cos(w * k) for k in range(n))
        im = sum(values[k] * math.sin(w * k) for k in range(n))
        mag = math.hypot(re, im) / n
        if mag > best_mag:
            best_f, best_mag = f, mag
    return best_f, best_mag, fs


def sparkline(samples, width=72):
    values = [v for _, v in samples]
    lo, hi = min(values), max(values)
    if hi == lo:
        return "─" * width
    chars = "▁▂▃▄▅▆▇█"
    bucket = max(1, len(values) // width)
    out = []
    for i in range(0, len(values) - bucket + 1, bucket):
        chunk = values[i:i + bucket]
        avg = sum(chunk) / len(chunk)
        out.append(chars[min(7, int((avg - lo) / (hi - lo) * 7.999))])
    return "".join(out[:width])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--tape", default="", help="napr. klid=82.0,jidlo_po=83.5")
    args = ap.parse_args()

    rows = load(args.csv)
    if not rows:
        sys.exit("v souboru nejsou zadna data")

    tape = {}
    for pair in filter(None, args.tape.split(",")):
        name, _, value = pair.partition("=")
        try:
            tape[name.strip()] = float(value)
        except ValueError:
            sys.exit(f"necitelna hodnota metru: {pair}")

    grouped = blocks(rows)
    print(f"\nVYLDOR P1 — {args.csv}")
    print(f"{len(rows)} vzorku, {len(grouped)} bloku\n")

    print(f"{'blok':<14} {'n':>6} {'fs Hz':>7} {'prumer':>12} {'sm.odch.':>11}   prubeh")
    print("-" * 100)
    summary = {}
    for name, samples in grouped.items():
        mean, sd, n = stats(samples)
        fs = rate_hz(samples)
        summary[name] = (mean, sd, n, fs)
        print(f"{name:<14} {n:>6} {fs:>7.1f} {mean:>12.0f} {sd:>11.0f}   {sparkline(samples, 40)}")

    # ---- gate 1: breathing -------------------------------------------------
    print("\n1) DECH — je v signalu videt dychani?")
    breath_ok = False
    for name in ("dech", "klid", "pres_tricko", "pres_mikinu"):
        if name not in grouped:
            continue
        f, mag, fs = dominant_band(grouped[name], 0.10, 0.60)
        if f is None:
            continue
        _, sd, _, _ = summary[name]
        # A peak has to stand clear of the block's own noise to mean anything.
        clear = mag > 0.25 * sd if sd > 0 else False
        verdict = "ANO" if clear else "ne"
        print(f"   {name:<14} {f * 60:>5.1f} dechu/min   amplituda {mag:>9.0f}   "
              f"(sm.odch. {sd:>8.0f})   {verdict}")
        if name in ("dech", "klid") and clear:
            breath_ok = True

    # ---- gate 2: circumference vs walking noise ----------------------------
    print("\n2) OBVOD — je zmena o 1 cm odlisitelna od sumu pri chuzi?")
    circ_ok = False
    if "chuze" in summary and len(tape) >= 2:
        walk_sd = summary["chuze"][1]
        names = [n for n in tape if n in summary]
        if len(names) >= 2:
            a, b = names[0], names[-1]
            d_raw = abs(summary[a][0] - summary[b][0])
            d_cm = abs(tape[a] - tape[b])
            if d_cm > 0:
                per_cm = d_raw / d_cm
                ratio = per_cm / walk_sd if walk_sd > 0 else float("inf")
                circ_ok = ratio >= 1.0
                print(f"   {a} vs {b}: {d_cm:.1f} cm metrem = {d_raw:.0f} jednotek")
                print(f"   1 cm = {per_cm:.0f} jednotek;  sum pri chuzi = {walk_sd:.0f}")
                print(f"   pomer signal/sum = {ratio:.2f}   "
                      f"({'ANO' if circ_ok else 'ne'} — potreba >= 1.0)")
            else:
                print("   metr namerill stejnou hodnotu v obou blocich — nelze skalovat")
        else:
            print("   hodnoty metru neodpovidaji zadnym blokum v zaznamu")
    else:
        print("   chybi blok 'chuze' nebo aspon dve hodnoty --tape.")
        print("   Bez metru tenhle test nelze uzavrit — zmer pas a pust znovu.")

    # ---- verdict -----------------------------------------------------------
    print("\n" + "=" * 60)
    if breath_ok and circ_ok:
        print("GO — obe brany z TESTING.md prosly.")
        print("Tenhle graf patri do decku a do mailu investorum.")
    elif not tape:
        print("NEROZHODNUTO — bez hodnot z krejcovskeho metru to nelze uzavrit.")
    else:
        print("NO-GO zatim.")
        print("Nez to prohlasis za mrtve, zkontroluj v tomhle poradi:")
        print("  1. Lezi mrizka tenzometru PODEL remenu? Otoceny o 90 stupnu nemeri nic.")
        print("  2. Je slepy tenzometr na stejne kuzi a stejne teple?")
        print("  3. Nejsou to uhlikove rezistory? S teplotou se hybou vic nez signal.")
        print("  4. Utahl jsi pasek stejne v obou merenych blocich?")
        print("Az kdyz tohle sedi a porad to nevychazi, je to skutecny NO-GO — a ten")
        print("zverejni. Zmereny zapor je porad vic, nez ma dnes kdokoliv jiny.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
