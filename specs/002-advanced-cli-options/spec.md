# Feature Specification: Options CLI avancées

**Feature Branch**: `002-advanced-cli-options`
**Created**: 2026-03-18
**Status**: Draft
**Input**: User description: "Ajout options avancées: sélection du modèle, inclusion de ressources par tag, validation des arguments CLI"

## Clarifications

### Session 2026-03-18

- Q: Quelle structure pour le fichier meta.json des tags de ressources ? → A: Minimaliste — un seul champ `{"prompt": "texte contextuel"}`.
- Q: Où stocker la configuration des modèles (alias → identifiant) ? → A: Fichier dédié `models.json` à la racine du projet, même pattern que `styles.json`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Valider les arguments avant exécution (Priority: P1)

L'utilisateur invoque `/generate-image` avec des arguments structurés en format CLI standard (préfixés par `--`). Avant toute exécution, le système vérifie la syntaxe des arguments : flags reconnus, valeurs requises présentes, format correct. En cas d'erreur de syntaxe, un message d'aide clair est affiché sans appel à l'API.

**Why this priority**: Fondation pour toutes les autres options. Sans validation, les nouvelles options ne peuvent pas fonctionner de manière fiable. Affecte aussi les options existantes (`--style`).

**Independent Test**: Invoquer la commande avec des arguments invalides (flag inconnu, valeur manquante) et vérifier que l'erreur est détectée avant tout appel réseau.

**Acceptance Scenarios**:

1. **Given** la commande configurée, **When** l'utilisateur invoque `/generate-image "un chat" --style ghibli`, **Then** les arguments sont correctement parsés et la génération s'exécute normalement.
2. **Given** la commande configurée, **When** l'utilisateur invoque `/generate-image "un chat" --unknown-flag`, **Then** un message d'erreur indique que le flag est inconnu et liste les flags disponibles.
3. **Given** la commande configurée, **When** l'utilisateur invoque `/generate-image "un chat" --style` (sans valeur), **Then** un message d'erreur indique que `--style` requiert une valeur.
4. **Given** la commande configurée, **When** l'utilisateur invoque `/generate-image` (sans prompt), **Then** un message d'aide affiche la syntaxe attendue avec des exemples.

---

### User Story 2 - Choisir le modèle de génération (Priority: P2)

L'utilisateur ajoute `--model <alias>` à sa commande pour spécifier quel modèle utiliser pour la génération. Un modèle par défaut est utilisé si l'option est omise. La liste des modèles disponibles est configurable et extensible au fur et à mesure que de nouveaux modèles sortent.

**Why this priority**: Permet d'exploiter les modèles les plus récents ou les plus adaptés selon le besoin (qualité vs vitesse vs coût).

**Independent Test**: Invoquer la commande avec `--model` suivi d'un nom de modèle valide, vérifier que le modèle utilisé est bien celui spécifié. Tester avec un modèle inconnu pour vérifier le message d'erreur.

**Acceptance Scenarios**:

1. **Given** plusieurs modèles configurés, **When** l'utilisateur invoque `/generate-image "un paysage" --model pro`, **Then** la génération utilise le modèle correspondant à l'alias "pro".
2. **Given** un modèle par défaut configuré, **When** l'utilisateur invoque `/generate-image "un paysage"` sans `--model`, **Then** le modèle par défaut est utilisé.
3. **Given** un alias de modèle inexistant, **When** l'utilisateur invoque `/generate-image "test" --model inexistant`, **Then** un message d'erreur liste les modèles disponibles avec leurs alias.
4. **Given** un nouveau modèle vient de sortir, **When** l'utilisateur ajoute son identifiant dans la configuration, **Then** il est immédiatement utilisable via `--model`.

---

### User Story 3 - Inclure des ressources par tag (Priority: P3)

L'utilisateur ajoute `--include <tag>` à sa commande pour injecter automatiquement des images de référence stockées dans un dossier dédié. Par exemple, `--include face-kim` charge toutes les images du dossier `resources/face-kim/` et les envoie à l'API en complément du prompt. Un fichier de métadonnées associé au tag peut enrichir le prompt avec des instructions contextuelles (ex: "cette personne doit apparaître dans l'image").

**Why this priority**: Fonctionnalité puissante mais qui repose sur les deux user stories précédentes (validation des arguments + appel API fonctionnel).

**Independent Test**: Créer un dossier de ressources avec des images et un fichier de métadonnées, invoquer la commande avec `--include`, vérifier que les images sont envoyées à l'API et que le prompt est enrichi.

**Acceptance Scenarios**:

1. **Given** un dossier `resources/face-kim/` contenant des images et un fichier de métadonnées avec un prompt contextuel, **When** l'utilisateur invoque `/generate-image "portrait en studio" --include face-kim`, **Then** les images du dossier sont envoyées comme référence ET le prompt contextuel du fichier de métadonnées est ajouté au prompt de l'utilisateur.
2. **Given** un tag inexistant, **When** l'utilisateur invoque `/generate-image "test" --include inexistant`, **Then** un message d'erreur indique que le tag n'existe pas et liste les tags disponibles.
3. **Given** un dossier de ressources valide, **When** l'utilisateur combine `--include` avec `--style`, **Then** les deux enrichissements sont cumulés (images de référence + style).
4. **Given** un dossier de ressources vide (sans images), **When** l'utilisateur invoque `/generate-image "test" --include tag-vide`, **Then** un message d'erreur indique que le dossier ne contient aucune image.
5. **Given** un tag valide, **When** l'utilisateur invoque la commande avec plusieurs `--include`, **Then** les ressources de tous les tags sont combinées.

---

### Edge Cases

- Que se passe-t-il si l'utilisateur combine `--include` et `--images` (images du chat) ? Les deux sources d'images DOIVENT être fusionnées et envoyées ensemble à l'API.
- Que se passe-t-il si le nombre total d'images (include + chat) dépasse la limite de l'API ? Le système DOIT afficher un avertissement clair avec la limite et le nombre d'images fournies.
- Que se passe-t-il si le fichier de métadonnées d'un tag est absent ? Le système DOIT fonctionner normalement en utilisant uniquement les images, sans enrichissement de prompt.
- Que se passe-t-il si un alias de modèle pointe vers un identifiant invalide ? Le système DOIT capturer l'erreur de l'API et afficher un message indiquant que le modèle n'est pas disponible.
- Que se passe-t-il si les arguments contiennent des caractères spéciaux ou des guillemets ? Le parseur DOIT gérer correctement l'échappement standard.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT valider tous les arguments CLI avant toute exécution (appel API, lecture de fichiers)
- **FR-002**: Le système DOIT afficher un message d'erreur clair listant les flags disponibles si un flag inconnu est utilisé
- **FR-003**: Le système DOIT afficher un message d'erreur si un flag requérant une valeur est utilisé sans valeur
- **FR-004**: Le système DOIT supporter l'option `--model <alias>` pour choisir le modèle de génération
- **FR-005**: Le système DOIT utiliser un modèle par défaut si `--model` est omis
- **FR-006**: Le système DOIT permettre la configuration des modèles disponibles (alias vers identifiant) dans un fichier de configuration
- **FR-007**: Le système DOIT lister les modèles disponibles quand un alias inconnu est fourni
- **FR-008**: Le système DOIT supporter l'option `--include <tag>` pour injecter des ressources depuis un dossier dédié
- **FR-009**: Le système DOIT charger toutes les images d'un dossier de ressources identifié par le tag
- **FR-010**: Le système DOIT lire un fichier de métadonnées optionnel associé au tag pour enrichir le prompt
- **FR-011**: Le système DOIT lister les tags disponibles quand un tag inconnu est fourni
- **FR-012**: Le système DOIT permettre la combinaison de plusieurs `--include` dans une même commande
- **FR-013**: Le système DOIT fusionner les images provenant de `--include` et `--images` (chat) sans conflit
- **FR-014**: Le système DOIT afficher la syntaxe attendue avec des exemples quand la commande est invoquée sans arguments

### Key Entities

- **Model Config**: Un alias court (ex: "pro", "flash") associé à un identifiant de modèle complet. Stocké dans `models.json` à la racine du projet. Un modèle est marqué comme défaut.
- **Resource Tag**: Un identifiant textuel (kebab-case) correspondant à un sous-dossier de `resources/`. Contient des images et optionnellement un fichier `meta.json`.
- **Resource Metadata**: Fichier `meta.json` minimaliste dans un dossier de ressources, contenant un seul champ `prompt` avec le texte contextuel à ajouter au prompt (ex: `{"prompt": "cette personne doit apparaître dans l'image"}`).

### Assumptions

- Les dossiers de ressources sont organisés sous `resources/` à la racine du projet
- Le fichier de métadonnées d'un tag est au format JSON (`meta.json`) dans le dossier du tag
- Les modèles sont configurés dans un fichier dédié `models.json` à la racine du projet
- Les formats d'images supportés dans les dossiers de ressources sont PNG, JPG et WEBP
- La limite du nombre d'images envoyées à l'API est déterminée par les contraintes du modèle utilisé

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% des erreurs d'arguments (flag inconnu, valeur manquante, tag inexistant, modèle inexistant) sont détectées et signalées avant tout appel réseau
- **SC-002**: L'utilisateur peut changer de modèle en ajoutant un seul flag `--model` à sa commande existante
- **SC-003**: L'utilisateur peut inclure un pack de ressources en ajoutant `--include <tag>`, sans modifier le reste de sa commande
- **SC-004**: Les options `--model`, `--include`, `--style` et `--images` sont combinables librement dans n'importe quel ordre
- **SC-005**: L'ajout d'un nouveau modèle ou d'un nouveau pack de ressources ne nécessite aucune modification de code — uniquement de la configuration ou des fichiers
