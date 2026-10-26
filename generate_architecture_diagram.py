"""
Generates publication-quality System Architecture Diagram for Project Synopsis
Contains:
1. Data Flow Diagram (DFD) Level 0
2. System Block Diagram & Layer Architecture
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8.5), dpi=300)
fig.patch.set_facecolor('#ffffff')

# ----------------- PANEL 1: DFD LEVEL 0 -----------------
ax1.set_facecolor('#f8fafc')
ax1.set_xlim(0, 11)
ax1.set_ylim(0, 4)
ax1.axis('off')
ax1.set_title("Data Flow Diagram (DFD Level 0) - Real-Time Anomaly Scoring Pipeline", 
              fontsize=12, fontweight='bold', pad=12, color='#1e293b')

def draw_box(ax, x, y, w, h, text, color, text_color='#ffffff', shape='rect'):
    if shape == 'round':
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1,rounding_size=0.15",
                                     edgecolor='#0f172a', facecolor=color, linewidth=1.5)
    else:
        box = patches.Rectangle((x, y), w, h, edgecolor='#0f172a', facecolor=color, linewidth=1.5)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, text, color=text_color, fontsize=8.5, fontweight='bold',
            ha='center', va='center', multialignment='center')

def draw_arrow(ax, x1, y1, x2, y2, label=""):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(facecolor='#334155', edgecolor='#334155', width=1.5, headwidth=6, headlength=6))
    if label:
        ax.text((x1+x2)/2, (y1+y2)/2 + 0.15, label, fontsize=7.5, color='#334155', ha='center', fontweight='semibold')

# DFD Entities & Processes
draw_box(ax1, 0.4, 1.3, 1.8, 1.4, "Cardholder / POS\nTerminal\n[External Entity]", '#3b82f6', shape='round')
draw_arrow(ax1, 2.2, 2.0, 3.0, 2.0, "Raw Stream")

draw_box(ax1, 3.0, 1.3, 2.0, 1.4, "Process 1.0\nValidation &\nToken Masking", '#0284c7')
draw_arrow(ax1, 5.0, 2.0, 5.8, 2.0, "Sanitized Txn")

draw_box(ax1, 5.8, 1.1, 2.4, 1.8, "Process 2.0\nAnomaly Detection\nEngine (IF, LOF,\nAutoencoder, SVM)", '#0f766e')
draw_arrow(ax1, 8.2, 2.4, 9.0, 2.8, "Score <= Cutoff")
draw_arrow(ax1, 8.2, 1.6, 9.0, 1.2, "Score > Cutoff")

draw_box(ax1, 9.0, 2.3, 1.7, 1.0, "Authorized Txn\n[Bank Ledger]", '#16a34a', shape='round')
draw_box(ax1, 9.0, 0.7, 1.7, 1.0, "Fraud Alert\n[Risk Ops]", '#dc2626', shape='round')

# ----------------- PANEL 2: SYSTEM BLOCK DIAGRAM -----------------
ax2.set_facecolor('#f8fafc')
ax2.set_xlim(0, 11)
ax2.set_ylim(0, 5)
ax2.axis('off')
ax2.set_title("System Block Architecture & Modular AI Pipeline", 
              fontsize=12, fontweight='bold', pad=12, color='#1e293b')

# 4 Horizontal Architecture Layers
layers = [
    ("Layer 1: Ingestion & Privacy Layer", 
     "dataset.csv (5,000 txns)  |  PCI-DSS Card Masking  |  Schema Validation  |  Nullity Handling",
     0.5, 3.8, 10.0, 0.8, '#475569'),
    ("Layer 2: Feature Engineering & SMOTE Pipeline",
     "Cyclic Diurnal Hours (sin/cos)  |  Log Amount Transform  |  Categorical Encoding  |  SMOTE Oversampling",
     0.5, 2.7, 10.0, 0.8, '#2563eb'),
    ("Layer 3: Multi-Model Anomaly Detection Engine",
     "Isolation Forest (iTrees)  |  Local Outlier Factor (k-NN Density)  |  PyTorch Autoencoder (Bottleneck)  |  One-Class SVM",
     0.5, 1.6, 10.0, 0.8, '#0d9488'),
    ("Layer 4: Evaluation & Ethical Governance Layer",
     "PR-AUC / ROC-AUC / F1  |  Demographic Parity Audit (Debit, Credit, Prepaid)  |  Automated False Positive Mitigation",
     0.5, 0.5, 10.0, 0.8, '#7c3aed')
]

for title, desc, x, y, w, h, col in layers:
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.12",
                                  edgecolor='#1e293b', facecolor=col, linewidth=1.2)
    ax2.add_patch(rect)
    ax2.text(x + 0.25, y + h - 0.26, title, color='#ffffff', fontsize=9, fontweight='bold', ha='left')
    ax2.text(x + 0.25, y + 0.22, desc, color='#e2e8f0', fontsize=8, ha='left')

# Downward flow arrows between layers
for y_pos in [3.8, 2.7, 1.6]:
    ax2.annotate('', xy=(5.5, y_pos - 0.25), xytext=(5.5, y_pos + 0.05),
                arrowprops=dict(facecolor='#0f172a', edgecolor='#0f172a', width=1.5, headwidth=5, headlength=5))

plt.tight_layout()
plt.savefig('visualizations/00_system_architecture.png', bbox_inches='tight', dpi=300)
print("Saved visualizations/00_system_architecture.png successfully.")
