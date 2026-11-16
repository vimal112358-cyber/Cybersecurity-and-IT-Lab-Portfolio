import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_audit_report(incidents, output_filename="daily_triage_report.pdf"):
    """
    Generates a professional executive PDF audit report of system and security incidents using ReportLab.
    """
    doc = SimpleDocTemplate(output_filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    styles = getSampleStyleSheet()

    # Custom Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=colors.HexColor('#1a365d'),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#718096'),
        spaceAfter=20
    )

    cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=colors.HexColor('#2d3748')
    )

    header_cell_style = ParagraphStyle(
        'HeaderCell',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=colors.white
    )

    # Document Header
    story.append(Paragraph("Endpoint Health & Security Triage Report", title_style))
    story.append(Paragraph("Automated Operations Pipeline | Generated via Python & ReportLab", subtitle_style))
    story.append(Spacer(1, 10))

    # Summary Section
    summary_text = f"<b>Total Incidents Detected:</b> {len(incidents)}"
    story.append(Paragraph(summary_text, styles['Normal']))
    story.append(Spacer(1, 15))

    # Incidents Table Construction
    if not incidents:
        story.append(Paragraph("No critical incidents or threshold breaches detected during this audit cycle.", styles['Normal']))
    else:
        table_data = [[
            Paragraph("Host", header_cell_style),
            Paragraph("Metric", header_cell_style),
            Paragraph("Value", header_cell_style),
            Paragraph("Severity", header_cell_style),
            Paragraph("Message", header_cell_style)
        ]]

        for inc in incidents:
            table_data.append([
                Paragraph(inc.get("host", "N/A"), cell_style),
                Paragraph(inc.get("metric", "N/A"), cell_style),
                Paragraph(inc.get("value", "N/A"), cell_style),
                Paragraph(inc.get("severity", "INFO"), cell_style),
                Paragraph(inc.get("message", "N/A"), cell_style)
            ])

        # Table Styling & Layout
        col_widths = [80, 90, 60, 65, 235]
        incident_table = Table(table_data, colWidths=col_widths)
        incident_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2b6cb0')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ]))
        story.append(incident_table)

    # Build PDF
    doc.build(story)
    print(f"[+] Audit PDF successfully generated: {output_filename}")

if __name__ == "__main__":
    # Test data generation
    sample_incidents = [
        {"host": "prod-node-01", "metric": "CPU Usage", "value": "88.4%", "severity": "HIGH", "message": "CPU utilization exceeded threshold."},
        {"host": "prod-node-01", "metric": "Disk Usage", "value": "94.1%", "severity": "CRITICAL", "message": "Disk space nearly exhausted."}
    ]
    generate_audit_report(sample_incidents)
