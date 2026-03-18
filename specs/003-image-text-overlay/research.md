# Research: Image Text Overlay

**Date**: 2026-03-18
**Branch**: `003-image-text-overlay`

## Approche d'injection du texte dans le prompt

**Decision**: Intégrer le texte dans le prompt Gemini via une instruction explicite en anglais, insérée après le prompt utilisateur et avant le style.

**Rationale**: L'API Gemini (modèles imagen-3.0 et gemini-2.0-flash) supporte la génération de texte dans les images lorsque l'instruction est formulée clairement dans le prompt. L'approche par prompt engineering est la plus simple, ne nécessite aucune dépendance supplémentaire et respecte le principe de simplicité de la constitution.

**Alternatives considered**:
- Post-traitement Pillow (superposition de texte après génération) : rejeté car nécessite gestion de polices, positionnement, et ne s'intègre pas naturellement dans l'image
- Paramètre API dédié : rejeté car l'API Gemini n'expose pas de paramètre séparé pour le texte sur image

## Format d'instruction du texte

**Decision**: Utiliser le format `Write the exact text "{text}" on the image, preserving the exact capitalization` inséré dans le prompt enrichi, entre le prompt utilisateur et le style.

**Rationale**:
- L'instruction en anglais est plus fiable avec l'API Gemini
- La mention "exact text" et "preserving the exact capitalization" insiste sur la préservation de la casse
- Les guillemets autour du texte le délimitent clairement

**Alternatives considered**:
- Instruction en français : moins fiable avec l'API
- Instruction sans guillemets : risque de confusion entre le texte à afficher et le reste du prompt

## Ordre d'enrichissement du prompt

**Decision**: prompt utilisateur → instruction texte → resource prompts → style

**Rationale**: Le texte est une instruction spécifique liée au contenu, il doit être proche du prompt utilisateur. Le style vient en dernier car il modifie l'apparence globale.

## Champ text dans l'historique

**Decision**: Ajouter un champ optionnel `text` (string | null) dans les entrées `history.jsonl`.

**Rationale**: Permet de retrouver le texte exact utilisé pour une génération passée, sans parser le prompt enrichi. Compatible avec les entrées existantes (champ absent = null).
