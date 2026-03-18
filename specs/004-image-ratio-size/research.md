# Research: Image Aspect Ratio & Size

**Date**: 2026-03-18
**Branch**: `004-image-ratio-size`

## Paramètres API Gemini pour ratio et taille

**Decision**: Utiliser `types.ImageConfig` avec les paramètres `aspect_ratio` et `image_size` dans `GenerateContentConfig`.

**Rationale**: L'API Gemini expose ces paramètres via `types.ImageConfig`, un objet imbriqué dans `GenerateContentConfig.image_config`. C'est le mécanisme officiel du SDK google-genai.

**Alternatives considered**: Injection via le prompt (ex: "generate in 16:9 format") — rejeté car l'API expose des paramètres dédiés plus fiables.

### Configuration API

```python
config = types.GenerateContentConfig(
    response_modalities=["Text", "Image"],
    image_config=types.ImageConfig(
        aspect_ratio="16:9",
        image_size="2K"
    )
)
```

## Valeurs supportées pour aspect_ratio

**Decision**: Supporter les ratios suivants comme valeurs utilisateur : 16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3, 4:5, 5:4.

**Rationale**: L'API supporte : 1:1, 1:4, 1:8, 2:3, 3:2, 3:4, 4:1, 4:3, 4:5, 5:4, 8:1, 9:16, 16:9, 21:9. On expose un sous-ensemble des plus courants. Les valeurs API utilisent le format `W:H` (string), identique au format utilisateur.

**Alternatives considered**: Exposer tous les ratios API — rejeté pour simplifier l'UX, les ratios exotiques (1:8, 8:1, 4:1) ont peu d'usage courant. L'utilisateur peut toujours demander un ajout futur.

## Valeurs supportées pour image_size

**Decision**: Mapper les valeurs utilisateur minuscules vers les valeurs API majuscules : `1k` → `"1K"`, `2k` → `"2K"`, `4k` → `"4K"`.

**Rationale**: L'API exige des majuscules (`"1K"`, `"2K"`, `"4K"`). L'utilisateur saisit naturellement en minuscules (`1k`, `2k`, `4k`). Le mapping est trivial (`.upper()`).

**Alternatives considered**:
- Exiger les majuscules côté utilisateur — rejeté car mauvaise UX
- Supporter `"512"` — rejeté car limité au modèle Gemini 3.1 Flash Image, hors scope

## Valeurs par défaut

**Decision**: `--ratio` par défaut : `16:9`. `--size` par défaut : `1k`.

**Rationale**: Conforme à la demande utilisateur. Le 16:9 est le format le plus courant pour les images génératives. Le 1k est la résolution par défaut de l'API.
