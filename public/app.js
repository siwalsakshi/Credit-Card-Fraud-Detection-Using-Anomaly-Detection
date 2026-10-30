/**
 * SHIELD-AI Real-Time Anomaly Detection Engine Client
 * Project: Credit Card Fraud Detection Using Anomaly Detection (Project 32)
 */

document.addEventListener('DOMContentLoaded', () => {
  // State
  let currentPage = 1;
  const pageSize = 15;
  let currentFilter = 'all';
  let searchQuery = '';

  // DOM Elements
  const form = document.getElementById('fraud-detect-form');
  const inputAmount = document.getElementById('input-amount');
  const inputCategory = document.getElementById('input-category');
  const inputCardType = document.getElementById('input-card-type');
  const inputModel = document.getElementById('input-model');
  const inputHour = document.getElementById('input-hour');
  const hourDisplay = document.getElementById('hour-display');
  const inputWeekend = document.getElementById('input-weekend');
  const displayToken = document.getElementById('display-token');

  // Result Elements
  const gaugeFill = document.getElementById('gauge-fill');
  const resScore = document.getElementById('res-score');
  const resDecisionBadge = document.getElementById('res-decision-badge');
  const resDecisionIcon = document.getElementById('res-decision-icon');
  const resDecisionText = document.getElementById('res-decision-text');
  const resRiskLevel = document.getElementById('res-risk-level');
  const resModelUsed = document.getElementById('res-model-used');
  const resLatency = document.getElementById('res-latency');
  const diagFactorsList = document.getElementById('diag-factors-list');

  // Votes
  const voteIf = document.getElementById('vote-if').querySelector('.vote-status');
  const voteLof = document.getElementById('vote-lof').querySelector('.vote-status');
  const voteAe = document.getElementById('vote-ae').querySelector('.vote-status');
  const voteSvm = document.getElementById('vote-svm').querySelector('.vote-status');

  // Table Elements
  const tableBody = document.getElementById('table-body');
  const paginationInfo = document.getElementById('table-pagination-info');
  const pageIndicator = document.getElementById('page-indicator');
  const btnPrevPage = document.getElementById('btn-prev-page');
  const btnNextPage = document.getElementById('btn-next-page');
  const tableSearchInput = document.getElementById('table-search-input');
  const filterButtons = document.querySelectorAll('.filter-btn');
  const presetButtons = document.querySelectorAll('.preset-btn');

  // 1. Hour Slider Event
  inputHour.addEventListener('input', (e) => {
    const val = parseInt(e.target.value);
    let period = "Daytime Traffic";
    if (val >= 1 && val <= 5) period = "Off-Peak Night Anomaly Window";
    else if (val >= 6 && val <= 11) period = "Morning Volume";
    else if (val >= 12 && val <= 17) period = "Peak Afternoon Commerce";
    else if (val >= 18 && val <= 22) period = "Evening Retail";
    else period = "Late Night Window";
    hourDisplay.textContent = `${String(val).padStart(2, '0')}:00 (${period})`;
  });

  // 2. Quick Preset Scenarios
  const presets = {
    grocery: {
      amount: 38.50,
      category: 'Grocery',
      card_type: 'Debit',
      hour: 14,
      weekend: false,
      token: 'CARD_XXXX8846'
    },
    probing: {
      amount: 1.99,
      category: 'Online',
      card_type: 'Prepaid',
      hour: 3,
      weekend: false,
      token: 'CARD_XXXX4901'
    },
    electronics: {
      amount: 2150.00,
      category: 'Electronics',
      card_type: 'Credit',
      hour: 2,
      weekend: true,
      token: 'CARD_XXXX6711'
    },
    fuel: {
      amount: 54.00,
      category: 'Fuel',
      card_type: 'Credit',
      hour: 8,
      weekend: false,
      token: 'CARD_XXXX2817'
    },
    travel: {
      amount: 3450.00,
      category: 'Travel',
      card_type: 'Credit',
      hour: 23,
      weekend: true,
      token: 'CARD_XXXX9012'
    }
  };

  presetButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const pKey = btn.getAttribute('data-preset');
      const p = presets[pKey];
      if (p) {
        inputAmount.value = p.amount;
        inputCategory.value = p.category;
        inputCardType.value = p.card_type;
        inputHour.value = p.hour;
        inputHour.dispatchEvent(new Event('input'));
        inputWeekend.checked = p.weekend;
        displayToken.textContent = p.token;
        executePrediction();
      }
    });
  });

  // 3. Form Submit Prediction
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    executePrediction();
  });

  async function executePrediction() {
    const payload = {
      amount: parseFloat(inputAmount.value),
      merchant_category: inputCategory.value,
      card_type: inputCardType.value,
      hour: parseInt(inputHour.value),
      is_weekend: inputWeekend.checked ? 1 : 0,
      model: inputModel.value,
      card_token: displayToken.textContent
    };

    try {
      resLatency.textContent = "Scoring...";
      const res = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      renderPrediction(data);
    } catch (err) {
      console.error("Prediction failed:", err);
      resLatency.textContent = "Offline simulation";
      simulateLocalPrediction(payload);
    }
  }

  function renderPrediction(data) {
    const score = data.risk_percentage;
    resScore.textContent = `${score}%`;
    resLatency.textContent = `Latency: ${data.latency_ms} ms`;
    resModelUsed.textContent = data.model_used;

    // Half circle circumference is approx 251.2
    // offset 251.2 is 0%, offset 0 is 100%
    const maxCircumference = 251.2;
    const offset = Math.max(0, maxCircumference - (maxCircumference * (score / 100)));
    gaugeFill.style.strokeDashoffset = offset;

    // Decision color and badges
    if (data.is_fraud === 1 || score >= 70) {
      gaugeFill.style.stroke = '#ef4444';
      resScore.style.color = '#ef4444';
      resDecisionBadge.className = 'decision-badge danger';
      resDecisionIcon.textContent = '✖';
      resDecisionText.textContent = 'FLAGGED FRAUDULENT ANOMALY';
      resRiskLevel.className = 'meta-val danger';
      resRiskLevel.textContent = 'CRITICAL ANOMALY';
    } else if (score >= 40) {
      gaugeFill.style.stroke = '#f59e0b';
      resScore.style.color = '#f59e0b';
      resDecisionBadge.className = 'decision-badge warning';
      resDecisionIcon.textContent = '⚠';
      resDecisionText.textContent = 'ELEVATED RISK - REVIEW';
      resRiskLevel.className = 'meta-val warning';
      resRiskLevel.textContent = 'MODERATE SUSPICION';
    } else {
      gaugeFill.style.stroke = '#10b981';
      resScore.style.color = '#10b981';
      resDecisionBadge.className = 'decision-badge normal';
      resDecisionIcon.textContent = '✓';
      resDecisionText.textContent = 'TRANSACTION APPROVED';
      resRiskLevel.className = 'meta-val normal';
      resRiskLevel.textContent = 'NORMAL / LOW RISK';
    }

    // Update individual model votes
    if (data.all_model_votes) {
      updateVoteBadge(voteIf, data.all_model_votes.isolation_forest);
      updateVoteBadge(voteLof, data.all_model_votes.lof);
      updateVoteBadge(voteAe, data.all_model_votes.autoencoder);
      updateVoteBadge(voteSvm, data.all_model_votes.one_class_svm);
    }

    // Update diagnostic factor list
    diagFactorsList.innerHTML = '';
    if (data.factors && data.factors.length > 0) {
      data.factors.forEach(f => {
        const li = document.createElement('li');
        const tagClass = f.impact.toLowerCase();
        li.innerHTML = `<span class="factor-tag ${tagClass}">${f.impact}</span><span><strong>${f.name}:</strong> ${f.desc}</span>`;
        diagFactorsList.appendChild(li);
      });
    }
  }

  function updateVoteBadge(el, isFraudVote) {
    if (isFraudVote === 1) {
      el.textContent = 'FLAG';
      el.className = 'vote-status flagged';
    } else {
      el.textContent = 'PASS';
      el.className = 'vote-status legit';
    }
  }

  function simulateLocalPrediction(p) {
    // Fallback if backend server not responding
    let score = 12.0;
    if (p.hour >= 1 && p.hour <= 5) score += 35;
    if (p.amount < 5.0 && (p.category === 'Online' || p.category === 'Electronics')) score += 45;
    if (p.amount > 1200) score += 40;
    score = Math.min(96.5, score);
    const isFraud = score >= 50 ? 1 : 0;
    renderPrediction({
      is_fraud: isFraud,
      risk_percentage: score,
      latency_ms: 1.4,
      model_used: "Offline Heuristic Fallback",
      all_model_votes: { isolation_forest: isFraud, lof: isFraud, autoencoder: isFraud, one_class_svm: isFraud },
      factors: [
        { name: "Simulation Mode", impact: isFraud ? "HIGH" : "LOW", desc: "Local heuristic active." }
      ]
    });
  }

  // 4. Load Data Explorer Table
  async function loadTransactions() {
    const offset = (currentPage - 1) * pageSize;
    tableBody.innerHTML = `<tr><td colspan="9" class="table-loading">Loading transaction stream (Page ${currentPage})...</td></tr>`;

    try {
      const res = await fetch(`/api/transactions?limit=${pageSize}&offset=${offset}&filter=${currentFilter}`);
      const data = await res.json();
      renderTable(data);
    } catch (err) {
      tableBody.innerHTML = `<tr><td colspan="9" class="table-loading">Unable to load transactions from API.</td></tr>`;
    }
  }

  function renderTable(data) {
    const txns = data.transactions || [];
    tableBody.innerHTML = '';

    if (txns.length === 0) {
      tableBody.innerHTML = `<tr><td colspan="9" class="table-loading">No transactions found matching filter.</td></tr>`;
      return;
    }

    txns.forEach(t => {
      const tr = document.createElement('tr');
      const isFraud = t.is_fraud === 1;
      const chipClass = isFraud ? 'fraud' : 'legit';
      const chipText = isFraud ? '1 Fraud' : '0 Legit';

      tr.innerHTML = `
        <td><strong>#${t.trans_id}</strong></td>
        <td>${t.timestamp}</td>
        <td><code>${t.card_token}</code></td>
        <td><strong>$${parseFloat(t.amount).toFixed(2)}</strong></td>
        <td>${t.merchant_category}</td>
        <td>${t.merchant_id}</td>
        <td>${t.card_type}</td>
        <td><span class="status-chip ${chipClass}">${chipText}</span></td>
        <td><button class="btn-table-action" data-trans="${t.trans_id}">Test in Sim</button></td>
      `;

      // Attach button action
      const btn = tr.querySelector('.btn-table-action');
      btn.addEventListener('click', () => {
        inputAmount.value = t.amount;
        inputCategory.value = t.merchant_category;
        inputCardType.value = t.card_type;
        displayToken.textContent = t.card_token;

        const dateObj = new Date(t.timestamp);
        if (!isNaN(dateObj.getHours())) {
          inputHour.value = dateObj.getHours();
          inputHour.dispatchEvent(new Event('input'));
          const day = dateObj.getDay();
          inputWeekend.checked = (day === 0 || day === 6);
        }

        executePrediction();
        window.location.hash = '#simulator';
      });

      tableBody.appendChild(tr);
    });

    // Update pagination indicators
    const startIdx = data.offset + 1;
    const endIdx = Math.min(data.offset + txns.length, data.total);
    paginationInfo.textContent = `Showing ${startIdx} to ${endIdx} of ${data.total.toLocaleString()} transactions`;
    pageIndicator.textContent = `Page ${currentPage}`;
    btnPrevPage.disabled = (currentPage === 1);
    btnNextPage.disabled = (endIdx >= data.total);
  }

  // 5. Pagination events
  btnPrevPage.addEventListener('click', () => {
    if (currentPage > 1) {
      currentPage--;
      loadTransactions();
    }
  });

  btnNextPage.addEventListener('click', () => {
    currentPage++;
    loadTransactions();
  });

  // 6. Filter Buttons
  filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      filterButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentFilter = btn.getAttribute('data-filter');
      currentPage = 1;
      loadTransactions();
    });
  });

  // 7. Initial Loads
  executePrediction();
  loadTransactions();
});
