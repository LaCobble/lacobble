# Police intégrée

Les SVG utilisent `embedded_font_css()` dans `scripts/lib/svg_utils.py`,
qui intègre en base64 les deux fichiers de ce dossier :

```
fonts/JetBrainsMono-Regular.woff2
fonts/JetBrainsMono-Bold.woff2
```

**JetBrains Mono**, licence SIL Open Font License 1.1 (voir `OFL.txt`).
Si les fichiers manquent, le script retombe sur la pile système
(`SF Mono` / `Cascadia Code` / `Consolas`).

Les fichiers sont réduits aux caractères latins (ASCII, Latin-1, `œ`,
`’`, `…`, tirets) : ~13 Ko chacun au lieu de ~90, ce qui compte puisque
chaque SVG embarque les deux.

## Les regénérer

Depuis la [dernière release](https://github.com/JetBrains/JetBrainsMono/releases),
dossier `fonts/webfonts/` de l'archive :

```bash
pip install fonttools brotli
for w in Regular Bold; do
  pyftsubset JetBrainsMono-$w.woff2 \
    --unicodes="U+0020-007E,U+00A0-00FF,U+0152-0153,U+2013-2014,U+2019,U+2026" \
    --flavor=woff2 --layout-features='' \
    --output-file=fonts/JetBrainsMono-$w.woff2
done
```

Si un titre ou un libellé utilise un caractère hors de cette liste,
ajoute-le à `--unicodes`, sinon il s'affichera dans la police de secours.
