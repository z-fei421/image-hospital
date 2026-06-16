// Main JavaScript for Image Hospital

// Utility function to fetch data
async function fetchAPI(url, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Load statistics
async function loadStatistics() {
    try {
        const result = await fetchAPI('/api/history');
        if (result.success) {
            document.getElementById('totalImages').textContent = result.total;
            
            // Calculate average score
            let totalScore = 0;
            let count = 0;
            result.history.forEach(item => {
                if (item.diagnosis && item.diagnosis.health_score) {
                    totalScore += item.diagnosis.health_score;
                    count++;
                }
            });
            
            const avgScore = count > 0 ? (totalScore / count).toFixed(1) : '-';
            document.getElementById('avgScore').textContent = avgScore;
        }
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadStatistics();
});

// Create radar chart
function createRadarChart(canvasId, labels, data) {
    const ctx = document.getElementById(canvasId)?.getContext('2d');
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: '图像质量指标',
                data: data,
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.2)',
                fill: true,
                pointBackgroundColor: '#667eea',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#667eea'
            }]
        },
        options: {
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100
                }
            },
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            }
        }
    });
}

// Utility: Get health grade badge
function getGradeBadge(grade) {
    const badgeClass = {
        'A': 'badge-grade-a',
        'B': 'badge-grade-b',
        'C': 'badge-grade-c',
        'D': 'badge-grade-d'
    }[grade] || 'badge-grade-d';
    
    return `<span class="badge ${badgeClass}">${grade}</span>`;
}
