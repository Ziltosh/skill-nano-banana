# Data Model: Image Aspect Ratio & Size

**Date**: 2026-03-18
**Branch**: `004-image-ratio-size`

## Modifications aux entités existantes

### GenerationLogEntry (modification)

Ajout de deux champs optionnels `ratio` et `size`.

| Field      | Type     | Description                                        | Changement |
| ---------- | -------- | -------------------------------------------------- | ---------- |
| timestamp  | string   | Date/heure ISO 8601                                | Existant   |
| prompt     | string   | Prompt texte original de l'utilisateur             | Existant   |
| style      | string?  | Nom du style appliqué                              | Existant   |
| model      | string?  | Identifiant du modèle utilisé                      | Existant   |
| text       | string?  | Texte à afficher sur l'image                       | Existant   |
| **ratio**  | **string?** | **Aspect ratio utilisé (ex: "16:9"), null = défaut** | **Nouveau** |
| **size**   | **string?** | **Taille utilisée (ex: "1k"), null = défaut**      | **Nouveau** |
| output     | string   | Chemin du fichier généré                           | Existant   |
| success    | boolean  | True si la génération a réussi                     | Existant   |
| error      | string?  | Message d'erreur si échec                          | Existant   |

**Rétrocompatibilité** : Les champs `ratio` et `size` sont optionnels. Les entrées existantes dans `history.jsonl` restent valides.

## Constantes de validation

### Ratios supportés

```
16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3, 4:5, 5:4
```

### Tailles supportées

| Valeur utilisateur | Valeur API |
|--------------------|------------|
| 1k                 | 1K         |
| 2k                 | 2K         |
| 4k                 | 4K         |

## Flux modifié

```
1. Input → Prompt + (opt) --ratio + (opt) --size + autres flags
2. Validation → Vérifier ratio ∈ SUPPORTED_RATIOS, size ∈ SUPPORTED_SIZES
3. Processing → Construire ImageConfig(aspect_ratio, image_size) → Appel API Gemini
4. Output → Sauvegarde image → Log (avec ratio/size) → Retour chemin
```
