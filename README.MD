Voici le fichier **`requirements.txt`** contenant les bibliothèques nécessaires :

```plaintext
matplotlib
numpy
```

---

Et voici le fichier **README.md** mis à jour :

---

# Projet d'Optimisation de Planning - Matheuristique

Ce projet implémente un algorithme de matheuristique pour optimiser les plannings de tournois sportifs. Vous pouvez tester le code en exécutant le notebook Jupyter `matheuristique.ipynb`, qui contient toutes les étapes de l'algorithme et les résultats.

## Prérequis

Avant de lancer le notebook, vous devez installer **Jupyter Notebook** ainsi que les dépendances `matplotlib` et `numpy`.

### Étape 1 : Installation de Jupyter et des dépendances

1. Assurez-vous d'avoir Python installé (vérifiez avec `python --version` dans votre terminal ou invite de commande).
2. Installez `pip`, le gestionnaire de paquets Python, s'il n'est pas encore disponible :
   ```bash
   python -m ensurepip --upgrade
   ```
3. Utilisez `pip` pour installer Jupyter Notebook ainsi que les dépendances listées dans `requirements.txt` :
   ```bash
   pip install notebook
   pip install -r requirements.txt
   ```

### Étape 2 : Lancer Jupyter dans l'IDE

Certaines IDEs, comme PyCharm, Visual Studio Code, ou Anaconda, supportent Jupyter Notebook. Voici comment l'exécuter :

- **Visual Studio Code** : Assurez-vous d'avoir l'extension Jupyter installée, puis ouvrez `matheuristique.ipynb` directement dans l'IDE.
- **PyCharm** : Installez le plugin **Scientific Mode** et ouvrez le notebook. Vérifiez que Jupyter est bien installé dans l'interpréteur Python de votre projet.
- **Terminal** : Si vous préférez, vous pouvez lancer Jupyter Notebook depuis le terminal :
  ```bash
  jupyter notebook
  ```
  Puis, dans le navigateur qui s'ouvre, naviguez jusqu'au fichier `matheuristique.ipynb`.

### Étape 3 : Exécuter le Notebook

1. Ouvrez `matheuristique.ipynb` dans votre environnement Jupyter.
2. Exécutez toutes les cellules du notebook en suivant l'ordre (utilisez `Shift + Enter` pour passer à la cellule suivante ou `Run All` pour tout exécuter).
3. Les résultats de chaque étape seront affichés directement sous chaque cellule, vous permettant d'observer le fonctionnement de l'algorithme.

## Structure du Notebook

- **Initialisation** : Chargement des bibliothèques et des fonctions nécessaires.
- **Implémentation de l'algorithme** : Explication et étapes de l'algorithme de matheuristique.
- **Résultats** : Exécution de l'algorithme et affichage des résultats finaux du planning.

### Des mains sont aussi présent dans les fichiers AGsimple.py, AGLocalsearch.py tabou.py et simulated_annealing.py pour tester l'impact de la variation des paramètres sur les résultats.

---

Avec ce guide et les installations, vous êtes prêt à exécuter `matheuristique.ipynb` et tester l'algorithme dans Jupyter Notebook.