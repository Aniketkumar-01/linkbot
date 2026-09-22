document.addEventListener('DOMContentLoaded', () => {
    // Tab Switching Logic
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    let currentTab = 'pdf';

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active classes
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab
            btn.classList.add('active');
            const tabId = btn.getAttribute('data-tab');
            document.getElementById(`tab-${tabId}`).classList.add('active');
            currentTab = tabId;
        });
    });

    // File Upload Display
    const resumeFileInput = document.getElementById('resumeFile');
    const fileNameDisplay = document.getElementById('fileName');

    resumeFileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            fileNameDisplay.textContent = e.target.files[0].name;
        } else {
            fileNameDisplay.textContent = '';
        }
    });

    // Form Submission
    const analyzeForm = document.getElementById('analyzeForm');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loadingState = document.getElementById('loadingState');
    const errorState = document.getElementById('errorState');
    const errorMessage = document.getElementById('errorMessage');
    const resultsSection = document.getElementById('resultsSection');

    analyzeForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Hide previous results/errors
        errorState.style.display = 'none';
        resultsSection.style.display = 'none';
        
        // Validate Inputs
        const geminiKey = document.getElementById('geminiKey').value;
        if (!geminiKey) {
            showError("Please enter your Gemini API Key in the sidebar.");
            return;
        }

        const formData = new FormData();
        formData.append('gemini_key', geminiKey);
        
        const serperKey = document.getElementById('serperKey').value;
        if (serperKey) formData.append('serper_key', serperKey);

        if (currentTab === 'pdf') {
            if (resumeFileInput.files.length === 0) {
                showError("Please upload a PDF resume.");
                return;
            }
            formData.append('resume_file', resumeFileInput.files[0]);
        } else if (currentTab === 'github') {
            const githubUrl = document.getElementById('githubUrl').value;
            if (!githubUrl) {
                showError("Please enter a GitHub URL.");
                return;
            }
            formData.append('github_url', githubUrl);
        } else if (currentTab === 'linkedin') {
            const linkedinUrl = document.getElementById('linkedinUrl').value;
            if (!linkedinUrl) {
                showError("Please enter a LinkedIn URL.");
                return;
            }
            formData.append('linkedin_url', linkedinUrl);
        }

        // UI Loading State
        analyzeBtn.disabled = true;
        loadingState.style.display = 'block';

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "An error occurred during analysis.");
            }

            renderResults(data.profile, data.suggestions);

        } catch (error) {
            showError(error.message);
        } finally {
            analyzeBtn.disabled = false;
            loadingState.style.display = 'none';
        }
    });

    function showError(msg) {
        errorMessage.textContent = msg;
        errorState.style.display = 'block';
    }

    // Render Results Function
    function renderResults(profile, suggestions) {
        // Render Profile
        const profilePreview = document.getElementById('profilePreview');
        
        let skillsHtml = profile.skills.map(s => `<span class="skill-tag">${s}</span>`).join('');
        
        profilePreview.innerHTML = `
            <h2>${profile.name || 'Analyzed Profile'}</h2>
            <div class="headline">${profile.headline || profile.job_titles.join(' | ')}</div>
            
            <div class="profile-meta">
                ${profile.location ? `<span><i class="fas fa-map-marker-alt"></i> ${profile.location}</span>` : ''}
                ${profile.experience_years ? `<span><i class="fas fa-briefcase"></i> ${profile.experience_years}+ Years Exp</span>` : ''}
                ${profile.industries && profile.industries.length ? `<span><i class="fas fa-industry"></i> ${profile.industries.join(', ')}</span>` : ''}
            </div>
            
            <div class="skills-tags">
                ${skillsHtml}
            </div>
        `;

        // Render Suggestions
        const grid = document.getElementById('suggestionsGrid');
        grid.innerHTML = '';
        
        suggestions.forEach(s => {
            const scoreColor = s.relevance_score >= 80 ? '#10B981' : (s.relevance_score >= 50 ? '#F59E0B' : '#EF4444');
            const card = document.createElement('div');
            card.className = 'suggestion-card';
            card.innerHTML = `
                <div class="score-badge" style="color: ${scoreColor}; border-color: ${scoreColor}; background: ${scoreColor}15;">
                    ${s.relevance_score}% Match
                </div>
                <div class="card-category"><i class="fas fa-tag"></i> ${s.category}</div>
                <h3 class="card-name">${s.name}</h3>
                <div class="card-title">${s.title}</div>
                
                ${s.psychological_profile ? `
                    <div class="card-section">
                        <h4><i class="fas fa-brain"></i> Persona</h4>
                        <p>${s.psychological_profile}</p>
                    </div>
                ` : ''}
                
                ${s.reason ? `
                    <div class="card-section">
                        <h4><i class="fas fa-lightbulb"></i> Why Connect</h4>
                        <p>${s.reason}</p>
                    </div>
                ` : ''}
                
                <div class="card-actions">
                    <a href="${s.url}" target="_blank" class="action-btn btn-primary">
                        <i class="fab fa-linkedin"></i> View Profile
                    </a>
                    ${s.connect_message ? `
                        <button class="action-btn btn-secondary" onclick="copyToClipboard('${s.connect_message.replace(/'/g, "\\'")}')">
                            <i class="fas fa-copy"></i> Msg
                        </button>
                    ` : ''}
                </div>
            `;
            grid.appendChild(card);
        });

        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
});

// Global copy function for the buttons
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert("Connection message copied to clipboard!");
    });
}
