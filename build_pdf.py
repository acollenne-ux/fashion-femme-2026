#!/usr/bin/env python3
"""
Tendances Vestimentaires Femme - Ete 2026
PDF professionnel illustre via HTML + Playwright
"""
import asyncio
import base64
import os
from pathlib import Path

IMG_DIR = Path(r"C:\tmp\fashion-femme-2026\images")
OUT_PDF = Path(r"C:\tmp\fashion-femme-2026\Tendances_Vestimentaires_Femme_Ete_2026.pdf")

def img_b64(subdir, prefix):
    """Encode une image en base64 pour l'integrer au HTML."""
    folder = IMG_DIR / subdir
    if not folder.exists():
        return ""
    for f in folder.iterdir():
        if f.suffix == ".png" and prefix in f.name:
            data = f.read_bytes()
            return f"data:image/png;base64,{base64.b64encode(data).decode()}"
    return ""

# Pre-charger toutes les images
IMAGES = {
    "romantisme": img_b64("img1", "romantisme"),
    "tailoring": img_b64("img2", "tailoring"),
    "drape": img_b64("img3", "drape"),
    "preppy": img_b64("img4", "preppy"),
    "sheer": img_b64("img5", "transparence"),
    "lin": img_b64("img6", "lin"),
    "imprimes": img_b64("img7", "imprimes"),
    "crochet": img_b64("img8", "crochet"),
    "slip": img_b64("img9", "slip"),
    "corset": img_b64("img10", "corset"),
}

CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Georgia', 'Times New Roman', serif; color: #1a1a1a; background: #fff; }

.cover {
    height: 297mm; width: 210mm;
    background: linear-gradient(135deg, #0d0d0d 0%, #2c1810 40%, #0d0d0d 100%);
    display: flex; flex-direction: column; justify-content: center; align-items: center;
    color: #fff; text-align: center; page-break-after: always;
    position: relative; overflow: hidden;
}
.cover::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at 30% 50%, rgba(180,140,100,0.15) 0%, transparent 70%);
}
.cover h1 { font-size: 42px; font-weight: 300; letter-spacing: 8px; text-transform: uppercase; margin-bottom: 12px; z-index: 1; }
.cover h2 { font-size: 22px; font-weight: 300; letter-spacing: 4px; color: #c4a882; margin-bottom: 40px; z-index: 1; }
.cover .subtitle { font-size: 14px; letter-spacing: 3px; color: #999; z-index: 1; }
.cover .line { width: 80px; height: 1px; background: #c4a882; margin: 20px auto; z-index: 1; }
.cover .date { font-size: 13px; color: #777; margin-top: 30px; z-index: 1; }

.page {
    width: 210mm; min-height: 297mm; padding: 25mm 22mm 20mm 22mm;
    page-break-after: always; position: relative;
}
.page-header {
    font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: #c4a882;
    border-bottom: 1px solid #e8e0d6; padding-bottom: 8px; margin-bottom: 20px;
}

h2.section-title {
    font-size: 28px; font-weight: 300; letter-spacing: 2px; color: #1a1a1a;
    margin-bottom: 6px;
}
.section-number { font-size: 12px; letter-spacing: 4px; color: #c4a882; text-transform: uppercase; margin-bottom: 4px; }

h3 { font-size: 18px; font-weight: 600; color: #2c1810; margin: 18px 0 8px 0; }
h4 { font-size: 14px; font-weight: 600; color: #555; margin: 12px 0 6px 0; }

p, li { font-size: 12px; line-height: 1.7; color: #333; }
ul { padding-left: 18px; margin: 6px 0; }
li { margin-bottom: 4px; }

.trend-card {
    background: #faf8f5; border-left: 3px solid #c4a882; padding: 14px 16px;
    margin: 14px 0; border-radius: 0 4px 4px 0;
}
.trend-card h3 { margin-top: 0; font-size: 16px; color: #2c1810; }
.trend-card .designers { font-size: 11px; color: #888; font-style: italic; margin-top: 6px; }

.img-section {
    display: flex; gap: 16px; margin: 16px 0; align-items: flex-start;
}
.img-section img {
    width: 220px; height: 280px; object-fit: cover; border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.img-section .text { flex: 1; }

.img-full {
    width: 100%; max-height: 320px; object-fit: cover; border-radius: 4px;
    margin: 12px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.two-images {
    display: flex; gap: 12px; margin: 14px 0;
}
.two-images img {
    width: 50%; height: 240px; object-fit: cover; border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.color-palette {
    display: flex; gap: 8px; margin: 12px 0; flex-wrap: wrap;
}
.color-swatch {
    width: 60px; height: 60px; border-radius: 4px; position: relative;
    box-shadow: 0 1px 4px rgba(0,0,0,0.15);
}
.color-swatch span {
    position: absolute; bottom: -18px; left: 0; right: 0; text-align: center;
    font-size: 8px; color: #666;
}

table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 11px; }
th { background: #2c1810; color: #fff; padding: 8px 10px; text-align: left; font-weight: 500; letter-spacing: 1px; }
td { padding: 7px 10px; border-bottom: 1px solid #eee; }
tr:nth-child(even) td { background: #faf8f5; }

/* Anti-coupure entre pages (hybride modern + legacy) */
table, .trend-card, .img-section, .highlight-box, .two-images, .color-palette {
    break-inside: avoid;
    page-break-inside: avoid;
}
h3, h4 {
    break-after: avoid;
    page-break-after: avoid;
}
tr {
    break-inside: avoid;
    page-break-inside: avoid;
}

.source-list { font-size: 10px; color: #777; line-height: 1.8; column-count: 2; column-gap: 20px; }
.source-list li { margin-bottom: 2px; }

.footer {
    position: absolute; bottom: 15mm; left: 22mm; right: 22mm;
    font-size: 9px; color: #bbb; text-align: center;
    border-top: 1px solid #eee; padding-top: 6px;
}

.sommaire { list-style: none; padding: 0; }
.sommaire li {
    font-size: 14px; padding: 10px 0; border-bottom: 1px solid #f0ebe4;
    display: flex; justify-content: space-between; align-items: baseline;
}
.sommaire .num { color: #c4a882; font-size: 12px; letter-spacing: 2px; }

.highlight-box {
    background: linear-gradient(135deg, #faf8f5, #f5f0ea);
    border: 1px solid #e8e0d6; padding: 16px; border-radius: 6px; margin: 14px 0;
}
"""

def build_html():
    return f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"><style>{CSS}</style></head><body>

<!-- COUVERTURE -->
<div class="cover">
    <div class="subtitle">ETUDE DE TENDANCES</div>
    <div class="line"></div>
    <h1>Mode Femme</h1>
    <h2>Printemps-Ete 2026</h2>
    <div class="line"></div>
    <div class="subtitle">Tendances Vestimentaires</div>
    <div class="date">Fashion Weeks SS26 &mdash; Paris &bull; Milan &bull; New York &bull; Londres<br>
    Avril 2026 &mdash; 130+ sources professionnelles</div>
</div>

<!-- SOMMAIRE -->
<div class="page">
    <div class="page-header">Tendances Vestimentaires Femme &mdash; Ete 2026</div>
    <h2 class="section-title">Sommaire</h2>
    <div class="line" style="width:60px;height:1px;background:#c4a882;margin:12px 0 24px 0;"></div>
    <ul class="sommaire">
        <li><span class="num">01</span> Silhouettes &amp; Coupes <span style="color:#999">p.3</span></li>
        <li><span class="num">02</span> Palette Chromatique <span style="color:#999">p.5</span></li>
        <li><span class="num">03</span> Matieres &amp; Tissus <span style="color:#999">p.7</span></li>
        <li><span class="num">04</span> Imprimes &amp; Motifs <span style="color:#999">p.9</span></li>
        <li><span class="num">05</span> Styles Dominants &amp; Esthetiques <span style="color:#999">p.11</span></li>
        <li><span class="num">06</span> Pieces Cles de la Garde-Robe <span style="color:#999">p.14</span></li>
        <li><span class="num">07</span> Guide Styling &amp; Combinaisons <span style="color:#999">p.17</span></li>
        <li><span class="num">08</span> Sources <span style="color:#999">p.18</span></li>
    </ul>
    <div class="footer">Etude Tendances Mode Femme SS26 &mdash; Confidentiel</div>
</div>

<!-- PAGE 3 : SILHOUETTES -->
<div class="page">
    <div class="page-header">01 &mdash; Silhouettes &amp; Coupes</div>
    <div class="section-number">Chapitre 01</div>
    <h2 class="section-title">Silhouettes &amp; Coupes</h2>
    <p style="margin:10px 0 16px;color:#666;font-size:13px;">Les podiums SS26 dessinent une femme aux silhouettes multiples : volumes sculpturaux, tailoring fluide et transparences architecturales coexistent dans une saison riche en contrastes.</p>

    <div class="img-section">
        <img src="{IMAGES['tailoring']}" alt="Tailoring fluide">
        <div class="text">
            <div class="trend-card">
                <h3>1. La Silhouette Bulle / Balloon Hem</h3>
                <p>Ourlets arrondis qui "gonflent" en forme de bulle, creant un volume spherique en bas du vetement. Le haut reste ajuste pour equilibrer. Heritage direct de Cristobal Balenciaga, annees 1950.</p>
                <div class="designers">Balenciaga (Piccioli) &bull; Loewe &bull; Simone Rocha &bull; Dior (Anderson)</div>
            </div>
            <div class="trend-card">
                <h3>2. Le "New New Look"</h3>
                <p>Reinterpretation du New Look de 1947. Taille extremement marquee, epaules arrondies, jupes tres amples et volumineuses. Jonathan Anderson pousse le concept jusqu'aux silhouettes en "abat-jour" chez Dior.</p>
                <div class="designers">Dior (Anderson) &bull; Alaia &bull; Christopher John Rogers &bull; Max Mara</div>
            </div>
        </div>
    </div>

    <div class="trend-card">
        <h3>3. Le Tailoring Fluide / "Liquid Tailoring"</h3>
        <p>Evolution du power suit rigide vers un tailleur souple et decontracte. Epaules adoucies, doublures allegees, coupes amples. Tissus a maintien sans rigidite : melanges lin-laine, crepe texture. Les vetements "coulent comme de l'eau" tout en conservant des lignes nettes.</p>
        <div class="designers">The Row &bull; Toteme &bull; Ferragamo &bull; COS</div>
    </div>

    <div class="two-images">
        <img src="{IMAGES['corset']}" alt="Corset moderne">
        <img src="{IMAGES['drape']}" alt="Drape volume">
    </div>

    <div class="trend-card">
        <h3>4. La Silhouette Pannier</h3>
        <p>Extension extreme du volume au niveau des hanches, inspiree du XVIIIe siecle. Forme large sur les cotes, plate devant/derriere. Versions modernes en tulle, tweed ou cuir.</p>
        <div class="designers">Christopher John Rogers &bull; Schiaparelli &bull; Dior &bull; Dries Van Noten</div>
    </div>

    <div class="footer">Etude Tendances Mode Femme SS26 &mdash; Page 3</div>
</div>

<!-- PAGE 4 : SILHOUETTES SUITE -->
<div class="page">
    <div class="page-header">01 &mdash; Silhouettes &amp; Coupes (suite)</div>

    <div class="trend-card">
        <h3>5. Le Body-Conscious Seducteur</h3>
        <p>Silhouettes epousant le corps, soulignant taille, hanches et buste. Cuir souple, maille seconde peau, boning apparent, details corset et harnais. Le sablier extreme fait un retour marque.</p>
        <div class="designers">Hermes (Vanhee) &bull; Mugler (Castro Freitas) &bull; Schiaparelli</div>
    </div>

    <div class="img-section">
        <img src="{IMAGES['sheer']}" alt="Transparence">
        <div class="text">
            <div class="trend-card">
                <h3>6. Le Sheer-Over-Structured</h3>
                <p>Superposition de tissus transparents (organza, tulle, mousseline) sur des fondations structurees. Tension entre exposition et controle creant un jeu visuel sophistique.</p>
                <div class="designers">Mugler &bull; Valentino &bull; Dior &bull; Chanel</div>
            </div>
            <div class="trend-card">
                <h3>7. Le Pantalon Balloon</h3>
                <p>Plisse, ample aux hanches et cuisses, resserre a la cheville. Taille haute. Drapee romantique et douce, loin des versions neon des annees 80.</p>
                <div class="designers">Isabel Marant &bull; Sacai &bull; Dries Van Noten</div>
            </div>
        </div>
    </div>

    <div class="trend-card">
        <h3>8. La Taille Basse / Drop Waist</h3>
        <p>Ligne de taille abaissee inspiree des annees 1920. Allonge le torse, parait elegante et moderne avec une ligne detendue mais polie. Versions tuxedo, ceinturees, en tissus varies.</p>
        <div class="designers">Dior (Anderson) &bull; Balenciaga &bull; Simone Rocha &bull; Cinq a Sept</div>
    </div>

    <div class="trend-card">
        <h3>9. Le Retour du Capri</h3>
        <p>Pantalon coupe a mi-mollet, version 2026 structuree et elevee. Coupe tailored, tissus premium, proportions intentionnelles. Se porte avec des pieces habillees.</p>
        <div class="designers">Versace &bull; Ralph Lauren &bull; Prada &bull; Ferragamo &bull; Chloe</div>
    </div>

    <div class="highlight-box">
        <h4>Synthese des directions silhouette</h4>
        <table>
            <tr><th>Direction</th><th>Mots-cles</th><th>Maisons leaders</th></tr>
            <tr><td>Volume bulle</td><td>Ourlets ronds, gonfles</td><td>Balenciaga, Loewe, Simone Rocha</td></tr>
            <tr><td>New New Look</td><td>Taille cintree, jupe volume</td><td>Dior, Alaia, C.J. Rogers</td></tr>
            <tr><td>Liquid tailoring</td><td>Fluide, epaules douces</td><td>The Row, Toteme, Ferragamo</td></tr>
            <tr><td>Body-conscious</td><td>Sablier, corset, cuir</td><td>Hermes, Mugler, Schiaparelli</td></tr>
            <tr><td>Cape/Cocoon</td><td>Enveloppant, drape</td><td>Valentino, Celine, Alaia</td></tr>
        </table>
    </div>
    <div class="footer">Etude Tendances Mode Femme SS26 &mdash; Page 4</div>
</div>

<!-- PAGE 5 : COULEURS -->
<div class="page">
    <div class="page-header">02 &mdash; Palette Chromatique</div>
    <div class="section-number">Chapitre 02</div>
    <h2 class="section-title">Palette Chromatique SS26</h2>
    <p style="margin:10px 0 16px;color:#666;font-size:13px;">Deux couleurs de l'annee 2026 : Cloud Dancer (Pantone) et Transformative Teal (WGSN x Coloro). La saison oscille entre pastels apaisants et couleurs saturees audacieuses.</p>

    <div class="color-palette">
        <div class="color-swatch" style="background:#F2EDE4;"><span>Cloud Dancer</span></div>
        <div class="color-swatch" style="background:#006B6B;"><span>Transform. Teal</span></div>
        <div class="color-swatch" style="background:#C5D63D;"><span>Chartreuse</span></div>
        <div class="color-swatch" style="background:#0047AB;"><span>Cobalt Blue</span></div>
        <div class="color-swatch" style="background:#D62839;"><span>Tomato Red</span></div>
        <div class="color-swatch" style="background:#C8A2C8;"><span>Burnished Lilac</span></div>
        <div class="color-swatch" style="background:#F5D491;"><span>Butter Yellow</span></div>
        <div class="color-swatch" style="background:#E85D9A;"><span>Electric Fuchsia</span></div>
        <div class="color-swatch" style="background:#98D8C8;"><span>Jelly Mint</span></div>
        <div class="color-swatch" style="background:#722F37;"><span>Burgundy</span></div>
    </div>

    <div style="margin-top:30px;">
    <div class="img-section">
        <img src="{IMAGES['imprimes']}" alt="Couleurs bold">
        <div class="text">
            <h3>La Chartreuse : Couleur N.1 de la saison</h3>
            <p>Vert-jaune lumineux neon, entre citron vert et vert acide. Presente chez <strong>Prada, Alaia, Simone Rocha, Issey Miyake, Erdem, Saint Laurent, Dries Van Noten, Burberry</strong> et Lanvin. Association iconique SS26 : <strong>Chartreuse + Burgundy</strong> (le duo Prada).</p>

            <h3 style="margin-top:16px;">Combinaisons cles</h3>
            <table>
                <tr><th>Duo</th><th>Inspiration</th></tr>
                <tr><td>Chartreuse + Burgundy</td><td>Prada SS26</td></tr>
                <tr><td>Pink + Merlot</td><td>Chanel SS26</td></tr>
                <tr><td>Cobalt + Lime</td><td>Transversal</td></tr>
                <tr><td>Chocolate + Baby Blue</td><td>Prada</td></tr>
                <tr><td>Lilac + Powder Blue</td><td>Pastel duo</td></tr>
                <tr><td>Orange + Grey</td><td>Maximalist</td></tr>
            </table>
        </div>
    </div>
    </div>

    <div class="highlight-box">
        <h4>7 familles chromatiques SS26</h4>
        <table>
            <tr><th>Famille</th><th>Teintes cles</th><th>Energie</th></tr>
            <tr><td>Verts</td><td>Chartreuse, Jelly Mint, Shale Green</td><td>Fraicheur, audace</td></tr>
            <tr><td>Bleus</td><td>Cobalt, Alexandrite, Blue Aura</td><td>Profondeur, puissance</td></tr>
            <tr><td>Roses/Violets</td><td>Lilac, Fuchsia, Amethyst Orchid</td><td>Romantisme, sophistication</td></tr>
            <tr><td>Jaunes</td><td>Acacia, Butter Yellow, Pale Banana</td><td>Soleil, optimisme</td></tr>
            <tr><td>Oranges/Rouges</td><td>Muskmelon, Tomato Red, Lava Falls</td><td>Energie, vitalite</td></tr>
            <tr><td>Neutres chauds</td><td>Caramel, Amber Haze, Angora</td><td>Luxe discret</td></tr>
            <tr><td>Blancs</td><td>Cloud Dancer, White Onyx, Ether</td><td>Purete, calme</td></tr>
        </table>
    </div>
    <div class="footer">Etude Tendances Mode Femme SS26 &mdash; Page 5</div>
</div>

<!-- PAGE 6 : COULEURS PANTONE DETAIL -->
<div class="page">
    <div class="page-header">02 &mdash; Palette Chromatique (suite)</div>

    <h3>Top 10 Pantone &mdash; NYFW SS26</h3>
    <table>
        <tr><th>#</th><th>Nom</th><th>Code Pantone</th><th>Description</th></tr>
        <tr><td>1</td><td>Acacia</td><td>13-0640 TCX</td><td>Jaune vif a sous-tons verts, lumineux et vegetal</td></tr>
        <tr><td>2</td><td>Marina</td><td>17-4041 TCX</td><td>Bleu moyen franc, aquatique et energisant</td></tr>
        <tr><td>3</td><td>Muskmelon</td><td>15-1242 TCX</td><td>Orange melon petillant, vinylique</td></tr>
        <tr><td>4</td><td>Alexandrite</td><td>18-4835 TCX</td><td>Bleu-vert teal intense, precieux</td></tr>
        <tr><td>5</td><td>Lava Falls</td><td>18-1552 TCX</td><td>Rouge lave profond et volcanique</td></tr>
        <tr><td>6</td><td>Dusty Rose</td><td>17-1718 TCX</td><td>Rose poudre vintage, doux et romantique</td></tr>
        <tr><td>7</td><td>Tea Rose</td><td>16-1620 TCX</td><td>Rose the delicat, feminite retenue</td></tr>
        <tr><td>8</td><td>Amaranth</td><td>19-2410 TCX</td><td>Pourpre sombre profond, sophistique</td></tr>
        <tr><td>9</td><td>Burnt Sienna</td><td>17-1544 TCX</td><td>Terre de Sienne brulee, teinte terreuse</td></tr>
        <tr><td>10</td><td>Burnished Lilac</td><td>15-1905 TCX</td><td>Lilas grise, charme vintage fume</td></tr>
    </table>

    <h3>Top 10 Pantone &mdash; LFW SS26</h3>
    <table>
        <tr><th>#</th><th>Nom</th><th>Code Pantone</th><th>Description</th></tr>
        <tr><td>1</td><td>Burnished Lilac</td><td>15-1905 TCX</td><td>Lilas fume (transversal NYFW + LFW)</td></tr>
        <tr><td>2</td><td>Teaberry</td><td>18-1756 TCX</td><td>Rose framboise vif, eclatant</td></tr>
        <tr><td>3</td><td>Pale Banana</td><td>12-0824 TCX</td><td>Jaune beurre pale, solaire</td></tr>
        <tr><td>4</td><td>Mandarin Orange</td><td>16-1459 TCX</td><td>Orange mandarine vitaminee</td></tr>
        <tr><td>5</td><td>Amaranth</td><td>19-2410 TCX</td><td>Pourpre profond (transversal)</td></tr>
        <tr><td>6</td><td>Tickled Pink</td><td>14-1910 TCX</td><td>Rose bonbon joyeux</td></tr>
        <tr><td>7</td><td>Amethyst Orchid</td><td>17-3628 TCX</td><td>Violet amethyste floral</td></tr>
        <tr><td>8</td><td>Caramel</td><td>16-1439 TCX</td><td>Caramel dore chaleureux</td></tr>
        <tr><td>9</td><td>Dutch Canal</td><td>14-4124 TCX</td><td>Bleu canal delicat, apaisant</td></tr>
        <tr><td>10</td><td>Shale Green</td><td>16-6116 TCX</td><td>Vert schiste mineral discret</td></tr>
    </table>

    <h3>5 couleurs cles WGSN x Coloro</h3>
    <table>
        <tr><th>Couleur</th><th>Description</th><th>Univers emotionnel</th></tr>
        <tr><td>Transformative Teal</td><td>Bleu-vert profond, marine/aquatique</td><td>Changement, eco-responsabilite</td></tr>
        <tr><td>Electric Fuchsia</td><td>Rose-violet neon</td><td>Rebellion, resilience</td></tr>
        <tr><td>Blue Aura</td><td>Bleu-gris pastel teinte</td><td>Guerison, serenite</td></tr>
        <tr><td>Amber Haze</td><td>Ambre dore envoutant</td><td>Ralentissement, regeneration</td></tr>
        <tr><td>Jelly Mint</td><td>Vert menthe bondissant</td><td>Kawaii, joie</td></tr>
    </table>
    <div class="footer">Etude Tendances Mode Femme SS26 &mdash; Page 6</div>
</div>

<!-- PAGE 7 : MATIERES -->
<div class="page">
    <div class="page-header">03 &mdash; Matieres &amp; Tissus</div>
    <div class="section-number">Chapitre 03</div>
    <h2 class="section-title">Matieres &amp; Tissus</h2>
    <p style="margin:10px 0 16px;color:#666;font-size:13px;">Le lin est sacre "hero fabric" SS26. La transparence (voile, organza, tulle) domine les podiums. Les matieres durables progressent fortement avec un marche estimé a 41 milliards USD en 2026.</p>

    <div class="img-section">
        <img src="{IMAGES['lin']}" alt="Tailleur lin">
        <div class="text">
            <div class="trend-card">
                <h3>1. Lin &amp; melanges de lin</h3>
                <p>Matiere reine SS26 : toucher naturel, texture slubee, excellente respirabilite. Melanges lin-viscose (fluidite), lin-soie (luxe), lin-coton (quotidien). Chemises oversized, pantalons wide-leg, blazers decontractes, robes bain-de-soleil.</p>
                <div class="designers">Hermes &bull; Loewe &bull; Brunello Cucinelli &bull; Loro Piana</div>
            </div>
            <div class="trend-card">
                <h3>2. Soie mate &amp; sandwashed</h3>
                <p>Toucher ultra-doux, surface mate, aspect "suede". Grande nouveaute : la soie quitte le registre soiree pour s'installer dans le vestiaire quotidien. Robes slip en coupe biais, tops a bretelles fines.</p>
                <div class="designers">Valentino &bull; Saint Laurent &bull; Luisa Spagnoli</div>
            </div>
        </div>
    </div>

    <div class="two-images">
        <img src="{IMAGES['crochet']}" alt="Crochet artisanal">
        <img src="{IMAGES['romantisme']}" alt="Dentelle romantique">
    </div>

    <div class="trend-card">
        <h3>3. Tissus transparents (Sheer / Voile / Chiffon)</h3>
        <p>Ultra-legers, aériens. Le sheer SS26 "drapé doucement et flirte avec la transparence sans etre totalement see-through". Voiles de laine semi-opaques et melanges maille whisper-light offrent une transparence sophistiquee.</p>
        <div class="designers">Chanel &bull; Dior &bull; Valentino &bull; Louis Vuitton &bull; McQueen</div>
    </div>

    <div class="trend-card">
        <h3>4. Dentelle elevee</h3>
        <p>La dentelle SS26 est "elevee et consideree". Robes longues, jupes (+20% croissance prevue UE). La dentelle comme trim est en forte croissance chez la Gen Z (+17% en Europe).</p>
        <div class="designers">Valentino &bull; Simone Rocha &bull; Dolce &amp; Gabbana</div>
    </div>

    <div class="footer">Etude Tendances Mode Femme SS26 &mdash; Page 7</div>
</div>

<!-- PAGE 8 : MATIERES SUITE -->
<div class="page">
    <div class="page-header">03 &mdash; Matieres &amp; Tissus (suite)</div>

    <div class="trend-card">
        <h3>5. Crochet &amp; maille ajouree</h3>
        <p>Texture artisanale tres tactile. Le crochet SS26 privilegie le drapé avec des fils fins et de grands crochets. Cross-occasion : du casual beach au soir. Manches dramatiques, formes geometriques, fleurs en crochet.</p>
        <div class="designers">Valentino &bull; Chloe &bull; Ulla Johnson &bull; Zimmermann</div>
    </div>

    <div class="trend-card">
        <h3>6. Organza &amp; tulle</h3>
        <p>Organza : rigide mais ultra-leger, transparent, toucher crissant. Ideal pour les volumes structures. Tulle : croissance +30% prevue SS26. Robes sculpturales, jupes volumineuses, constructions "explosant" depuis les epaules.</p>
        <div class="designers">Valentino Haute Couture &bull; Giambattista Valli &bull; Elie Saab &bull; Dolce &amp; Gabbana</div>
    </div>

    <div class="trend-card">
        <h3>7. "Liquid denim"</h3>
        <p>Denim drape, fluide et leger pour pantalons wide-leg et shackets. Coupe stovepipe chez Valentino et Khaite. Dior : jean blanc elegant. Alternative au jean classique pour l'ete.</p>
        <div class="designers">Valentino &bull; Khaite &bull; Celine &bull; Dior</div>
    </div>

    <div class="highlight-box">
        <h4>Matieres emergentes &amp; innovation</h4>
        <ul>
            <li><strong>Paillettes recyclees</strong> : Sequins en polyester recycle tracable (+20% croissance). Valentino collection "Fireflies".</li>
            <li><strong>PLAX</strong> : Bio-polymere silk-like chimiquement recyclable, plus resistant a la chaleur que le PLA.</li>
            <li><strong>Tissu de lotus</strong> : Aspect soie/lin, respirant, anti-taches, 100% waterproof.</li>
            <li><strong>Fils d'algues</strong> : Explores par les maisons de luxe.</li>
            <li><strong>Cuir de champignon (mycelium)</strong> : Alternatives orange peel en cours d'adoption.</li>
            <li><strong>Smart textiles</strong> : Capteurs integres, materiaux PCM au graphene. Marche : 9,61 milliards USD en 2026.</li>
        </ul>
    </div>

    <div class="highlight-box">
        <h4>Hierarchie des matieres SS26</h4>
        <table>
            <tr><th>Rang</th><th>Matiere</th><th>Usage principal</th><th>Durabilite</th></tr>
            <tr><td>1</td><td>Lin</td><td>Tailoring decontracte, robes</td><td>Excellente</td></tr>
            <tr><td>2</td><td>Organza / Tulle</td><td>Volumes sculpturaux</td><td>Variable</td></tr>
            <tr><td>3</td><td>Dentelle</td><td>Lingerie chic, ornements</td><td>Bonne (recycle)</td></tr>
            <tr><td>4</td><td>Soie / Satin</td><td>Slips, chemises fluides</td><td>Bonne (naturelle)</td></tr>
            <tr><td>5</td><td>Cuir souple</td><td>Vestes, blazers</td><td>Moyenne</td></tr>
            <tr><td>6</td><td>Crochet</td><td>Robes, tops ajoures</td><td>Excellente</td></tr>
            <tr><td>7</td><td>Liquid denim</td><td>Pantalons, vestes</td><td>Bonne</td></tr>
        </table>
    </div>
    <div class="footer">Etude Tendances Mode Femme SS26 &mdash; Page 8</div>
</div>

<!-- PAGE 9 : IMPRIMES -->
<div class="page">
    <div class="page-header">04 &mdash; Imprimes &amp; Motifs</div>
    <div class="section-number">Chapitre 04</div>
    <h2 class="section-title">Imprimes &amp; Motifs</h2>
    <p style="margin:10px 0 16px;color:#666;font-size:13px;">Les floraux se reinventent en 3D et "blurred vision". Les rayures passent du classique au bold. Le zebre remplace le leopard.</p>

    <div class="trend-card">
        <h3>1. Floraux reinventes</h3>
        <p>Trois sous-tendances : <strong>Bedtime Florals</strong> (petites fleurs delicates, Dior, Altuzarra), <strong>XXL Flowers</strong> (motifs surdimensionnes hypercolores), et <strong>Blurred Vision</strong> (floraux numeriquement distordus, Proenza Schouler). Chanel : jupes-boules en fleurs plumes, robes nues en blooms perles.</p>
        <div class="designers">Erdem &bull; Miu Miu &bull; Dior &bull; Chanel &bull; Proenza Schouler &bull; Dries Van Noten</div>
    </div>

    <div class="trend-card">
        <h3>2. Rayures bold</h3>
        <p>Rayures epaisses, diagonales, multi-largeurs et multi-couleurs. Finies les fines rayures marines : place a l'audace. Rayures imprimees sur tissus plisses pour un effet tridimensionnel.</p>
    </div>

    <div class="trend-card">
        <h3>3. Pois modernises</h3>
        <p>Grand retour en version modernisee : echelles exagerees (gros pois), tons neutres ou haut contraste. Versions transparentes et romantiques chez Dries Van Noten.</p>
    </div>

    <div class="trend-card">
        <h3>4. Carreaux &amp; tartans</h3>
        <p>Retour grace a Burberry dans un esprit preppy et heritage. Chanel (Matthieu Blazy) reinterprete le tweed signature en imprime tartan. Mix tons terreux et vifs.</p>
    </div>

    <div class="trend-card">
        <h3>5. Animal prints renouveles</h3>
        <p>Le <strong>zebre</strong> s'impose en 2026 (+21% UE, +17% US selon Heuritech). Le cow print explose : +87% chez les femmes US. Traitements pastel et metallise : leopard rose, python argente, zebre arc-en-ciel.</p>
    </div>

    <div class="trend-card">
        <h3>6. Motifs tropicaux revisites</h3>
        <p>Hibiscus, palmes, fruits tropicaux en palette sourde et sophistiquee : verts olive, bleu-vert, gris-vert profond, eclaires de roses poudres.</p>
    </div>

    <div class="trend-card">
        <h3>7. Graphiques &amp; abstraits</h3>
        <p>Abstractions artistiques, coups de pinceau, glitchs numeriques, illusions optiques. L'imprime devient oeuvre d'art.</p>
    </div>
    <div class="footer">Etude Tendances Mode Femme SS26 &mdash; Page 9</div>
</div>

<!-- PAGE 10 : IMPRIMES VISUEL -->
<div class="page">
    <div class="page-header">04 &mdash; Imprimes &amp; Motifs (visuels)</div>

    <div class="two-images">
        <img src="{IMAGES['imprimes']}" alt="Imprimes bold">
        <img src="{IMAGES['preppy']}" alt="Preppy carreaux">
    </div>

    <div class="highlight-box">
        <h4>Synthese des imprimes par croissance prevue (Heuritech)</h4>
        <table>
            <tr><th>Imprime</th><th>Croissance EU</th><th>Croissance US</th><th>Segment cle</th></tr>
            <tr><td>Zebre</td><td>+21%</td><td>+17%</td><td>Jupes, robes, sacs</td></tr>
            <tr><td>Cow print</td><td>--</td><td>+87%</td><td>Femmes US, casual</td></tr>
            <tr><td>Dentelle (trim)</td><td>+17%</td><td>--</td><td>Gen Z, ornements</td></tr>
            <tr><td>Jaune vanille</td><td>+22%</td><td>--</td><td>Femmes, tops, robes</td></tr>
            <tr><td>Jupes dentelle</td><td>+20%</td><td>+13%</td><td>Midi et maxi</td></tr>
            <tr><td>Tulle</td><td>+30%</td><td>+30%</td><td>Robes, jupes</td></tr>
        </table>
    </div>

    <div class="footer">Etude Tendances Mode Femme SS26 &mdash; Page 10</div>
</div>

<!-- PAGE 11 : STYLES DOMINANTS -->
<div class="page">
    <div class="page-header">05 &mdash; Styles Dominants</div>
    <div class="section-number">Chapitre 05</div>
    <h2 class="section-title">Styles Dominants &amp; Esthetiques</h2>
    <p style="margin:10px 0 16px;color:#666;font-size:13px;">10 courants stylistiques definissent l'ete 2026, du neo-romantisme structure a l'indie sleaze revival.</p>

    <div class="img-section">
        <img src="{IMAGES['romantisme']}" alt="Neo-romantisme">
        <div class="text">
            <div class="trend-card">
                <h3>1. Neo-Romantisme Structure</h3>
                <p>Retour aux codes romantiques historiques revisites avec precision contemporaine. Dentelle, volumes, emotion, mais avec maitrise structurelle. Robes en dentelle maxi, corsets legers, blouses a manches bouffantes.</p>
                <div class="designers">Valentino &bull; Simone Rocha &bull; Dries Van Noten &bull; Chanel (Blazy)</div>
            </div>
        </div>
    </div>

    <div class="trend-card">
        <h3>2. Neo-Coquette / Hyper-Feminite Sculpturale</h3>
        <p>Evolution de la coquette TikTok (15,3 milliards de vues) vers une esthetique mature et architecturale. Noeuds XXL structurels, robes a volumes exageres, bustiers en dentelle, jupes ballon.</p>
        <div class="designers">Valentino &bull; Miu Miu &bull; Loewe &bull; Mugler</div>
    </div>

    <div class="trend-card">
        <h3>3. Lingerie-as-Outerwear</h3>
        <p>La lingerie sort de l'intimite. Bralettes portees comme tops, camisoles dentelle avec jean, robes chiffon translucides. Palette sensuelle noir-rouge. Le corps est celebre a travers des matieres diaphanes.</p>
        <div class="designers">Stella McCartney &bull; Hermes &bull; Ferragamo &bull; Mugler &bull; Givenchy</div>
    </div>

    <div class="trend-card">
        <h3>4. Quiet Luxury 2.0</h3>
        <p>Le quiet luxury s'adoucit : il accepte des eclats de personnalite. Un bijou bold, un imprime inattendu, une texture surprenante. Blazers impeccables en tons neutres avec detail signature.</p>
        <div class="designers">Khaite &bull; Toteme &bull; Victoria Beckham &bull; The Row &bull; Burberry</div>
    </div>
    <div class="footer">Etude Tendances Mode Femme SS26 &mdash; Page 11</div>
</div>

<!-- PAGE 12 : STYLES SUITE -->
<div class="page">
    <div class="page-header">05 &mdash; Styles Dominants (suite)</div>

    <div class="img-section">
        <img src="{IMAGES['slip']}" alt="Slip dress satin">
        <div class="text">
            <div class="trend-card">
                <h3>5. Bold Boho / Neo-Boheme Artisanale</h3>
                <p>Un boheme "grown-up" : artisanat authentique, matieres naturelles, approche consciente. Pantalons large lin, robes crochet, pieces brodees. Moins de bangles, plus de substance.</p>
                <div class="designers">Chloe &bull; Zimmermann &bull; Ulla Johnson &bull; Isabel Marant &bull; Etro</div>
            </div>
            <div class="trend-card">
                <h3>6. Ballet Core</h3>
                <p>Grace fluide et mouvement. Robes tulle, tops maille fine, wraps et cache-coeur. Alternative douce aux esthetiques controlees. +30% croissance tulle.</p>
                <div class="designers">Simone Rocha &bull; Valentino &bull; Chanel (Blazy)</div>
            </div>
        </div>
    </div>

    <div class="trend-card">
        <h3>7. Office Siren / Power Dressing 2.0</h3>
        <p>Le bureau redevient sexy. 2,4 milliards de vues TikTok. Epaules exagerees, silhouettes sablier, seduction corporate. Blazers padded, jupes crayon, robes fourreau.</p>
        <div class="designers">Saint Laurent &bull; Versace &bull; Dolce &amp; Gabbana &bull; Prada &bull; Balenciaga</div>
    </div>

    <div class="trend-card">
        <h3>8. Gorpcore Chic / Outdoor Urbain</h3>
        <p>L'outdoor se raffine en "Quiet Outdoor" (6 milliards de vues TikTok). Vetements techniques aux lignes epurees, sans logos agressifs. Du sentier au bureau.</p>
        <div class="designers">Saint Laurent &bull; Fendi &bull; Miu Miu &bull; Arc'teryx</div>
    </div>

    <div class="trend-card">
        <h3>9. Indie Sleaze Revival</h3>
        <p>Nostalgie 2006-2012 : grunge lo-fi, glamour nocturne, rebellion decontractee. Skinny jeans (retour confirme), vestes cuir use, band tees vintage, robes chainmail (Burberry).</p>
        <div class="designers">Burberry &bull; Saint Laurent &bull; Celine &bull; Balenciaga</div>
    </div>

    <div class="trend-card">
        <h3>10. Color Blocking / Maximisme Chromatique</h3>
        <p>La couleur explose de maniere deliberee et graphique. Blocs nets, associations inattendues (cobalt/tangerine, pistache/lilas). La couleur n'est plus decorative mais structurelle.</p>
        <div class="designers">Fendi &bull; Loewe &bull; Versace &bull; Dior &bull; Dries Van Noten</div>
    </div>
    <div class="footer">Etude Tendances Mode Femme SS26 &mdash; Page 12</div>
</div>

<!-- PAGE 13 : STYLES VISUELS -->
<div class="page">
    <div class="page-header">05 &mdash; Styles Dominants (visuels)</div>

    <div class="two-images">
        <img src="{IMAGES['corset']}" alt="Corset power">
        <img src="{IMAGES['crochet']}" alt="Boho artisanal">
    </div>

    <div class="highlight-box">
        <h4>Impact reseaux sociaux par esthetique</h4>
        <table>
            <tr><th>Esthetique</th><th>Vues TikTok</th><th>Evolution 2026</th></tr>
            <tr><td>Coquette / Neo-Coquette</td><td>15,3 milliards</td><td>Evolue vers #NeoCoquette mature</td></tr>
            <tr><td>Gorpcore</td><td>6 milliards</td><td>Se raffine en "Quiet Outdoor"</td></tr>
            <tr><td>Office Siren</td><td>2,4 milliards</td><td>Sous-culture corporate seduction</td></tr>
            <tr><td>Quiet Luxury</td><td>Multi-milliards</td><td>Evolue vers #RefinedElegance</td></tr>
            <tr><td>Ballet Core</td><td>En croissance</td><td>+30% tulle depuis SS25</td></tr>
            <tr><td>Indie Sleaze</td><td>En croissance</td><td>"Dirty glamour" Gen Z</td></tr>
            <tr><td>Crochet</td><td>450M (#CrochetTop)</td><td>Festival au quotidien</td></tr>
        </table>
    </div>
    <div class="footer">Etude Tendances Mode Femme SS26 &mdash; Page 13</div>
</div>

<!-- PAGE 14 : PIECES CLES -->
<div class="page">
    <div class="page-header">06 &mdash; Pieces Cles</div>
    <div class="section-number">Chapitre 06</div>
    <h2 class="section-title">Pieces Cles de la Garde-Robe</h2>
    <p style="margin:10px 0 16px;color:#666;font-size:13px;">14 pieces incontournables, de la robe drop-waist au top polo, avec gammes de prix du luxe a l'accessible.</p>

    <div class="img-section">
        <img src="{IMAGES['drape']}" alt="Robe drapee">
        <div class="text">
            <div class="trend-card">
                <h3>1. Robe a taille basse (Drop-Waist)</h3>
                <p>LA silhouette robe N.1. Inspiration annees 1920/flapper, taille abaissee aux hanches, allongement du buste. Versions a pois ou franges pour le soir.</p>
                <div class="designers">Chanel (Blazy) &bull; Versace &bull; Ferragamo &bull; Tory Burch</div>
                <p style="font-size:10px;color:#888;margin-top:4px;">Luxe 1 500-4 000 EUR | Accessible 40-120 EUR</p>
            </div>
            <div class="trend-card">
                <h3>2. Pantalon large taille haute</h3>
                <p>Performeur N.1 avec +400% de croissance sur les podiums de Milan. Le "smart pant" remplace le jean de juin a septembre. Lin matiere reine.</p>
                <div class="designers">Prada &bull; Max Mara &bull; Celine &bull; COS</div>
                <p style="font-size:10px;color:#888;margin-top:4px;">Luxe 800-2 200 EUR | Accessible 30-80 EUR</p>
            </div>
        </div>
    </div>

    <div class="trend-card">
        <h3>3. Blazer oversize a col releve</h3>
        <p>Esprit annees 80 mais en version fluide et drapee. Le col releve est le detail signature. Double-boutonnage type Napoleon. Combo star : blazer + bermuda.</p>
        <div class="designers">Celine &bull; Chloe &bull; Calvin Klein Collection &bull; Khaite &bull; Max Mara</div>
        <p style="font-size:10px;color:#888;margin-top:4px;">Luxe 2 000-4 500 EUR | Accessible 60-150 EUR</p>
    </div>

    <div class="trend-card">
        <h3>4. Jupe evasee / Flare (+300% podiums)</h3>
        <p>Jupons froufroutants en tulle, organza, taffetas dans des tons "glace". Jupes a godets, versions patineuse. Silhouettes sculpturales et joyeuses.</p>
        <div class="designers">Prada &bull; Erdem &bull; Jacquemus &bull; Stella McCartney</div>
    </div>

    <div class="trend-card">
        <h3>5. Robe slip / nuisette en dentelle</h3>
        <p>La tendance "lingerie-as-outerwear" domine Paris. Slips en soie garnis de dentelle, nuisettes portees en plein jour. Version mature du "naked dressing".</p>
        <div class="designers">Saint Laurent &bull; Chloe &bull; Magda Butrym &bull; Valentino</div>
        <p style="font-size:10px;color:#888;margin-top:4px;">Luxe 1 500-4 000 EUR | Accessible 30-80 EUR</p>
    </div>
    <div class="footer">Etude Tendances Mode Femme SS26 &mdash; Page 14</div>
</div>

<!-- PAGE 15 : PIECES CLES SUITE -->
<div class="page">
    <div class="page-header">06 &mdash; Pieces Cles (suite)</div>

    <div class="two-images">
        <img src="{IMAGES['tailoring']}" alt="Blazer oversize">
        <img src="{IMAGES['preppy']}" alt="Preppy chic">
    </div>

    <div class="trend-card">
        <h3>6. Trench court (Cropped)</h3>
        <p>Piece outerwear star. Coupe aux hanches ou au-dessus. Deux directions : minimaliste ou excentrique. Louise Trotter chez Bottega Veneta sculpte des versions cuir.</p>
        <div class="designers">Bottega Veneta &bull; The Attico &bull; Burberry &bull; Saint Laurent &bull; Khaite</div>
        <p style="font-size:10px;color:#888;margin-top:4px;">Luxe 2 000-5 000 EUR | Accessible 60-150 EUR</p>
    </div>

    <div class="trend-card">
        <h3>7. Bralette structuree (portee comme top)</h3>
        <p>Passe du sous-vetement au vetement. Sous blazers, superposee sur chemises. Structures en satin, tricot cotele ou lin.</p>
        <div class="designers">Loewe &bull; Prada &bull; Dior &bull; Saint Laurent &bull; Erdem</div>
        <p style="font-size:10px;color:#888;margin-top:4px;">Luxe 400-1 200 EUR | Accessible 15-50 EUR</p>
    </div>

    <div class="trend-card">
        <h3>8. Jupe ballon (Bubble Hem)</h3>
        <p>Ourlet elastique creant une forme cloche/puffball. Prada : mini noire preppy avec chemise boutonnee. Regle d'or : haut simple, la forme IS la declaration.</p>
        <div class="designers">Prada &bull; Erdem &bull; Jacquemus &bull; Stella McCartney</div>
    </div>

    <div class="trend-card">
        <h3>9. Piece a franges</h3>
        <p>Franges PARTOUT : detail texture dominant. Plus industrielles et architecturales que boho. Bottega Veneta : franges en fibre de verre recyclee sur l'Intrecciato.</p>
        <div class="designers">Bottega Veneta &bull; Balmain &bull; Dolce &amp; Gabbana &bull; Chanel &bull; Rick Owens</div>
    </div>

    <div class="trend-card">
        <h3>10. Bermuda elegant</h3>
        <p>Short mi-long structure. Compagnon ideal du blazer oversize. Le duo blazer + bermuda = combo star SS26.</p>
        <div class="designers">Celine &bull; Max Mara &bull; Miu Miu</div>
    </div>

    <div class="trend-card">
        <h3>11. Top polo</h3>
        <p>Piece versatile : sous un pull, avec une jupe midi, ou seul. Coupe ajustee, manches courtes.</p>
        <div class="designers">Lacoste &bull; Ralph Lauren &bull; Miu Miu &bull; Celine</div>
    </div>
    <div class="footer">Etude Tendances Mode Femme SS26 &mdash; Page 15</div>
</div>

<!-- PAGE 16 : PIECES CLES VISUELS -->
<div class="page">
    <div class="page-header">06 &mdash; Pieces Cles (visuels)</div>

    <div class="two-images">
        <img src="{IMAGES['slip']}" alt="Slip dress">
        <img src="{IMAGES['sheer']}" alt="Transparence layering">
    </div>

    <div class="highlight-box">
        <h4>Top 14 pieces SS26 &mdash; Synthese complete</h4>
        <table>
            <tr><th>Piece</th><th>Croissance podiums</th><th>Matiere phare</th><th>Prix accessible</th></tr>
            <tr><td>Pantalon large taille haute</td><td>+400%</td><td>Lin</td><td>30-80 EUR</td></tr>
            <tr><td>Jupe evasee</td><td>+300%</td><td>Tulle, organza</td><td>40-100 EUR</td></tr>
            <tr><td>Robe drop-waist</td><td>N.1 robe</td><td>Coton, lin</td><td>40-120 EUR</td></tr>
            <tr><td>Blazer oversize</td><td>Stable fort</td><td>Laine legere</td><td>60-150 EUR</td></tr>
            <tr><td>Robe slip dentelle</td><td>Forte</td><td>Soie, satin</td><td>30-80 EUR</td></tr>
            <tr><td>Trench court</td><td>Star outerwear</td><td>Gabardine, cuir</td><td>60-150 EUR</td></tr>
            <tr><td>Bralette structuree</td><td>Forte</td><td>Satin, cotele</td><td>15-50 EUR</td></tr>
            <tr><td>Jupe ballon</td><td>Forte</td><td>Taffetas, nylon</td><td>40-90 EUR</td></tr>
            <tr><td>Piece a franges</td><td>Forte</td><td>Cuir, raffia</td><td>50-150 EUR</td></tr>
            <tr><td>Bermuda elegant</td><td>Forte</td><td>Lin, gabardine</td><td>30-80 EUR</td></tr>
            <tr><td>Top polo</td><td>Stable</td><td>Coton pique</td><td>20-60 EUR</td></tr>
            <tr><td>Pantalon ballon</td><td>Surprise SS26</td><td>Denim, coton</td><td>50-100 EUR</td></tr>
            <tr><td>Robe chemise</td><td>Stable</td><td>Popeline, lin</td><td>40-100 EUR</td></tr>
            <tr><td>Veste cuir ajustee</td><td>Retour</td><td>Cuir agneau</td><td>80-200 EUR</td></tr>
        </table>
    </div>
    <div class="footer">Etude Tendances Mode Femme SS26 &mdash; Page 16</div>
</div>

<!-- PAGE 17 : GUIDE STYLING -->
<div class="page">
    <div class="page-header">07 &mdash; Guide Styling</div>
    <div class="section-number">Chapitre 07</div>
    <h2 class="section-title">Guide Styling &amp; Combinaisons</h2>

    <h3>5 looks cles a adopter cet ete</h3>

    <div class="trend-card">
        <h3>Look 1 : Neo-Romantique Bureau</h3>
        <p><strong>Pieces :</strong> Robe midi dentelle ivoire + blazer oversize col releve creme + bralette structuree en dessous<br>
        <strong>Matiere :</strong> Dentelle soie + laine legere<br>
        <strong>Couleur :</strong> Ton sur ton ivoire/creme + touche Burnished Lilac (sac)</p>
    </div>

    <div class="trend-card">
        <h3>Look 2 : Power Tailoring Fluide</h3>
        <p><strong>Pieces :</strong> Tailleur pantalon lin + top polo ajuste + bermuda alternatif<br>
        <strong>Matiere :</strong> Lin lave, soie sandwashed<br>
        <strong>Couleur :</strong> Chartreuse (top) + Burgundy (pantalon) = duo Prada SS26</p>
    </div>

    <div class="trend-card">
        <h3>Look 3 : Boho Artisanal Chic</h3>
        <p><strong>Pieces :</strong> Robe crochet midi + ceinture cuir fine + cardigan fin noue<br>
        <strong>Matiere :</strong> Crochet coton bio, cuir souple<br>
        <strong>Couleur :</strong> Ecru/naturel + touches Amber Haze</p>
    </div>

    <div class="trend-card">
        <h3>Look 4 : Lingerie-Chic Soiree</h3>
        <p><strong>Pieces :</strong> Slip dress satin + chemise ouverte oversize + corset leger<br>
        <strong>Matiere :</strong> Satin soie, mousseline, dentelle<br>
        <strong>Couleur :</strong> Noir + Lava Falls (rouge lave) pour le contraste</p>
    </div>

    <div class="trend-card">
        <h3>Look 5 : Color Block Maximaliste</h3>
        <p><strong>Pieces :</strong> Jupe evasee tulle + top ajuste contraste + trench court<br>
        <strong>Matiere :</strong> Tulle, organza, gabardine<br>
        <strong>Couleur :</strong> Cobalt blue (jupe) + Mandarin orange (top) + Cloud Dancer (trench)</p>
    </div>

    <div class="highlight-box">
        <h4>Regles d'or du styling SS26</h4>
        <ul>
            <li><strong>Equilibre des volumes :</strong> haut ajuste + bas ample OU haut volumineux + bas slim</li>
            <li><strong>Le layering est roi :</strong> sheer sur structure, bralette sous blazer, cardigan noue sur slip dress</li>
            <li><strong>Un seul point focal :</strong> si la jupe est volumineuse, le haut reste sobre. Si le top est bold, le bas est neutre</li>
            <li><strong>Mix matieres :</strong> cuir + dentelle, lin + soie, crochet + satin</li>
            <li><strong>Le duo star :</strong> blazer oversize + bermuda elegant</li>
        </ul>
    </div>
    <div class="footer">Etude Tendances Mode Femme SS26 &mdash; Page 17</div>
</div>

<!-- PAGE 18 : SOURCES -->
<div class="page">
    <div class="page-header">08 &mdash; Sources</div>
    <div class="section-number">Chapitre 08</div>
    <h2 class="section-title">Sources</h2>
    <p style="margin:10px 0 16px;color:#666;font-size:13px;">130+ sources professionnelles collectees via 5 agents de recherche paralleles.</p>

    <h4>Institutions &amp; previsions</h4>
    <ul class="source-list">
        <li>Pantone (NYFW + LFW SS26 Color Reports)</li>
        <li>WGSN x Coloro (Colour of the Year 2026)</li>
        <li>Heuritech (Top 10 SS26 Trend Forecast)</li>
        <li>Premiere Vision (SS26 Fabric Trends)</li>
        <li>Milano Unica (Textile Sourcing)</li>
        <li>McKinsey State of Fashion 2026</li>
    </ul>

    <h4>Presse specialisee</h4>
    <ul class="source-list">
        <li>Who What Wear (16+ articles SS26)</li>
        <li>Vogue (Scandinavia, Adria, France)</li>
        <li>W Magazine (Runway reviews)</li>
        <li>Harper's Bazaar (India, UK, US)</li>
        <li>Elle (Australia, France)</li>
        <li>Marie Claire (US, UK, France)</li>
        <li>Grazia (Singapore, US)</li>
        <li>Refinery29 (Spring 2026 Trends)</li>
        <li>Coveteur (SS26 Runway Report)</li>
        <li>Numero Magazine</li>
        <li>FashionUnited (Trend Reports)</li>
        <li>WWD (Textiles + Fashion Trends)</li>
        <li>Net-a-Porter PORTER</li>
    </ul>

    <h4>Fashion Weeks couvertes</h4>
    <ul class="source-list">
        <li>Paris Fashion Week SS26</li>
        <li>Milan Fashion Week SS26</li>
        <li>New York Fashion Week SS26</li>
        <li>London Fashion Week SS26</li>
    </ul>

    <h4>Marques &amp; createurs cites (30+)</h4>
    <p style="font-size:11px;color:#555;line-height:1.6;">
        Alaia, Alexander McQueen, Balenciaga (Piccioli), Balmain, Bottega Veneta (Louise Trotter), Brunello Cucinelli, Burberry, Celine, Chanel (Matthieu Blazy), Chloe (Chemena Kamali), Christopher John Rogers, COS, Dior (Jonathan Anderson), Dolce &amp; Gabbana, Dries Van Noten, Erdem, Fendi, Ferragamo, Giambattista Valli, Givenchy, Hermes (Nadege Vanhee), Isabel Marant, Jacquemus, Khaite, Loewe, Loro Piana, Max Mara, Miu Miu, Mugler (Castro Freitas), Prada, Ralph Lauren, Saint Laurent, Schiaparelli, Simone Rocha, Stella McCartney, The Row, Toteme, Valentino (Alessandro Michele), Versace, Victoria Beckham, Zimmermann.
    </p>

    <div style="margin-top:20px;text-align:center;color:#999;font-size:11px;">
        <div class="line" style="width:60px;height:1px;background:#c4a882;margin:20px auto;"></div>
        <p>Etude realisee le 10 avril 2026<br>
        130+ sources professionnelles &bull; 5 agents de recherche paralleles<br>
        10 images generees par IA (FLUX.1-schnell, Black Forest Labs)</p>
    </div>
    <div class="footer">Etude Tendances Mode Femme SS26 &mdash; Page 18</div>
</div>

</body></html>"""

async def generate_pdf():
    from playwright.async_api import async_playwright
    html = build_html()
    html_path = Path(r"C:\tmp\fashion-femme-2026\rapport.html")
    html_path.write_text(html, encoding="utf-8")
    print(f"[OK] HTML genere : {html_path}")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"file:///{html_path.as_posix()}", wait_until="networkidle")
        await page.pdf(
            path=str(OUT_PDF),
            format="A4",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
        )
        await browser.close()
    print(f"[OK] PDF genere : {OUT_PDF} ({OUT_PDF.stat().st_size / 1024:.0f} KB)")

if __name__ == "__main__":
    asyncio.run(generate_pdf())
