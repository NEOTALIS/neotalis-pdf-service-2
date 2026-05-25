# -*- coding: utf-8 -*-
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Register DejaVu fonts for full UTF-8 support
_dir = os.path.dirname(__file__)
try:
    pdfmetrics.registerFont(TTFont("DejaVu", os.path.join(_dir, "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", os.path.join(_dir, "DejaVuSans-Bold.ttf")))
    FONT_NORMAL = "DejaVu"
    FONT_BOLD   = "DejaVu-Bold"
except Exception:
    FONT_NORMAL = "Helvetica"
    FONT_BOLD   = "Helvetica-Bold"

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
    "Confirm\u00e9":         BLUE,
    "Confirme":         BLUE,
    "En d\u00e9veloppement": AMBER,
    "En developpement": AMBER,
    "\u00c9mergent":         RED,
    "Emergent":         RED,
}

LOGO_PATH = "/mnt/user-data/uploads/NEOTALIS_Logo_rond.jpeg"

MOCK = {
    "candidate_name": "Sophie Martin",
    "position":       "Charg\u00e9e de Recrutement Senior",
    "company":        "DEMO BANK SA",
    "date":           "20 mai 2026",
    "job_profile":    "Banquier Junior",
    "fit_score":      78,
    "axes": [
        {"name": "M\u00e9moire de travail",      "level": "Confirm\u00e9",          "score": 72, "target": 70},
        {"name": "Contr\u00f4le inhibiteur",     "level": "Expert",            "score": 88, "target": 75},
        {"name": "Vitesse de traitement",   "level": "En d\u00e9veloppement",  "score": 54, "target": 80},
        {"name": "Flexibilit\u00e9 cognitive",   "level": "Confirm\u00e9",          "score": 68, "target": 65},
        {"name": "Attention soutenue",      "level": "\u00c9mergent",          "score": 38, "target": 70},
        {"name": "Performance sous charge", "level": "En d\u00e9veloppement",  "score": 51, "target": 60},
    ],
    "executive_summary": (
        "Sophie Martin pr\u00e9sente un profil cognitif solide sur les dimensions de contr\u00f4le inhibiteur et de m\u00e9moire de "
        "travail, deux comp\u00e9tences cl\u00e9s pour un poste orient\u00e9 relation client et gestion de dossiers complexes. "
        "Sa vitesse de traitement et son attention soutenue sont en dessous des cibles du poste, ce qui m\u00e9rite "
        "une exploration en entretien pour \u00e9valuer ses strat\u00e9gies compensatoires. Dans l'ensemble, le profil est "
        "prometteur pour le poste vis\u00e9 avec un accompagnement cibl\u00e9 sur les axes de d\u00e9veloppement."
    ),
    "interview_questions": [
        {
            "axis":     "Vitesse de traitement",
            "question": "D\u00e9crivez une situation o\u00f9 vous avez d\u00fb traiter un volume important d'informations dans un d\u00e9lai tr\u00e8s court. Comment avez-vous prioris\u00e9 ?",
            "why":      "Score en dessous de la cible (54/80). Explorer les strat\u00e9gies de gestion de l'urgence.",
        },
        {
            "axis":     "Attention soutenue",
            "question": "Comment organisez-vous vos journ\u00e9es pour maintenir votre concentration sur des t\u00e2ches longues et r\u00e9p\u00e9titives ?",
            "why":      "Niveau \u00c9mergent (38/70). \u00c9valuer les m\u00e9canismes de maintien du focus.",
        },
        {
            "axis":     "Performance sous charge",
            "question": "Racontez une situation de forte pression o\u00f9 votre performance a \u00e9t\u00e9 mise \u00e0 l'\u00e9preuve. Qu'avez-vous appris sur vous-m\u00eame ?",
            "why":      "Score l\u00e9g\u00e8rement sous la cible (51/60). Comprendre la r\u00e9silience sous stress.",
        },
    ],
    "vigilance_points": [
        "L'attention soutenue (\u00c9mergent) peut impacter la qualit\u00e9 sur des t\u00e2ches administratives longues \u2014 pr\u00e9voir un environnement de travail structur\u00e9.",
        "La vitesse de traitement en dessous de la cible peut ralentir la gestion de dossiers \u00e0 fort volume \u2014 \u00e9valuer la charge de travail initiale.",
        "V\u00e9rifier si la candidate a d\u00e9velopp\u00e9 des strat\u00e9gies compensatoires efficaces pour ses axes plus faibles.",
    ],
    "strengths": [
        "Contr\u00f4le inhibiteur exceptionnel (Expert, 88/75) \u2014 atout majeur pour la prise de d\u00e9cision r\u00e9fl\u00e9chie.",
        "M\u00e9moire de travail au-dessus de la cible (72/70) \u2014 capacit\u00e9 \u00e0 g\u00e9rer plusieurs dossiers simultan\u00e9ment.",
        "Flexibilit\u00e9 cognitive au-dessus de la cible (68/65) \u2014 bonne adaptabilit\u00e9 aux changements de contexte.",
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
    c.setFont(FONT_BOLD, fs)
    tw = c.stringWidth(text, FONT_BOLD, fs)
    pw = tw + 6*mm
    rrect(c, x, y, pw, ph, r=ph/2, fill=bg)
    c.setFillColor(fg)
    c.drawString(x + 3*mm, y + (ph - fs*0.352778)/2, text)
    c.restoreState()
    return pw

def pill_width(c, text, fs=7):
    c.setFont(FONT_BOLD, fs)
    return c.stringWidth(text, FONT_BOLD, fs) + 6*mm

def score_bar(c, x, y, score, target, bw=55*mm, bh=3*mm):
    rrect(c, x, y, bw, bh, r=1.5*mm, fill=GRAY_BORDER)
    fw  = max(4*mm, bw * score / 100)
    col = GREEN if score >= target else (AMBER if score >= target*0.8 else RED)
    rrect(c, x, y, fw, bh, r=1.5*mm, fill=col)
    tx  = x + bw * target / 100
    c.setStrokeColor(NAVY); c.setLineWidth(1.2)
    c.line(tx, y-1, tx, y+bh+1)

def para_style(fs=8, color=GRAY_DARK, align=TA_JUSTIFY, font=None, leading=None):
    return ParagraphStyle(
        "s",
        fontName=font or FONT_NORMAL,
        fontSize=fs,
        textColor=color,
        alignment=align,
        leading=leading or fs * 1.5,
        spaceAfter=0,
        spaceBefore=0,
    )

def draw_para(c, text, x, y, w, style):
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
    rrect(c, x, y-7*mm, w, 7*mm, r=2*mm, fill=NAVY)
    c.setFillColor(WHITE); c.setFont(FONT_BOLD, 8)
    c.drawCentredString(x + w/2, y - 5.2*mm, label)
    return y - 9*mm

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
        c.setFillColor(GRAY_TEXT); c.setFont(FONT_NORMAL, 6.5)
        c.drawString(M, 4*mm,
            "neotalis.com \u2014 Document confidentiel \u00e0 usage exclusif du recruteur \u2014 Conforme LPD/RGPD")
        c.drawRightString(W - M, 4*mm, f"G\u00e9n\u00e9r\u00e9 le {self.data['date']}")

    def new_page(self):
        self._footer(); self.c.showPage()
        self.y = self.H - self.M

    def ensure(self, h):
        if self.y - h < self.FOOTER_H + 6*mm:
            self.new_page()

    def finish(self):
        self._footer(); self.c.save()

def generate_recruiter_pdf(data=MOCK, output_path="/mnt/user-data/outputs/neotalis_recruiter_report.pdf", logo_path=LOGO_PATH):
    doc = Doc(output_path, data)
    c   = doc.c
    W, H, M, CW = doc.W, doc.H, doc.M, doc.CW
    PAD = 5*mm

    HDR_H  = 40*mm
    hdr_x  = M
    hdr_y  = H - M - HDR_H

    rrect(c, hdr_x, hdr_y, CW, HDR_H, r=3*mm, fill=WHITE, stroke=BLUE, sw=1.5)

    LOGO_S = 24*mm
    logo_x = hdr_x + 6*mm
    logo_y = hdr_y + HDR_H/2 - LOGO_S/2
    try:
        c.drawImage(logo_path, logo_x, logo_y, width=LOGO_S, height=LOGO_S,
                    preserveAspectRatio=True, mask="auto")
    except Exception:
        pass

    text_zone_x = logo_x + LOGO_S + 6*mm
    text_zone_w = CW - (logo_x - hdr_x) - LOGO_S - 14*mm
    name_cx = text_zone_x + text_zone_w / 2

    c.setFillColor(NAVY); c.setFont(FONT_BOLD, 18)
    c.drawCentredString(name_cx, hdr_y + HDR_H/2 + 3*mm, data["candidate_name"])
    c.setFont(FONT_NORMAL, 9); c.setFillColor(BLUE)
    c.drawCentredString(name_cx, hdr_y + HDR_H/2 - 4*mm, data["position"])

    tag = "RAPPORT RECRUTEUR CONFIDENTIEL"
    c.setFont(FONT_BOLD, 6.5)
    tag_tw = c.stringWidth(tag, FONT_BOLD, 6.5)
    tag_w  = tag_tw + 6*mm; tag_h = 5*mm
    tag_x  = W - M - tag_w - 5*mm
    tag_y2 = hdr_y + HDR_H - 9*mm
    rrect(c, tag_x, tag_y2, tag_w, tag_h, r=tag_h/2, fill=BLUE)
    c.setFillColor(WHITE)
    c.drawString(tag_x + 3*mm, tag_y2 + (tag_h - 6.5*0.352778)/2, tag)

    c.setFont(FONT_NORMAL, 7.5); c.setFillColor(GRAY_TEXT)
    c.drawRightString(W - M - 5*mm, hdr_y + 10*mm, data["company"])
    c.drawRightString(W - M - 5*mm, hdr_y + 4.5*mm, data["date"])

    doc.y = hdr_y - 6*mm

    fit   = data["fit_score"]
    fcol  = GREEN if fit >= 75 else (AMBER if fit >= 55 else RED)
    flbl  = "Bon fit" if fit >= 75 else ("Fit mod\u00e9r\u00e9" if fit >= 55 else "Fit faible")
    BNR_H = 18*mm
    doc.ensure(BNR_H + 4*mm)
    bx = M; by = doc.y - BNR_H
    rrect(c, bx, by, CW, BNR_H, r=3*mm, fill=BLUE_LIGHT, stroke=BLUE_MID, sw=0.6)

    cr   = 7.5*mm; cx_ = bx + 5*mm + cr; cy_ = by + BNR_H/2
    c.setFillColor(fcol); c.circle(cx_, cy_, cr, fill=1, stroke=0)
    c.setFillColor(WHITE)
    score_str = str(fit)
    c.setFont(FONT_BOLD, 16)
    sw_score = c.stringWidth(score_str, FONT_BOLD, 16)
    c.setFont(FONT_NORMAL, 8)
    sw_denom = c.stringWidth("/100", FONT_NORMAL, 8)
    gap_px = 1
    total_w = sw_score + gap_px + sw_denom
    sx = cx_ - total_w / 2
    base_y = cy_ - 3*mm
    c.setFont(FONT_BOLD, 16); c.setFillColor(WHITE)
    c.drawString(sx, base_y, score_str)
    c.setFont(FONT_NORMAL, 8); c.setFillColor(WHITE)
    c.drawString(sx + sw_score + gap_px, base_y, "/100")

    lx = cx_ + cr + 5*mm
    c.setFillColor(NAVY); c.setFont(FONT_BOLD, 11)
    c.drawString(lx, cy_ + 2*mm, f"Score d'ad\u00e9quation : {flbl}  ({fit}/100)")
    c.setFillColor(GRAY_TEXT); c.setFont(FONT_NORMAL, 8)
    c.drawString(lx, cy_ - 4.5*mm, f"Profil de poste r\u00e9f\u00e9rence : {data['job_profile']}")

    leg_x = W - M - 42*mm
    c.setFont(FONT_NORMAL, 7)
    c.setFillColor(fcol);  c.rect(leg_x, cy_+1.5*mm, 3*mm, 3*mm, fill=1, stroke=0)
    c.setFillColor(GRAY_TEXT); c.drawString(leg_x+4*mm, cy_+2*mm, "Score candidat")
    c.setFillColor(NAVY);  c.rect(leg_x, cy_-4*mm,   3*mm, 3*mm, fill=1, stroke=0)
    c.setFillColor(GRAY_TEXT); c.drawString(leg_x+4*mm, cy_-3.5*mm, "Cible du poste")

    doc.y = by - 6*mm

    st_just = para_style(fs=8, align=TA_JUSTIFY, leading=13)
    ph = para_height(data["executive_summary"], CW - 2*PAD, st_just)
    blk_h = ph + 2*PAD
    doc.ensure(9*mm + blk_h + 4*mm)
    doc.y = section_hdr(c, M, doc.y, CW, "SYNTH\u00c8SE EX\u00c9CUTIVE")
    rrect(c, M, doc.y - blk_h, CW, blk_h, r=2*mm, fill=GRAY_BG, stroke=GRAY_BORDER, sw=0.5)
    draw_para(c, data["executive_summary"], M+PAD, doc.y-PAD, CW-2*PAD, st_just)
    doc.y -= blk_h + 5*mm

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

    doc.ensure(9*mm)
    doc.y = section_hdr(c, M, doc.y, CW, "PROFIL COGNITIF D\u00c9TAILL\u00c9")

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

        sc_r  = 5.5*mm
        sc_cx = cx_ + 4*mm + sc_r
        sc_cy = cy_ + CARD_H - sc_r - 4*mm
        c.setFillColor(lvc); c.circle(sc_cx, sc_cy, sc_r, fill=1, stroke=0)
        c.setFillColor(WHITE); c.setFont(FONT_BOLD, 9)
        c.drawCentredString(sc_cx, sc_cy - 1.5*mm, str(ax["score"]))

        nm_x = sc_cx + sc_r + 3*mm
        nm_y = sc_cy + 2*mm
        c.setFillColor(GRAY_DARK); c.setFont(FONT_BOLD, 8)
        c.drawString(nm_x, nm_y, ax["name"])

        pill_draw(c, nm_x, nm_y - 6*mm, ax["level"], lvc, fs=6.5, ph=4.5*mm)

        c.setFont(FONT_NORMAL, 7); c.setFillColor(GRAY_TEXT)
        c.drawRightString(cx_+CARD_W-3*mm, nm_y, f"Cible : {ax['target']}")
        gap_str = f"+{gap}" if gap >= 0 else str(gap)
        c.setFont(FONT_BOLD, 7); c.setFillColor(gcol)
        c.drawRightString(cx_+CARD_W-3*mm, nm_y-5*mm, f"\u00c9cart : {gap_str}")

        bar_w = CARD_W - 8*mm
        score_bar(c, cx_+4*mm, cy_+5.5*mm, ax["score"], ax["target"], bw=bar_w)

        lbl = "Au-dessus de la cible \u2713" if gap >= 0 else "En dessous de la cible"
        c.setFont(FONT_NORMAL, 6.5); c.setFillColor(gcol)
        c.drawString(cx_+4*mm, cy_+1.8*mm, lbl)

    doc.y -= grid_h + 5*mm

    doc.ensure(9*mm)
    doc.y = section_hdr(c, M, doc.y, CW, "QUESTIONS D'ENTRETIEN RECOMMAND\u00c9ES")

    st_q   = para_style(fs=8, font=FONT_BOLD, align=TA_JUSTIFY, leading=13, color=GRAY_DARK)
    st_why = para_style(fs=7.5, align=TA_JUSTIFY, leading=12, color=GRAY_TEXT)
    NR     = 4.5*mm

    for qi, q in enumerate(data["interview_questions"]):
        q_ph   = para_height(f'\u00ab {q["question"]} \u00bb', CW-2*PAD, st_q)
        why_ph = para_height(f"Pourquoi : {q['why']}", CW-2*PAD, st_why)
        row_h  = NR*2 + 2*mm
        card_h = PAD + row_h + 3*mm + q_ph + 2*mm + why_ph + PAD
        doc.ensure(card_h + 4*mm)

        top = doc.y; bot = top - card_h
        rrect(c, M, bot, CW, card_h, r=2*mm, fill=WHITE, stroke=GRAY_BORDER, sw=0.5)

        pw    = pill_width(c, q["axis"], fs=7)
        ph_   = NR*2
        gap_  = 4*mm
        total = NR*2 + gap_ + pw
        start = M + CW/2 - total/2

        nc_cx = start + NR
        nc_cy = top - PAD - NR
        c.setFillColor(BLUE); c.circle(nc_cx, nc_cy, NR, fill=1, stroke=0)
        c.setFillColor(WHITE); c.setFont(FONT_BOLD, 8)
        c.drawCentredString(nc_cx, nc_cy-1.5*mm, str(qi+1))

        pill_draw(c, start+NR*2+gap_, nc_cy-NR, q["axis"], BLUE_LIGHT, fg=BLUE, fs=7, ph=ph_)

        q_top = nc_cy - NR - 4*mm
        draw_para(c, f'\u00ab {q["question"]} \u00bb', M+PAD, q_top, CW-2*PAD, st_q)

        why_top = q_top - q_ph - 2*mm
        draw_para(c, f"Pourquoi : {q['why']}", M+PAD, why_top, CW-2*PAD, st_why)

        doc.y = bot - 4*mm

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
    print(f"PDF g\u00e9n\u00e9r\u00e9 : {output_path}")

if __name__ == "__main__":
    generate_recruiter_pdf()
