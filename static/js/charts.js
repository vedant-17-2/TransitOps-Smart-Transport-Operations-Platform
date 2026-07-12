// Global Chart.js defaults
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.responsive = true;
Chart.defaults.maintainAspectRatio = false;
Chart.defaults.animation.duration = 1500;
Chart.defaults.animation.easing = 'easeOutQuart';
Chart.defaults.plugins.legend.position = 'bottom';
Chart.defaults.plugins.tooltip.backgroundColor = '#0f172a';
Chart.defaults.plugins.tooltip.padding = 10;
Chart.defaults.plugins.tooltip.cornerRadius = 6;
Chart.defaults.plugins.tooltip.titleFont = { size: 14, weight: 'bold' };
Chart.defaults.plugins.tooltip.bodyFont = { size: 13 };
Chart.defaults.scale.grid.color = '#f1f5f9';

// Color Palette Constants
const CHART_COLORS = {
    primary: '#714B67',
    success: '#059669',
    warning: '#d97706',
    danger: '#dc2626',
    info: '#0891b2',
    purple: '#7c3aed',
    pink: '#db2777',
    orange: '#ea580c'
};

const COLOR_PALETTE = [
    CHART_COLORS.primary,
    CHART_COLORS.success,
    CHART_COLORS.warning,
    CHART_COLORS.danger,
    CHART_COLORS.info,
    CHART_COLORS.purple,
    CHART_COLORS.pink,
    CHART_COLORS.orange
];

function hexToRgb(hex) {
    if (!hex) return '113, 75, 103'; // Default primary rgb
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? `${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(result[3], 16)}` : '113, 75, 103';
}

/**
 * Reusable function to create a Chart.js instance
 */
function createChart(canvasElement, type, labels, data, options = {}) {
    if (!canvasElement) return null;
    const ctx = canvasElement.getContext('2d');
    
    // Default dataset structure
    const dataset = {
        data: data,
        ...options // Merge specific dataset options like backgroundColor, etc.
    };

    // Apply gradient shading for line and bar charts
    if ((type === 'line' || type === 'bar') && options.backgroundColor && !Array.isArray(options.backgroundColor)) {
        // Create vertical gradient
        const gradient = ctx.createLinearGradient(0, 0, 0, 350);
        const rgb = hexToRgb(options.backgroundColor);
        
        // Bar charts get a slightly more solid gradient, lines get a transparent fill
        if (type === 'bar') {
            gradient.addColorStop(0, `rgba(${rgb}, 0.9)`);
            gradient.addColorStop(1, `rgba(${rgb}, 0.3)`);
        } else {
            gradient.addColorStop(0, `rgba(${rgb}, 0.5)`);
            gradient.addColorStop(1, `rgba(${rgb}, 0.02)`);
            dataset.fill = true;
        }
        dataset.backgroundColor = gradient;
        dataset.borderColor = options.backgroundColor; // Ensure border matches the solid color
        if (type === 'line') dataset.borderWidth = 2;
    }

    // Remove dataset options from root options object for Chart config
    const chartOptions = { ...options };
    delete chartOptions.backgroundColor;
    delete chartOptions.borderColor;
    delete chartOptions.borderWidth;
    delete chartOptions.fill;
    delete chartOptions.tension;
    delete chartOptions.cutout;
    delete chartOptions.borderRadius;

    return new Chart(canvasElement, {
        type: type,
        data: {
            labels: labels,
            datasets: [dataset]
        },
        options: chartOptions
    });
}
