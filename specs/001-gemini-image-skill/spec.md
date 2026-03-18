# Feature Specification: Gemini Image Generation Skill

**Feature Branch**: `001-gemini-image-skill`
**Created**: 2026-03-18
**Status**: Draft
**Input**: User description: "Skill Claude Code generate-image pour générer des images via l'API Gemini avec styles prédéfinis, nommage intelligent et historique"

## Clarifications

### Session 2026-03-18

- Q: Un preset de style est-il du texte simple ajouté au prompt, ou une structure avec champs séparés (description, termes à éviter, paramètres) ? → A: Texte simple — le style est une phrase concaténée au prompt avant envoi à l'API.
- Q: L'historique est-il consulté via une commande dédiée ou en lisant directement le fichier ? → A: Fichier lisible directement — pas de commande dédiée, l'utilisateur consulte le fichier d'historique manuellement ou via Claude.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Générer une image depuis un prompt texte (Priority: P1)

L'utilisateur tape `/generate-image "un chat astronaute sur la lune"` dans une conversation Claude Code. Le système envoie le prompt à l'API Gemini, récupère l'image générée, la sauvegarde dans le dossier `out/` avec un nom dérivé du prompt (ex: `chat-astronaute-sur-la-lune.png`), et confirme à l'utilisateur avec le chemin du fichier.

**Why this priority**: C'est la fonctionnalité centrale — sans génération d'image, rien d'autre n'a de sens. Constitue le MVP complet à elle seule.

**Independent Test**: Peut être testé en invoquant la commande avec un prompt simple et en vérifiant qu'un fichier image apparaît dans `out/`.

**Acceptance Scenarios**:

1. **Given** une clé API Gemini valide dans `.env` et le dossier `out/` absent, **When** l'utilisateur invoque `/generate-image "un paysage montagneux"`, **Then** le dossier `out/` est créé, une image est sauvegardée avec un nom lisible dérivé du prompt, et le chemin complet est affiché à l'utilisateur.
2. **Given** une clé API Gemini valide dans `.env`, **When** l'utilisateur invoque `/generate-image "un chat"`, **Then** le fichier généré porte un nom basé sur le contenu du prompt (ex: `un-chat.png`) et non un identifiant aléatoire.
3. **Given** aucune clé API configurée dans `.env`, **When** l'utilisateur invoque `/generate-image "test"`, **Then** un message d'erreur clair indique que la clé API est manquante et explique comment la configurer.
4. **Given** une clé API invalide ou expirée, **When** l'utilisateur invoque `/generate-image "test"`, **Then** un message d'erreur clair indique que l'authentification a échoué.

---

### User Story 2 - Générer une image en utilisant des images de référence (Priority: P2)

L'utilisateur fournit des images dans le contexte du chat (captures d'écran, photos, maquettes) et invoque `/generate-image "transforme ça en style aquarelle"`. Le système transmet les images du chat comme ressources d'entrée à l'API Gemini en plus du prompt texte, permettant la génération basée sur des références visuelles.

**Why this priority**: Différenciateur majeur — permet l'édition et la transformation d'images existantes, pas juste la génération from scratch.

**Independent Test**: Peut être testé en partageant une image dans le chat puis en invoquant la commande avec un prompt de transformation. Vérifier que l'image résultante reflète la référence.

**Acceptance Scenarios**:

1. **Given** une ou plusieurs images partagées dans le contexte du chat, **When** l'utilisateur invoque `/generate-image "rends cette image en pixel art"`, **Then** les images du chat sont envoyées à l'API comme ressources d'entrée et l'image générée reflète la transformation demandée.
2. **Given** aucune image dans le contexte du chat, **When** l'utilisateur invoque `/generate-image "un paysage"`, **Then** la génération fonctionne normalement à partir du prompt texte seul (comportement US1).

---

### User Story 3 - Appliquer un style prédéfini (Priority: P3)

L'utilisateur invoque `/generate-image "un château" --style ghibli` pour enrichir automatiquement son prompt avec des instructions de style prédéfinies. Le système dispose d'une bibliothèque de presets de styles (ex: ghibli, pixel-art, photo-réaliste, aquarelle) qui ajoutent des instructions au prompt avant envoi à l'API.

**Why this priority**: Améliore significativement l'expérience utilisateur en simplifiant la création de prompts complexes, mais requiert que la génération de base fonctionne (US1).

**Independent Test**: Invoquer la commande avec et sans flag `--style`, comparer les résultats pour vérifier que le style influence la sortie.

**Acceptance Scenarios**:

1. **Given** des styles prédéfinis disponibles, **When** l'utilisateur invoque `/generate-image "un château" --style ghibli`, **Then** l'image générée reflète le style demandé.
2. **Given** un nom de style inexistant, **When** l'utilisateur invoque `/generate-image "test" --style inexistant`, **Then** un message d'erreur liste les styles disponibles.
3. **Given** aucun style spécifié, **When** l'utilisateur invoque `/generate-image "un château"`, **Then** la génération fonctionne normalement sans enrichissement de style.

---

### User Story 4 - Créer un nouveau style personnalisé (Priority: P4)

L'utilisateur invoque `/create-style "cyberpunk-neon" "Style cyberpunk avec néons lumineux, couleurs vives sur fond sombre, reflets sur surfaces mouillées"` pour ajouter un nouveau preset de style réutilisable dans la bibliothèque.

**Why this priority**: Étend le système de styles (US3) en le rendant personnalisable. Nécessite que les styles soient implémentés au préalable.

**Independent Test**: Créer un style, puis l'utiliser dans `/generate-image` pour vérifier qu'il est bien disponible et appliqué.

**Acceptance Scenarios**:

1. **Given** la bibliothèque de styles existante, **When** l'utilisateur invoque `/create-style "mon-style" "description détaillée du style"`, **Then** le nouveau style est sauvegardé et immédiatement utilisable via `--style mon-style`.
2. **Given** un style nommé "ghibli" existe déjà, **When** l'utilisateur invoque `/create-style "ghibli" "nouvelle description"`, **Then** le système demande confirmation avant d'écraser le style existant.
3. **Given** la bibliothèque de styles, **When** l'utilisateur invoque `/create-style` sans arguments, **Then** un message d'aide explique l'utilisation attendue.

---

### User Story 5 - Consulter l'historique des générations (Priority: P5)

Chaque génération d'image est automatiquement journalisée (prompt, date/heure, fichier de sortie, style utilisé le cas échéant). L'utilisateur peut consulter cet historique pour retrouver ou reproduire une génération passée.

**Why this priority**: Fonctionnalité de confort et de traçabilité. Utile mais pas bloquante pour les fonctionnalités principales.

**Independent Test**: Générer plusieurs images, puis vérifier que le fichier d'historique contient toutes les entrées avec les informations attendues.

**Acceptance Scenarios**:

1. **Given** une génération d'image réussie, **When** la commande se termine, **Then** une entrée est ajoutée au fichier d'historique avec : date/heure, prompt utilisé, style (si applicable), chemin du fichier généré.
2. **Given** un historique existant avec plusieurs entrées, **When** l'utilisateur ouvre directement le fichier d'historique (ou demande à Claude de le lire), **Then** les entrées sont lisibles et triées chronologiquement.

---

### Edge Cases

- Que se passe-t-il si l'API Gemini retourne une erreur de contenu (prompt rejeté pour politique de contenu) ? Le système DOIT afficher un message clair expliquant le rejet sans exposer les détails techniques bruts de l'API.
- Que se passe-t-il si le dossier `out/` existe déjà et contient un fichier portant le même nom ? Le système DOIT ajouter un suffixe numérique (ex: `chat-2.png`) pour éviter l'écrasement.
- Que se passe-t-il si le prompt est vide ? Le système DOIT afficher un message d'aide avec un exemple d'utilisation.
- Que se passe-t-il si la connexion réseau est interrompue pendant la génération ? Le système DOIT afficher un message d'erreur compréhensible et ne pas laisser de fichier partiel dans `out/`.
- Que se passe-t-il si les images du chat sont dans un format non supporté par l'API ? Le système DOIT tenter une conversion ou indiquer les formats acceptés.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT accepter un prompt texte en entrée via la commande `/generate-image`
- **FR-002**: Le système DOIT envoyer le prompt à l'API Gemini et récupérer l'image générée
- **FR-003**: Le système DOIT sauvegarder l'image générée dans le dossier `out/` à la racine du projet
- **FR-004**: Le système DOIT créer le dossier `out/` automatiquement s'il n'existe pas
- **FR-005**: Le système DOIT nommer les fichiers de sortie de manière intelligente, basée sur le contenu du prompt (slugification)
- **FR-006**: Le système DOIT éviter l'écrasement de fichiers existants en ajoutant un suffixe numérique si nécessaire
- **FR-007**: Le système DOIT lire la clé API Gemini depuis un fichier `.env`
- **FR-008**: Le système DOIT afficher un message d'erreur clair et actionnable si la clé API est absente ou invalide
- **FR-009**: Le système DOIT détecter et transmettre les images présentes dans le contexte du chat comme ressources d'entrée à l'API
- **FR-010**: Le système DOIT supporter un flag `--style` permettant d'appliquer un preset de style au prompt
- **FR-011**: Le système DOIT fournir un ensemble initial de styles prédéfinis (minimum : ghibli, pixel-art, photo-réaliste, aquarelle)
- **FR-012**: Le système DOIT lister les styles disponibles quand un style inconnu est demandé
- **FR-013**: Le système DOIT fournir une commande `/create-style` pour ajouter de nouveaux presets de style
- **FR-014**: Le système DOIT demander confirmation avant d'écraser un style existant
- **FR-015**: Le système DOIT journaliser chaque génération (date, prompt, style, fichier de sortie) dans un fichier d'historique
- **FR-016**: Le système DOIT gérer gracieusement les erreurs de l'API (rejet de contenu, quota, réseau) avec des messages lisibles
- **FR-017**: Le système DOIT afficher le chemin complet du fichier généré à l'utilisateur après une génération réussie

### Key Entities

- **Generation Request**: Un prompt texte, optionnellement accompagné d'images de référence et d'un style. Représente l'intention de l'utilisateur.
- **Style Preset**: Un nom identifiant et une phrase de style (texte simple) concaténée au prompt avant envoi à l'API. Stocké de manière persistante et réutilisable.
- **Generation Log Entry**: Un enregistrement horodaté d'une génération : prompt original, style appliqué, chemin du fichier de sortie, statut (succès/échec).
- **Generated Image**: Le fichier image résultant, stocké dans `out/` avec un nom dérivé du prompt.

### Assumptions

- L'utilisateur dispose d'une connexion internet pour accéder à l'API Gemini
- L'API Gemini utilisée supporte la génération d'images à partir de texte et d'images de référence
- Le format de sortie par défaut est PNG
- Les styles sont stockés localement dans le projet (fichier de configuration)
- L'historique est stocké localement dans un fichier texte structuré (pas de base de données)
- L'outil est destiné à un usage personnel sur macOS via Claude Code

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: L'utilisateur peut générer une image à partir d'un prompt texte en une seule commande, et le fichier résultant est disponible dans `out/` en moins de 30 secondes (hors temps de réponse API)
- **SC-002**: 100% des erreurs prévisibles (clé manquante, API indisponible, prompt vide, style inconnu) produisent un message d'erreur compréhensible sans stack trace
- **SC-003**: Les fichiers générés portent systématiquement un nom lisible dérivé du prompt, sans collision avec les fichiers existants
- **SC-004**: L'utilisateur peut appliquer un style prédéfini ou personnalisé en ajoutant un seul flag à sa commande
- **SC-005**: Chaque génération est automatiquement tracée dans l'historique, consultable à tout moment
- **SC-006**: L'utilisateur peut créer et réutiliser un nouveau style en moins de 2 commandes
