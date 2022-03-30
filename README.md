# Description du projet

Ce projet Github est un composant de la plate-forme pédagogique réalisée dans le cadre du projet Ephemer (https://lillethics.com/projet-ephemer/). Cette plate-forme est constituée de 3 composants conçus pour fonctionner ensemble :

- une app Django pour le frontend : c'est ce projet !
- un oTree project pour le backend : `https://github.com/io-craft-org/ephemer-otree`
- un moteur oTree modifié : `https://github.com/io-craft-org/otree-core`


# Déploiement en production

## Environnement nécessaire

- Python 3.9 (contrainte du serveur oTree 5.4, on a remarqué une incompatibilité avec Python 3.10)
- postgresql
- serveur web configuré pour une app python/Django (Apache ou Nginx)


## Installation et configuration

Le module `ephemer.settings.py` contient une configuration pour un serveur de DEV. Surcharger les variables qui le nécessitent pour une configuration de PROD.

Plus d'infos dans la doc de Django : https://docs.djangoproject.com/en/3.2/howto/deployment/

(cette application est compatible WSGI et n'a pas besoin du support ASGI)

Quelques variables de configuration sont spécifiques à la plate-forme EPHEMER :

```python
# OTREE Configuration
OTREE_HOST = "http://localhost:8001"  # Emplacement du serveur ephemer-otree
OTREE_REST_KEY = <clé secrète>        # Clé secrète de l'API otree. À placer également dans la configuration de ephemer-otree

# EPHEMER Configuration
# Le hostname est utilisé pour créer le QR code.
EPHEMER_HOSTNAME = "http://localhost:8000"  # L'emplacement public de ce serveur. Permet de générer un QR code pour la page d'accès des participants
```


## Initialisation des données

Avec le virtualenv activé exécuter les commandes admin suivantes :

```bash
$ python manage.py migrate  # Crée le schéma de la BD
$ python manage.py initcontent  # Crée le contenu initial de la plate-forme
$ python manage.py init-test-content  # Optionnel. Crée de fausses sessions pour tester le bon fonctionnement (des graphiques en particulier)
$ python manage.py create-super-user
$ python manage.py create_qr_code  # Nécessite la valeur EPHEMER_HOSTNAME dans `settings.py`
```


## Démarrer le serveur Django via le serveur web (Apache ou Nginx)
