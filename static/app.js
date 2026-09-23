document.addEventListener('DOMContentLoaded', () => {
  // Ingestion Tab Switching Logic
  const tabButtons = document.querySelectorAll('.tab-button');
  const tabContents = {
    pdf: document.getElementById('tab-content-pdf'),
    github: document.getElementById('tab-content-github'),
    linkedin: document.getElementById('tab-content-linkedin')
  };

  let activeTab = 'pdf';

  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      activeTab = btn.getAttribute('data-tab');
      
      // Update buttons
      tabButtons.forEach(b => {
        if (b.getAttribute('data-tab') === activeTab) {
          b.className = "tab-button active px-space-md py-1.5 rounded-lg bg-primary-container text-on-primary-container font-label-md shadow-md";
        } else {
          b.className = "tab-button px-space-md py-1.5 rounded-lg text-on-surface-variant hover:text-on-surface font-label-md";
        }
      });

      // Update contents
      Object.keys(tabContents).forEach(key => {
        if (key === activeTab) {
          tabContents[key].classList.remove('hidden');
          tabContents[key].classList.add('flex');
        } else {
          tabContents[key].classList.add('hidden');
          tabContents[key].classList.remove('flex');
        }
      });
    });
  });

  // File Upload Display
  const resumeUpload = document.getElementById('resume-upload');
  const fileNameDisplay = document.getElementById('file-name-display');
  resumeUpload.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
      fileNameDisplay.textContent = e.target.files[0].name;
      fileNameDisplay.classList.remove('hidden');
    } else {
      fileNameDisplay.classList.add('hidden');
    }
  });

  // Engine Config Drawer Toggle
  const toggleEngineBtn = document.getElementById('toggle-engine-btn');
  const closeEngineBtn = document.getElementById('close-engine-btn');
  const engineDrawer = document.getElementById('engine-config-drawer');

  if (toggleEngineBtn && engineDrawer) {
    toggleEngineBtn.addEventListener('click', (e) => {
      e.preventDefault();
      engineDrawer.classList.toggle('hidden');
      if (!engineDrawer.classList.contains('hidden')) {
        engineDrawer.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  }
  if (closeEngineBtn && engineDrawer) {
    closeEngineBtn.addEventListener('click', () => {
      engineDrawer.classList.add('hidden');
    });
  }

  // Analysis Pipeline
  const analyzeBtn = document.getElementById('analyze-action-btn');
  const tracker = document.getElementById('pipeline-tracker');
  const resultsSection = document.getElementById('results-section');
  const profileContainer = document.getElementById('profile-container');
  const candidateGrid = document.getElementById('candidate-grid');

  analyzeBtn.addEventListener('click', async () => {
    const geminiKey = document.getElementById('gemini-key').value.trim();
    if (!geminiKey) {
      alert('Gemini API Key is required.');
      engineDrawer.classList.remove('hidden');
      return;
    }

    const formData = new FormData();
    formData.append('gemini_key', geminiKey);
    
    const serperKey = document.getElementById('serper-key').value.trim();
    if (serperKey) {
      formData.append('serper_key', serperKey);
    }

    if (activeTab === 'pdf') {
      const file = resumeUpload.files[0];
      if (!file) {
        alert('Please select a PDF resume.');
        return;
      }
      formData.append('resume_file', file);
    } else if (activeTab === 'github') {
      const url = document.getElementById('github-url').value.trim();
      if (!url) {
        alert('Please enter a GitHub URL.');
        return;
      }
      formData.append('github_url', url);
    } else if (activeTab === 'linkedin') {
      const url = document.getElementById('linkedin-url').value.trim();
      if (!url) {
        alert('Please enter a LinkedIn URL.');
        return;
      }
      formData.append('linkedin_url', url);
    }

    // UI Loading state
    const originalHTML = analyzeBtn.innerHTML;
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = `
      <span class="material-symbols-outlined text-[24px] animate-spin">progress_activity</span>
      <span>Synthesizing Identity Vector...</span>
    `;
    
    tracker.classList.remove('hidden');
    tracker.innerHTML = 'Crawling SERP Nodes & Ranking...';
    resultsSection.classList.add('hidden');

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        let errData;
        try {
          errData = await response.json();
        } catch(e) {
          throw new Error("We had trouble connecting to the server. Please try again.");
        }
        
        let message = 'Analysis failed';
        if (Array.isArray(errData.detail)) {
          message = "We couldn't process your input. Please make sure your links and files are valid.";
        } else if (errData.detail) {
          message = errData.detail;
        }
        throw new Error(message);
      }

      const data = await response.json();
      renderResults(data);
      
      tracker.innerHTML = 'Step Complete &bull; 100%';
      resultsSection.classList.remove('hidden');
      resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (error) {
      alert(error.message);
      tracker.classList.add('hidden');
    } finally {
      analyzeBtn.innerHTML = originalHTML;
      analyzeBtn.disabled = false;
    }
  });

  function renderResults(data) {
    const profile = data.profile;
    const suggestions = data.suggestions;

    // Render Profile
    const profileTpl = document.getElementById('profile-template').content.cloneNode(true);
    profileTpl.querySelector('.profile-name').textContent = profile.name || 'Unknown';
    profileTpl.querySelector('.profile-headline').textContent = profile.headline || '';
    profileTpl.querySelector('.profile-location').textContent = profile.location || 'Unknown Location';
    profileTpl.querySelector('.profile-experience').textContent = profile.experience_years ? `${profile.experience_years} Years Experience` : 'N/A';
    profileTpl.querySelector('.profile-education').textContent = profile.education || 'N/A';
    
    const skillsContainer = profileTpl.querySelector('.profile-skills');
    (profile.skills || []).slice(0, 10).forEach((skill, i) => {
      const span = document.createElement('span');
      // Alternate colors based on index for a dynamic look
      const classes = ['text-primary', 'text-secondary', 'text-on-surface', 'text-primary-fixed', 'text-secondary-fixed'];
      span.className = `px-2.5 py-1 rounded-md bg-surface-container-high font-label-sm font-medium shadow-sm ${classes[i % classes.length]}`;
      span.textContent = skill;
      skillsContainer.appendChild(span);
    });

    profileTpl.querySelector('.profile-interests').textContent = (profile.interests || []).join(' • ');

    profileContainer.innerHTML = '';
    profileContainer.appendChild(profileTpl);

    // Render Candidates
    candidateGrid.innerHTML = '';
    suggestions.forEach(suggestion => {
      const candTpl = document.getElementById('candidate-template').content.cloneNode(true);
      const card = candTpl.querySelector('.candidate-card');
      
      // Set type for filtering
      card.setAttribute('data-type', suggestion.action);
      
      // Initials
      const initials = (suggestion.name || '??').split(' ').map(n => n[0]).join('').substring(0,2).toUpperCase();
      candTpl.querySelector('.initials-badge').textContent = initials;

      // Category badge
      const catBadge = candTpl.querySelector('.category-badge');
      catBadge.classList.add('bg-tertiary/15', 'text-tertiary-fixed');
      catBadge.innerHTML = `<span class="material-symbols-outlined text-[14px]">psychology</span><span>${suggestion.category || 'Peer'}</span>`;

      // Action badge
      const actBadge = candTpl.querySelector('.action-badge');
      if (suggestion.action === 'Connect') {
        actBadge.classList.add('bg-secondary/15', 'text-secondary');
        actBadge.innerHTML = `<span class="material-symbols-outlined text-[13px]">hub</span><span>Connect</span>`;
      } else {
        actBadge.classList.add('bg-primary-container/20', 'text-primary');
        actBadge.innerHTML = `<span class="material-symbols-outlined text-[13px]">rss_feed</span><span>Follow</span>`;
      }

      candTpl.querySelector('.candidate-name').textContent = suggestion.name;
      candTpl.querySelector('.candidate-title').textContent = suggestion.title;

      
      const link = candTpl.querySelector('.candidate-url');
      if (suggestion.url) {
        link.href = suggestion.url;
      } else {
        link.classList.add('hidden');
      }

      candidateGrid.appendChild(candTpl);
    });

    // Apply current filter
    applyCandidateFilter();
  }

  // Filtering Logic
  const filterBtns = document.querySelectorAll('.filter-btn');
  let currentFilter = 'all';

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      currentFilter = btn.getAttribute('data-filter');
      
      filterBtns.forEach(b => {
        if (b.getAttribute('data-filter') === currentFilter) {
          b.className = "filter-btn px-space-md py-1.5 rounded-full bg-primary-container text-on-primary-container font-label-md transition-all";
        } else {
          b.className = "filter-btn px-space-md py-1.5 rounded-full bg-surface-container text-on-surface-variant hover:text-on-surface font-label-md transition-all";
        }
      });

      applyCandidateFilter();
    });
  });

  function applyCandidateFilter() {
    const cards = document.querySelectorAll('.candidate-card');
    cards.forEach(card => {
      if (currentFilter === 'all' || card.getAttribute('data-type') === currentFilter) {
        card.classList.remove('hidden');
        card.classList.add('flex');
      } else {
        card.classList.add('hidden');
        card.classList.remove('flex');
      }
    });
  }
});
