# -*- coding: utf-8 -*-
# vim: set ts=4
import sys

from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer


def generate_devis(buff, dps):
    # Our container for 'Flowable' objects
    elements = []

    # A large collection of style sheets pre-made for us
    styles = getSampleStyleSheet()

    # Create the document
    doc = SimpleDocTemplate(buff, pagesize = A4,
                            rightMargin = 72, leftMargin = 72, topMargin = 72, bottomMargin = 18,
                            title = "Devis - DPS du XX/XX/XXXX",
                            author = "Croix-Rouge Francaise - UL de %s" % (dps.structure.nom),
                            subject = "Devis")

    # Add elements to print in one raw at the end
    elements.append(Paragraph("XXX, le XXX XXX XXX", ParagraphStyle(name = 'Date', alignment = TA_RIGHT)))

    #I = Image("logo_crf.gif")
    #I.drawHeight = 1.25 * inch * I.drawHeight / I.drawWidth
    #I.drawWidth = 1.25 * inch
    #I.hAlign = 'LEFT'

    #elements.append(I)

    elements.append(Spacer(1, 20))
    elements.append(Paragraph(dps.organisateur.contact(), ParagraphStyle(name = 'destinataire', alignment = TA_RIGHT)))
    elements.append(Paragraph(dps.organisateur.nom, ParagraphStyle(name = 'destinataire', alignment = TA_RIGHT)))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph(dps.organisateur.adresse, ParagraphStyle(name = 'destinataire', alignment = TA_RIGHT)))

    # Object
    identFirstLine = ParagraphStyle(name ='paragraph', firstLineIndent = 12)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("<u>Objet</u> : Devis suite à une demande de poste de secours", styles['Normal']))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("%s," % (dps.organisateur.contact_civilite), identFirstLine))
    elements.append(Paragraph("Suite à votre demande à l'occasion de la manifestation :", styles['Normal']))

    # The title
    centered = ParagraphStyle(name = 'centered', alignment = TA_CENTER)
    elements.append(Spacer(1, 5))
    elements.append(Paragraph("<b><u>%s</u></b>" % (dps.intitule), centered))
    elements.append(Paragraph("Du XXX au XXX, de XXX à XXX", centered))
    elements.append(Paragraph("Qui se déroule à l'endroit suivant :", centered))
    elements.append(Paragraph(dps.lieu, centered))

    # List the persons
    ident = ParagraphStyle(name = 'listing', leftIndent = 30)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Selon vos informations, nous vous proposons de mettre à votre disposition :", styles['Normal']))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph("<b><u>Effectifs secouristes</u></b>", styles['Normal']))
    elements.append(Paragraph("X Équiper de secours (4 à 5 intervenants)", ident))
    elements.append(Paragraph("X Binôme rattaché à l'équipe de secours", ident))
    elements.append(Paragraph("X Point d'alerte et de premiers secours (2 intervenants)", ident))
    elements.append(Paragraph("X Équipe d'évacuation", ident))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<b><u>Matériel</u></b>", styles['Normal']))
    elements.append(Paragraph("X lot A (matériel de secours avec oxygénothérapie, défibrillateur, moyens d'immobilisation...)", ident))
    elements.append(Paragraph("X lot B (sac de premiers secours pour binôme)", ident))
    elements.append(Paragraph("X lot C (sacs de premiers secours et d'oxygénothérapie)", ident))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<b><u>Véhicules</u></b>", styles['Normal']))
    elements.append(Paragraph("X véhicule logistiques ou de transport de personnel", ident))
    elements.append(Paragraph("X véhicule de premiers secours à personnes (VPSP)", ident))
    elements.append(Paragraph("X véhicule tout terrain", ident))

    # Create the needed style for the paragraphs
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("La facturation de cette prestation est estimée à XXX€, pour la prestation et les horaires mentionnés ci-dessus.", identFirstLine))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("XXX Emplacement du DPS XXX.", identFirstLine))
    elements.append(Paragraph("Nous rappellons que les secouristes sont bénévoles et ne touchent aucune indemnités. Nous \
    espèrons que vous ferez appel à nos services et à sa qualité.", identFirstLine))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(u'Dans l’attente d’une confirmation écrite de votre part, veuillez agréer, Monsieur, mes salutations distinguées.', identFirstLine))

    # Sign it
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("XXX Auteur XXX", centered))
    elements.append(Paragraph("XXX Titre XXX", centered))
    elements.append(Paragraph(u'Croix-Rouge Française', centered))
    elements.append(Paragraph(u"Unitée Locale de %s" % (dps.structure.nom), centered))

    # Write the document to the buffer
    doc.build(elements)

    return
