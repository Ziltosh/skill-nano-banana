# Feature Specification: Image Aspect Ratio & Size

**Feature Branch**: `004-image-ratio-size`
**Created**: 2026-03-18
**Status**: Draft
**Input**: User description: "Ajouter des flags aspect ratio et taille pour les images générées. Aspect ratio configurable (16/9 par défaut). Taille 1k, 2k ou 4k (1k par défaut)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Choisir l'aspect ratio de l'image (Priority: P1)

L'utilisateur invoque `/generate-image "un paysage" --ratio 16:9` pour générer une image au format 16:9. S'il ne spécifie aucun ratio, l'image est générée en 16:9 par défaut. Il peut aussi choisir d'autres ratios courants comme 1:1 (carré), 4:3, 3:2, ou 9:16 (portrait).

**Why this priority**: L'aspect ratio est le contrôle de format le plus fondamental. Il détermine la forme de l'image et impacte directement son utilisation (bannière, post social, portrait, etc.).

**Independent Test**: Invoquer la commande avec différents ratios et vérifier que les images générées respectent les proportions demandées.

**Acceptance Scenarios**:

1. **Given** une clé API valide, **When** l'utilisateur invoque `/generate-image "un paysage"` sans flag `--ratio`, **Then** l'image est générée au format 16:9 par défaut.
2. **Given** une clé API valide, **When** l'utilisateur invoque `/generate-image "un portrait" --ratio 9:16`, **Then** l'image est générée au format portrait 9:16.
3. **Given** une clé API valide, **When** l'utilisateur invoque `/generate-image "un logo" --ratio 1:1`, **Then** l'image est générée au format carré.
4. **Given** un ratio non supporté, **When** l'utilisateur invoque `/generate-image "test" --ratio 7:3`, **Then** un message d'erreur liste les ratios disponibles.

---

### User Story 2 - Choisir la taille de l'image (Priority: P2)

L'utilisateur invoque `/generate-image "un paysage" --size 2k` pour générer une image en résolution 2k. Les tailles disponibles sont 1k, 2k et 4k. Par défaut, la taille est 1k si aucun flag n'est spécifié.

**Why this priority**: La taille complète le contrôle de format offert par le ratio. Elle est essentielle pour les usages nécessitant une haute résolution (impression, fonds d'écran).

**Independent Test**: Invoquer la commande avec différentes tailles et vérifier que la résolution de l'image correspond.

**Acceptance Scenarios**:

1. **Given** une clé API valide, **When** l'utilisateur invoque `/generate-image "un paysage"` sans flag `--size`, **Then** l'image est générée en résolution 1k par défaut.
2. **Given** une clé API valide, **When** l'utilisateur invoque `/generate-image "un paysage" --size 4k`, **Then** l'image est générée en résolution 4k.
3. **Given** une taille non supportée, **When** l'utilisateur invoque `/generate-image "test" --size 8k`, **Then** un message d'erreur liste les tailles disponibles (1k, 2k, 4k).

---

### User Story 3 - Combiner ratio, taille et autres options (Priority: P3)

L'utilisateur invoque `/generate-image "un poster" --ratio 9:16 --size 4k --style ghibli --text "CONCERT"` pour combiner tous les flags disponibles. Tous les flags doivent fonctionner ensemble sans conflit.

**Why this priority**: Assure la compatibilité avec les fonctionnalités existantes. Nécessite que ratio et taille fonctionnent individuellement.

**Independent Test**: Invoquer la commande avec plusieurs flags combinés et vérifier que tous s'appliquent correctement.

**Acceptance Scenarios**:

1. **Given** une clé API valide, **When** l'utilisateur invoque `/generate-image "un poster" --ratio 9:16 --size 2k --style ghibli`, **Then** l'image est en format portrait 9:16, résolution 2k, style Ghibli.
2. **Given** une clé API valide, **When** l'utilisateur invoque `/generate-image "un logo" --ratio 1:1 --size 4k --text "BRAND"`, **Then** l'image est carrée, en 4k, avec le texte "BRAND" visible.

---

### Edge Cases

- Que se passe-t-il si l'utilisateur fournit un ratio invalide (ex: `--ratio abc`) ? Le système DOIT afficher un message d'erreur avec le format attendu et la liste des ratios supportés.
- Que se passe-t-il si l'utilisateur fournit une taille invalide (ex: `--size 3k`) ? Le système DOIT afficher un message d'erreur listant les tailles valides (1k, 2k, 4k).
- Que se passe-t-il si le ratio et la taille sont incompatibles avec les capacités de l'API ? Le système DOIT transmettre les paramètres et laisser l'API gérer la contrainte, en relayant tout message d'erreur de manière lisible.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT accepter un flag optionnel `--ratio` dans la commande `/generate-image`
- **FR-002**: Le système DOIT utiliser 16:9 comme ratio par défaut lorsque `--ratio` n'est pas spécifié
- **FR-003**: Le système DOIT supporter au minimum les ratios suivants : 16:9, 9:16, 1:1, 4:3, 3:2
- **FR-004**: Le système DOIT rejeter les ratios non supportés avec un message d'erreur listant les valeurs valides
- **FR-005**: Le système DOIT accepter un flag optionnel `--size` dans la commande `/generate-image`
- **FR-006**: Le système DOIT utiliser 1k comme taille par défaut lorsque `--size` n'est pas spécifié
- **FR-007**: Le système DOIT supporter les tailles suivantes : 1k, 2k, 4k
- **FR-008**: Le système DOIT rejeter les tailles non supportées avec un message d'erreur listant les valeurs valides
- **FR-009**: Le système DOIT transmettre le ratio et la taille à l'API de génération d'images
- **FR-010**: Le système DOIT être compatible avec tous les flags existants (`--style`, `--model`, `--include`, `--images`, `--text`)
- **FR-011**: Le système DOIT journaliser le ratio et la taille utilisés dans l'historique des générations

### Assumptions

- Les ratios sont exprimés au format `W:H` (ex: 16:9, 1:1)
- Les tailles 1k, 2k et 4k correspondent aux résolutions supportées par l'API de génération d'images
- Le ratio et la taille par défaut s'appliquent à toutes les générations, y compris celles avec images de référence
- L'API de génération d'images supporte la spécification de ratio et taille comme paramètres distincts

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: L'utilisateur peut contrôler l'aspect ratio de l'image en ajoutant un seul flag `--ratio` à sa commande
- **SC-002**: L'utilisateur peut contrôler la taille de l'image en ajoutant un seul flag `--size` à sa commande
- **SC-003**: Les images générées sans flags ratio/taille sont systématiquement en 16:9 et 1k (valeurs par défaut prévisibles)
- **SC-004**: 100% des combinaisons ratio/taille invalides produisent un message d'erreur clair listant les options valides
- **SC-005**: L'ajout des flags `--ratio` et `--size` n'altère pas le fonctionnement des flags existants (rétrocompatibilité totale)
