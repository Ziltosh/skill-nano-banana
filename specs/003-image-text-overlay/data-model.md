# Data Model: Image Text Overlay

**Date**: 2026-03-18
**Branch**: `003-image-text-overlay`

## Modifications aux entités existantes

### GenerationLogEntry (modification)

Ajout d'un champ optionnel `text` à l'entité existante.

| Field      | Type     | Description                                        | Changement |
| ---------- | -------- | -------------------------------------------------- | ---------- |
| timestamp  | string   | Date/heure ISO 8601                                | Existant   |
| prompt     | string   | Prompt texte original de l'utilisateur             | Existant   |
| style      | string?  | Nom du style appliqué (null si aucun)              | Existant   |
| model      | string?  | Identifiant du modèle utilisé                      | Existant   |
| **text**   | **string?** | **Texte à afficher sur l'image (null si aucun)** | **Nouveau** |
| output     | string   | Chemin du fichier généré                           | Existant   |
| success    | boolean  | True si la génération a réussi                     | Existant   |
| error      | string?  | Message d'erreur si échec                          | Existant   |

**Rétrocompatibilité** : Le champ `text` est optionnel (null par défaut). Les entrées existantes dans `history.jsonl` restent valides car le champ est simplement absent.

## Aucune nouvelle entité

La fonctionnalité ne crée pas de nouvelle entité. Elle étend le flux existant en ajoutant une instruction de texte dans le prompt enrichi.

## Flux modifié

```
1. Input → Prompt texte + (optionnel) --text + (optionnel) images + (optionnel) style
2. Processing → Enrichissement du prompt :
   prompt + instruction texte + resource prompts + style → Appel API Gemini
3. Output → Sauvegarde image → Log (avec champ text) → Retour chemin
```
