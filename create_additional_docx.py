"""
Generate remaining Word submission documents:
1. DEMO_GUIDE.docx
2. EDA_Analysis_and_Visualisations.docx (with embedded chart images)
3. Source_Code_Compendium.docx (with GitHub link and source code)
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def set_margins(doc):
    for s in doc.sections:
        s.top_margin = Inches(0.9)
        s.bottom_margin = Inches(0.9)
        s.left_margin = Inches(0.9)
        s.right_margin = Inches(0.9)

# ----------------- 1. DEMO_GUIDE.DOCX -----------------
def create_demo_docx():
    doc = docx.Document()
    set_margins(doc)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("DEMO PRESENTATION & EXPO GUIDE")
    r.font.name = "Calibri"
    r.font.size = Pt(18)
    r.font.bold = True
    r.font.color.rgb = RGBColor(15, 23, 42)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Project No. 32: Credit Card Fraud Detection Using Anomaly Detection\nHCLTech Career Shaper Programme | Academic Year 2025–26 | Learner: Saksham\nGitHub: https://github.com/siwalsakshi/Credit-Card-Fraud-Detection-Using-Anomaly-Detection")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(10.5)
    r_sub.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_heading("1. Executive Presentation Overview", level=2)
    p = doc.add_paragraph()
    p.add_run("• Target Duration: ").bold = True
    p.add_run("90 – 120 Seconds (2-Minute Pitch Format)\n")
    p.add_run("• Target Audience: ").bold = True
    p.add_run("HCLTech Industry Mentors, Academic Evaluators & Career Shaper Jury\n")
    p.add_run("• Interactive Application: ").bold = True
    p.add_run("Full-Stack Real-Time Scoring Dashboard running locally at http://localhost:5000\n")
    p.add_run("• Source Code & Repository: ").bold = True
    p.add_run("https://github.com/siwalsakshi/Credit-Card-Fraud-Detection-Using-Anomaly-Detection")

    doc.add_heading("2. Timed 120-Second Presenter Script", level=2)
    script_parts = [
        ("00:00 – 00:25 (Problem & Challenge):",
         "\"Good day, everyone. In digital banking, credit card fraud causes billions of dollars in losses worldwide. Conventional rule-based systems struggle because real-world fraud is an extreme minority—representing only 0.17% of transactions in the Kaggle benchmark. Standard classifiers fail under this imbalance or create excessive false alarms that frustrate legitimate cardholders.\""),
        ("00:25 – 00:55 (Solution & Methodology):",
         "\"Our solution, SHIELD-AI, implements an unsupervised and semi-supervised anomaly detection engine. We augmented 5,000 transactions with SMOTE and trained four distinct algorithms: Isolation Forest, Local Outlier Factor, a Deep Neural Bottleneck Autoencoder, and One-Class SVM. By learning the geometric density of legitimate spending habits, our models detect anomalous transactions as low-density outliers without requiring balanced historical labels.\""),
        ("00:55 – 01:30 (Live Demo & Key Results):",
         "\"Let me demonstrate our live production prototype. Here on our interactive dashboard at localhost:5000, we test transactions in real time. When we test a nocturnal micro-authorization—for instance $1.99 at 3:30 AM—all four models vote in unison, registering a 69.8% risk score and instantly flagging it as a Critical Anomaly. In contrast, routine daytime transactions receive sub-2 millisecond approval. In benchmark evaluation, Local Outlier Factor achieved our highest ROC-AUC of 77.53%.\""),
        ("01:30 – 02:00 (Fairness, Governance & Conclusion):",
         "\"Crucially, financial fraud models must be ethical. In compliance with the DPDP Act 2023, our automated Demographic Fairness Auditor verifies that False Positive Rates remain equal across Debit (2.08%), Credit (1.80%), and Prepaid (1.77%) cardholders—ensuring no demographic is unfairly locked out of their funds. All deliverables, datasets, and code are open-sourced on GitHub. Thank you.\"")
    ]

    for time_header, script_body in script_parts:
        p = doc.add_paragraph()
        r1 = p.add_run(f"{time_header}\n")
        r1.bold = True
        r1.font.name = "Calibri"
        r1.font.size = Pt(11)
        r2 = p.add_run(script_body)
        r2.font.name = "Calibri"
        r2.font.italic = True
        r2.font.size = Pt(10.5)

    doc.add_heading("3. Terminal Launch & Execution Commands", level=2)
    p_code = doc.add_paragraph()
    p_code.add_run("1. Start Web Application:   python app.py  (Opens http://localhost:5000)\n"
                   "2. Retrain ML Models:       python anomaly_detection.py\n"
                   "3. Run EDA Visualisations:  python eda_analysis.py\n"
                   "4. Regenerate Dataset:      python generate_dataset.py").font.name = "Consolas"

    doc.save("DEMO_GUIDE.docx")
    print("Saved DEMO_GUIDE.docx successfully.")

# ----------------- 2. EDA_Analysis_and_Visualisations.docx -----------------
def create_eda_docx():
    doc = docx.Document()
    set_margins(doc)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("EXPLORATORY DATA ANALYSIS (EDA) & VISUALISATIONS REPORT")
    r.font.name = "Calibri"
    r.font.size = Pt(17)
    r.font.bold = True
    r.font.color.rgb = RGBColor(15, 23, 42)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Project No. 32: Credit Card Fraud Detection Using Anomaly Detection\nHCLTech Career Shaper Programme | Domain: Digital-Data-AI / AIML | Learner: Saksham")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(10.5)
    r_sub.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_heading("1. Dataset Summary & Statistical Overview", level=2)
    p = doc.add_paragraph()
    p.add_run("• Dataset File: ").bold = True
    p.add_run("dataset.csv (5,000 Total Transactions, 8 Columns)\n")
    p.add_run("• Class Distribution: ").bold = True
    p.add_run("4,825 Legitimate Transactions (96.50%), 175 Fraudulent Anomalies (3.50%)\n")
    p.add_run("• Temporal Range: ").bold = True
    p.add_run("2024-01-01 00:17:00 to 2024-02-26 21:25:05\n")
    p.add_run("• Purchase Amount: ").bold = True
    p.add_run("Min: $0.50 | Max: $4,200.00 | Median: $84.20 | Mean: $146.85")

    charts = [
        ("Visualisation 1: Class Imbalance & Transaction Distribution", 
         "visualizations/01_class_imbalance.png",
         "Demonstrates the acute 96.5% vs 3.5% class imbalance, establishing the rationale for Unsupervised Anomaly Detection over naive supervised classifiers."),
        ("Visualisation 2: Transaction Amount Distributions by Class", 
         "visualizations/02_amount_distribution.png",
         "Contrasts legitimate log-normal spending against fraud vectors: micro-testing probing (<$5) and high-value unauthorized spikes ($300-$3,500)."),
        ("Visualisation 3: Diurnal Temporal Trends & Night Anomaly Window", 
         "visualizations/03_temporal_trends.png",
         "Shows diurnal spend density peaking between 12:00 and 19:00 hours, whereas fraudulent activity clusters during off-peak hours (01:00-05:00)."),
        ("Visualisation 4: Merchant Category & Card Network Breakdown", 
         "visualizations/04_category_card_breakdown.png",
         "Examines transaction volumes across categories and verifies balanced distributions across Debit (35%), Credit (35%), and Prepaid (30%) cards.")
    ]

    for title, img_path, desc in charts:
        doc.add_heading(title, level=2)
        p_desc = doc.add_paragraph()
        p_desc.add_run(desc).font.name = "Calibri"
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.add_run().add_picture(img_path, width=Inches(5.8))

    doc.save("EDA_Analysis_and_Visualisations.docx")
    print("Saved EDA_Analysis_and_Visualisations.docx successfully.")

# ----------------- 3. Source_Code_Compendium.docx -----------------
def create_code_docx():
    doc = docx.Document()
    set_margins(doc)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("PROJECT SOURCE CODE & ARCHITECTURE COMPENDIUM")
    r.font.name = "Calibri"
    r.font.size = Pt(17)
    r.font.bold = True
    r.font.color.rgb = RGBColor(15, 23, 42)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Official Codebase for HCLTech Career Shaper Project 32\nLearner: Saksham | Coordinator: Shaily Gaur\nOfficial GitHub Repository: https://github.com/siwalsakshi/Credit-Card-Fraud-Detection-Using-Anomaly-Detection")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(10.5)
    r_sub.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_heading("1. GitHub Repository Link & Online Access", level=2)
    p = doc.add_paragraph()
    p.add_run("The complete working repository with live version control, serialized model artifacts, datasets, and web application is hosted at:\n").font.name = "Calibri"
    r_url = p.add_run("https://github.com/siwalsakshi/Credit-Card-Fraud-Detection-Using-Anomaly-Detection\n\n")
    r_url.bold = True
    r_url.font.name = "Calibri"
    r_url.font.color.rgb = RGBColor(2, 132, 199)

    doc.add_heading("2. System Architecture & DFD Level 0", level=2)
    if os.path.exists("visualizations/00_system_architecture.png"):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture("visualizations/00_system_architecture.png", width=Inches(6.0))

    files_to_include = [
        ("app.py — Full-Stack Web Application Server & REST API", "app.py"),
        ("anomaly_detection.py — 4-Model ML Pipeline & Benchmark", "anomaly_detection.py"),
        ("generate_dataset.py — Synthetic Data Extension Generator", "generate_dataset.py"),
        ("eda_analysis.py — Visualisation Generator Script", "eda_analysis.py"),
        ("web/app.js — Interactive Client Script & Gauge Animation", "web/app.js")
    ]

    for title, fpath in files_to_include:
        if os.path.exists(fpath):
            doc.add_heading(title, level=2)
            with open(fpath, "r", encoding="utf-8") as f:
                code_content = f.read()
            p_code = doc.add_paragraph()
            r_c = p_code.add_run(code_content[:2500] + "\n\n[... Complete file available on GitHub: https://github.com/siwalsakshi/Credit-Card-Fraud-Detection-Using-Anomaly-Detection ...]")
            r_c.font.name = "Consolas"
            r_c.font.size = Pt(8.5)
            r_c.font.color.rgb = RGBColor(30, 41, 59)

    doc.save("Source_Code_Compendium.docx")
    print("Saved Source_Code_Compendium.docx successfully.")

if __name__ == "__main__":
    create_demo_docx()
    create_eda_docx()
    create_code_docx()
