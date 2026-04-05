document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('critique-form');
    const statementInput = document.getElementById('statement-input');
    const inputSection = document.getElementById('input-section');
    const loadingSection = document.getElementById('loading-section');
    const resultsSection = document.getElementById('results-section');
    const resetBtn = document.getElementById('reset-btn');

    // Results Elements
    const scoreValue = document.getElementById('score-value');
    const logicList = document.getElementById('logic-list');
    const philosophyContent = document.getElementById('philosophy-content');
    const evidenceList = document.getElementById('evidence-list');
    const promptsList = document.getElementById('prompts-list');

    // Initial Display Setup
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'none';

    function switchSection(hideElem, showElem) {
        hideElem.classList.remove('active');
        hideElem.classList.add('hidden');
        
        setTimeout(() => {
            hideElem.style.display = 'none';
            showElem.style.display = 'block';
            setTimeout(() => {
                showElem.classList.remove('hidden');
                showElem.classList.add('active');
            }, 50); // slight delay to allow display block to render
        }, 800); // Wait for opacity transition
    }

    function populateResults(data) {
        // Score
        const scorePercentage = Math.round(data.argument_strength * 100);
        scoreValue.textContent = `${scorePercentage}%`;

        // Logic Issues
        logicList.innerHTML = '';
        if (data.logic_issues && data.logic_issues.length > 0) {
            data.logic_issues.forEach(issue => {
                const li = document.createElement('li');
                li.innerHTML = `<strong>${issue.issue || issue.name || 'Logical Fallacy'}:</strong> ${issue.explanation || issue.description || issue.detail || JSON.stringify(issue)}`;
                logicList.appendChild(li);
            });
        } else {
            logicList.innerHTML = '<li>No significant logical fallacies detected.</li>';
        }

        // Philosophy Insights
        philosophyContent.innerHTML = '';
        if (data.philosophical_insights && data.philosophical_insights.length > 0) {
            data.philosophical_insights.forEach(insight => {
                const p = document.createElement('p');
                p.style.marginBottom = '15px';
                p.innerHTML = `<strong>${insight.issue || insight.name || 'Insight'}:</strong> ${insight.explanation || insight.description || insight.detail || JSON.stringify(insight)}`;
                philosophyContent.appendChild(p);
            });
        } else {
            philosophyContent.innerHTML = '<p>A straightforward statement devoid of deeper philosophical complexity.</p>';
        }

        // Missing Evidence
        evidenceList.innerHTML = '';
        if (data.missing_evidence && data.missing_evidence.length > 0) {
            data.missing_evidence.forEach(evidence => {
                const li = document.createElement('li');
                li.textContent = evidence;
                evidenceList.appendChild(li);
            });
        } else {
            evidenceList.innerHTML = '<li>The statement appears to be adequately substantiated or is purely axiomatic.</li>';
        }

        // Reflection Prompts
        promptsList.innerHTML = '';
        if (data.reflection_prompts && data.reflection_prompts.length > 0) {
            data.reflection_prompts.forEach(prompt => {
                const li = document.createElement('li');
                li.textContent = `"${prompt}"`;
                promptsList.appendChild(li);
            });
        } else {
            promptsList.innerHTML = '<li>What truth lies beyond this statement?</li>';
        }
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const statement = statementInput.value.trim();
        if (!statement) return;

        // Transition to loading
        switchSection(inputSection, loadingSection);

        try {
            const response = await fetch('http://127.0.0.1:8000/api/v1/submit_statement', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ statement: statement })
            });

            if (!response.ok) {
                throw new Error('Failed to analyze the statement.');
            }

            const data = await response.json();
            
            // Populate and transition to results
            populateResults(data);
            switchSection(loadingSection, resultsSection);

        } catch (error) {
            console.error('Error:', error);
            alert('A disruption occurred in the contemplative process. Please try again.');
            switchSection(loadingSection, inputSection);
        }
    });

    resetBtn.addEventListener('click', () => {
        statementInput.value = '';
        switchSection(resultsSection, inputSection);
        setTimeout(() => {
            statementInput.focus();
        }, 800);
    });

    // Auto-resize textarea
    statementInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
});
