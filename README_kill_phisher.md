# 🛡️ kill-phisher — Anti-Phishing Detection Tool

```
  ██╗  ██╗██╗██╗     ██╗       ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗███████╗██████╗
  ██║ ██╔╝██║██║     ██║      ██╔══██╗██║  ██║██║██╔════╝██║  ██║██╔════╝██╔══██╗
  █████╔╝ ██║██║     ██║      ██████╔╝███████║██║███████╗███████║█████╗  ██████╔╝
  ██╔═██╗ ██║██║     ██║      ██╔═══╝ ██╔══██║██║╚════██║██╔══██║██╔══╝  ██╔══██╗
  ██║  ██╗██║███████╗███████╗ ██║     ██║  ██║██║███████║██║  ██║███████╗██║  ██║
  ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝ ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
```

> ⚠️ **AVERTISSEMENT ÉTHIQUE ET LÉGAL**
>
> Cet outil est destiné **exclusivement** à la détection, l'analyse et la
> prévention des attaques de phishing. Il est conçu pour protéger les
> utilisateurs et sensibiliser à la cybersécurité défensive.
>
> **Toute utilisation à des fins malveillantes est illégale** et contraire
> à l'éthique professionnelle. L'auteur décline toute responsabilité en cas
> d'utilisation non autorisée.

---

## 📦 Dépôt

```
https://github.com/Durrell-229/Kill-phisher.git
```

---

## ✅ Prérequis

- **Python 3.6+** — aucune dépendance externe (bibliothèque standard uniquement)
- Compatible **Linux**, **Windows**, **macOS**, **Termux (Android)**

---

## 🚀 Installation & Lancement

### 🐧 Linux / macOS
```bash
git clone https://github.com/Durrell-229/Kill-phisher.git
cd Kill-phisher
python3 kill_phisher.py
```

### 🪟 Windows
```cmd
git clone https://github.com/Durrell-229/Kill-phisher.git
cd Kill-phisher
python kill_phisher.py
```

### 📱 Termux (Android)
```bash
pkg update && pkg install python git
git clone https://github.com/Durrell-229/Kill-phisher.git
cd Kill-phisher
python kill_phisher.py
```

### ⚡ Raccourci Termux (optionnel)
```bash
echo "alias killphisher='python ~/Kill-phisher/kill_phisher.py'" >> ~/.bashrc
source ~/.bashrc
# Lancer depuis n'importe où :
killphisher
```

---

## 🛠️ Modules disponibles (9 modules)

| # | Module | Description |
|---|--------|-------------|
| 1 | **Analyser une URL suspecte** | Détection TLD suspect, typosquat, mots-clés phishing, homoglyphes, encodage |
| 2 | **Détection typosquatting** | Comparaison avec 15+ domaines légitimes, substitution de caractères |
| 3 | **Analyser une page web** | Mots-clés phishing dans le HTML, formulaires password, iFrames, JS obfusqué |
| 4 | **Vérification SSL suspect** | Âge du certificat, Let's Encrypt, CN mismatch, protocole obsolète |
| 5 | **Analyser un email suspect** | Analyse headers, domaine expéditeur, Reply-To divergent, sujet alarmiste |
| 6 | **Score de risque global** | Analyse combinée URL + SSL + Contenu + DNS avec score pondéré /100 |
| 7 | **Base de données phishing** | Domaines connus, TLDs suspects, marques les plus ciblées |
| 8 | **Conseils anti-phishing** | Sensibilisation, bonnes pratiques, ressources officielles (ANSSI, Cybermalveillance) |
| 9 | **Rapport & export** | Session complète, export JSON horodaté, export TXT |

---

## 🎯 Système de scoring

Chaque analyse produit un score de risque sur 100 :

| Score | Niveau | Signification |
|-------|--------|---------------|
| 70-100 | 🔴 DANGEREUX | Forte probabilité de phishing |
| 40-69  | 🟡 SUSPECT | À vérifier manuellement |
| 20-39  | 🔵 À SURVEILLER | Quelques signaux faibles |
| 0-19   | 🟢 PROBABLEMENT SÛR | Faible risque détecté |

---

## 🔍 Ce que kill-phisher détecte

- **TLDs gratuits/suspects** : .tk, .ml, .xyz, .top, .online, .site...
- **Typosquatting** : paypa1.com, amaz0n.com, g00gle.com...
- **Usurpation de marques** : PayPal, Amazon, Apple, Google, banques françaises...
- **Certificats SSL suspects** : trop récents, Let's Encrypt, CN mismatch
- **Contenu phishing** : formulaires de mots de passe, mots-clés alarmistes
- **Emails frauduleux** : Reply-To divergent, sujets urgents, IP suspectes
- **Obfuscation** : JavaScript eval(), images base64, iFrames cachés
- **Homoglyphes** : caractères Unicode imitant des lettres latines

---

## 🔄 Mise à jour

```bash
cd Kill-phisher
git pull
```

---

## 📤 Pousser des modifications

```bash
cd Kill-phisher
git add .
git commit -m "mise à jour kill-phisher"
git push
```

> 💡 Pour `git push`, utilise un **token d'accès personnel** GitHub.
> GitHub → Settings → Developer settings → Personal access tokens → Generate new token

---

## 📁 Structure

```
Kill-phisher/
├── kill_phisher.py     # Script principal tout-en-un
└── README.md           # Ce fichier
```

---

## 🔒 Note Éthique

Cet outil est conçu **uniquement** pour :
- Détecter et analyser les tentatives de phishing
- Sensibiliser les utilisateurs aux risques
- Protéger les systèmes d'information
- La formation en cybersécurité défensive

**Ne l'utilisez jamais à des fins malveillantes.**
Tout usage non autorisé est une infraction pénale.

---

*Créé par **Léonard Durrell (hacking jack)***
*https://github.com/Durrell-229/Kill-phisher.git*
*kill-phisher v1.0 — Usage éthique et légal uniquement*
