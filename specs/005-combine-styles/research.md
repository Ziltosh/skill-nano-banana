# Research: Combine Multiple Styles

**Date**: 2026-03-18
**Branch**: `005-combine-styles`

## Approche pour le flag --style répétable

**Decision**: Changer `--style` de `parser.add_argument("--style")` à `parser.add_argument("--style", action="append", default=[])`, identique au pattern déjà utilisé pour `--include`.

**Rationale**: Le pattern `action="append"` est déjà en place pour `--include` dans le même fichier. C'est le mécanisme standard d'argparse pour les flags répétables. Pas besoin de syntaxe spéciale (virgules, etc.).

**Alternatives considered**:
- Syntaxe à virgules (`--style "ghibli,pixel-art"`) : rejeté car moins intuitif et nécessite du parsing supplémentaire
- Flag séparé `--styles` (pluriel) : rejeté car casse la rétrocompatibilité et ajoute de la confusion

## Concaténation des textes de styles

**Decision**: Les textes de style sont concaténés séparés par `, ` dans le prompt enrichi, dans l'ordre de saisie.

**Rationale**: C'est le même séparateur déjà utilisé pour joindre le prompt et le style unique. L'ordre de saisie est prévisible pour l'utilisateur.

## Changement du type du champ style

**Decision**: Le champ `style` dans le résultat JSON et l'historique passe de `string | null` à `list[string] | null`. `null` quand aucun style n'est spécifié, liste d'un élément pour un seul style, liste de N éléments pour N styles.

**Rationale**: Une liste est le type naturel pour des valeurs multiples. Le `null` est préservé pour le cas sans style (pas de liste vide).

**Alternatives considered**:
- Garder string avec virgules : rejeté car perd la structure et complique le parsing côté consommateur
- Liste vide au lieu de null : rejeté car change le comportement existant pour le cas sans style

## Validation

**Decision**: Valider chaque style individuellement avant l'appel API. Si un style est invalide, la commande échoue immédiatement avec le message d'erreur existant.

**Rationale**: Fail-fast — pas de raison de générer une image si un style est manquant. L'erreur indique quel style est invalide.
