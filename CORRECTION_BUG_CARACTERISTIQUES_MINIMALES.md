# Document technique : Correction du bug "caractéristiques minimales qui sautent une génération"

## Problème
Dans DofusFashionista, les utilisateurs ont signalé que les caractéristiques minimales et 
les poids des statistiques "sautent une génération" lors de la création d'équipements.
Ce comportement était particulièrement visible pour les caractéristiques minimales :
quand un utilisateur les modifiait, ces modifications n'étaient pas prises en compte
dans la génération suivante mais seulement dans la génération d'après.

## Cause identifiée
En analysant le code, nous avons découvert que dans le fichier `stats_weights.py`, 
la fonction `set_stats_weights()` appelle correctement `remove_cache_for_char(char.id)` 
pour invalider le cache après une modification des poids. En revanche, dans le fichier 
`min_stats.py`, la fonction `set_min_stats()` ne fait pas cet appel.

Cette différence d'implémentation explique pourquoi les caractéristiques minimales étaient
ignorées lors de la génération suivant une modification, car le système utilisait un résultat
mis en cache basé sur les anciennes valeurs.

## Correction appliquée
Nous avons modifié la fonction `set_min_stats()` dans le fichier `min_stats.py` pour y ajouter
l'appel à `remove_cache_for_char(char.id)` après la sauvegarde des modifications, ce qui force
l'invalidation du cache lié au personnage.

## Bénéfices
1. Les caractéristiques minimales sont désormais prises en compte immédiatement après leur modification
2. Amélioration de la cohérence du comportement entre les caractéristiques minimales et les poids
3. Meilleure expérience utilisateur : l'équipement généré respecte toujours les dernières préférences

## Changement effectué
Fichier modifié : `fashionsite/chardata/min_stats.py`

Avant :
```python
def set_min_stats(char, minimum_values):
    # [...]
    char.minimum_stats = pickle.dumps(minimum_values)
    char.save()
```

Après :
```python
def set_min_stats(char, minimum_values):
    # [...]
    char.minimum_stats = pickle.dumps(minimum_values)
    char.save()
    from chardata.util import remove_cache_for_char
    remove_cache_for_char(char.id)
```

## Tests effectués
1. Test de vérification de présence de l'appel à `remove_cache_for_char()`
2. Test de simulation du comportement avant/après
3. Test manuel de modification des caractéristiques minimales et génération d'équipement

## Résultats des tests
✅ L'appel à `remove_cache_for_char()` est bien présent dans `set_min_stats()`
✅ Le cache est correctement invalidé après chaque modification des caractéristiques minimales
✅ Les caractéristiques minimales sont prises en compte immédiatement après leur modification

Cette correction garantit que chaque fois que l'utilisateur modifie ses caractéristiques minimales,
le prochain équipement généré tiendra compte des nouvelles valeurs, éliminant le comportement
où les modifications "sautaient une génération".