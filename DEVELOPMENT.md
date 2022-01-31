## Initial Configuration

The server must accept your RSA key. Make sure you can connect passwordless first.

Add to your `~/.ssh/config`:

    Host ephemer
     Hostname your_hostname
     User your_user
     IdentityFile ~/.ssh/id_rsa.pub


## Deployment

First, bump the version number in `ephemer/__init__.py`.

Then:

    fab deploy --hosts=ephemer --site=production
 
Once you're done, commit:

    git commit ephemer/__init__.py
 
Then, tag:

    git tag v0.1.0
 
And push:

    git push
    git push --tags


## Mettre à jour les dépendances

Les versions des packages dont dépend le projet Ephemer sont fixées dans `requirements.txt`. C'est pour diminuer le risque
qu'une nouvelle version d'une dépendance soit utilisée lors d'un déploiement et cause un problème de conflit/changement d'API/bug upstream.

Pour mettre à jour les dépendances et bénéficier de features/bugfixes/security fixes :

1. repartir d'un environnement vierge
2. `$ pip install -r requirements-base.txt`
3. `$ pip freeze > requirements.txt`

Attention à ne pas ajouter les packages pour le développement et les tests dans `requirements.txt`.


## Charger le contenu initial dans la base de données

Après l'initialisation de la BD avec `$ python manage.py migrate` utiliser la commande `loaddata` :

```
    $ python manage.py loaddata initial_experimens_data.json
```


## Créer le QR code pour un site

Définir le hostname du service dans `settings.EPHEMER_HOSTNAME`, par exemple "http://ephemer.iocraft.org".

Exécuter la commande admin correspondante :

```.env
    $ python manage.py create_qr_code
```
