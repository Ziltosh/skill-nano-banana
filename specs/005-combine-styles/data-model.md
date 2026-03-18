# Data Model: Combine Multiple Styles

**Date**: 2026-03-18
**Branch**: `005-combine-styles`

## Modifications aux entités existantes

### GenerationLogEntry (modification)

Changement de type du champ `style`.

| Field      | Type             | Description                              | Changement |
| ---------- | ---------------- | ---------------------------------------- | ---------- |
| timestamp  | string           | Date/heure ISO 8601                      | Existant   |
| prompt     | string           | Prompt texte original                    | Existant   |
| **style**  | **list[string]?** | **Liste des styles appliqués (null si aucun)** | **Modifié** (était string?) |
| model      | string?          | Identifiant du modèle                    | Existant   |
| text       | string?          | Texte à afficher                         | Existant   |
| ratio      | string?          | Aspect ratio                             | Existant   |
| size       | string?          | Taille                                   | Existant   |
| output     | string           | Chemin du fichier                        | Existant   |
| success    | boolean          | Succès de la génération                  | Existant   |
| error      | string?          | Message d'erreur                         | Existant   |

**Rétrocompatibilité** : Les anciennes entrées dans `history.jsonl` ont `style` comme string ou null. Les nouvelles entrées auront une liste ou null. Les consommateurs doivent gérer les deux formats lors de la lecture de l'historique existant.

## Aucune nouvelle entité

La fonctionnalité modifie le flux existant sans créer de nouvelle entité.
