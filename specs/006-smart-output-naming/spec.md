# Feature Specification: Smart Output Naming

**Feature Branch**: `006-smart-output-naming`
**Created**: 2026-03-18
**Status**: Draft
**Input**: User description: "Lorsqu'on envoie des images de référence, il faudrait que, s'il n'y a qu'une seule image, le nom de l'image de sortie reprenne le nom de l'image de référence. Si l'on a plusieurs images, il faudra analyser la demande et le résultat pour déterminer un nom d'image cohérent. Ajout d'un paramètre --name pour forcer le nom manuellement."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Nom basé sur l'image de référence unique (Priority: P1)

L'utilisateur envoie une seule image de référence avec son prompt. Le fichier de sortie reprend automatiquement le nom de base de cette image de référence (sans extension), au lieu d'utiliser le slug du prompt.

**Why this priority**: C'est le cas d'usage le plus fréquent et le plus intuitif. Quand on modifie une seule image, on s'attend à retrouver un fichier nommé de manière cohérente avec l'original.

**Independent Test**: Peut être testé en générant une image avec `--images photo-vacances.png` et en vérifiant que le fichier de sortie s'appelle `photo-vacances.png` (ou `photo-vacances-2.png` si collision).

**Acceptance Scenarios**:

1. **Given** une image de référence `mon-logo.png`, **When** l'utilisateur exécute `generate "rends ce logo plus moderne" --images mon-logo.png`, **Then** le fichier de sortie est nommé `mon-logo.png` dans le dossier `out/`
2. **Given** une image de référence `mon-logo.png` et un fichier `out/mon-logo.png` existant, **When** l'utilisateur exécute la même commande, **Then** le fichier de sortie est nommé `mon-logo-2.png`
3. **Given** une image de référence `My Photo (2024).jpg`, **When** l'utilisateur exécute une génération avec cette image, **Then** le nom de base est nettoyé/slugifié de manière cohérente (ex: `my-photo-2024.png`)

---

### User Story 2 - Forçage du nom via --name (Priority: P1)

L'utilisateur veut contrôler explicitement le nom du fichier de sortie, indépendamment du prompt ou des images de référence. Il utilise le paramètre `--name` pour imposer le nom.

**Why this priority**: Permet de bypasser toute logique automatique quand l'utilisateur sait exactement quel nom il veut. Essentiel pour les workflows scriptés ou les cas où le nommage automatique ne convient pas.

**Independent Test**: Peut être testé en exécutant `generate "un chat" --name "resultat-final"` et en vérifiant que le fichier s'appelle `resultat-final.png`.

**Acceptance Scenarios**:

1. **Given** un prompt quelconque, **When** l'utilisateur passe `--name "mon-fichier"`, **Then** le fichier de sortie est nommé `mon-fichier.png`
2. **Given** `--name "mon-fichier"` et un fichier `out/mon-fichier.png` existant, **When** l'utilisateur exécute la commande, **Then** le fichier de sortie est nommé `mon-fichier-2.png`
3. **Given** `--name "mon-fichier"` et `--images reference.png`, **When** l'utilisateur exécute la commande, **Then** le paramètre `--name` prend priorité et le fichier s'appelle `mon-fichier.png`
4. **Given** `--name "Mon Fichier Spécial!"`, **When** l'utilisateur exécute la commande, **Then** le nom est slugifié en `mon-fichier-special.png`

---

### User Story 3 - Nom court par extraction de mots-clés (Priority: P2)

Quand le nommage automatique s'appuie sur le prompt (plusieurs images de référence ou aucune image), le système extrait les 3-4 mots-clés les plus significatifs du prompt au lieu de slugifier l'intégralité du texte. Cela produit des noms de fichiers courts et lisibles, même pour des prompts longs.

**Why this priority**: Un prompt de 200 mots ne doit pas produire un nom de fichier tronqué et illisible. L'extraction de mots-clés rend les fichiers de sortie faciles à identifier dans un explorateur de fichiers.

**Independent Test**: Peut être testé en générant avec un prompt long et en vérifiant que le nom de sortie contient uniquement quelques mots-clés pertinents.

**Acceptance Scenarios**:

1. **Given** un prompt court `"un chat sur un skateboard"` sans images de référence, **When** l'utilisateur exécute la génération, **Then** le fichier de sortie a un nom court basé sur les mots-clés (ex: `chat-skateboard.png`)
2. **Given** un prompt long de 200 mots décrivant une scène complexe, **When** l'utilisateur exécute la génération, **Then** le nom de fichier contient au maximum 3-4 mots-clés significatifs (ex: `paysage-montagne-coucher-soleil.png`)
3. **Given** plusieurs images de référence `chat.png` et `chien.png`, **When** l'utilisateur exécute `generate "fusionne ces deux animaux en un seul être fantastique" --images chat.png chien.png`, **Then** le fichier de sortie est nommé d'après les mots-clés du prompt (ex: `animaux-fantastique.png`)
4. **Given** un prompt composé uniquement de mots vides (ex: `"le la les un une des"`), **When** l'utilisateur exécute la génération, **Then** le système utilise le fallback `image.png`

---

### User Story 4 - Rétrocompatibilité sans image de référence (Priority: P2)

L'utilisateur n'envoie aucune image de référence. Le nom de fichier est désormais basé sur les mots-clés extraits du prompt (plus court et lisible que l'ancien slug complet).

**Why this priority**: Garantir que le cas d'usage le plus courant (pas d'image de référence) bénéficie aussi du nommage intelligent.

**Independent Test**: Peut être testé en exécutant `generate "un paysage de montagne"` sans `--images` et en vérifiant que le nom est basé sur les mots-clés.

**Acceptance Scenarios**:

1. **Given** aucun `--images` ni `--name`, **When** l'utilisateur exécute `generate "un paysage de montagne enneigée au coucher du soleil"`, **Then** le fichier est nommé avec les mots-clés extraits (ex: `paysage-montagne-coucher-soleil.png`)

---

### Edge Cases

- Que se passe-t-il quand l'image de référence n'a pas d'extension reconnue (ex: fichier sans extension) ? Le nom de base du fichier est utilisé tel quel, puis slugifié
- Que se passe-t-il quand `--name` reçoit une chaîne vide ? Erreur de validation, le paramètre doit contenir au moins un caractère significatif
- Que se passe-t-il quand le nom de l'image de référence contient uniquement des caractères spéciaux (ex: `@#$.png`) ? Après slugification, si le résultat est vide, on retombe sur les mots-clés du prompt
- Que se passe-t-il quand `--name` contient une extension (ex: `--name "fichier.png"`) ? L'extension fournie est ignorée, le système utilise toujours `.png`
- Que se passe-t-il quand l'image de référence est dans un sous-dossier (ex: `--images dossier/photo.png`) ? Seul le nom du fichier est utilisé, pas le chemin
- Que se passe-t-il quand le prompt ne contient aucun mot-clé significatif (uniquement des mots vides) ? Le système utilise le fallback `image.png`
- Que se passe-t-il quand le prompt est très court (1-2 mots) ? Les mots sont utilisés directement sans filtrage supplémentaire

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT nommer le fichier de sortie d'après le nom de base de l'image de référence quand une seule image est fournie via `--images`
- **FR-002**: Le système DOIT accepter un paramètre `--name` qui force le nom du fichier de sortie
- **FR-003**: Le paramètre `--name` DOIT avoir la priorité la plus haute dans la logique de nommage (priorité : `--name` > image de référence unique > slug du prompt)
- **FR-004**: Le système DOIT slugifier le nom obtenu (que ce soit via `--name`, image de référence, ou prompt) pour garantir la compatibilité filesystem
- **FR-005**: Le système DOIT conserver le mécanisme anti-collision existant (suffixe numérique `-2`, `-3`, etc.)
- **FR-006**: Le système DOIT extraire 3-4 mots-clés significatifs du prompt (en filtrant les mots vides : articles, prépositions, conjonctions) pour construire le nom de fichier quand il n'y a ni `--name` ni image de référence unique
- **FR-007**: Le système DOIT utiliser les mots-clés extraits du prompt quand plusieurs images de référence sont fournies (sans `--name`)
- **FR-011**: Le système DOIT utiliser le fallback `image` comme nom quand l'extraction de mots-clés ne produit aucun résultat significatif
- **FR-008**: Le système DOIT retourner une erreur si `--name` est fourni avec une valeur vide
- **FR-009**: Le fichier de sortie DOIT toujours utiliser l'extension `.png`, quel que soit le mode de nommage
- **FR-010**: Le champ `output` dans `history.jsonl` DOIT refléter le nom de fichier effectivement utilisé

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% des générations avec une seule image de référence produisent un fichier nommé d'après cette image
- **SC-002**: 100% des générations avec `--name` produisent un fichier portant le nom spécifié
- **SC-003**: Le paramètre `--name` prend systématiquement priorité sur les autres logiques de nommage
- **SC-004**: Les noms de fichiers basés sur le prompt contiennent au maximum 4 mots-clés significatifs (pas de noms tronqués illisibles)
- **SC-005**: Les noms de fichiers produits sont toujours valides sur les systèmes de fichiers courants (pas de caractères spéciaux non échappés)
