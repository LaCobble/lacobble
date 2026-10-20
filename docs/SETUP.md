# Mise en route

## 1. Le dépôt profil
Le dépôt est [`LaCobble/lacobble`](https://github.com/LaCobble/lacobble) :
un dépôt public qui porte le nom de ton pseudo (la casse ne compte pas).
C'est ce nom précis qui fait que GitHub affiche son README sur ta page de
profil.

## 2. Pousser ces fichiers
Par branche et pull request, comme le reste :
```bash
git switch -c <type>/<sujet>
git push -u origin <branche>
gh pr create --base main
```

## 3. Créer le token pour les stats
Le `GITHUB_TOKEN` fourni automatiquement par les Actions ne voit que ce
dépôt : il ne peut pas lister tes dépôts privés pour les totaux de
langages.

1. https://github.com/settings/tokens → **Generate new token (classic)**
2. Scope : `repo`, pour compter les langages des dépôts privés. Seuls des totaux par langage sortent de l'API, jamais
   le nom d'un dépôt privé. Mets une expiration et note-la : quand le
   token expire, l'Action échoue et les graphiques ne bougent plus.
3. Copie le token
4. Dans le dépôt `LaCobble/LaCobble` → **Settings → Secrets and variables →
   Actions → New repository secret**
   - Nom : `GH_PAT`
   - Valeur : le token

## 4. Autoriser l'Action à commit
**Settings → Actions → General → Workflow permissions** → coche
*"Read and write permissions"*. Sans ça, le `git push` du workflow échoue.

## 5. Premier run
**Actions → update-profile-graphics → Run workflow** (le bouton manuel,
`workflow_dispatch`). Vérifie que `assets/*.svg` se met à jour et que le
commit `chore: refresh profile graphics` apparaît. Ensuite il tourne seul,
une fois par jour à 04h15 UTC.

## 6. La police intégrée
JetBrains Mono est déjà dans `fonts/`, réduite aux caractères latins.
Voir [`fonts/README.md`](../fonts/README.md) pour la regénérer.

## Test en local avant de pousser
```bash
cd scripts
pip install -r requirements.txt
GH_TOKEN=$(gh auth token --user LaCobble) python build_all.py LaCobble
```
