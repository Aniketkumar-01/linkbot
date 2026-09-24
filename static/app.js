document.addEventListener('DOMContentLoaded', () => {
  // Tab Switching Logic
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
      alert('Gemini API Key is required. Please open API Settings to enter it.');
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
        alert('Please enter a GitHub profile URL.');
        return;
      }
      formData.append('github_url', url);
    } else if (activeTab === 'linkedin') {
      const text = document.getElementById('bio-text').value.trim();
      if (!text) {
        alert('Please paste your professional bio or summary.');
        return;
      }
      formData.append('bio_text', text);
    }

    // UI Loading state
    const originalHTML = analyzeBtn.innerHTML;
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = `
      <span class="material-symbols-outlined text-[24px] animate-spin">progress_activity</span>
      <span>Analyzing profile...</span>
    `;
    
    tracker.classList.remove('hidden');
    
    if (serperKey) {
      tracker.innerHTML = 'Finding relevant LinkedIn connections...';
    } else {
      tracker.innerHTML = 'Analyzing profile (Search skipped — Serper key omitted)...';
    }
    
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
      
      tracker.innerHTML = 'Analysis complete!';
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
    const profile = data.profile || {};
    const suggestions = data.suggestions || [];

    // Render Profile
    const profileTpl = document.getElementById('profile-template').content.cloneNode(true);
    profileTpl.querySelector('.profile-name').textContent = profile.name || 'Professional';
    profileTpl.querySelector('.profile-headline').textContent = profile.headline || '';
    profileTpl.querySelector('.profile-location').textContent = profile.location || 'Location Not Specified';
    profileTpl.querySelector('.profile-experience').textContent = profile.experience_years ? `${profile.experience_years} Years Experience` : 'Experience Not Specified';
    
    // Format education safely
    const edu = profile.education;
    let eduText = 'N/A';
    if (Array.isArray(edu) && edu.length > 0) {
      eduText = edu.join(' • ');
    } else if (typeof edu === 'string' && edu.trim()) {
      eduText = edu;
    }
    profileTpl.querySelector('.profile-education').textContent = eduText;
    
    const skillsContainer = profileTpl.querySelector('.profile-skills');
    const skillsList = profile.skills || [];
    if (skillsList.length > 0) {
      skillsList.slice(0, 15).forEach((skill, i) => {
        const span = document.createElement('span');
        const classes = ['text-primary', 'text-secondary', 'text-on-surface', 'text-primary-fixed', 'text-secondary-fixed'];
        span.className = `px-2.5 py-1 rounded-md bg-surface-container-high font-label-sm font-medium shadow-sm ${classes[i % classes.length]}`;
        span.textContent = skill;
        skillsContainer.appendChild(span);
      });
    } else {
      const span = document.createElement('span');
      span.className = 'text-on-surface-variant font-body-sm';
      span.textContent = 'None identified';
      skillsContainer.appendChild(span);
    }

    const interestsList = profile.interests || [];
    profileTpl.querySelector('.profile-interests').textContent = interestsList.length > 0 ? interestsList.join(' • ') : 'General Networking';

    profileContainer.innerHTML = '';
    profileContainer.appendChild(profileTpl);

    // Render Candidates
    candidateGrid.innerHTML = '';
    if (suggestions.length === 0) {
      candidateGrid.innerHTML = `
        <div class="col-span-full text-center py-12 text-on-surface-variant bg-surface-container-low/40 rounded-2xl">
          <span class="material-symbols-outlined text-[48px] text-primary/60 mb-2">person_search</span>
          <p class="font-headline-sm text-on-surface">No live candidates fetched</p>
          <p class="font-body-md text-sm mt-1">To search and rank live LinkedIn profiles, make sure to add your Serper API Key in API Settings.</p>
        </div>
      `;
      return;
    }

    suggestions.forEach(suggestion => {
      const candTpl = document.getElementById('candidate-template').content.cloneNode(true);
      const card = candTpl.querySelector('.candidate-card');
      
      // Set type for filtering
      card.setAttribute('data-type', suggestion.action || 'Connect');
      
      // Initials
      const initials = (suggestion.name || '??')
        .split(' ')
        .filter(Boolean)
        .map(n => n[0])
        .join('')
        .substring(0, 2)
        .toUpperCase() || '??';
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

      candTpl.querySelector('.candidate-name').textContent = suggestion.name || 'Unknown';
      candTpl.querySelector('.candidate-title').textContent = suggestion.title || 'LinkedIn Member';

      const snippetEl = candTpl.querySelector('.candidate-snippet');
      if (snippetEl) {
        snippetEl.textContent = suggestion.snippet || '';
      }

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
          b.className = "filter-btn px-space-md py-1.5 rounded-full bg-primary-container text-on-primary-container font-label-md transition-all cursor-pointer";
        } else {
          b.className = "filter-btn px-space-md py-1.5 rounded-full bg-surface-container text-on-surface-variant hover:text-on-surface font-label-md transition-all cursor-pointer";
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
