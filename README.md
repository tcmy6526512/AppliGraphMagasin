# SAE C12 2024 - Graphes et IHM

**Projet à rendre le 8 juin 2024**

**Groupe 3 :**
- **Alexandre Damman** (kadlex0)
- **Thomas Champy** (tcmy6526512)
- **Noé Lefebvre** (renose391)

## Table des Matières

- [Introduction](#introduction)
- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
- [Auteurs](#auteurs)

## Introduction

Ce projet a été réalisé dans le cadre du BUT Informatique à l'IUT du Littoral Côte d’Opale pour la SAÉ C12 (Graphes-IHM). L'objectif est de développer deux applications :

1. Une application permettant de positionner des produits sur un plan de magasin.
2. Une application traçant un chemin optimal pour collecter les produits d'une liste de courses.

## Fonctionnalités

### Application 1 : Positionnement des Produits

- Créer un nouveau projet :
  - Définir le nom du projet, l'auteur, la date de création, le nom et l'adresse du magasin.
  - Charger et afficher un plan du magasin.
  - Réaliser un quadrillage sur ce plan (ajustable en taille et position).
  - Choisir les produits vendus par le magasin parmi une liste complète.
  - Associer à chaque produit une position dans le magasin (case dans le quadrillage).
- Enregistrer un projet :
  - Un fichier contenant les informations sur le projet (auteur, date, etc.).
  - Un dossier contenant les données de positionnement (plan, quadrillage, produits avec position).
- Ouvrir un projet en cours ou terminé à partir du nom du projet.
- Supprimer un projet.

### Application 2 : Traçage du Chemin

- Choisir un magasin.
- Voir la position des produits sur le plan du magasin.
- Établir une liste de courses.
- Afficher, sur le plan, le chemin le plus efficace pour récupérer les produits de la liste de courses.

## Installation

Pour installer et exécuter ce projet localement, suivez ces étapes :

```sh
git clone https://github.com/kaldex0/sae-c12.git
cd sae-c12
npm install  # ou autre commande d'installation spécifique

```

## Auteurs  
Alexandre Damman  
Thomas Champy
