# Feature Specification: Image Text Overlay

**Feature Branch**: `003-image-text-overlay`
**Created**: 2026-03-18
**Status**: Draft
**Input**: User description: "Ajouter un paramètre pour insérer du texte sur l'image générée. Le texte indiqué doit apparaître tel quel sur l'image, en respectant la casse (majuscules/minuscules)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ajouter du texte sur une image générée (Priority: P1)

L'utilisateur invoque `/generate-image "un coucher de soleil" --text "VACANCES 2026"` pour générer une image avec du texte superposé. Le texte "VACANCES 2026" apparaît sur l'image finale exactement tel qu'il a été saisi, en majuscules. Le fichier résultant dans `out/` contient l'image avec le texte incrusté.

**Why this priority**: C'est la fonctionnalité centrale demandée — insérer du texte sur l'image. Constitue le MVP complet à elle seule.

**Independent Test**: Invoquer la commande avec un prompt et un flag `--text`, puis vérifier visuellement que le texte apparaît sur l'image générée en respectant la casse saisie.

**Acceptance Scenarios**:

1. **Given** une clé API Gemini valide, **When** l'utilisateur invoque `/generate-image "un paysage" --text "Hello World"`, **Then** l'image générée contient le texte "Hello World" visible et lisible, avec la casse respectée (H et W majuscules).
2. **Given** une clé API Gemini valide, **When** l'utilisateur invoque `/generate-image "un logo" --text "ACME CORP"`, **Then** le texte "ACME CORP" apparaît entièrement en majuscules sur l'image.
3. **Given** une clé API Gemini valide, **When** l'utilisateur invoque `/generate-image "une carte" --text "joyeux anniversaire"`, **Then** le texte apparaît entièrement en minuscules sur l'image.
4. **Given** une clé API Gemini valide, **When** l'utilisateur invoque `/generate-image "un paysage"` sans flag `--text`, **Then** l'image est générée normalement sans texte superposé (comportement existant inchangé).

---

### User Story 2 - Combiner texte avec style et autres options (Priority: P2)

L'utilisateur invoque `/generate-image "un poster" --text "CONCERT" --style pixel-art` pour générer une image stylisée avec du texte. Le flag `--text` fonctionne de manière combinée avec tous les autres flags existants (`--style`, `--model`, `--include`, `--images`).

**Why this priority**: Assure la compatibilité avec les fonctionnalités existantes. Nécessite que l'insertion de texte de base fonctionne (US1).

**Independent Test**: Invoquer la commande avec `--text` combiné à `--style`, vérifier que le style est appliqué et le texte présent sur l'image.

**Acceptance Scenarios**:

1. **Given** une clé API valide et un style "ghibli" existant, **When** l'utilisateur invoque `/generate-image "un château" --text "Bienvenue" --style ghibli`, **Then** l'image est générée dans le style Ghibli avec le texte "Bienvenue" visible.
2. **Given** une clé API valide, **When** l'utilisateur invoque `/generate-image "un logo" --text "BRAND" --model pro`, **Then** l'image est générée avec le modèle spécifié et le texte "BRAND" visible.

---

### Edge Cases

- Que se passe-t-il si le texte fourni est une chaîne vide (`--text ""`) ? Le système DOIT ignorer le flag et générer l'image normalement sans texte.
- Que se passe-t-il si le texte contient des caractères spéciaux (accents, émojis, ponctuation) ? Le système DOIT transmettre le texte tel quel à l'API, qui gère le rendu au mieux de ses capacités.
- Que se passe-t-il si le texte est très long ? Le système DOIT transmettre le texte tel quel ; c'est à l'API de gérer le placement et le dimensionnement.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT accepter un flag optionnel `--text` dans la commande `/generate-image`
- **FR-002**: Le système DOIT transmettre le texte fourni à l'API Gemini en l'intégrant dans le prompt de manière à ce qu'il apparaisse sur l'image générée
- **FR-003**: Le système DOIT préserver exactement la casse du texte fourni (majuscules, minuscules, casse mixte)
- **FR-004**: Le système DOIT être compatible avec tous les flags existants (`--style`, `--model`, `--include`, `--images`)
- **FR-005**: Le système DOIT ignorer le flag `--text` si la valeur fournie est une chaîne vide
- **FR-006**: Le système DOIT journaliser le texte utilisé dans l'historique des générations

### Assumptions

- Le texte est intégré dans le prompt envoyé à l'API Gemini via une instruction explicite (ex: "avec le texte 'XYZ' écrit sur l'image") plutôt que par une superposition en post-traitement
- L'API Gemini est capable de générer des images contenant du texte lisible lorsqu'elle reçoit une instruction appropriée dans le prompt
- Le positionnement, la taille et la police du texte sont déterminés par l'API Gemini (pas de contrôle fin côté utilisateur pour cette version)
- Les caractères spéciaux et accents sont supportés dans la mesure des capacités de l'API

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: L'utilisateur peut ajouter du texte sur une image en ajoutant un seul flag `--text` à sa commande existante
- **SC-002**: Le texte affiché sur l'image respecte 100% de la casse saisie par l'utilisateur (majuscules restent majuscules, minuscules restent minuscules)
- **SC-003**: L'ajout du flag `--text` n'altère pas le fonctionnement des autres flags existants
- **SC-004**: La génération sans flag `--text` fonctionne de manière identique au comportement actuel (rétrocompatibilité totale)
