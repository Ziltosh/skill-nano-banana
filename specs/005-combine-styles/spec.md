# Feature Specification: Combine Multiple Styles

**Feature Branch**: `005-combine-styles`
**Created**: 2026-03-18
**Status**: Draft
**Input**: User description: "Permettre de combiner plusieurs styles sur une même génération d'image, par exemple une miniature YouTube en style Ghibli."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Appliquer plusieurs styles à une image (Priority: P1)

L'utilisateur invoque `/generate-image "un chat sur la lune" --style ghibli --style pixel-art` pour combiner deux styles sur la même image. Les textes des deux presets de style sont concaténés dans le prompt enrichi envoyé à l'API. Le flag `--style` peut être répété autant de fois que souhaité.

**Why this priority**: C'est la fonctionnalité centrale demandée — combiner des styles. L'exemple principal (miniature YouTube + Ghibli) nécessite exactement cette capacité.

**Independent Test**: Invoquer la commande avec deux flags `--style` et vérifier que le prompt enrichi contient les textes des deux styles. Vérifier que l'image générée reflète l'influence des deux styles.

**Acceptance Scenarios**:

1. **Given** les styles "ghibli" et "pixel-art" existants, **When** l'utilisateur invoque `/generate-image "un chat" --style ghibli --style pixel-art`, **Then** l'image est générée avec le prompt enrichi contenant les textes des deux styles et tous les styles sont journalisés dans l'historique.
2. **Given** un seul style "ghibli" existant, **When** l'utilisateur invoque `/generate-image "un chat" --style ghibli`, **Then** le comportement est identique à l'existant (rétrocompatibilité avec un seul style).
3. **Given** aucun style spécifié, **When** l'utilisateur invoque `/generate-image "un chat"`, **Then** l'image est générée normalement sans enrichissement de style (rétrocompatibilité).
4. **Given** les styles "ghibli" et "inexistant", **When** l'utilisateur invoque `/generate-image "un chat" --style ghibli --style inexistant`, **Then** un message d'erreur indique que le style "inexistant" n'existe pas et liste les styles disponibles.

---

### User Story 2 - Combiner styles avec les autres options (Priority: P2)

L'utilisateur invoque `/generate-image "une miniature YouTube" --style ghibli --style pixel-art --text "NOUVEAU" --ratio 16:9 --size 2k` pour combiner plusieurs styles avec texte, ratio et taille. Tous les flags existants restent compatibles avec les styles multiples.

**Why this priority**: Assure la compatibilité avec toutes les fonctionnalités existantes. Nécessite que la combinaison de styles de base fonctionne (US1).

**Independent Test**: Invoquer la commande avec plusieurs styles et d'autres flags combinés, vérifier que tous s'appliquent correctement.

**Acceptance Scenarios**:

1. **Given** les styles "ghibli" et "pixel-art" existants, **When** l'utilisateur invoque `/generate-image "un poster" --style ghibli --style pixel-art --text "CONCERT" --ratio 9:16`, **Then** l'image est générée avec les deux styles, le texte et le ratio corrects.

---

### Edge Cases

- Que se passe-t-il si l'utilisateur spécifie le même style deux fois (`--style ghibli --style ghibli`) ? Le système DOIT accepter sans erreur et concaténer le texte du style deux fois (pas de dédoublonnage, le comportement est prévisible).
- Que se passe-t-il si un des styles est invalide et les autres valides ? Le système DOIT rejeter la commande avec un message d'erreur indiquant le style invalide, sans générer d'image (validation avant appel API).
- Que se passe-t-il si l'utilisateur passe un grand nombre de styles (ex: 10) ? Le système DOIT les accepter tous et les concaténer ; c'est à l'API de gérer la longueur du prompt.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le flag `--style` DOIT être répétable pour accepter plusieurs styles dans une même commande
- **FR-002**: Le système DOIT concaténer les textes de tous les styles spécifiés dans le prompt enrichi, dans l'ordre de saisie
- **FR-003**: Le système DOIT valider chaque style spécifié et rejeter la commande si un style est inconnu, en listant les styles disponibles
- **FR-004**: Le système DOIT rester compatible avec l'usage d'un seul `--style` (rétrocompatibilité)
- **FR-005**: Le système DOIT rester compatible avec l'absence de `--style` (rétrocompatibilité)
- **FR-006**: Le système DOIT journaliser tous les styles utilisés dans l'historique des générations
- **FR-007**: Le système DOIT être compatible avec tous les autres flags existants (`--text`, `--ratio`, `--size`, `--model`, `--include`, `--images`)

### Assumptions

- Les textes de styles sont concaténés dans l'ordre de saisie, séparés par une virgule
- L'historique journalise la liste de tous les styles appliqués (pas seulement le dernier)
- Le résultat JSON retourne la liste des styles dans le champ `style` (changement de type : string → liste de strings ou null)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: L'utilisateur peut combiner 2 styles ou plus en répétant le flag `--style` dans la même commande
- **SC-002**: Les images générées avec plusieurs styles reflètent visuellement l'influence de chaque style combiné
- **SC-003**: L'usage avec un seul `--style` ou sans `--style` fonctionne de manière identique au comportement actuel (rétrocompatibilité totale)
- **SC-004**: 100% des styles invalides dans une combinaison produisent un message d'erreur clair avant toute génération
