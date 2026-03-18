<!--
Sync Impact Report
==================
- Version change: 0.0.0 → 1.0.0
- Modified principles: N/A (initial creation)
- Added sections: Core Principles (4), Technical Stack, Development Workflow, Governance
- Removed sections: None
- Templates requiring updates:
  - .specify/templates/plan-template.md ✅ compatible (Constitution Check section present)
  - .specify/templates/spec-template.md ✅ compatible (user stories + requirements structure)
  - .specify/templates/tasks-template.md ✅ compatible (phase structure matches workflow)
- Follow-up TODOs: None
-->

# Nano Banana Constitution

## Core Principles

### I. Skill-First Design

Toute fonctionnalité DOIT être exposée comme un skill Claude Code
(commande slash invocable dans une conversation Claude).

- Chaque skill DOIT accepter un prompt textuel en entrée et produire
  un résultat concret (fichier, message de confirmation)
- Les images présentes dans le contexte du chat DOIVENT pouvoir être
  transmises à l'API comme ressources d'entrée
- Les fichiers générés DOIVENT être placés dans le dossier `out/` à
  la racine du projet (créé automatiquement si absent)
- Les skills disponibles sont : `/generate-image` (génération),
  `/create-style` (création de preset de style)

### II. Sécurité & Configuration

La clé API Gemini et toute donnée sensible DOIVENT être gérées via
un fichier d'environnement (`.env`), jamais en dur dans le code.

- Le fichier `.env` DOIT être listé dans `.gitignore`
- Un fichier `.env.example` DOIT documenter les variables attendues
  sans valeurs réelles
- Le programme DOIT échouer avec un message clair si la clé API est
  absente ou invalide
- Les erreurs de l'API Gemini DOIVENT être capturées et restituées
  à l'utilisateur de manière lisible (pas de stack trace brute)

### III. Tests Standard

Les tests unitaires avec mocks de l'API Gemini sont obligatoires
pour toute logique métier.

- Utiliser `pytest` comme framework de test
- Les appels à l'API Gemini DOIVENT être mockés dans les tests
  unitaires (pas d'appels réels en CI)
- Les fonctions utilitaires (nommage de fichiers, gestion des
  styles, parsing de prompts) DOIVENT avoir des tests unitaires
- Couverture visée : fonctions critiques couvertes, pas d'objectif
  de pourcentage arbitraire

### IV. Simplicité

Le projet DOIT rester un outil simple et ciblé. Pas de
sur-ingénierie.

- YAGNI : ne pas implémenter de fonctionnalités spéculatives
- Dépendances minimales : SDK Gemini, python-dotenv, et le strict
  nécessaire
- Un seul point d'entrée par skill (un script = une commande)
- Préférer le code explicite aux abstractions prématurées

## Technical Stack

- **Langage** : Python 3.11+
- **Gestionnaire de paquets** : `uv`
- **API** : Google Gemini (génération d'images)
- **Tests** : pytest + mocks
- **Configuration** : python-dotenv (fichier `.env`)
- **Plateforme cible** : macOS (usage local via Claude Code)
- **Type de projet** : CLI / Skill Claude Code

## Development Workflow

- **Gestion de projet** : Speckit (`.specify/`)
- **Branching** : une branche par feature, merge sur `main`
- **Commits** : messages concis en anglais, conventionnels
- **Revue** : auto-revue avant merge (usage personnel)
- **Fonctionnalités bonus intégrées dès le départ** :
  - Styles prédéfinis (presets applicables au prompt)
  - Nommage intelligent des fichiers de sortie (basé sur le prompt)
  - Historique/log des générations (prompt, date, fichier)
  - Skill `/create-style` pour ajouter de nouveaux presets

## Governance

Cette constitution est le document de référence pour toutes les
décisions architecturales et de développement du projet Nano Banana.

- Toute modification des principes DOIT être documentée avec une
  justification
- Le versionnement de la constitution suit le Semantic Versioning :
  - MAJOR : suppression ou redéfinition d'un principe
  - MINOR : ajout d'un principe ou extension significative
  - PATCH : clarifications, corrections de formulation
- Les templates Speckit DOIVENT rester alignés avec les principes
  définis ici (vérification lors de chaque amendement)

**Version**: 1.0.0 | **Ratified**: 2026-03-18 | **Last Amended**: 2026-03-18
