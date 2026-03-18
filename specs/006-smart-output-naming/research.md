# Research: Smart Output Naming

## R1 — Extraction de mots-clés : approche

**Decision**: Filtrage par liste de stop words (articles, prépositions, conjonctions) en français et anglais, puis sélection des N premiers mots restants (max 4).

**Rationale**: Approche la plus simple et prédictible, sans dépendance externe (pas de NLP, pas de tokenizer). Le projet utilise principalement des prompts en français et anglais. Une liste statique de ~100 stop words couvre les deux langues. Les mots-clés restants après filtrage sont les noms, adjectifs et verbes qui décrivent le mieux l'image.

**Alternatives considered**:
- **TF-IDF / extraction NLP** : trop lourd, nécessite des dépendances (spaCy, NLTK). Contraire au principe IV (Simplicité).
- **Demander au modèle Gemini** : l'API est déjà configurée avec `response_modalities=["Text", "Image"]` donc techniquement faisable, mais ajoute de l'imprévisibilité et un couplage fort au modèle. Rejeté par l'utilisateur.
- **Slug brut tronqué (actuel)** : produit des noms illisibles pour les longs prompts (ex: `un-chat-qui-fait-du-skateboard-dans-un-parc-avec-`).

## R2 — Liste de stop words : portée linguistique

**Decision**: Stop words français + anglais embarqués en dur dans le code (constante Python).

**Rationale**: Les prompts sont rédigés principalement en français, parfois en anglais. Une liste combinée de ~120 mots couvre les cas d'usage. Pas besoin de détection de langue.

**Alternatives considered**:
- **Fichier externe configurable** : over-engineering pour un usage personnel.
- **Package `stopwords` (NLTK)** : nouvelle dépendance, contraire au principe IV.
- **Français uniquement** : raterait les prompts en anglais qui sont fréquents dans la génération d'images.

## R3 — Nombre de mots-clés retenus

**Decision**: Maximum 4 mots-clés, séparés par des tirets. Si le prompt filtré produit moins de 4 mots, tous sont utilisés.

**Rationale**: 4 mots donnent des noms suffisamment descriptifs tout en restant courts (ex: `chat-skateboard-parc-arbres.png`). Au-delà, les noms deviennent trop longs. En-deçà, pas assez descriptifs.

**Alternatives considered**:
- **3 mots** : parfois insuffisant pour distinguer des images proches.
- **5+ mots** : noms trop longs, peu lisibles dans un explorateur de fichiers.

## R4 — Gestion de `--name` avec extension

**Decision**: Si la valeur de `--name` contient un point suivi d'une extension image connue (.png, .jpg, .jpeg, .gif, .webp), cette extension est retirée avant slugification. Le système ajoute toujours `.png`.

**Rationale**: L'utilisateur pourrait naturellement écrire `--name "logo.png"` par habitude. Retirer l'extension évite des noms comme `logo-png.png`.

**Alternatives considered**:
- **Retirer tout ce qui suit le dernier point** : dangereux, `logo.v2` deviendrait `logo` au lieu de `logo-v2`.
- **Ne rien retirer** : produirait `logo-png.png`, confus.

## R5 — Extraction du nom de base depuis le chemin d'image de référence

**Decision**: Utiliser `Path(image_path).stem` pour obtenir le nom sans extension ni chemin parent, puis passer dans `slugify()`.

**Rationale**: `Path.stem` est standard Python, gère tous les cas (chemins absolus, relatifs, sous-dossiers). La slugification assure la compatibilité filesystem.

**Alternatives considered**:
- **Parsing manuel avec split('/')** : fragile, ne gère pas Windows.
- **Garder l'extension originale** : non, la spec impose `.png` systématiquement.
