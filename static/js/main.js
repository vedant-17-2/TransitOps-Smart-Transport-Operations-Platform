/**
 * TransitOps - Main JavaScript
 * Sidebar toggle, search, confirmations, and interactive behaviors
 */

document.addEventListener('DOMContentLoaded', function() {

    // ============================================================
    // SIDEBAR CLOSING LOGIC (Toggle is handled below)
    // ============================================================
    const sidebar = document.getElementById('sidebar');
    const sidebarClose = document.getElementById('sidebarClose');
    const sidebarOverlay = document.getElementById('sidebarOverlay');

    if (sidebarClose) {
        sidebarClose.addEventListener('click', function() {
            sidebar.classList.remove('show');
            sidebarOverlay.classList.remove('show');
        });
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', function() {
            sidebar.classList.remove('show');
            sidebarOverlay.classList.remove('show');
        });
    }

    // ============================================================
    // AUTO-DISMISS ALERTS
    // ============================================================
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });

    // ============================================================
    // CONFIRM DELETE
    // ============================================================
    document.querySelectorAll('[data-confirm]').forEach(function(el) {
        el.addEventListener('click', function(e) {
            if (!confirm(this.dataset.confirm || 'Are you sure you want to proceed?')) {
                e.preventDefault();
            }
        });
    });

    // ============================================================
    // TABLE SEARCH
    // ============================================================
    const tableSearch = document.getElementById('tableSearch');
    if (tableSearch) {
        tableSearch.addEventListener('keyup', function() {
            const query = this.value.toLowerCase();
            const table = document.querySelector('.searchable-table');
            if (!table) return;

            const rows = table.querySelectorAll('tbody tr');
            rows.forEach(function(row) {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(query) ? '' : 'none';
            });
        });
    }

    // ============================================================
    // TOOLTIPS
    // ============================================================
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(function(tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // ============================================================
    // NUMBER ANIMATION (for KPI cards)
    // ============================================================
    function animateValue(element, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const value = Math.floor(progress * (end - start) + start);
            element.textContent = value.toLocaleString();
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }

    document.querySelectorAll('.kpi-value[data-value]').forEach(function(el) {
        const endValue = parseInt(el.dataset.value);
        if (!isNaN(endValue)) {
            animateValue(el, 0, endValue, 800);
        }
    });

    // ============================================================
    // STAGGERED ANIMATIONS
    // ============================================================
    const animateElements = document.querySelectorAll('.card, .table-container, .page-header, .filter-bar, .kpi-card');
    let delay = 0;
    animateElements.forEach(function(el) {
        if (!el.classList.contains('animate-fade-in-up')) {
            el.classList.add('animate-fade-in-up');
            el.style.animationDelay = delay + 's';
            delay += 0.05; // 50ms stagger
        }
    });

    // ============================================================
    // ACTIVE NAV HIGHLIGHTING
    // ============================================================
    const currentPath = window.location.pathname;
    document.querySelectorAll('.sidebar-nav .nav-link').forEach(function(link) {
        const href = link.getAttribute('href');
        if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('active');
        } else if (href === '/' && currentPath === '/') {
            link.classList.add('active');
        }
    });
});

// ============================================================
// PDF EXPORT
// ============================================================
function downloadPDF(elementId, filename) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const opt = {
        margin:       10,
        filename:     filename + '.pdf',
        image:        { type: 'jpeg', quality: 1.0 },
        html2canvas:  { 
            scale: 4, 
            useCORS: true, 
            backgroundColor: '#ffffff', 
            windowWidth: 1200,
            onclone: function(doc) {
                const el = doc.getElementById(elementId);
                if (el) {
                    el.style.setProperty('color', '#111827', 'important');
                    el.style.setProperty('background-color', '#ffffff', 'important');
                    const all = el.getElementsByTagName('*');
                    for (let i = 0; i < all.length; i++) {
                        let node = all[i];
                        if (node.classList.contains('text-danger')) {
                            node.style.setProperty('color', '#dc3545', 'important');
                        } else if (node.classList.contains('text-success')) {
                            node.style.setProperty('color', '#198754', 'important');
                        } else if (node.classList.contains('text-warning')) {
                            node.style.setProperty('color', '#ffc107', 'important');
                        } else if (node.classList.contains('text-muted')) {
                            node.style.setProperty('color', '#6c757d', 'important');
                        } else if (node.tagName === 'A' || node.classList.contains('text-primary')) {
                            node.style.setProperty('color', '#0d6efd', 'important');
                        } else if (node.classList.contains('badge')) {
                            node.style.setProperty('color', '#ffffff', 'important');
                        } else {
                            node.style.setProperty('color', '#111827', 'important');
                        }
                        
                        if (node.tagName === 'TH') {
                            node.style.setProperty('background-color', '#f8f9fa', 'important');
                        }
                    }
                }
            }
        },
        jsPDF:        { unit: 'mm', format: 'a4', orientation: 'landscape' }
    };
    
    try {
        html2pdf().set(opt).from(element).save().then(function() {
            console.log('PDF exported successfully');
        }).catch(function(err) {
            console.error('PDF export promise rejected:', err);
            alert('Failed to generate PDF. Error: ' + err);
        });
    } catch (e) {
        console.error('Error generating PDF:', e);
        alert('Error generating PDF: ' + e.message);
    }
}



/* ============================================================
   KPI COUNT-UP ANIMATION
   ============================================================ */
document.addEventListener('DOMContentLoaded', function() {
    const countElements = document.querySelectorAll('.count-up');
    
    countElements.forEach(el => {
        const endValStr = el.getAttribute('data-value').replace(',', '');
        const endVal = parseFloat(endValStr);
        if (isNaN(endVal)) return;
        
        const isFloat = endValStr.includes('.');
        const duration = 1500; // ms
        let startTime = null;
        
        const step = (currentTime) => {
            if (!startTime) startTime = currentTime;
            const progress = Math.min((currentTime - startTime) / duration, 1);
            
            // easeOutQuart
            const easeProgress = 1 - Math.pow(1 - progress, 4);
            const currentVal = (easeProgress * endVal);
            
            if (isFloat) {
                el.innerText = currentVal.toFixed(1);
            } else {
                el.innerText = Math.floor(currentVal).toString();
            }
            
            if (progress < 1) {
                window.requestAnimationFrame(step);
            } else {
                el.innerText = isFloat ? endVal.toFixed(1) : endVal.toString();
            }
        };
        
        window.requestAnimationFrame(step);
    });
});

/* ============================================================
   SIDEBAR TOGGLE ANIMATION
   ============================================================ */
document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggleBtn = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.sidebar-overlay');
    
    if (sidebarToggleBtn) {
        sidebarToggleBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (window.innerWidth < 992) {
                // Mobile view
                if (sidebar) sidebar.classList.toggle('show');
                if (overlay) overlay.classList.toggle('show');
            } else {
                // Desktop view
                document.body.classList.toggle('sidebar-mini');
            }
        });
    }
    
    if (overlay) {
        overlay.addEventListener('click', function() {
            if (sidebar) sidebar.classList.remove('show');
            overlay.classList.remove('show');
        });
    }
});

/* ============================================================
   PAGE FADE TRANSITION
   ============================================================ */
document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('a[href]:not([target="_blank"]):not([href^="#"]):not([data-toggle]):not([data-bs-toggle])');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            // Prevent transition if it has a prevent class or is external or modifier key is pressed
            if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey || this.classList.contains('no-transition') || this.href.includes('export=csv')) {
                return;
            }
            
            // Only transition if it's the same origin
            if (this.origin === window.location.origin) {
                e.preventDefault();
                document.body.classList.add('page-is-exiting');
                setTimeout(() => {
                    window.location.href = this.href;
                }, 250);
            }
        });
    });
});

/* ============================================================
   TOAST NOTIFICATIONS
   ============================================================ */
document.addEventListener('DOMContentLoaded', function() {
    var toastElList = [].slice.call(document.querySelectorAll('.toast'))
    var toastList = toastElList.map(function (toastEl) {
        return new bootstrap.Toast(toastEl)
    });
    // The "show" class is added by default in HTML, so they will appear,
    // but initializing them ensures they auto-hide according to data-bs-delay
});
