from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT

BLUE        = HexColor("#2563eb")
BLUE_LIGHT  = HexColor("#eff6ff")
BLUE_MID    = HexColor("#bfdbfe")
NAVY        = HexColor("#1e3a5f")
GREEN       = HexColor("#10b981")
AMBER       = HexColor("#f59e0b")
RED         = HexColor("#f43f5e")
GRAY_BG     = HexColor("#f8fafc")
GRAY_BORDER = HexColor("#e2e8f0")
GRAY_TEXT   = HexColor("#64748b")
GRAY_DARK   = HexColor("#1e293b")
WHITE       = white

LEVEL_COLORS = {
    "Expert":           GREEN,
    "Confirmé":         BLUE,
    "En développement": AMBER,
    "Émergent":         RED,
}

LOGO_PATH = "/mnt/user-data/uploads/NEOTALIS_Logo_rond.jpeg"

MOCK = {
    "candidate_name": "Sophie Martin",
    "position":       "Chargée de Recrutement Senior",
    "company":        "DEMO BANK SA",
    "date":           "20 mai 2026",
    "job_profile":    "Banquier Junior",
    "fit_score":      78,
    "axes": [
        {"name": "Mémoire de travail",      "level": "Confirmé",          "score": 72, "target": 70},
        {"name": "Contrôle inhibiteur",     "level": "Expert",            "score": 88, "target": 75},
        {"name": "Vitesse de traitement",   "level": "En développement",  "score": 54, "target": 80},
        {"name": "Flexibilité cognitive",   "level": "Confirmé",          "score": 68, "target": 65},
        {"name": "Attention soutenue",      "level": "Émergent",          "score": 38, "target": 70},
        {"name": "Performance sous charge", "level": "En développement",  "score": 51, "target": 60},
    ],
    "executive_summary": (
        "Sophie Martin présente un profil cognitif solide sur les dimensions de contrôle inhibiteur et de mémoire de "
        "travail, deux compétences clés pour un poste orienté relation client et gestion de dossiers complexes. "
        "Sa vitesse de traitement et son attention soutenue sont en dessous des cibles du poste, ce qui mérite "
        "une exploration en entretien pour évaluer ses stratégies compensatoires. Dans l'ensemble, le profil est "
        "prometteur pour le poste visé avec un accompagnement ciblé sur les axes de développement."
    ),
    "interview_questions": [
        {
            "axis":     "Vitesse de traitement",
            "question": "Décrivez une situation où vous avez dû traiter un volume important d'informations dans un délai très court. Comment avez-vous priorisé ?",
            "why":      "Score en dessous de la cible (54/80). Explorer les stratégies de gestion de l'urgence.",
        },
        {
            "axis":     "Attention soutenue",
            "question": "Comment organisez-vous vos journées pour maintenir votre concentration sur des tâches longues et répétitives ?",
            "why":      "Niveau Émergent (38/70). Évaluer les mécanismes de maintien du focus.",
        },
        {
            "axis":     "Performance sous charge",
            "question": "Racontez une situation de forte pression où votre performance a été mise à l'épreuve. Qu'avez-vous appris sur vous-même ?",
            "why":      "Score légèrement sous la cible (51/60). Comprendre la résilience sous stress.",
        },
    ],
    "vigilance_points": [
        "L'attention soutenue (Émergent) peut impacter la qualité sur des tâches administratives longues — prévoir un environnement de travail structuré.",
        "La vitesse de traitement en dessous de la cible peut ralentir la gestion de dossiers à fort volume — évaluer la charge de travail initiale.",
        "Vérifier si la candidate a développé des stratégies compensatoires efficaces pour ses axes plus faibles.",
    ],
    "strengths": [
        "Contrôle inhibiteur exceptionnel (Expert, 88/75) — atout majeur pour la prise de décision réfléchie.",
        "Mémoire de travail au-dessus de la cible (72/70) — capacité à gérer plusieurs dossiers simultanément.",
        "Flexibilité cognitive au-dessus de la cible (68/65) — bonne adaptabilité aux changements de contexte.",
    ],
}

# ── Drawing primitives ────────────────────────────────────────────────────────

def rrect(c, x, y, w, h, r=3*mm, fill=None, stroke=None, sw=0.5):
    c.saveState()
    if fill:   c.setFillColor(fill)
    if stroke: c.setStrokeColor(stroke); c.setLineWidth(sw)
    else:      c.setLineWidth(0)
    p = c.beginPath()
    p.moveTo(x+r, y)
    p.lineTo(x+w-r, y);     p.arcTo(x+w-2*r, y,       x+w,   y+2*r,   270, 90)
    p.lineTo(x+w, y+h-r);   p.arcTo(x+w-2*r, y+h-2*r, x+w,   y+h,     0,   90)
    p.lineTo(x+r, y+h);     p.arcTo(x,       y+h-2*r,  x+2*r, y+h,     90,  90)
    p.lineTo(x,   y+r);     p.arcTo(x,       y,        x+2*r, y+2*r,   180, 90)
    p.close()
    if fill and stroke: c.drawPath(p, fill=1, stroke=1)
    elif fill:          c.drawPath(p, fill=1, stroke=0)
    else:               c.drawPath(p, fill=0, stroke=1)
    c.restoreState()

def pill_draw(c, x, y, text, bg, fg=WHITE, fs=7, ph=5*mm):
    c.saveState()
    c.setFont("Helvetica-Bold", fs)
    tw = c.stringWidth(text, "Helvetica-Bold", fs)
    pw = tw + 6*mm
    rrect(c, x, y, pw, ph, r=ph/2, fill=bg)
    c.setFillColor(fg)
    c.drawString(x + 3*mm, y + (ph - fs*0.352778)/2, text)
    c.restoreState()
    return pw

def pill_width(c, text, fs=7):
    c.setFont("Helvetica-Bold", fs)
    return c.stringWidth(text, "Helvetica-Bold", fs) + 6*mm

def score_bar(c, x, y, score, target, bw=55*mm, bh=3*mm):
    rrect(c, x, y, bw, bh, r=1.5*mm, fill=GRAY_BORDER)
    fw  = max(4*mm, bw * score / 100)
    col = GREEN if score >= target else (AMBER if score >= target*0.8 else RED)
    rrect(c, x, y, fw, bh, r=1.5*mm, fill=col)
    tx  = x + bw * target / 100
    c.setStrokeColor(NAVY); c.setLineWidth(1.2)
    c.line(tx, y-1, tx, y+bh+1)

# ── Paragraph helpers (justified / centred) ───────────────────────────────────

def para_style(fs=8, color=GRAY_DARK, align=TA_JUSTIFY, font="Helvetica", leading=None):
    return ParagraphStyle(
        "s",
        fontName=font,
        fontSize=fs,
        textColor=color,
        alignment=align,
        leading=leading or fs * 1.5,
        spaceAfter=0,
        spaceBefore=0,
    )

def draw_para(c, text, x, y, w, style):
    """Draw a Paragraph at (x,y) top-left, return bottom y."""
    p = Paragraph(text, style)
    pw, ph = p.wrap(w, 9999)
    p.drawOn(c, x, y - ph)
    return y - ph

def para_height(text, w, style):
    from reportlab.platypus import Paragraph as P
    p = P(text, style)
    _, ph = p.wrap(w, 9999)
    return ph

def section_hdr(c, x, y, w, label):
    """Navy header bar with CENTRED white title. Returns y below."""
    rrect(c, x, y-7*mm, w, 7*mm, r=2*mm, fill=NAVY)
    c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(x + w/2, y - 5.2*mm, label)
    return y - 9*mm

# ── Page manager ──────────────────────────────────────────────────────────────

class Doc:
    FOOTER_H = 13*mm

    def __init__(self, path, data):
        self.path = path; self.data = data
        self.W, self.H = A4
        self.M  = 15*mm
        self.CW = self.W - 2*self.M
        self.c  = canvas.Canvas(path, pagesize=A4)
        self.y  = self.H

    def _footer(self):
        c, W, M = self.c, self.W, self.M
        c.setFillColor(GRAY_BG); c.rect(0, 0, W, 11*mm, fill=1, stroke=0)
        c.setStrokeColor(GRAY_BORDER); c.setLineWidth(0.5); c.line(0, 11*mm, W, 11*mm)
        c.setFillColor(GRAY_TEXT); c.setFont("Helvetica", 6.5)
        c.drawString(M, 4*mm,
            "neotalis.com — Document confidentiel à usage exclusif du recruteur — Conforme LPD/RGPD")
        c.drawRightString(W - M, 4*mm, f"Généré le {self.data['date']}")

    def new_page(self):
        self._footer(); self.c.showPage()
        self.y = self.H - self.M

    def ensure(self, h):
        if self.y - h < self.FOOTER_H + 6*mm:
            self.new_page()

    def finish(self):
        self._footer(); self.c.save()

# ── Build ─────────────────────────────────────────────────────────────────────

def generate_recruiter_pdf(data=MOCK, output_path="/mnt/user-data/outputs/neotalis_recruiter_report.pdf", logo_path=LOGO_PATH):
    doc = Doc(output_path, data)
    c   = doc.c
    W, H, M, CW = doc.W, doc.H, doc.M, doc.CW
    PAD = 5*mm

    # ── HEADER ────────────────────────────────────────────────────────────────
    HDR_H  = 40*mm
    hdr_x  = M
    hdr_y  = H - M - HDR_H

    # White bg, blue border
    rrect(c, hdr_x, hdr_y, CW, HDR_H, r=3*mm, fill=WHITE, stroke=BLUE, sw=1.5)

    # Logo — left side, vertically centred
    LOGO_S = 24*mm
    logo_x = hdr_x + 6*mm
    logo_y = hdr_y + HDR_H/2 - LOGO_S/2
    try:
        c.drawImage(logo_path, logo_x, logo_y, width=LOGO_S, height=LOGO_S,
                    preserveAspectRatio=True, mask="auto")
    except Exception:
        pass

    # Name + position — centred in remaining space
    text_zone_x = logo_x + LOGO_S + 6*mm
    text_zone_w = CW - (logo_x - hdr_x) - LOGO_S - 14*mm
    name_cx = text_zone_x + text_zone_w / 2

    c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(name_cx, hdr_y + HDR_H/2 + 3*mm, data["candidate_name"])
    c.setFont("Helvetica", 9); c.setFillColor(BLUE)
    c.drawCentredString(name_cx, hdr_y + HDR_H/2 - 4*mm, data["position"])

    # Confidential tag — top right
    tag = "RAPPORT RECRUTEUR CONFIDENTIEL"
    c.setFont("Helvetica-Bold", 6.5)
    tag_tw = c.stringWidth(tag, "Helvetica-Bold", 6.5)
    tag_w  = tag_tw + 6*mm; tag_h = 5*mm
    tag_x  = W - M - tag_w - 5*mm
    tag_y2 = hdr_y + HDR_H - 9*mm
    rrect(c, tag_x, tag_y2, tag_w, tag_h, r=tag_h/2, fill=BLUE)
    c.setFillColor(WHITE)
    c.drawString(tag_x + 3*mm, tag_y2 + (tag_h - 6.5*0.352778)/2, tag)

    # Company / date — bottom right
    c.setFont("Helvetica", 7.5); c.setFillColor(GRAY_TEXT)
    c.drawRightString(W - M - 5*mm, hdr_y + 10*mm, data["company"])
    c.drawRightString(W - M - 5*mm, hdr_y + 4.5*mm, data["date"])

    doc.y = hdr_y - 6*mm

    # ── FIT BANNER ────────────────────────────────────────────────────────────
    fit   = data["fit_score"]
    fcol  = GREEN if fit >= 75 else (AMBER if fit >= 55 else RED)
    flbl  = "Bon fit" if fit >= 75 else ("Fit modéré" if fit >= 55 else "Fit faible")
    BNR_H = 18*mm
    doc.ensure(BNR_H + 4*mm)
    bx = M; by = doc.y - BNR_H
    rrect(c, bx, by, CW, BNR_H, r=3*mm, fill=BLUE_LIGHT, stroke=BLUE_MID, sw=0.6)

    cr   = 7.5*mm; cx_ = bx + 5*mm + cr; cy_ = by + BNR_H/2
    c.setFillColor(fcol); c.circle(cx_, cy_, cr, fill=1, stroke=0)
    c.setFillColor(WHITE)
    # "78/100" side by side, centred in circle
    score_str = str(fit)
    c.setFont("Helvetica-Bold", 16)
    sw_score = c.stringWidth(score_str, "Helvetica-Bold", 16)
    c.setFont("Helvetica", 8)
    sw_denom = c.stringWidth("/100", "Helvetica", 8)
    gap_px = 1
    total_w = sw_score + gap_px + sw_denom
    sx = cx_ - total_w / 2
    # baseline: vertically centred in circle
    base_y = cy_ - 3*mm
    c.setFont("Helvetica-Bold", 16); c.setFillColor(WHITE)
    c.drawString(sx, base_y, score_str)
    c.setFont("Helvetica", 8); c.setFillColor(WHITE)
    c.drawString(sx + sw_score + gap_px, base_y, "/100")

    lx = cx_ + cr + 5*mm
    c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 11)
    c.drawString(lx, cy_ + 2*mm, f"Score d'adéquation : {flbl}  ({fit}/100)")
    c.setFillColor(GRAY_TEXT); c.setFont("Helvetica", 8)
    c.drawString(lx, cy_ - 4.5*mm, f"Profil de poste référence : {data['job_profile']}")

    leg_x = W - M - 42*mm
    c.setFont("Helvetica", 7)
    c.setFillColor(fcol);  c.rect(leg_x, cy_+1.5*mm, 3*mm, 3*mm, fill=1, stroke=0)
    c.setFillColor(GRAY_TEXT); c.drawString(leg_x+4*mm, cy_+2*mm, "Score candidat")
    c.setFillColor(NAVY);  c.rect(leg_x, cy_-4*mm,   3*mm, 3*mm, fill=1, stroke=0)
    c.setFillColor(GRAY_TEXT); c.drawString(leg_x+4*mm, cy_-3.5*mm, "Cible du poste")

    doc.y = by - 6*mm

    # ── EXECUTIVE SUMMARY ─────────────────────────────────────────────────────
    st_just = para_style(fs=8, align=TA_JUSTIFY, leading=13)
    ph = para_height(data["executive_summary"], CW - 2*PAD, st_just)
    blk_h = ph + 2*PAD
    doc.ensure(9*mm + blk_h + 4*mm)
    doc.y = section_hdr(c, M, doc.y, CW, "SYNTHÈSE EXÉCUTIVE")
    rrect(c, M, doc.y - blk_h, CW, blk_h, r=2*mm, fill=GRAY_BG, stroke=GRAY_BORDER, sw=0.5)
    draw_para(c, data["executive_summary"], M+PAD, doc.y-PAD, CW-2*PAD, st_just)
    doc.y -= blk_h + 5*mm

    # ── STRENGTHS ─────────────────────────────────────────────────────────────
    st_str = para_style(fs=8, align=TA_JUSTIFY, leading=13)
    b_heights = [para_height(s, CW-14*mm, st_str) for s in data["strengths"]]
    str_h = sum(b_heights) + len(data["strengths"])*3*mm + 2*PAD
    doc.ensure(9*mm + str_h + 4*mm)
    doc.y = section_hdr(c, M, doc.y, CW, "POINTS FORTS POUR LE POSTE")
    rrect(c, M, doc.y-str_h, CW, str_h, r=2*mm,
          fill=HexColor("#f0fdf4"), stroke=HexColor("#bbf7d0"), sw=0.5)
    sy = doc.y - PAD
    for s, bh in zip(data["strengths"], b_heights):
        c.setFillColor(GREEN); c.circle(M+PAD+1.5*mm, sy-bh/2, 1.8*mm, fill=1, stroke=0)
        draw_para(c, s, M+PAD+5*mm, sy, CW-PAD-7*mm, st_str)
        sy -= bh + 3*mm
    doc.y -= str_h + 5*mm

    # ── COGNITIVE AXES ────────────────────────────────────────────────────────
    doc.ensure(9*mm)
    doc.y = section_hdr(c, M, doc.y, CW, "PROFIL COGNITIF DÉTAILLÉ")

    CARD_W = (CW - 4*mm) / 2
    CARD_H = 25*mm
    n_rows = (len(data["axes"]) + 1) // 2
    grid_h = n_rows*CARD_H + (n_rows-1)*3*mm
    doc.ensure(grid_h + 2*mm)

    for i, ax in enumerate(data["axes"]):
        col = i % 2; row = i // 2
        cx_ = M + col*(CARD_W+4*mm)
        cy_ = doc.y - row*(CARD_H+3*mm) - CARD_H
        lvc = LEVEL_COLORS.get(ax["level"], GRAY_TEXT)
        gap = ax["score"] - ax["target"]
        gcol = GREEN if gap >= 0 else RED

        rrect(c, cx_, cy_, CARD_W, CARD_H, r=2*mm, fill=WHITE, stroke=GRAY_BORDER, sw=0.5)

        # Score circle — top-left
        sc_r  = 5.5*mm
        sc_cx = cx_ + 4*mm + sc_r
        sc_cy = cy_ + CARD_H - sc_r - 4*mm
        c.setFillColor(lvc); c.circle(sc_cx, sc_cy, sc_r, fill=1, stroke=0)
        c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(sc_cx, sc_cy - 1.5*mm, str(ax["score"]))

        # Axis name — right of circle, top-aligned with circle centre
        nm_x = sc_cx + sc_r + 3*mm
        nm_y = sc_cy + 2*mm
        c.setFillColor(GRAY_DARK); c.setFont("Helvetica-Bold", 8)
        c.drawString(nm_x, nm_y, ax["name"])

        # Level pill — below axis name
        pill_draw(c, nm_x, nm_y - 6*mm, ax["level"], lvc, fs=6.5, ph=4.5*mm)

        # Target + gap — right-aligned, same vertical band as name
        c.setFont("Helvetica", 7); c.setFillColor(GRAY_TEXT)
        c.drawRightString(cx_+CARD_W-3*mm, nm_y, f"Cible : {ax['target']}")
        gap_str = f"+{gap}" if gap >= 0 else str(gap)
        c.setFont("Helvetica-Bold", 7); c.setFillColor(gcol)
        c.drawRightString(cx_+CARD_W-3*mm, nm_y-5*mm, f"Écart : {gap_str}")

        # Score bar — bottom of card
        bar_w = CARD_W - 8*mm
        score_bar(c, cx_+4*mm, cy_+5.5*mm, ax["score"], ax["target"], bw=bar_w)

        # Label below bar
        lbl = "Au-dessus de la cible ✓" if gap >= 0 else "En dessous de la cible"
        c.setFont("Helvetica", 6.5); c.setFillColor(gcol)
        c.drawString(cx_+4*mm, cy_+1.8*mm, lbl)

    doc.y -= grid_h + 5*mm

    # ── INTERVIEW QUESTIONS ───────────────────────────────────────────────────
    doc.ensure(9*mm)
    doc.y = section_hdr(c, M, doc.y, CW, "QUESTIONS D'ENTRETIEN RECOMMANDÉES")

    st_q   = para_style(fs=8, font="Helvetica-Bold", align=TA_JUSTIFY, leading=13, color=GRAY_DARK)
    st_why = para_style(fs=7.5, align=TA_JUSTIFY, leading=12, color=GRAY_TEXT)
    NR     = 4.5*mm

    for qi, q in enumerate(data["interview_questions"]):
        q_ph   = para_height(f'« {q["question"]} »', CW-2*PAD, st_q)
        why_ph = para_height(f"Pourquoi : {q['why']}", CW-2*PAD, st_why)
        # row: NR circle + pill on same line
        row_h  = NR*2 + 2*mm
        card_h = PAD + row_h + 3*mm + q_ph + 2*mm + why_ph + PAD
        doc.ensure(card_h + 4*mm)

        top = doc.y; bot = top - card_h
        rrect(c, M, bot, CW, card_h, r=2*mm, fill=WHITE, stroke=GRAY_BORDER, sw=0.5)

        # Number circle + pill — horizontally centred together
        pw    = pill_width(c, q["axis"], fs=7)
        ph_   = NR*2
        gap_  = 4*mm
        total = NR*2 + gap_ + pw
        start = M + CW/2 - total/2

        nc_cx = start + NR
        nc_cy = top - PAD - NR
        c.setFillColor(BLUE); c.circle(nc_cx, nc_cy, NR, fill=1, stroke=0)
        c.setFillColor(WHITE); c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(nc_cx, nc_cy-1.5*mm, str(qi+1))

        pill_draw(c, start+NR*2+gap_, nc_cy-NR, q["axis"], BLUE_LIGHT, fg=BLUE, fs=7, ph=ph_)

        # Question text — justified, full width
        q_top = nc_cy - NR - 4*mm
        draw_para(c, f'« {q["question"]} »', M+PAD, q_top, CW-2*PAD, st_q)

        # Why — justified
        why_top = q_top - q_ph - 2*mm
        draw_para(c, f"Pourquoi : {q['why']}", M+PAD, why_top, CW-2*PAD, st_why)

        doc.y = bot - 4*mm

    # ── VIGILANCE POINTS ──────────────────────────────────────────────────────
    st_v  = para_style(fs=8, align=TA_JUSTIFY, leading=13)
    v_phs = [para_height(v, CW-14*mm, st_v) for v in data["vigilance_points"]]
    vig_h = sum(v_phs) + len(data["vigilance_points"])*3*mm + 2*PAD
    doc.ensure(9*mm + vig_h + 4*mm)
    doc.y = section_hdr(c, M, doc.y, CW, "AXES DE VIGILANCE")
    rrect(c, M, doc.y-vig_h, CW, vig_h, r=2*mm,
          fill=HexColor("#fff7ed"), stroke=HexColor("#fed7aa"), sw=0.5)
    SQ = 3.5*mm
    vy = doc.y - PAD
    for v, vh in zip(data["vigilance_points"], v_phs):
        c.setFillColor(AMBER); c.rect(M+PAD, vy-vh/2-SQ/2+1*mm, SQ, SQ, fill=1, stroke=0)
        draw_para(c, v, M+PAD+SQ+2*mm, vy, CW-PAD-SQ-4*mm, st_v)
        vy -= vh + 3*mm

    doc.finish()
    print(f"PDF généré : {output_path}")

if __name__ == "__main__":
    generate_recruiter_pdf()
