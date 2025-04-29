
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Set active navigation link based on current page
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (currentPath === linkPath || 
            (linkPath !== '/' && currentPath.startsWith(linkPath))) {
            link.classList.add('active');
        }
    });

    // Form validation for date fields
    const startDateField = document.querySelector('input[name="start_date"]');
    const endDateField = document.querySelector('input[name="end_date"]');
    
    if (startDateField && endDateField) {
        endDateField.addEventListener('change', function() {
            if (endDateField.value && new Date(endDateField.value) < new Date(startDateField.value)) {
                alert('End date cannot be earlier than start date');
                endDateField.value = '';
            }
        });
    }

    // Handle frequency field in reminder form to show/hide relevant fields
    const frequencyField = document.querySelector('select[name="frequency"]');
    const daysOfWeekField = document.querySelector('#div_id_days_of_week');
    const dateOfMonthField = document.querySelector('#div_id_date_of_month');
    
    if (frequencyField && daysOfWeekField && dateOfMonthField) {
        function updateFields() {
            if (frequencyField.value === 'weekly') {
                daysOfWeekField.style.display = 'block';
                dateOfMonthField.style.display = 'none';
            } else if (frequencyField.value === 'monthly') {
                daysOfWeekField.style.display = 'none';
                dateOfMonthField.style.display = 'block';
            } else {
                daysOfWeekField.style.display = 'none';
                dateOfMonthField.style.display = 'none';
            }
        }
        
        frequencyField.addEventListener('change', updateFields);
        updateFields(); // Call on page load
    }
});