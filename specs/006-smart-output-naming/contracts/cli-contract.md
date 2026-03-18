# CLI Contract: Smart Output Naming

## Nouveau paramètre

```
--name TEXT    Nom forcé pour le fichier de sortie (optionnel)
```

## Exemples d'invocation et noms de sortie attendus

### Priorité 1 : `--name` (forçage)

```bash
# Nom simple
generate "un chat" --name "resultat-final"
# → out/resultat-final.png

# Nom avec caractères spéciaux (slugifié)
generate "un chat" --name "Mon Logo V2!"
# → out/mon-logo-v2.png

# --name prend priorité sur --images
generate "modifie ce logo" --images logo.png --name "nouveau-logo"
# → out/nouveau-logo.png

# Extension image retirée automatiquement
generate "un chat" --name "fichier.png"
# → out/fichier.png (pas out/fichier-png.png)
```

### Priorité 2 : Image de référence unique

```bash
# Une seule image de référence
generate "rends ce logo plus moderne" --images mon-logo.png
# → out/mon-logo.png

# Image dans un sous-dossier
generate "améliore cette photo" --images photos/vacances-2024.jpg
# → out/vacances-2024.png
```

### Priorité 3 : Mots-clés du prompt

```bash
# Prompt court
generate "un chat sur un skateboard"
# → out/chat-skateboard.png

# Prompt long
generate "un magnifique paysage de montagne enneigée au coucher du soleil avec des reflets dorés sur un lac cristallin"
# → out/paysage-montagne-coucher-soleil.png (max 4 mots-clés)

# Plusieurs images de référence (fallback mots-clés)
generate "fusionne ces deux animaux" --images chat.png chien.png
# → out/fusionne-animaux.png
```

### Erreurs

```bash
# --name vide
generate "un chat" --name ""
# → erreur, code INVALID_ARGS

# --name avec uniquement des caractères spéciaux
generate "un chat" --name "@#$"
# → erreur, code INVALID_ARGS
```

## Sortie JSON

Pas de changement de structure. Le champ `path` reflète le nom résolu :

```json
{
  "success": true,
  "path": "/absolute/path/out/mon-logo.png",
  "prompt": "...",
  "style": null,
  "model": "...",
  "text": null,
  "ratio": "16:9",
  "size": "1k"
}
```
