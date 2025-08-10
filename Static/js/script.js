document.getElementById('resumeForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData();
    const resumeFile = document.getElementById('resume').files[0];
    const jobDescription = document.getElementById('jobDescription').value;
    
    formData.append('resume', resumeFile);
    formData.append('job_description', jobDescription);
    
    // Show loading state
    const submitBtn = document.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analyzing...';
    
    fetch('/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        
        displayResults(data);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while analyzing your resume.');
    })
    .finally(() => {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Analyze Resume';
    });
});

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    const scoreBar = document.getElementById('scoreBar');
    const scoreText = document.getElementById('scoreText');
    const feedbackDiv = document.getElementById('feedback');
    const missingKeywordsDiv = document.getElementById('missingKeywords');
    
    // Update score
    scoreBar.style.width = `${data.score}%`;
    scoreBar.className = `progress-bar ${getScoreColorClass(data.score)}`;
    scoreText.textContent = `Match Score: ${data.score}%`;
    
    // Update feedback
    feedbackDiv.innerHTML = data.feedback.map(item => 
        `<div class="feedback-item">${item}</div>`
    ).join('');
    
    // Update missing keywords
    if (data.missing_keywords && data.missing_keywords.length > 0) {
        missingKeywordsDiv.innerHTML = data.missing_keywords.map(keyword => 
            `<span class="badge bg-warning text-dark keyword-badge">${keyword}</span>`
        ).join('');
    } else {
        missingKeywordsDiv.innerHTML = '<p>No important keywords missing. Good job!</p>';
    }
    
    // Show results
    resultsDiv.style.display = 'block';
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
}

function getScoreColorClass(score) {
    if (score >= 80) return 'bg-success';
    if (score >= 60) return 'bg-primary';
    if (score >= 40) return 'bg-warning';
    return 'bg-danger';
}