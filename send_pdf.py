#!/usr/bin/env python3
"""Envoie le PDF par email."""
import smtplib, json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

CFG = json.loads(Path(r"C:\Users\Alexandre collenne\.claude\tools\email_config.json").read_text(encoding="utf-8"))
SENDER = CFG.get("sender_email") or CFG.get("sender")
PASSWORD = CFG.get("gmail_app_password") or CFG.get("app_password")
RECIPIENT = "acollenne@gmail.com"
PDF = Path(r"C:\tmp\fashion-femme-2026\Tendances_Vestimentaires_Femme_Ete_2026.pdf")

msg = MIMEMultipart()
msg["From"] = SENDER
msg["To"] = RECIPIENT
msg["Subject"] = "Tendances Vestimentaires Femme - Ete 2026 (PDF illustre)"

body = """<html><body style="font-family:Georgia,serif;color:#333;">
<h2 style="color:#2c1810;">Tendances Vestimentaires Femme — Ete 2026</h2>
<p>Ci-joint votre etude complete <strong>18 pages illustrees</strong> couvrant :</p>
<ul>
<li><strong>11 silhouettes & coupes</strong> (bulle, New New Look, liquid tailoring, body-conscious...)</li>
<li><strong>Palette chromatique complete</strong> (Pantone NYFW + LFW, WGSN x Coloro, 7 familles)</li>
<li><strong>12 matieres & tissus</strong> (lin, soie sandwashed, sheer, dentelle, crochet, liquid denim...)</li>
<li><strong>7 imprimes & motifs</strong> (floraux reinventes, rayures bold, zebre, pois, abstraits...)</li>
<li><strong>10 styles dominants</strong> (neo-romantisme, quiet luxury 2.0, lingerie-as-outerwear, gorpcore chic...)</li>
<li><strong>14 pieces cles</strong> avec gammes de prix luxe et accessible</li>
<li><strong>5 looks complets</strong> avec guide styling</li>
<li><strong>10 images IA</strong> generees par FLUX.1 illustrant chaque tendance</li>
</ul>
<p><strong>130+ sources professionnelles</strong> : Pantone, WGSN, Heuritech, Vogue, Elle, Harper's Bazaar, Marie Claire, W Magazine, WWD, Premiere Vision...</p>
<p style="color:#999;font-size:12px;">Genere automatiquement le 10 avril 2026</p>
</body></html>"""

msg.attach(MIMEText(body, "html"))

with open(PDF, "rb") as f:
    part = MIMEBase("application", "pdf")
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f'attachment; filename="{PDF.name}"')
    msg.attach(part)

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
    print(f"[OK] Email envoye a {RECIPIENT} avec {PDF.name} ({PDF.stat().st_size / 1024 / 1024:.1f} MB)")
except Exception as e:
    print(f"[ERREUR] {e}")
