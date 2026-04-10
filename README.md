# Tendances Vestimentaires Femme - Ete 2026

Etude professionnelle des tendances mode femme pour la saison Printemps-Ete 2026, basee sur 130+ sources (Fashion Weeks SS26, Vogue, Elle, Harper's Bazaar, WGSN, Heuritech, Pantone, Premiere Vision).

## Contenu

- **18 pages illustrees** avec 10 images IA (FLUX.1)
- 11 silhouettes & coupes
- Palette chromatique complete (Pantone NYFW + LFW)
- 12 matieres & tissus
- 7 imprimes & motifs
- 10 styles dominants
- 14 pieces cles avec gammes de prix
- 5 looks complets avec guide styling

## Fichiers

| Fichier | Description |
|---------|-------------|
| `build_pdf.py` | Generateur HTML + Playwright → PDF |
| `send_pdf.py` | Envoi du PDF par email (Gmail SMTP) |
| `images/` | 10 images FLUX.1-schnell (par tendance) |
| `Tendances_Vestimentaires_Femme_Ete_2026.pdf` | PDF final (18 pages, ~18 MB) |

## Stack technique

- Python 3.13 + Playwright (Chromium)
- FLUX.1-schnell (Black Forest Labs) via HuggingFace Spaces
- HTML/CSS magazine-style → PDF A4

## Auteur

Alexandre Collenne — Avril 2026
