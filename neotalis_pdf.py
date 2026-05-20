from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.utils import simpleSplit, ImageReader

W, H = A4
MARGIN_X = 14*mm
MARGIN_Y = 14*mm
UW = W - 2*MARGIN_X

NAVY       = colors.HexColor("#1a1a2e")
BLUE       = colors.HexColor("#2563eb")
BLUE_LIGHT = colors.HexColor("#eff6ff")
WHITE      = colors.white
SLATE_200  = colors.HexColor("#e2e8f0")
SLATE_400  = colors.HexColor("#94a3b8")
SLATE_600  = colors.HexColor("#475569")
BODY_TEXT  = colors.HexColor("#374151")
GREY_TEXT  = colors.HexColor("#6b7280")
GREEN_E    = colors.HexColor("#10b981")
AMBER_D    = colors.HexColor("#f59e0b")
ROSE_Em    = colors.HexColor("#f43f5e")

LEVEL_COLOR = {"Expert": GREEN_E, "Confirmé": BLUE, "En développement": AMBER_D, "Émergent": ROSE_Em}
LEVELS_ORDER = ["Émergent", "En développement", "Confirmé", "Expert"]

AXIS_DATA = {
    "Mémoire de travail": {
        "Expert":           ("Vous retenez et manipulez l'information avec une aisance remarquable, même sous pression. Vous gérez plusieurs fils en parallèle sans perdre le fil conducteur.", ["Continuez à vous exposer à des défis cognitifs variés.", "Les exercices dual n-back maintiennent ce niveau.", "Entraînez-vous à expliquer des sujets complexes à voix haute."]),
        "Confirmé":         ("Vous retenez et manipulez l'information avec aisance dans la plupart des contextes, à l'aise pour suivre plusieurs fils en parallèle dans des situations stables.", ["Pratiquez la mémorisation active (flashcards, lecture sans relecture).", "Introduisez progressivement des tâches multi-contextes.", "La pleine conscience améliore la rétention à court terme."]),
        "En développement": ("Votre mémoire de travail fonctionne bien dans des contextes structurés. Dans des situations très fragmentées ou multitâches, vous pouvez ressentir une surcharge.", ["Utilisez des outils visuels pour alléger la charge cognitive.", "Pratiquez le dual n-back 10 min/jour pendant 4 semaines.", "Structurez vos journées en blocs thématiques."]),
        "Émergent":         ("Votre mémoire de travail est plus efficace dans des environnements calmes et structurés. Des outils de support peuvent considérablement amplifier vos capacités.", ["Adoptez un système de capture systématique (listes, mind maps).", "Commencez par des exercices simples de mémorisation de séquences.", "Réduisez les distractions lors des tâches importantes."]),
    },
    "Contrôle inhibiteur": {
        "Expert":           ("Vous résistez efficacement aux distractions et aux automatismes. Dans des environnements à forte pression, vous gardez le cap avec une constance remarquable.", ["Challengez-vous avec des environnements de plus en plus complexes.", "Transmettez vos stratégies de concentration à votre entourage.", "Explorez la pratique du flow pour aller encore plus loin."]),
        "Confirmé":         ("Vous gérez bien les distractions dans la majorité des contextes. Votre capacité à freiner les réponses automatiques est solide dans des situations modérément exigeantes.", ["Entraînez-vous à des exercices de Stroop ou Go/No-Go en ligne.", "Pratiquez la méditation focalisée pour renforcer l'inhibition.", "Intégrez des pauses intentionnelles avant de répondre."]),
        "En développement": ("Dans des contextes rapides ou chargés en stimuli, il peut vous arriver de répondre avant d'avoir pleinement évalué la situation. Les progrès sont souvent rapides.", ["Adoptez la règle des 3 secondes avant toute décision sous pression.", "Pratiquez la cohérence cardiaque pour réguler les réponses impulsives.", "Utilisez des check-lists pour les décisions importantes."]),
        "Émergent":         ("Vous fonctionnez mieux dans des contextes calmes où les réponses automatiques sont peu sollicitées. Ce domaine offre un fort potentiel de développement.", ["Commencez par des exercices simples d'inhibition (Stroop basique).", "Intégrez des rituels de pause dans vos transitions de tâches.", "Travaillez avec un professionnel sur des stratégies d'autorégulation."]),
    },
    "Vitesse de traitement": {
        "Expert":           ("Vous traitez l'information et prenez vos décisions à un rythme soutenu avec une précision maintenue. Vous excellez dans les environnements qui demandent réactivité et fluidité.", ["Explorez des disciplines qui combinent vitesse et précision (échecs en blitz).", "Mentoriser d'autres personnes renforce encore cette capacité.", "Restez attentif à la qualité sous pression extrême."]),
        "Confirmé":         ("Vous traitez l'information à un rythme efficace dans la plupart des contextes, fluide dans les environnements qui demandent de la réactivité.", ["Pratiquez des exercices de lecture rapide pour augmenter votre débit.", "Les jeux de réaction en ligne maintiennent et développent cette capacité.", "Entraînez-vous dans des délais progressivement réduits."]),
        "En développement": ("Votre vitesse de traitement est efficace dans des contextes stables. Dans des environnements très dynamiques, quelques stratégies peuvent vous aider.", ["Pratiquez la prise de décision rapide sur des situations à faible enjeu.", "Les applications de brain training pour la catégorisation rapide sont utiles.", "Identifiez vos pics d'énergie et concentrez-y les tâches exigeantes."]),
        "Émergent":         ("Vous privilégiez la précision sur la rapidité, ce qui est une force dans les contextes qui demandent de la rigueur. La vitesse de traitement se développe progressivement.", ["Commencez par des exercices d'appariement de symboles simples.", "Fixez-vous des délais légèrement compressés pour vos tâches habituelles.", "La régularité du sommeil a un impact direct sur la vitesse de traitement."]),
    },
    "Flexibilité cognitive": {
        "Expert":           ("Vous passez d'un registre à l'autre avec naturel. Le changement vous stimule, l'ambiguïté ne vous déstabilise pas. Vous êtes un atout dans les environnements en évolution rapide.", ["Exposez-vous à des domaines très différents du vôtre.", "Prenez des responsabilités dans des projets transversaux.", "Partagez vos approches adaptatives avec vos équipes."]),
        "Confirmé":         ("Vous adaptez votre pensée et vos stratégies avec efficacité dans la plupart des contextes. Vous gérez bien les transitions et les changements de priorités.", ["Pratiquez la résolution de problèmes par des approches multiples.", "Exposez-vous à des points de vue différents des vôtres.", "La simulation de scénarios renforce la flexibilité."]),
        "En développement": ("Vous fonctionnez bien dans des cadres semi-structurés. Dans des contextes très changeants, vous pouvez avoir besoin d'un temps d'adaptation supplémentaire.", ["Introduisez volontairement de petits changements dans vos routines.", "Pratiquez l'écriture de perspectives alternatives sur des situations vécues.", "Les arts créatifs (impro, dessin) développent la flexibilité mentale."]),
        "Émergent":         ("Vous fonctionnez mieux dans des environnements prévisibles, ce qui est une force pour la constance et la fiabilité. La flexibilité se développe progressivement.", ["Commencez par de petits changements volontaires dans vos habitudes.", "Lisez des points de vue opposés aux vôtres sur des sujets maîtrisés.", "Travaillez sur la tolérance à l'ambiguïté avec un accompagnement."]),
    },
    "Attention soutenue": {
        "Expert":           ("Vous maintenez votre concentration sur de longues durées avec régularité et constance. Les tâches répétitives ou prolongées ne vous épuisent pas facilement.", ["Valorisez cette capacité dans vos missions, elle est rare et précieuse.", "Combinez-la avec des pauses stratégiques pour éviter la fatigue.", "Transmettez vos techniques de concentration à votre entourage."]),
        "Confirmé":         ("Votre attention est soutenue et régulière dans la durée. Vous gérez bien les tâches longues sans perte significative de qualité.", ["Maintenez cette capacité avec la technique Pomodoro en sessions longues.", "La pleine conscience renforce l'attention soutenue.", "Variez les formats de travail pour garder l'engagement."]),
        "En développement": ("Votre attention est efficace sur des périodes courtes à moyennes. Pour les tâches longues, des stratégies de segmentation peuvent maintenir votre niveau.", ["Utilisez la technique Pomodoro (25 min focus, 5 min pause).", "Identifiez et éliminez vos principales sources de distraction.", "Pratiquez la méditation de concentration 10 minutes par jour."]),
        "Émergent":         ("Votre attention se maintient mieux sur des durées courtes dans des environnements stimulants. C'est un axe avec un fort potentiel de développement.", ["Commencez par des sessions de concentration de 10 minutes chronométrées.", "Aménagez un espace de travail dédié, sans distracteurs visuels.", "L'activité physique régulière a un impact direct sur l'attention."]),
    },
    "Performance sous charge": {
        "Expert":           ("Sous pression, vous maintenez, voire améliorez vos performances. Le stress devient pour vous un activateur. Vous êtes précieux dans les situations critiques.", ["Continuez à vous exposer à des défis à enjeux élevés.", "Partagez vos stratégies de gestion du stress avec vos équipes.", "Restez attentif à la récupération, même les profils résilients ont besoin de recharge."]),
        "Confirmé":         ("Vous maintenez une bonne performance dans la plupart des situations de pression. Votre régulation émotionnelle et cognitive sous stress est solide.", ["Pratiquez des simulations de situations stressantes pour maintenir ce niveau.", "La cohérence cardiaque avant les moments clés consolide la régulation.", "Développez vos routines de récupération post-stress."]),
        "En développement": ("Dans des situations de forte pression, votre performance peut fluctuer. Identifier vos signaux personnels de surcharge est une étape clé.", ["Apprenez à reconnaître vos premiers signaux de surcharge.", "Pratiquez la cohérence cardiaque quotidiennement (3 fois 5 minutes).", "Développez un rituel pré-performance pour ancrer votre état optimal."]),
        "Émergent":         ("Les situations de forte pression impactent significativement votre performance actuelle. C'est un axe de développement prioritaire avec des progrès rapides possibles.", ["Commencez par des techniques de régulation corporelle (respiration 4-7-8).", "Exposez-vous progressivement à des micro-défis à enjeux croissants.", "Un accompagnement en gestion du stress peut accélérer les progrès."]),
    },
}

def get_dev_axis(results):
    level_rank = {"Émergent": 0, "En développement": 1, "Confirmé": 2, "Expert": 3}
    return min(results, key=lambda r: level_rank.get(r["level"], 99))

def section_pill(c, x, y, w, text):
    c.setFillColor(NAVY)
    c.roundRect(x, y, w, 5.5*mm, 3, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(x + 4*mm, y + 1.8*mm, text.upper())

def draw_axis_card(c, x, y, cw, ch, axis, level):
    lc = LEVEL_COLOR.get(level, BLUE)
    c.setFillColor(colors.HexColor("#00000009"))
    c.roundRect(x+0.5, y-0.8, cw, ch, 4, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setStrokeColor(SLATE_200); c.setLineWidth(0.5)
    c.roundRect(x, y, cw, ch, 4, fill=1, stroke=1)
    c.setFillColor(lc)
    c.roundRect(x, y, 4, ch, 2.5, fill=1, stroke=0)
    c.rect(x+2.5, y, 1.5, ch, fill=1, stroke=0)
    # Name
    c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 8.5)
    c.drawString(x+6*mm, y+ch-6*mm, axis)
    # Pill
    c.setFillColor(lc)
    pw = len(level)*3.9 + 9
    c.roundRect(x+cw-pw-2.5*mm, y+ch-7*mm, pw, 4.5*mm, 2, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 6)
    c.drawCentredString(x+cw-pw/2-2.5*mm, y+ch-5.2*mm, level)
    # Sep
    c.setStrokeColor(SLATE_200); c.setLineWidth(0.4)
    c.line(x+6*mm, y+ch-9.5*mm, x+cw-3*mm, y+ch-9.5*mm)
    # Desc
    desc = AXIS_DATA.get(axis, {}).get(level, ("",))[0]
    c.setFillColor(BODY_TEXT); c.setFont("Helvetica", 7)
    dlines = simpleSplit(desc, "Helvetica", 7, cw-10*mm)
    dy = y+ch-13*mm
    for dl in dlines[:3]:
        c.drawString(x+6*mm, dy, dl)
        dy -= 3.5*mm
    # Bar
    bar_y = y+2.8*mm
    idx = LEVELS_ORDER.index(level) if level in LEVELS_ORDER else 0
    seg_w = (cw-7*mm)/4
    for si in range(4):
        sx = x+4.5*mm+si*seg_w+1
        sw = seg_w-2
        c.setFillColor(lc if si<=idx else colors.HexColor("#e5e7eb"))
        c.roundRect(sx, bar_y, sw, 2.2*mm, 1, fill=1, stroke=0)


def build_pdf(output_path, logo_path, candidate_name, position, date, results):
    c = pdf_canvas.Canvas(output_path, pagesize=A4)
    ox = MARGIN_X
    col_gap = 4*mm
    col_w = (UW - col_gap) / 2
    logo_img = ImageReader(logo_path)

    # Budget: usable height = H - 2*MARGIN_Y = 841.9 - 28 = 813.9 pt
    # Sections:
    #   header       = 46mm
    #   gap          = 7mm
    #   intro pill   = 5.5mm
    #   gap          = 3mm
    #   intro text   = 2 lines * 4mm = 8mm
    #   gap          = 6mm
    #   axes pill    = 5.5mm
    #   gap          = 3mm
    #   axes grid    = 3*(card_h+row_gap) - row_gap
    #   gap          = 6mm
    #   dev pill     = 5.5mm
    #   gap          = 3mm
    #   dev card     = dev_h
    #   gap          = 5mm
    #   closing sep  = 0.5mm
    #   gap          = 3mm
    #   closing txt  = 3 lines * 3.8mm = 11.4mm
    #   footer       = 5mm
    # Total fixed (excl card_h, dev_h): ~78mm
    # Remaining for cards + dev: 813.9pt - 78mm*2.835 = 813.9 - 221 = 592.9pt = 209mm
    # card_h*6 + row_gap*2 + col_gap (already col) + dev_h
    # Let card_h=26mm, row_gap=3mm, dev_h=21mm
    # = 26*6 + 3*2 + 21 = 156+6+21 = 183mm → fits with margin

    hdr_h = 46*mm
    card_h = 26*mm
    row_gap = 3*mm
    dev_h = 21*mm

    # ── HEADER ────────────────────────────────────────────────────────────────
    hdr_y = H - MARGIN_Y - hdr_h
    c.setFillColor(colors.HexColor("#00000009"))
    c.roundRect(ox+0.5, hdr_y-0.8, UW, hdr_h, 6, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setStrokeColor(SLATE_200); c.setLineWidth(0.7)
    c.roundRect(ox, hdr_y, UW, hdr_h, 6, fill=1, stroke=1)
    c.setFillColor(BLUE)
    c.roundRect(ox, hdr_y+hdr_h-4, UW, 4, 4, fill=1, stroke=0)
    c.rect(ox, hdr_y+hdr_h-4, UW, 2.5, fill=1, stroke=0)

    logo_size = 16*mm
    lx = ox+UW/2-logo_size/2
    ly = hdr_y+hdr_h-21*mm
    c.drawImage(logo_img, lx, ly, width=logo_size, height=logo_size,
                preserveAspectRatio=True, mask='auto')

    c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(ox+UW/2, hdr_y+hdr_h-27.5*mm, candidate_name)

    pos_w = len(position)*5.0 + 16
    pos_x = ox+UW/2-pos_w/2
    c.setFillColor(BLUE_LIGHT)
    c.roundRect(pos_x, hdr_y+hdr_h-34.5*mm, pos_w, 5.5*mm, 2.5, fill=1, stroke=0)
    c.setFillColor(BLUE); c.setFont("Helvetica", 7.5)
    c.drawCentredString(ox+UW/2, hdr_y+hdr_h-32*mm, position)

    c.setFillColor(SLATE_400); c.setFont("Helvetica", 7.5)
    c.drawCentredString(ox+UW/2, hdr_y+hdr_h-40.5*mm, date)

    cursor = hdr_y - 7*mm

    # ── INTRO ─────────────────────────────────────────────────────────────────
    section_pill(c, ox, cursor-5.5*mm, UW, "Votre profil cognitif du jour")
    cursor -= 5.5*mm + 4*mm

    intro = ("Ce rapport vous offre une lecture de votre profil cognitif, obtenue dans des conditions standardisées. "
             "Il met en lumière vos forces naturelles, vos zones de confort et les directions dans lesquelles "
             "un investissement ciblé peut faire une vraie différence.")
    c.setFillColor(BODY_TEXT); c.setFont("Helvetica", 8)
    for il in simpleSplit(intro, "Helvetica", 8, UW)[:2]:
        c.drawString(ox, cursor, il)
        cursor -= 4.2*mm

    cursor -= 6*mm

    # ── AXES ──────────────────────────────────────────────────────────────────
    section_pill(c, ox, cursor-5.5*mm, UW, "Vos dimensions cognitives")
    cursor -= 5.5*mm + 3.5*mm

    for i, r in enumerate(results):
        col = i % 2
        row = i // 2
        cx = ox + col*(col_w+col_gap)
        cy = cursor - row*(card_h+row_gap) - card_h
        draw_axis_card(c, cx, cy, col_w, card_h, r["axis"], r["level"])

    cursor -= 3*(card_h+row_gap) + 6*mm

    # ── DEV AXIS ──────────────────────────────────────────────────────────────
    section_pill(c, ox, cursor-5.5*mm, UW, "Votre axe de développement prioritaire")
    cursor -= 5.5*mm + 3.5*mm

    dev = get_dev_axis(results)
    dev_axis, dev_level = dev["axis"], dev["level"]
    dev_data = AXIS_DATA.get(dev_axis, {}).get(dev_level, ("", []))
    dev_tips = dev_data[1] if len(dev_data) > 1 else []
    lc2 = LEVEL_COLOR.get(dev_level, AMBER_D)

    dev_y = cursor - dev_h
    c.setFillColor(colors.HexColor("#00000009"))
    c.roundRect(ox+0.5, dev_y-0.8, UW, dev_h, 4, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setStrokeColor(SLATE_200); c.setLineWidth(0.5)
    c.roundRect(ox, dev_y, UW, dev_h, 4, fill=1, stroke=1)
    c.setFillColor(lc2)
    c.roundRect(ox, dev_y, 4, dev_h, 2.5, fill=1, stroke=0)
    c.rect(ox+2.5, dev_y, 1.5, dev_h, fill=1, stroke=0)

    c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 9)
    c.drawString(ox+6*mm, dev_y+dev_h-6*mm, f"{dev_axis}, niveau actuel : {dev_level}")
    c.setStrokeColor(SLATE_200); c.setLineWidth(0.3)
    c.line(ox+6*mm, dev_y+dev_h-9*mm, ox+UW-3*mm, dev_y+dev_h-9*mm)
    c.setFillColor(BODY_TEXT); c.setFont("Helvetica", 7.5)
    c.drawString(ox+6*mm, dev_y+dev_h-12.5*mm,
                 "Ce n'est pas une faiblesse, c'est une direction. 3 pratiques pour progresser :")

    tip_col_w = (UW-9*mm)/3
    for ti, tip in enumerate(dev_tips[:3]):
        tx = ox+6*mm+ti*(tip_col_w+1.5*mm)
        tlines = simpleSplit(f"• {tip}", "Helvetica", 7, tip_col_w)
        c.setFont("Helvetica", 7); ty = dev_y+dev_h-16*mm
        for tl in tlines[:2]:
            c.setFillColor(BODY_TEXT); c.drawString(tx, ty, tl); ty -= 3.5*mm

    cursor = dev_y - 6*mm

    # ── CLOSING ───────────────────────────────────────────────────────────────


    closing_card_h = 28*mm
    closing_y = cursor - closing_card_h

    # Navy card
    c.setFillColor(NAVY)
    c.roundRect(ox, closing_y, UW, closing_card_h, 5, fill=1, stroke=0)

    # Blue accent bar on left
    c.setFillColor(BLUE)
    c.roundRect(ox, closing_y, 4, closing_card_h, 2.5, fill=1, stroke=0)
    c.rect(ox+2.5, closing_y, 1.5, closing_card_h, fill=1, stroke=0)

    # Quote mark decoration
    c.setFillColor(colors.HexColor("#2563eb44"))
    c.setFont("Helvetica-Bold", 36)
    c.drawString(ox+UW-14*mm, closing_y+closing_card_h-10*mm, "\u201c")

    # Title line
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(ox+7*mm, closing_y+closing_card_h-6.5*mm, "Merci d'avoir fait confiance à Neotalis.")

    # Thin separator
    c.setStrokeColor(colors.HexColor("#ffffff33"))
    c.setLineWidth(0.4)
    c.line(ox+7*mm, closing_y+closing_card_h-9*mm, ox+UW-7*mm, closing_y+closing_card_h-9*mm)

    # Body text
    body = ("Ce que vous venez de vivre n'est pas un test parmi d'autres. C'est une fenêtre sur votre façon "
            "unique de traiter le monde, et nous sommes honorés d'en avoir été les témoins. "
            "Votre profil rejoint une communauté de personnes qui croient qu'un recrutement juste "
            "commence par une meilleure connaissance de soi.")
    c.setFillColor(colors.HexColor("#cbd5e1"))
    c.setFont("Helvetica", 7.5)
    body_lines = simpleSplit(body, "Helvetica", 7.5, UW-14*mm)
    by = closing_y + closing_card_h - 12.5*mm
    for bl in body_lines[:4]:
        c.drawString(ox+7*mm, by, bl)
        by -= 3.8*mm

    # Sign-off
    c.setFillColor(colors.HexColor("#94a3b8"))
    c.setFont("Helvetica-Oblique", 7)
    c.drawString(ox+7*mm, closing_y+3.5*mm, "À bientôt,  L'équipe Neotalis")

    cursor = closing_y - 4*mm

    # Footer
    c.setFillColor(SLATE_400); c.setFont("Helvetica", 6.5)
    c.drawCentredString(ox+UW/2, MARGIN_Y-5*mm, "neotalis.com  —  Conforme LPD/RGPD")

    c.save()
    overflow = MARGIN_Y - cursor
    print(f"Cursor final: {cursor:.1f}pt  bottom margin: {MARGIN_Y:.1f}pt  overflow: {overflow:.1f}pt ({'OK' if overflow < 0 else 'OVERFLOW'})")


if __name__ == "__main__":
    build_pdf(
        "/mnt/user-data/outputs/neotalis_rapport_template.pdf",
        logo_path="/home/claude/neotalis_logo.jpeg",
        candidate_name="Marie Dupont",
        position="Chargée de recrutement",
        date="20 mai 2026",
        results=[
            {"axis": "Mémoire de travail",     "level": "Confirmé"},
            {"axis": "Contrôle inhibiteur",    "level": "En développement"},
            {"axis": "Vitesse de traitement",  "level": "Expert"},
            {"axis": "Flexibilité cognitive",  "level": "Confirmé"},
            {"axis": "Attention soutenue",     "level": "Émergent"},
            {"axis": "Performance sous charge","level": "En développement"},
        ]
    )
