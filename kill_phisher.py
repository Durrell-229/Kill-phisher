#!/usr/bin/env python3
"""
╔═╗╔═╗╔╦╗  ╔═╗╦ ╦╦╔═╗╦ ╦╔═╗╦═╗
╠╣ ║║║ ║║  ╠═╝╠═╣║╚═╗╠═╣║╣ ╠╦╝
╚  ╚╩╝═╩╝  ╩  ╩ ╩╩╚═╝╩ ╩╚═╝╩╚═
   Anti-Phishing Detection Tool v1.0
   Créé par Léonard Durrell (hacking jack)
   https://github.com/Durrell-229/Leo_jack
"""

import sys, os, re, ssl, socket, json, time, hashlib
import urllib.request, urllib.parse, urllib.error
import platform, threading, base64
from datetime import datetime
from collections import defaultdict

# ══════════════════════════════════════════════════════════
#  COLORS
# ══════════════════════════════════════════════════════════
class C:
    RED     = "\033[91m"; GREEN   = "\033[92m"; YELLOW  = "\033[93m"
    BLUE    = "\033[94m"; MAGENTA = "\033[95m"; CYAN    = "\033[96m"
    WHITE   = "\033[97m"; BOLD    = "\033[1m";  DIM     = "\033[2m"
    UNDER   = "\033[4m";  RESET   = "\033[0m"

if platform.system() == "Windows":
    os.system("color")
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleMode(
            ctypes.windll.kernel32.GetStdHandle(-11), 7)
    except: pass

# ══════════════════════════════════════════════════════════
#  BANNER
# ══════════════════════════════════════════════════════════
BANNER = f"""
{C.GREEN}{C.BOLD}
  ██╗  ██╗██╗██╗     ██╗       ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗███████╗██████╗
  ██║ ██╔╝██║██║     ██║      ██╔══██╗██║  ██║██║██╔════╝██║  ██║██╔════╝██╔══██╗
  █████╔╝ ██║██║     ██║      ██████╔╝███████║██║███████╗███████║█████╗  ██████╔╝
  ██╔═██╗ ██║██║     ██║      ██╔═══╝ ██╔══██║██║╚════██║██╔══██║██╔══╝  ██╔══██╗
  ██║  ██╗██║███████╗███████╗ ██║     ██║  ██║██║███████║██║  ██║███████╗██║  ██║
  ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝ ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
{C.RESET}
{C.DIM}  ━━━━━━━━━━━━━━━━ Anti-Phishing Detection Tool v1.0 ━━━━━━━━━━━━━━━━{C.RESET}
{C.YELLOW}  ⚠  Usage éthique & légal uniquement — Environnements autorisés seulement{C.RESET}
{C.DIM}  Créé par Léonard Durrell (hacking jack) — https://github.com/Durrell-229/Leo_jack{C.RESET}
"""

MENU = f"""
{C.GREEN}{C.BOLD}
  ╔══════════════════════════════════════════════════════════╗
  ║           KILL-PHISHER — MENU PRINCIPAL                  ║
  ╠══════════════════════════════════════════════════════════╣{C.RESET}
{C.GREEN}  ║  [1]  🎣  Analyser une URL suspecte                      ║
  ║  [2]  🔍  Détecter typosquatting / domaine clone         ║
  ║  [3]  🌐  Analyser une page web (contenu phishing)       ║
  ║  [4]  🔐  Vérification SSL / certificat suspect          ║
  ║  [5]  📧  Analyser un email suspect (headers)            ║
  ║  [6]  🧠  Score de risque global (URL + contenu + SSL)   ║
  ║  [7]  📋  Base de données domaines phishing connus       ║
  ║  [8]  🛡️   Conseils anti-phishing & sensibilisation       ║
  ║  [9]  📊  Rapport & export session                       ║
  ║  [0]  ❌  Quitter                                        ║{C.RESET}
{C.GREEN}{C.BOLD}  ╚══════════════════════════════════════════════════════════╝{C.RESET}
"""

# ══════════════════════════════════════════════════════════
#  SESSION
# ══════════════════════════════════════════════════════════
session = {
    "start": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "analyses": []
}

def save(module, target, score, details):
    session["analyses"].append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "module": module, "target": target,
        "score": score, "details": details
    })

# ══════════════════════════════════════════════════════════
#  UTILITIES
# ══════════════════════════════════════════════════════════
def log(msg, level="info"):
    icons = {
        "info":  f"{C.CYAN}[*]{C.RESET}",
        "ok":    f"{C.GREEN}[+]{C.RESET}",
        "warn":  f"{C.YELLOW}[!]{C.RESET}",
        "err":   f"{C.RED}[-]{C.RESET}",
        "found": f"{C.MAGENTA}[✓]{C.RESET}",
        "alert": f"{C.RED}{C.BOLD}[⚠]{C.RESET}",
    }
    print(f"  {icons.get(level,'[?]')} {msg}")

def sep(title="", color=C.GREEN):
    w = 56
    if title:
        pad = (w - len(title) - 2) // 2
        print(f"\n{color}{C.BOLD}  {'─'*pad} {title} {'─'*pad}{C.RESET}")
    else:
        print(f"{C.DIM}  {'─'*w}{C.RESET}")

def prompt(msg, default=""):
    d = f" [{default}]" if default else ""
    val = input(f"\n{C.YELLOW}  ▶ {msg}{d}: {C.RESET}").strip()
    return val if val else default

def clear():
    os.system("cls" if platform.system() == "Windows" else "clear")

def risk_bar(score, max_score=100):
    pct = score / max_score
    filled = int(pct * 30)
    empty  = 30 - filled
    if pct >= 0.7:   color = C.RED
    elif pct >= 0.4: color = C.YELLOW
    else:            color = C.GREEN
    bar = f"{color}{'█' * filled}{'░' * empty}{C.RESET}"
    return bar

def risk_label(score):
    if score >= 70: return f"{C.RED}{C.BOLD}DANGEREUX 🔴{C.RESET}"
    if score >= 40: return f"{C.YELLOW}{C.BOLD}SUSPECT 🟡{C.RESET}"
    if score >= 20: return f"{C.CYAN}{C.BOLD}À SURVEILLER 🔵{C.RESET}"
    return f"{C.GREEN}{C.BOLD}PROBABLEMENT SÛR 🟢{C.RESET}"

# ══════════════════════════════════════════════════════════
#  BASES DE DONNÉES INTÉGRÉES
# ══════════════════════════════════════════════════════════

# Marques fréquemment ciblées par le phishing
BRAND_TARGETS = [
    "paypal","amazon","apple","google","microsoft","facebook","instagram",
    "netflix","ebay","linkedin","twitter","whatsapp","telegram","discord",
    "bank","banque","creditcard","chase","wellsfargo","hsbc","barclays",
    "societegenerale","bnpparibas","lcl","caissedepargne","creditagricole",
    "laposte","impots","ameli","caf","cpam","urssaf","gouv",
    "coinbase","binance","blockchain","crypto","metamask","wallet",
    "steam","epicgames","roblox","playstation","xbox","nintendo",
    "dhl","fedex","ups","colissimo","chronopost","ups","laposte",
]

# TLDs suspects souvent utilisés en phishing
SUSPICIOUS_TLDS = [
    ".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".top", ".club",
    ".online", ".site", ".live", ".buzz", ".icu", ".vip", ".work",
    ".click", ".link", ".download", ".stream", ".gdn", ".loan",
    ".win", ".racing", ".party", ".trade", ".review", ".science",
]

# Mots-clés suspects dans les URLs
SUSPICIOUS_URL_KEYWORDS = [
    "login","signin","sign-in","secure","verify","verification","confirm",
    "update","account","password","credential","billing","payment","invoice",
    "suspended","locked","unusual","activity","recover","restore","validate",
    "webscr","cmdflow","dispatch","alert","notice","urgent","limited",
    "free","prize","winner","congratulation","bonus","reward","gift",
    "support","helpdesk","client","service","official","authentic",
]

# Mots-clés phishing dans le contenu HTML
PHISHING_CONTENT_KEYWORDS = [
    "enter your password","enter password","your account has been",
    "verify your account","confirm your identity","unusual activity",
    "click here to verify","your account will be suspended",
    "update your payment","your card has been declined",
    "you have won","claim your prize","limited time offer",
    "verify now","act immediately","your account is at risk",
    "entrez votre mot de passe","votre compte a été",
    "vérifiez votre compte","activité inhabituelle",
    "compte suspendu","mise à jour de paiement",
]

# Domaines phishing connus (échantillon éducatif)
KNOWN_PHISHING_DOMAINS = [
    "paypa1.com","paypаl.com","amazon-security.tk","apple-id-verify.ml",
    "microsoft-support.xyz","google-account-verify.top","netflix-billing.site",
    "facebook-login-verify.online","instagram-verify.club","secure-bank-login.tk",
]

# Domaines légitimes de référence pour comparaison
LEGITIMATE_DOMAINS = {
    "paypal":     "paypal.com",
    "amazon":     "amazon.com",
    "apple":      "apple.com",
    "google":     "google.com",
    "microsoft":  "microsoft.com",
    "facebook":   "facebook.com",
    "instagram":  "instagram.com",
    "netflix":    "netflix.com",
    "ebay":       "ebay.com",
    "linkedin":   "linkedin.com",
    "twitter":    "twitter.com",
    "x":          "x.com",
    "discord":    "discord.com",
    "steam":      "steampowered.com",
    "coinbase":   "coinbase.com",
    "binance":    "binance.com",
    "impots":     "impots.gouv.fr",
    "ameli":      "ameli.fr",
    "laposte":    "laposte.fr",
    "gouv":       "gouv.fr",
}

# ══════════════════════════════════════════════════════════
#  MODULE 1 — ANALYSER UNE URL SUSPECTE
# ══════════════════════════════════════════════════════════
def analyze_url():
    sep("ANALYSE URL SUSPECTE", C.GREEN)
    url = prompt("URL suspecte à analyser")
    if not url: return
    if not url.startswith("http"): url = "http://" + url

    score = 0
    findings = []

    try:
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.lower().replace("www.", "")
        path   = parsed.path.lower()
        params = parsed.query.lower()
        full   = url.lower()
    except Exception as e:
        log(f"URL invalide: {e}", "err"); return

    sep("DÉCOMPOSITION DE L'URL")
    print(f"  {C.CYAN}Protocole  {C.RESET} {parsed.scheme}")
    print(f"  {C.CYAN}Domaine    {C.RESET} {domain}")
    print(f"  {C.CYAN}Chemin     {C.RESET} {parsed.path or '/'}")
    print(f"  {C.CYAN}Paramètres {C.RESET} {parsed.query or 'aucun'}")

    sep("INDICATEURS DE RISQUE")

    # 1. Protocole HTTP (pas HTTPS)
    if parsed.scheme == "http":
        log("Protocole HTTP non sécurisé (pas de HTTPS)", "alert")
        score += 15; findings.append("HTTP non sécurisé (+15)")
    else:
        log("Protocole HTTPS présent", "ok")

    # 2. TLD suspect
    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            log(f"TLD suspect détecté: {tld}", "alert")
            score += 20; findings.append(f"TLD suspect: {tld} (+20)"); break

    # 3. Marque connue dans sous-domaine ou chemin (pas dans domaine racine)
    for brand in BRAND_TARGETS:
        if brand in domain and brand not in domain.split(".")[-2]:
            log(f"Marque '{brand}' dans sous-domaine (usurpation probable)", "alert")
            score += 25; findings.append(f"Usurpation marque: {brand} (+25)"); break

    # 4. Mots-clés suspects dans l'URL
    kw_found = [kw for kw in SUSPICIOUS_URL_KEYWORDS if kw in full]
    if kw_found:
        log(f"Mots-clés suspects: {', '.join(kw_found[:4])}", "warn")
        score += min(len(kw_found) * 5, 20)
        findings.append(f"Mots-clés suspects: {kw_found[:4]} (+{min(len(kw_found)*5,20)})")

    # 5. Trop de sous-domaines
    subdomain_count = domain.count(".")
    if subdomain_count >= 3:
        log(f"Nombreux sous-domaines: {subdomain_count} niveaux", "warn")
        score += 10; findings.append(f"Sous-domaines excessifs: {subdomain_count} (+10)")

    # 6. IP au lieu d'un domaine
    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain):
        log("IP utilisée comme domaine (très suspect)", "alert")
        score += 30; findings.append("IP comme domaine (+30)")

    # 7. Domaine connu dans base phishing
    if domain in KNOWN_PHISHING_DOMAINS:
        log(f"DOMAINE RÉPERTORIÉ COMME PHISHING: {domain}", "alert")
        score += 50; findings.append(f"Domaine phishing connu (+50)")

    # 8. URL très longue
    if len(url) > 100:
        log(f"URL très longue ({len(url)} caractères)", "warn")
        score += 10; findings.append(f"URL longue: {len(url)} chars (+10)")

    # 9. Caractères spéciaux suspects (homoglyphes)
    suspicious_chars = [c for c in domain if ord(c) > 127]
    if suspicious_chars:
        log(f"Caractères Unicode suspects (homoglyphes): {suspicious_chars}", "alert")
        score += 30; findings.append("Homoglyphes Unicode (+30)")

    # 10. Encodage suspect dans l'URL
    if "%" in url and url.count("%") > 5:
        log("Encodage URL excessif (obfuscation probable)", "warn")
        score += 15; findings.append("Encodage URL suspect (+15)")

    # 11. Redirections multiples
    if url.count("http") > 1:
        log("Redirection encodée dans l'URL", "alert")
        score += 20; findings.append("Redirection encodée (+20)")

    # 12. Tirets excessifs (technique courante: pay-pal-secure.com)
    if domain.count("-") >= 3:
        log(f"Tirets excessifs dans le domaine: {domain.count('-')}", "warn")
        score += 10; findings.append(f"Tirets excessifs (+10)")

    score = min(score, 100)
    sep("VERDICT")
    print(f"\n  {risk_bar(score)}  {score}/100")
    print(f"\n  Niveau de risque: {risk_label(score)}\n")

    save("URL Analysis", url, score, findings)
    return score

# ══════════════════════════════════════════════════════════
#  MODULE 2 — TYPOSQUATTING / DOMAINE CLONE
# ══════════════════════════════════════════════════════════
def typosquatting_detect():
    sep("DÉTECTION TYPOSQUATTING", C.GREEN)
    domain = prompt("Domaine à analyser (ex: paypa1.com)")
    if not domain: return
    domain = domain.lower().replace("www.", "")

    score = 0; findings = []

    sep("ANALYSE TYPOGRAPHIQUE")

    # 1. Comparaison avec domaines légitimes
    for brand, legit in LEGITIMATE_DOMAINS.items():
        legit_base = legit.split(".")[0]

        # Substitution de caractères (0→o, 1→l, etc.)
        substitutions = {
            "0": "o", "1": "l", "3": "e", "4": "a",
            "5": "s", "6": "g", "7": "t", "@": "a",
        }
        normalized = domain.split(".")[0]
        for fake, real in substitutions.items():
            normalized = normalized.replace(fake, real)

        if normalized == legit_base:
            log(f"TYPOSQUAT détecté: '{domain}' imite '{legit}'", "alert")
            score += 60; findings.append(f"Typosquat de {legit} (+60)")

        # Distance de Levenshtein simplifiée
        d = domain.split(".")[0]
        if d != legit_base and legit_base in d:
            log(f"Domaine contient la marque '{legit_base}' (usurpation)", "alert")
            score += 40; findings.append(f"Marque incluse: {legit_base} (+40)")

        # Addition de mots avant/après
        for prefix in ["secure-","login-","verify-","my-","account-","safe-"]:
            if d == prefix.rstrip("-") + legit_base or d == legit_base + "-" + prefix.rstrip("-"):
                log(f"Préfixe/suffixe suspect autour de '{legit_base}'", "alert")
                score += 35; findings.append(f"Affixe suspect sur {legit_base} (+35)")

    # 2. Longueur et structure
    parts = domain.split(".")
    if len(parts) > 3:
        log(f"Structure de domaine complexe: {domain}", "warn")
        score += 15; findings.append("Structure complexe (+15)")

    # 3. TLD suspect
    tld = "." + parts[-1] if parts else ""
    if tld in SUSPICIOUS_TLDS:
        log(f"TLD gratuit/suspect: {tld}", "alert")
        score += 20; findings.append(f"TLD suspect: {tld} (+20)")

    # 4. Résolution DNS
    try:
        ip = socket.gethostbyname(domain)
        log(f"Domaine résolvable: {ip}", "warn")
        findings.append(f"Résolu vers: {ip}")
    except:
        log("Domaine non résolvable (peut-être inactif)", "info")

    # 5. Vérifier si domaine connu
    if domain in KNOWN_PHISHING_DOMAINS:
        log("Domaine dans la base phishing connue !", "alert")
        score += 50; findings.append("Base phishing connue (+50)")

    score = min(score, 100)
    sep("VERDICT")
    print(f"\n  {risk_bar(score)}  {score}/100")
    print(f"\n  Niveau de risque: {risk_label(score)}\n")
    save("Typosquatting", domain, score, findings)

# ══════════════════════════════════════════════════════════
#  MODULE 3 — ANALYSER CONTENU PAGE WEB
# ══════════════════════════════════════════════════════════
def webpage_analysis():
    sep("ANALYSE CONTENU PAGE WEB", C.GREEN)
    log("⚠  Ne visitez pas de sites suspects sur votre machine principale.", "warn")
    url = prompt("URL à analyser")
    if not url: return
    if not url.startswith("http"): url = "http://" + url

    score = 0; findings = []

    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        resp = urllib.request.urlopen(req, timeout=8)
        html = resp.read().decode(errors="replace").lower()
        headers = dict(resp.getheaders())
        final_url = resp.geturl()
    except Exception as e:
        log(f"Impossible d'accéder à la page: {e}", "err"); return

    sep("ANALYSE DU CONTENU HTML")

    # 1. Mots-clés phishing dans le contenu
    found_keywords = [kw for kw in PHISHING_CONTENT_KEYWORDS if kw in html]
    if found_keywords:
        log(f"Mots-clés phishing dans la page ({len(found_keywords)} trouvés):", "alert")
        for kw in found_keywords[:6]:
            print(f"    {C.RED}→ \"{kw}\"{C.RESET}")
        score += min(len(found_keywords) * 8, 40)
        findings.append(f"Mots-clés phishing: {len(found_keywords)} (+{min(len(found_keywords)*8,40)})")

    # 2. Formulaires de login
    form_count = html.count("<form")
    password_inputs = html.count('type="password"') + html.count("type='password'")
    if password_inputs > 0:
        log(f"Formulaire(s) de mot de passe détecté(s): {password_inputs}", "alert")
        score += 20; findings.append(f"Formulaire password ({password_inputs}) (+20)")

    # 3. Marques usurpées dans le contenu
    for brand in BRAND_TARGETS[:20]:
        if brand in html:
            log(f"Marque '{brand}' mentionnée dans la page", "warn")
            score += 10; findings.append(f"Marque mentionnée: {brand} (+10)")
            break

    # 4. Redirection suspecte
    if final_url.lower() != url.lower():
        log(f"Redirection détectée: {final_url[:80]}", "warn")
        score += 15; findings.append(f"Redirection (+15)")

    # 5. Absence d'en-têtes sécurité
    h_lower = {k.lower(): v for k, v in headers.items()}
    missing_headers = []
    for h in ["x-frame-options","content-security-policy","x-content-type-options"]:
        if h not in h_lower:
            missing_headers.append(h)
    if missing_headers:
        log(f"En-têtes sécurité manquants: {len(missing_headers)}", "warn")
        score += 10; findings.append(f"Headers sécurité manquants (+10)")

    # 6. Logos/images en base64 (technique d'obfuscation)
    b64_count = html.count("base64,")
    if b64_count > 3:
        log(f"Nombreuses images base64 ({b64_count}) — obfuscation possible", "warn")
        score += 10; findings.append(f"Images base64 obfusquées: {b64_count} (+10)")

    # 7. Liens externes suspects
    external_links = re.findall(r'href=["\']https?://([^"\']+)["\']', html)
    suspicious_ext = [l for l in external_links
                      if any(tld in l for tld in [t.lstrip(".") for t in SUSPICIOUS_TLDS])]
    if suspicious_ext:
        log(f"Liens externes suspects: {len(suspicious_ext)}", "warn")
        score += 10; findings.append(f"Liens suspects: {len(suspicious_ext)} (+10)")

    # 8. iFrames cachés
    iframe_count = html.count("<iframe")
    if iframe_count > 0:
        log(f"iFrame(s) détecté(s): {iframe_count}", "warn")
        score += 5 * iframe_count; findings.append(f"iFrames: {iframe_count} (+{5*iframe_count})")

    # 9. Scripts obfusqués
    if "eval(" in html and "unescape" in html:
        log("Code JavaScript obfusqué détecté (eval+unescape)", "alert")
        score += 20; findings.append("JS obfusqué (+20)")

    score = min(score, 100)
    sep("VERDICT")
    print(f"\n  {risk_bar(score)}  {score}/100")
    print(f"\n  Niveau de risque: {risk_label(score)}\n")
    save("Webpage Analysis", url, score, findings)

# ══════════════════════════════════════════════════════════
#  MODULE 4 — VÉRIFICATION SSL SUSPECT
# ══════════════════════════════════════════════════════════
def ssl_phishing_check():
    sep("VÉRIFICATION SSL / CERTIFICAT SUSPECT", C.GREEN)
    host = prompt("Domaine à vérifier")
    if not host: return
    host = host.replace("https://","").replace("http://","").split("/")[0]

    score = 0; findings = []

    try:
        ctx = ssl.create_default_context()
        conn = ctx.wrap_socket(socket.socket(socket.AF_INET), server_hostname=host)
        conn.settimeout(5)
        conn.connect((host, 443))
        cert = conn.getpeercert()
        cipher = conn.cipher()
        version = conn.version()
        conn.close()

        subject = dict(x[0] for x in cert.get("subject", []))
        issuer  = dict(x[0] for x in cert.get("issuer", []))
        not_before = cert.get("notBefore", "?")
        not_after  = cert.get("notAfter", "?")
        san = [v for t,v in cert.get("subjectAltName", []) if t == "DNS"]

        sep("INFORMATIONS DU CERTIFICAT")
        print(f"  {C.CYAN}Sujet      {C.RESET} {subject.get('commonName','?')}")
        print(f"  {C.CYAN}Émetteur   {C.RESET} {issuer.get('organizationName','?')}")
        print(f"  {C.CYAN}Valide du  {C.RESET} {not_before}")
        print(f"  {C.CYAN}Expire le  {C.RESET} {not_after}")
        print(f"  {C.CYAN}Protocol   {C.RESET} {version}")
        print(f"  {C.CYAN}Cipher     {C.RESET} {cipher[0] if cipher else '?'}")
        if san: print(f"  {C.CYAN}SAN        {C.RESET} {', '.join(san[:5])}")

        sep("INDICATEURS DE RISQUE SSL")

        # 1. Durée de vie du certificat
        try:
            issued  = datetime.strptime(not_before, "%b %d %H:%M:%S %Y %Z")
            expires = datetime.strptime(not_after,  "%b %d %H:%M:%S %Y %Z")
            validity_days = (expires - issued).days
            age_days = (datetime.utcnow() - issued).days

            if validity_days <= 30:
                log(f"Certificat de très courte durée: {validity_days} jours", "alert")
                score += 25; findings.append(f"Durée courte: {validity_days}j (+25)")
            elif validity_days <= 90:
                log(f"Certificat de courte durée: {validity_days} jours (Let's Encrypt courant en phishing)", "warn")
                score += 10; findings.append(f"Durée 90j (+10)")
            else:
                log(f"Durée du certificat: {validity_days} jours (normal)", "ok")

            if age_days <= 7:
                log(f"Certificat très récent: {age_days} jour(s) seulement", "alert")
                score += 20; findings.append(f"Certificat récent: {age_days}j (+20)")
        except: pass

        # 2. Émetteur gratuit (Let's Encrypt = souvent utilisé en phishing)
        issuer_org = issuer.get("organizationName","").lower()
        if "let's encrypt" in issuer_org:
            log("Émetteur Let's Encrypt (gratuit — courant en phishing)", "warn")
            score += 10; findings.append("Let's Encrypt (+10)")
        elif "comodo" in issuer_org or "digicert" in issuer_org:
            log(f"Émetteur réputé: {issuer.get('organizationName')}", "ok")

        # 3. CN ne correspond pas au domaine
        cn = subject.get("commonName","")
        if cn and host not in cn and cn not in host:
            log(f"CN '{cn}' ne correspond pas au domaine '{host}'", "alert")
            score += 30; findings.append(f"CN mismatch (+30)")

        # 4. Marque dans le CN
        for brand in BRAND_TARGETS[:15]:
            if brand in cn.lower() and brand not in host.lower():
                log(f"Marque '{brand}' dans le CN mais pas dans le domaine", "alert")
                score += 25; findings.append(f"Marque dans CN: {brand} (+25)"); break

        # 5. Protocol obsolète
        if version in ["TLSv1", "TLSv1.1", "SSLv2", "SSLv3"]:
            log(f"Protocol obsolète: {version}", "alert")
            score += 15; findings.append(f"Protocol obsolète: {version} (+15)")
        else:
            log(f"Protocol récent: {version}", "ok")

    except ssl.SSLCertVerificationError as e:
        log(f"Certificat INVALIDE: {e}", "alert")
        score += 40; findings.append("Certificat invalide (+40)")
    except ConnectionRefusedError:
        log("Port 443 fermé — pas de HTTPS", "warn")
        score += 20; findings.append("Pas de HTTPS (+20)")
    except Exception as e:
        log(f"Erreur SSL: {e}", "err")

    score = min(score, 100)
    sep("VERDICT")
    print(f"\n  {risk_bar(score)}  {score}/100")
    print(f"\n  Niveau de risque: {risk_label(score)}\n")
    save("SSL Check", host, score, findings)

# ══════════════════════════════════════════════════════════
#  MODULE 5 — ANALYSER EMAIL SUSPECT
# ══════════════════════════════════════════════════════════
def email_analysis():
    sep("ANALYSE EMAIL SUSPECT", C.GREEN)
    print(f"""
  {C.DIM}Collez les headers de l'email suspect (terminez avec une ligne vide):{C.RESET}
  {C.DIM}(Dans Gmail: Afficher l'original | Outlook: Propriétés du message){C.RESET}
    """)

    lines = []
    print(f"  {C.YELLOW}▶ Headers (ligne vide pour terminer):{C.RESET}")
    while True:
        try:
            line = input("  ")
            if line == "": break
            lines.append(line)
        except (EOFError, KeyboardInterrupt):
            break

    if not lines:
        # Mode demo si pas d'input
        log("Aucun header fourni. Lancement en mode démonstration.", "warn")
        lines = [
            "From: PayPal Support <support@paypa1-secure.tk>",
            "Reply-To: noreply@evil-domain.xyz",
            "Subject: URGENT: Votre compte PayPal est suspendu !",
            "Received: from mail.suspicious.top (unknown [185.220.101.1])",
            "X-Mailer: Sendgrid v7",
            "MIME-Version: 1.0",
        ]

    headers_text = "\n".join(lines).lower()
    score = 0; findings = []

    sep("ANALYSE DES EN-TÊTES")

    # 1. Domaine expéditeur suspect
    from_match = re.search(r'from:.*?<(.+?)>', headers_text)
    if from_match:
        from_email = from_match.group(1)
        from_domain = from_email.split("@")[-1] if "@" in from_email else ""
        print(f"  {C.CYAN}From       {C.RESET} {from_email}")

        for tld in SUSPICIOUS_TLDS:
            if from_domain.endswith(tld.lstrip(".")):
                log(f"Domaine expéditeur avec TLD suspect: {from_domain}", "alert")
                score += 25; findings.append(f"TLD suspect expéditeur (+25)"); break

        for brand in BRAND_TARGETS:
            legit = LEGITIMATE_DOMAINS.get(brand)
            if legit and brand in from_domain and from_domain != legit:
                log(f"Usurpation d'identité: '{brand}' dans domaine expéditeur", "alert")
                score += 35; findings.append(f"Usurpation {brand} dans From (+35)"); break

    # 2. Reply-To différent du From
    reply_match = re.search(r'reply-to:.*?([a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,})', headers_text)
    if reply_match:
        reply_email = reply_match.group(1)
        print(f"  {C.CYAN}Reply-To   {C.RESET} {reply_email}")
        if from_match and reply_email not in headers_text.split("from:")[1][:100]:
            log("Reply-To différent du From (technique d'usurpation)", "alert")
            score += 20; findings.append("Reply-To divergent (+20)")

    # 3. Sujet urgent/alarmant
    subject_match = re.search(r'subject:\s*(.+)', headers_text)
    if subject_match:
        subject = subject_match.group(1).strip()
        print(f"  {C.CYAN}Sujet      {C.RESET} {subject}")
        urgency_words = ["urgent","suspendu","suspended","verify","alert",
                         "immediately","action required","compte bloqué",
                         "winner","congratulation","limited","expire"]
        found_urgency = [w for w in urgency_words if w in subject.lower()]
        if found_urgency:
            log(f"Sujet alarmiste: {found_urgency}", "alert")
            score += 20; findings.append(f"Sujet urgent: {found_urgency} (+20)")

    # 4. IP dans les headers Received
    ip_matches = re.findall(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', headers_text)
    if ip_matches:
        for ip in set(ip_matches[:3]):
            print(f"  {C.CYAN}IP serveur {C.RESET} {ip}")
            # IPs dans ranges connus comme spam
            octets = [int(o) for o in ip.split(".")]
            if octets[0] in [185, 194, 91, 45, 5]:
                log(f"IP dans range souvent associée au spam: {ip}", "warn")
                score += 15; findings.append(f"IP suspecte: {ip} (+15)")

    # 5. Mailer suspect
    if "sendgrid" in headers_text or "mailchimp" in headers_text or "bulk" in headers_text:
        log("Service d'envoi en masse détecté", "warn")
        score += 10; findings.append("Envoi en masse (+10)")

    score = min(score, 100)
    sep("VERDICT")
    print(f"\n  {risk_bar(score)}  {score}/100")
    print(f"\n  Niveau de risque: {risk_label(score)}\n")
    save("Email Analysis", "email", score, findings)

# ══════════════════════════════════════════════════════════
#  MODULE 6 — SCORE DE RISQUE GLOBAL
# ══════════════════════════════════════════════════════════
def global_risk_score():
    sep("ANALYSE GLOBALE — SCORE DE RISQUE COMPLET", C.GREEN)
    url = prompt("URL cible à analyser complètement")
    if not url: return
    if not url.startswith("http"): url = "http://" + url

    log("Lancement de l'analyse complète...", "info")
    scores = {}; all_findings = []

    # --- Analyse URL
    sep("1/4 — ANALYSE URL")
    try:
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.lower().replace("www.", "")
        s = 0
        if parsed.scheme == "http": s += 15
        for tld in SUSPICIOUS_TLDS:
            if domain.endswith(tld): s += 20; break
        kw = [k for k in SUSPICIOUS_URL_KEYWORDS if k in url.lower()]
        s += min(len(kw)*5, 20)
        if domain.count(".") >= 3: s += 10
        if re.match(r'^\d{1,3}\.\d{1,3}', domain): s += 30
        if len(url) > 100: s += 10
        scores["URL"] = min(s, 100)
        log(f"Score URL: {scores['URL']}/100", "info")
        all_findings.append(f"URL: {scores['URL']}/100")
    except: scores["URL"] = 0

    # --- Analyse SSL
    sep("2/4 — VÉRIFICATION SSL")
    host = parsed.netloc.replace("www.", "").split(":")[0]
    ssl_score = 0
    try:
        ctx = ssl.create_default_context()
        conn = ctx.wrap_socket(socket.socket(socket.AF_INET), server_hostname=host)
        conn.settimeout(4); conn.connect((host, 443))
        cert = conn.getpeercert(); conn.close()
        not_before = cert.get("notBefore","")
        not_after  = cert.get("notAfter","")
        issuer = dict(x[0] for x in cert.get("issuer",[]))
        try:
            issued  = datetime.strptime(not_before, "%b %d %H:%M:%S %Y %Z")
            expires = datetime.strptime(not_after,  "%b %d %H:%M:%S %Y %Z")
            age = (datetime.utcnow() - issued).days
            dur = (expires - issued).days
            if age <= 7: ssl_score += 20
            if dur <= 90: ssl_score += 10
        except: pass
        if "let's encrypt" in issuer.get("organizationName","").lower(): ssl_score += 10
        log(f"SSL accessible, score: {ssl_score}", "info")
    except ssl.SSLCertVerificationError:
        ssl_score = 40; log("Certificat SSL invalide", "alert")
    except:
        ssl_score = 20; log("HTTPS non disponible", "warn")
    scores["SSL"] = min(ssl_score, 100)
    all_findings.append(f"SSL: {scores['SSL']}/100")

    # --- Analyse contenu
    sep("3/4 — ANALYSE CONTENU")
    content_score = 0
    try:
        ctx2 = ssl.create_default_context()
        ctx2.check_hostname = False; ctx2.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=8)
        html = resp.read().decode(errors="replace").lower()
        kw_found = [kw for kw in PHISHING_CONTENT_KEYWORDS if kw in html]
        content_score += min(len(kw_found)*8, 40)
        if html.count('type="password"') > 0: content_score += 20
        if html.count("<iframe") > 0: content_score += 10
        log(f"Contenu analysé, score: {content_score}", "info")
    except Exception as e:
        log(f"Contenu inaccessible: {e}", "warn"); content_score = 10
    scores["Contenu"] = min(content_score, 100)
    all_findings.append(f"Contenu: {scores['Contenu']}/100")

    # --- DNS / réputation
    sep("4/4 — RÉPUTATION DOMAINE")
    dns_score = 0
    try:
        ip = socket.gethostbyname(host)
        log(f"Domaine résolvable: {ip}", "ok")
        if host in KNOWN_PHISHING_DOMAINS:
            dns_score = 80; log("Domaine répertorié phishing !", "alert")
    except:
        dns_score = 15; log("Domaine non résolvable", "warn")
    scores["DNS"] = min(dns_score, 100)
    all_findings.append(f"DNS: {scores['DNS']}/100")

    # Score final pondéré
    global_score = int(
        scores.get("URL",0) * 0.35 +
        scores.get("SSL",0) * 0.25 +
        scores.get("Contenu",0) * 0.30 +
        scores.get("DNS",0) * 0.10
    )

    sep("RAPPORT FINAL")
    print(f"\n  {'Module':<12} {'Score':>6}  Barre")
    sep()
    for mod, sc in scores.items():
        bar = risk_bar(sc, 100)
        print(f"  {mod:<12} {sc:>5}/100  {bar}")
    sep()
    print(f"\n  {C.BOLD}SCORE GLOBAL: {global_score}/100{C.RESET}")
    print(f"  {risk_bar(global_score)}  {global_score}/100")
    print(f"\n  Verdict: {risk_label(global_score)}\n")

    if global_score >= 70:
        print(f"  {C.RED}{C.BOLD}⛔ FORTE PROBABILITÉ DE PHISHING — Ne pas visiter / Ne pas cliquer{C.RESET}")
    elif global_score >= 40:
        print(f"  {C.YELLOW}{C.BOLD}⚠  URL SUSPECTE — Vérifier manuellement avant d'interagir{C.RESET}")
    else:
        print(f"  {C.GREEN}{C.BOLD}✓  URL probablement sûre — Restez vigilant{C.RESET}")

    save("Global Risk", url, global_score, all_findings)

# ══════════════════════════════════════════════════════════
#  MODULE 7 — BASE DE DONNÉES PHISHING
# ══════════════════════════════════════════════════════════
def phishing_database():
    sep("BASE DE DONNÉES PHISHING", C.GREEN)
    print(f"""
  {C.CYAN}[1]{C.RESET} Voir les domaines phishing connus
  {C.CYAN}[2]{C.RESET} Vérifier un domaine dans la base
  {C.CYAN}[3]{C.RESET} Voir les TLDs suspects
  {C.CYAN}[4]{C.RESET} Voir les marques les plus ciblées
    """)
    choice = prompt("Choix", "1")

    if choice == "1":
        sep(f"DOMAINES PHISHING CONNUS ({len(KNOWN_PHISHING_DOMAINS)})")
        for d in KNOWN_PHISHING_DOMAINS:
            print(f"  {C.RED}✗{C.RESET} {d}")

    elif choice == "2":
        domain = prompt("Domaine à vérifier")
        if domain.lower().replace("www.","") in KNOWN_PHISHING_DOMAINS:
            log(f"ALERTE: '{domain}' est dans la base phishing !", "alert")
        else:
            log(f"'{domain}' n'est pas dans la base locale.", "ok")
            log("Note: la base locale est limitée. Utilisez VirusTotal pour une vérification complète.", "info")

    elif choice == "3":
        sep(f"TLDs SUSPECTS ({len(SUSPICIOUS_TLDS)})")
        for i, tld in enumerate(SUSPICIOUS_TLDS):
            end = "\n" if (i+1) % 5 == 0 else "  "
            print(f"  {C.YELLOW}{tld:<8}{C.RESET}", end=end)
        print()

    elif choice == "4":
        sep("MARQUES LES PLUS CIBLÉES")
        top = ["paypal","amazon","apple","google","microsoft","facebook",
               "netflix","instagram","coinbase","impots"]
        for brand in top:
            legit = LEGITIMATE_DOMAINS.get(brand,"?")
            print(f"  {C.RED}🎯{C.RESET} {brand:<15} {C.DIM}→ légitime: {legit}{C.RESET}")

# ══════════════════════════════════════════════════════════
#  MODULE 8 — CONSEILS ANTI-PHISHING
# ══════════════════════════════════════════════════════════
def anti_phishing_tips():
    sep("CONSEILS ANTI-PHISHING & SENSIBILISATION", C.GREEN)

    tips = [
        ("🔍 Vérifier l'URL",
         "Regardez toujours l'URL complète dans la barre d'adresse.\n"
         "     paypal.com ✓ vs paypa1-secure.tk ✗"),

        ("🔐 HTTPS ne garantit pas la légitimité",
         "Un cadenas SSL ne signifie pas que le site est sûr.\n"
         "     Les phishers utilisent Let's Encrypt gratuitement."),

        ("📧 Méfiance des emails urgents",
         "Les vrais services ne demandent JAMAIS vos mots de passe par email.\n"
         "     'Urgent', 'Suspendu', 'Vérifiez maintenant' = signaux d'alarme."),

        ("🖱️ Survoler avant de cliquer",
         "Survolez les liens pour voir l'URL réelle avant de cliquer.\n"
         "     Sur mobile: appui long sur le lien."),

        ("🔑 Activer le 2FA partout",
         "L'authentification à deux facteurs protège même si le mot de passe est volé.\n"
         "     Applications recommandées: Authy, Google Authenticator."),

        ("📱 Signaler le phishing",
         "France: phishing-initiative.fr, signal-spam.fr\n"
         "     Google: reportphishing@apwg.org"),

        ("🧠 Former son entourage",
         "La meilleure défense est la sensibilisation.\n"
         "     Partagez ces conseils avec votre famille et collègues."),

        ("🔄 Ne jamais réutiliser les mots de passe",
         "Utilisez un gestionnaire de mots de passe (Bitwarden, KeePass).\n"
         "     Un site compromis = tous vos comptes en danger."),
    ]

    for i, (title, desc) in enumerate(tips, 1):
        print(f"\n  {C.GREEN}{C.BOLD}[{i}] {title}{C.RESET}")
        print(f"     {C.DIM}{desc}{C.RESET}")

    sep()
    print(f"\n  {C.BOLD}Ressources officielles:{C.RESET}")
    resources = [
        ("ANSSI (France)",      "https://www.ssi.gouv.fr"),
        ("Cybermalveillance",   "https://www.cybermalveillance.gouv.fr"),
        ("Phishing Initiative", "https://phishing-initiative.fr"),
        ("VirusTotal",          "https://www.virustotal.com"),
        ("Google Safe Browse",  "https://safebrowsing.google.com"),
    ]
    for name, url in resources:
        print(f"  {C.CYAN}→{C.RESET} {name:<22} {C.DIM}{url}{C.RESET}")

# ══════════════════════════════════════════════════════════
#  MODULE 9 — RAPPORT & EXPORT
# ══════════════════════════════════════════════════════════
def report_export():
    sep("RAPPORT & EXPORT SESSION", C.GREEN)
    print(f"""
  {C.CYAN}[1]{C.RESET} Afficher le rapport de session
  {C.CYAN}[2]{C.RESET} Exporter en JSON
  {C.CYAN}[3]{C.RESET} Exporter en TXT
  {C.CYAN}[4]{C.RESET} Effacer la session
    """)
    choice = prompt("Choix", "1")

    if choice == "1":
        sep(f"RAPPORT SESSION ({len(session['analyses'])} analyses)")
        log(f"Démarrage: {session['start']}", "info")
        if not session["analyses"]:
            log("Aucune analyse effectuée.", "warn"); return
        for a in session["analyses"]:
            col = C.RED if a["score"] >= 70 else (C.YELLOW if a["score"] >= 40 else C.GREEN)
            print(f"\n  {C.BOLD}[{a['time']}] {a['module']}{C.RESET} — {C.DIM}{a['target'][:60]}{C.RESET}")
            print(f"  Score: {col}{a['score']}/100{C.RESET}  {risk_label(a['score'])}")
            for d in a["details"][:4]:
                print(f"    {C.DIM}→ {d}{C.RESET}")

    elif choice == "2":
        fname = f"kill_phisher_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(fname, "w") as f:
                json.dump(session, f, indent=2, ensure_ascii=False)
            log(f"Rapport JSON exporté: {fname}", "ok")
        except Exception as e:
            log(f"Erreur: {e}", "err")

    elif choice == "3":
        fname = f"kill_phisher_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(fname, "w", encoding="utf-8") as f:
                f.write("═" * 60 + "\n")
                f.write("     KILL-PHISHER — Rapport d'Analyse Anti-Phishing\n")
                f.write("═" * 60 + "\n")
                f.write(f"Généré le : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Début session : {session['start']}\n\n")
                for a in session["analyses"]:
                    f.write(f"[{a['time']}] {a['module']} — {a['target']}\n")
                    f.write(f"  Score: {a['score']}/100\n")
                    for d in a["details"]:
                        f.write(f"  → {d}\n")
                    f.write("\n")
                f.write("─" * 60 + "\n")
                f.write("Créé par Léonard Durrell (hacking jack)\n")
                f.write("https://github.com/Durrell-229/Leo_jack\n")
                f.write("kill-phisher v1.0 — Usage éthique et légal uniquement\n")
            log(f"Rapport TXT exporté: {fname}", "ok")
        except Exception as e:
            log(f"Erreur: {e}", "err")

    elif choice == "4":
        confirm = prompt("Effacer la session? (oui/non)", "non")
        if confirm.lower() == "oui":
            session["analyses"].clear()
            log("Session effacée.", "ok")

# ══════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════
MODULES = {
    "1": analyze_url,
    "2": typosquatting_detect,
    "3": webpage_analysis,
    "4": ssl_phishing_check,
    "5": email_analysis,
    "6": global_risk_score,
    "7": phishing_database,
    "8": anti_phishing_tips,
    "9": report_export,
}

def main():
    clear()
    print(BANNER)

    while True:
        print(MENU)
        choice = input(f"  {C.GREEN}{C.BOLD}kill-phisher{C.RESET}{C.YELLOW}#{C.RESET} ").strip()

        if choice == "0":
            print(f"\n{C.GREEN}  [kill-phisher] Session terminée. Stay safe.{C.RESET}")
            print(f"{C.DIM}  Créé par Léonard Durrell (hacking jack){C.RESET}")
            print(f"{C.DIM}  https://github.com/Durrell-229/Leo_jack{C.RESET}\n")
            sys.exit(0)
        elif choice in MODULES:
            try:
                MODULES[choice]()
            except KeyboardInterrupt:
                log("Opération annulée.", "warn")
            except Exception as e:
                log(f"Erreur inattendue: {e}", "err")
            input(f"\n{C.DIM}  ↩  Appuie sur Entrée pour continuer...{C.RESET}")
            clear()
            print(BANNER)
        else:
            log("Option invalide.", "warn")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{C.GREEN}  [kill-phisher] Bye.{C.RESET}")
        print(f"{C.DIM}  Créé par Léonard Durrell (hacking jack){C.RESET}\n")
        sys.exit(0)
