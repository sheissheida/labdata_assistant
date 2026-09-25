from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.platypus import Image


def _create_styled_table(data, col_widths=None):
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f766e")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
        ('GRID', (0, 0), (-1, -1), 1, colors.silver),
    ]))
    return t

def _create_chart_image(chart_data: dict):
    fig, ax = plt.subplots(figsize=(6, 4))

    x = chart_data.get('x', [1, 2, 3, 4, 5])
    y_actual = chart_data.get('y_actual', [2, 4, 5, 4, 5])
    y_pred = chart_data.get('y_pred', [2.2, 3.8, 5.1, 4.2, 4.9])

    ax.scatter(x, y_actual, color='#8b5cf6', label='Actual Data')
    ax.plot(x, y_pred, color='#0f766e', linewidth=2, label='Fitted Model')

    ax.set_title("Regression Fit Analysis", fontsize=12, color='#1e293b')
    ax.set_xlabel(chart_data.get('x_label', 'Independent Variable (X)'))
    ax.set_ylabel(chart_data.get('y_label', 'Dependent Varianle (Y)'))
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6)

    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
    img_buffer.seek(0)
    plt.close(fig)

    return Image(img_buffer, width=400, height=260)

def generate_pdf_report(report_data: dict, output_path_or_stream):
    doc = SimpleDocTemplate(
        output_path_or_stream,
        pagesize=A4,
        rightMargin=50, leftMargin=50,
        topMargin=50, bottomMargin=50
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('ReportTitle', parent=styles['Heading1'], fontSize=22, spaceAfter=20, textColor=colors.HexColor("#0f766e"))
    heading_style = ParagraphStyle('SectionHeading', parent=styles['Heading2'], fontSize=14, spaceBefore=20, spaceAfter=10, textColor=colors.HexColor("#1e293b"))
    normal_style = styles['Normal']
    italic_style = ParagraphStyle('ItalicNote', parent=styles['Normal'], fontName='Helvetica-Oblique', textColor=colors.dimgrey)

    story = []

    story.append(Paragraph("LABDATA ASSISTANT", title_style))
    story.append(Paragraph("Automated Data Analysis Report", normal_style))
    story.append(Spacer(1, 20))

    story.append(Paragraph("1. Dataset Overview", heading_style))
    overview_data = [
        ['Metric', 'Value'],
        ['Total Rows', str(report_data.get('total_rows', 'N/A'))],
        ['Total Columns', str(report_data.get('total_columns', 'N/A'))]
    ]
    story.append(_create_styled_table(overview_data, col_widths=[200, 150]))

    story.append(Paragraph("2. Data Cleaning Summary", heading_style))
    cleaning_history = report_data.get("cleaning_history", [])
    if cleaning_history:
        clean_table_data = [['Operation', 'Details']]
        for step in cleaning_history:
            clean_table_data.append([step.get("Operation", ""), step.get("Details", "")])
        story.append(_create_styled_table(clean_table_data, col_widths=[150, 250]))
    else:
        story.append(Paragraph("No cleaning operations were performed on this dataset.", italic_style))

    story.append(Paragraph("3. Descriptive Statistics", heading_style))
    stats = report_data.get("statistics", [])
    if stats:
        stat_headers = ['Column', 'Mean', 'Std', 'Min', 'Max']
        stat_table_data = [stat_headers]
        for s in stats:
            stat_table_data.append([
                str(s.get('Column', '')),
                f"{s.get('Mean', 0):.2f}",
                f"{s.get('Std', 0):.2f}",
                str(s.get('Min', '')),
                str(s.get('Max', ''))
            ])
        story.append(_create_styled_table(stat_table_data, col_widths=[120, 70, 70, 70, 70]))
    else:
        story.append(Paragraph("No descriptive statistics available.", italic_style))

    story.append(Paragraph("4. Model Comparison", heading_style))
    models = report_data.get("model_comparison", [])
    if models:
        model_headers = ['Model', 'R² Score', 'RMSE', 'MAE']
        model_table_data = [model_headers]
        best_model_name = ""
        best_r2 = -float('inf')

        for m in models:
            r2_val = float(m.get('raw_r2', m.get('R² Score', 0)))
            if r2_val > best_r2:
                best_r2 = r2_val
                best_model_name = m.get('model', m.get('Model', ''))

            model_table_data.append([
                str(m.get('model', m.get('Model', ''))),
                str(m.get('r2', m.get('R² Score', ''))),
                str(m.get('rmse', m.get('RMSE', ''))),
                str(m.get('mae', m.get('MAE', '')))
            ])

        story.append(_create_styled_table(model_table_data, col_widths=[160, 80, 80, 80]))
        story.append(Spacer(1, 10))

        interpretation_text = (
            f"<b>Conclusion:</b> Based on the R² score, the <b>{best_model_name}</b> "
            f"provides the best fit for this dataset, explaining approximately "
            f"{best_r2 * 100:.1f}% of the variance in the target variable."
        )
        story.append(Paragraph(interpretation_text, normal_style))
    else:
        story.append(Paragraph("No regression models were evaluated.", italic_style))

    story.append(Spacer(1, 20))
    story.append(Paragraph("5. Visual Diagnostics", heading_style))
    story.append(Paragraph("The following chart illustrates the fitted regression model against the actual data points.", normal_style))
    story.append(Spacer(1, 15))

    chart_image = _create_chart_image(report_data.get("chart_data", {}))
    story.append(chart_image)

    doc.build(story)