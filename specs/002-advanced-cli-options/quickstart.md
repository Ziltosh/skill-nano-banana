# Quickstart: Options CLI avancées

## Prérequis

- Feature 001 (Gemini Image Generation Skill) installée et fonctionnelle
- Clé API Gemini configurée dans `.env`

## Nouvelles options

### Choisir un modèle

```
/generate-image "un paysage" --model pro
```

Modèles disponibles (configurables dans `models.json`) :
- `flash` (défaut) — rapide et économique
- `pro` — qualité supérieure
- `nano` — dernière génération, optimisé vitesse

### Inclure des ressources

1. Créer un dossier de ressources :

```bash
mkdir -p resources/face-kim
# Ajouter des images de la personne
cp photo1.png photo2.jpg resources/face-kim/
```

2. Optionnel — ajouter des métadonnées :

```bash
echo '{"prompt": "cette personne doit apparaître dans la scène"}' > resources/face-kim/meta.json
```

3. Utiliser le tag :

```
/generate-image "portrait en studio" --include face-kim
```

### Combiner les options

Toutes les options sont combinables :

```
/generate-image "portrait artistique" --model pro --style ghibli --include face-kim
```

### Ajouter un nouveau modèle

Éditer `models.json` :

```json
{
  "flash": "gemini-2.5-flash-image",
  "pro": "gemini-3-pro-image-preview",
  "nano": "gemini-3.1-flash-image-preview",
  "nouveau": "gemini-4.0-whatever-preview",
  "_default": "flash"
}
```

Le nouveau modèle est immédiatement utilisable via `--model nouveau`.

## Vérification

1. Tester la validation : `/generate-image "test" --unknown-flag` → erreur claire
2. Tester le modèle : `/generate-image "test" --model pro` → utilise le modèle pro
3. Tester les ressources : créer un dossier dans `resources/`, ajouter des images, puis `/generate-image "test" --include <tag>`

## Tests

```bash
uv run pytest tests/ -v
```
