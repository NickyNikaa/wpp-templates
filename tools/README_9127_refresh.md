# TUIC 9127 YoY-Tool — Auto-Refresh (Backup-Tooling)

Reproduzierbares Tooling für das öffentliche Mein-Schiff-DACH-9127-YoY-Tool.
Liegt hier im GitHub-Repo als Backup, falls der lokale Ordner
`~/Documents/Claude/Projects/WPP Media` verloren geht.

## Was liegt hier
- `tuic_9127_daily_fetch.py` — zieht tägliche Umsätze Advertiser 9127 via AWIN
  Transactions-API, exkl. Payback (426667+469409), netto (declined raus).
  Schreibt LOKAL `.tuic_9127_daily_data.json` (absolute € → bleibt lokal).
- `tuic_9127_regen_abs.py` — baut `tuic_9127_abs_data.json` (Ziele 2025 = 24,5 Mio,
  2026 = 30,7 Mio; corr-Block; d2025/d2026 als {"MM-DD": wert}).
- `tuic_9127_bake.py` — ersetzt NUR den `const DATA = {…};`-Block in
  `tuic-9127-yoy-tool.html`. Kompensationsmodell (COMP_CFG / COMP / COMP_MONTHS /
  COMP_TOTAL / F2026) bleibt unangetastet.

## NICHT im Repo (bleibt immer lokal, per .gitignore geschützt)
- `.awin-credentials` (AWIN API Token)
- `.tuic_9127_daily_data.json` (absolute €-Rohdaten)
- `tuic_9127_abs_data.json` (absolute €-Daten)

## Wiederherstellen nach Verlust des lokalen Ordners
    REPO="$HOME/Documents/Claude/Projects/wpp-templates"
    WM="$HOME/Documents/Claude/Projects/WPP Media"
    cd "$REPO" && git pull
    mkdir -p "$WM"
    cp "$REPO/tools/tuic_9127_daily_fetch.py" "$WM/.tuic_9127_daily_fetch.py"
    cp "$REPO/tools/tuic_9127_regen_abs.py"  "$WM/.tuic_9127_regen_abs.py"
    cp "$REPO/tools/tuic_9127_bake.py"       "$WM/.tuic_9127_bake.py"
    cp "$REPO/tuic-9127-yoy-tool.html"       "$WM/tuic-9127-yoy-tool.html"
    # .awin-credentials manuell wieder einlegen — Token ist NICHT im Repo!

## Refresh-Lauf (kompletter Ablauf)
    WM="$HOME/Documents/Claude/Projects/WPP Media"
    REPO="$HOME/Documents/Claude/Projects/wpp-templates"
    cd "$WM"
    /usr/bin/python3 .tuic_9127_daily_fetch.py
    /usr/bin/python3 .tuic_9127_regen_abs.py > /dev/null
    /usr/bin/python3 .tuic_9127_bake.py
    cp "$WM/tuic-9127-yoy-tool.html" "$REPO/tuic-9127-yoy-tool.html"
    cd "$REPO" && git add tuic-9127-yoy-tool.html && \
      git commit -m "Auto-Refresh AWIN-Daten 9127" && git push

GitHub Pages braucht danach 1–2 Min bis die Live-Seite aktualisiert ist.
