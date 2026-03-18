# Quickstart: Smart Output Naming

## Résumé des modifications

2 fichiers sources modifiés, 4 fichiers de tests modifiés. Aucune nouvelle dépendance.

## Fichiers à modifier

### `src/slugify.py`
- Ajouter constante `STOP_WORDS` (FR + EN, ~120 mots)
- Ajouter fonction `extract_keywords(text, max_words=4)` : filtre stop words, retourne les premiers mots-clés
- Ajouter fonction `strip_image_extension(name)` : retire .png/.jpg/.jpeg/.gif/.webp en fin de chaîne
- Fonction `slugify()` : inchangée

### `src/generate.py`
- `parse_args()` : ajouter argument `--name`
- `generate_image()` : ajouter paramètre `name: str | None = None`
- Logique de nommage (lignes 228-230) : remplacer `slug = slugify(prompt)` par la résolution à 3 niveaux
- `main()` : passer `args.name` à `generate_image()`
- Validation : erreur si `--name` est fourni mais vide/invalide après slugification

### Tests
- `tests/test_slugify.py` : tests pour `extract_keywords()` et `strip_image_extension()`
- `tests/test_generate.py` : tests nommage avec `--name`
- `tests/test_generate_images.py` : tests nommage avec 1 image de référence
- `tests/test_args_validation.py` : tests validation `--name`

## Ordre d'implémentation

1. `extract_keywords()` + `strip_image_extension()` dans `slugify.py` + tests
2. Paramètre `--name` dans `generate.py` (parsing + validation) + tests
3. Logique de résolution du nom dans `generate_image()` + tests
4. Tests d'intégration nommage avec images de référence
