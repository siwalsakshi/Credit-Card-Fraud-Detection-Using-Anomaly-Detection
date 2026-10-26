# 1–2 Minute Live Demo & Presentation Script
**Project No. 32: Credit Card Fraud Detection Using Anomaly Detection**  
**HCLTech Career Shaper Programme — III Year Industry Project**  

---

## ⏱️ Video / Expo Demo Breakdown (Total: 90–120 Seconds)

### Slide / Screen 1: Problem Statement & Motivation (0:00 – 0:25)
- **Presenter Script:**
  > *"Hello everyone! I'm Saksham, presenting Project 32: Credit Card Fraud Detection Using Anomaly Detection for the HCLTech Career Shaper Programme.  
  > In digital payments, fraud represents an acute imbalanced challenge: only 0.17% of transactions in real-world benchmarks are fraudulent. Conventional supervised models struggle with such extreme scarcity, while hard rule engines generate excessive false alarms. Our solution uses Unsupervised and Semi-Supervised Anomaly Detection to profile normative spending patterns and pinpoint emerging fraud vectors in real time."*
- **Visual:** Show slide with Problem Statement & Imbalanced Distribution donut chart (`visualizations/01_class_imbalance.png`).

---

### Slide / Screen 2: Data Engineering & SMOTE Augmentation (0:25 – 0:50)
- **Presenter Script:**
  > *"We engineered a production-grade 5,000-row transaction dataset using SMOTE-style synthetic interpolation based on empirical Kaggle distributions, maintaining an ethical 3.5% calibrated anomaly rate.  
  > Key features include PCI-compliant masked card tokens, cyclical trigonometric encodings for circadian transaction rhythms, and log-transformed amounts to isolate both micro-testing card probes and high-value luxury ticket incursions."*
- **Visual:** Open and scroll `dataset.csv` or show `visualizations/02_amount_distribution.png` & `visualizations/03_temporal_trends.png`.

---

### Slide / Screen 3: Live ML Benchmark Execution (0:50 – 1:20)
- **Presenter Script:**
  > *"Here is our live machine learning pipeline in action. With a single command, we benchmark four distinct algorithms: Isolation Forest, Local Outlier Factor, a Deep Neural Bottleneck Autoencoder, and One-Class SVM."*
- **Action:** Open terminal and run:
  ```bash
  python anomaly_detection.py
  ```
- **Presenter Script:**
  > *"As the results display on screen: Local Outlier Factor achieved top performance with a PR-AUC of 0.0659 and ROC-AUC of 0.6111, while maintaining a very low False Positive Rate of only 2.57%."*
- **Visual:** Highlight terminal table `BENCHMARK EVALUATION RESULTS`.

---

### Slide / Screen 4: Ethical Fairness Audit & Conclusion (1:20 – 1:45)
- **Presenter Script:**
  > *"Crucially, aligned with HCLTech's ethical guidelines, we built an automated Fairness Auditor. When inspecting False Positive Rates across payment brands—Visa, MasterCard, Amex, Discover, and RuPay—we verified that legitimate cardholders experience balanced, low false alarms across networks, ensuring unhindered financial access.  
  > All deliverables including the 8-page report, interactive EDA notebook, and trained model artifacts are fully packaged. Thank you!"*
- **Visual:** Display the `ETHICAL FAIRNESS AUDIT` table and point to `Ethical_Compliance_Declaration.md`.

---

## 💻 Commands for Live Demo

```bash
# 1. Show dataset structure & head
python -c "import pandas as pd; df = pd.read_csv('dataset.csv'); print(df[['trans_id', 'amount', 'merchant_category', 'is_fraud', 'card_type']].head(5))"

# 2. Run the end-to-end ML training & fairness audit
python anomaly_detection.py

# 3. View saved charts in visualizations/
```
