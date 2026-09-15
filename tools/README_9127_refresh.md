# TUIC 9127 YoY-Tool — Auto-Refresh

Reproduzierbares Tooling für das öffentliche Mein-Schiff-DACH-9127-YoY-Tool.
Liegt hier im GitHub-Repo, damit es sowohl lokal als auch automatisiert läuft.

## Automatischer nächtlicher Refresh (GitHub Actions)

`.github/workflows/refresh-tuic-9127.yml` zieht jede Nacht (02:15 UTC) automatisch
die aktuellen AWIN-Daten für 2025 und 2026, netto (Stornos raus, exkl. Payback
426667+469409), und aktualisiert `tuic-9127-yoy-tool.html` per Commit. Damit
basiert auch 2025 immer auf dem aktuellen Live-Stand (bestätigt + pending, minus
inzwischen erfolgter Stornos) statt auf einem eingefrorenen Wert.

- Läuft mit dem Repo-Secret `AWIN_API_TOKEN` (verschlüsselt hinterlegt, taucht
  nirgendwo im Code auf). Secret erneuern: `gh secret set AWIN_API_TOKEN --repo
  NickyNikaa/wpp-templates < token.txt`
- Manuell anstoßen: `gh workflow run refresh-tuic-9127.yml --repo
  NickyNikaa/wpp-templates` oder über den "Run workflow"-Button im Actions-Tab
  auf GitHub.
- Läuft nur wenn nötig: committet nur, wenn sich der `DATA`-Block tatsächlich
  geändert hat.
- Rate-Limit: AWIN erlaubt max. 20 Requests/Minute; das Fetch-Script wartet
  automatisch zwischen den Monats-Chunks und retried einmal bei HTTP 429.
- Das Kompensationsmodell für die Tracking-Ausfälle Jan/Apr/Mai 2026 (COMP_CFG
  / COMP / COMP_MONTHS / COMP_TOTAL / F2026, direkt im HTML) bleibt von diesem
  Refresh unberührt — es wird weiterhin zusätzlich zu den echten AWIN-Zahlen
  angewendet.

## Was liegt hier

- `tuic_9127_daily_fetch.py` — zieht tägliche Umsätze Advertiser 9127 via AWIN
  Transactions-API, exkl. Payback (426667+469409), netto (declined raus).
  Lokal (Mac): schreibt `.tuic_9127_daily_data.json`, Token aus
  `.awin-credentials`. In CI: Pfad über `DAILY_OUT`, Token aus
  `AWIN_API_TOKEN`-Umgebungsvariable (Secret).
- `tuic_9127_regen_abs.py` — baut `tuic_9127_abs_data.json` (Ziele 2025 = 24,5 Mio,
  2026 = 30,7 Mio; corr-Block; d2025/d2026 als {"MM-DD": wert}). Pfade lokal wie
  gehabt, in CI über `WPP_BASE` / `DAILY_SRC` / `ABS_DST` überschreibbar.
- `tuic_9127_bake.py` — ersetzt NUR den `const DATA = {…};`-Block in
  `tuic-9127-yoy-tool.html`. Kompensationsmodell bleibt unangetastet. Pfade in
  CI über `HTML_PATH` / `ABS_DATA` überschreibbar.

Alle drei Scripts verhalten sich bei fehlenden Umgebungsvariablen exakt wie
vorher (lokale Mac-Pfade, `.awin-credentials`-Datei) — der lokale manuelle
Refresh-Workflow unten funktioniert unverändert.

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

## Manueller Refresh-Lauf (falls mal gebraucht, sonst übernimmt das die Action)

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
