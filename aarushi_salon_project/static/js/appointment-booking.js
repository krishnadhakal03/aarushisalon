/**
 * Appointment Booking JavaScript
 * Handles dynamic slot loading and form interactions
 */

document.addEventListener('DOMContentLoaded', function() {
    const serviceCheckboxes = document.querySelectorAll('input[name="services"]');
    const dateSelect = document.getElementById('id_appointment_date');
    const timeSelect = document.getElementById('id_appointment_time');
    const form = document.querySelector('form');
    
    if (!serviceCheckboxes.length || !dateSelect || !timeSelect) {
        console.log('Appointment booking form elements not found');
        return;
    }

    // Initialize form
    initializeForm();
    
    // Event listeners
    serviceCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', handleServiceChange);
    });
    dateSelect.addEventListener('change', handleDateChange);
    timeSelect.addEventListener('change', handleTimeChange);
    
    // Form submission
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }

    function initializeForm() {
        // Disable date and time selects initially
        dateSelect.disabled = true;
        timeSelect.disabled = true;
        
        // Add loading states
        addLoadingState(dateSelect, 'Select a service first');
        addLoadingState(timeSelect, 'Select a date first');
    }

    function handleServiceChange() {
        const selectedServices = Array.from(serviceCheckboxes)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.value);
        
        console.log('Service changed:', selectedServices);
        
        if (selectedServices.length === 0) {
            resetDateAndTimeSelects();
            return;
        }
        
        // Enable date select and load available dates
        dateSelect.disabled = false;
        addLoadingState(dateSelect, 'Loading available dates...');
        loadAvailableDates(selectedServices);
    }

    function handleDateChange() {
        const selectedServices = Array.from(serviceCheckboxes)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.value);
        const selectedDate = dateSelect.value;
        
        console.log('Date changed:', selectedDate);
        console.log('Selected services:', selectedServices);
        
        if (selectedServices.length === 0 || !selectedDate) {
            resetTimeSelect();
            return;
        }
        
        // Enable time select and load available times
        timeSelect.disabled = false;
        addLoadingState(timeSelect, 'Loading available times...');
        loadAvailableSlots(selectedServices, selectedDate);
    }

    function handleTimeChange() {
        // Time slot selected - form is ready for submission
        console.log('Time slot selected:', timeSelect.value);
    }

    function loadAvailableDates(serviceIds) {
        const serviceIdParam = serviceIds.map(id => `service_id=${id}`).join('&');
        fetch(`/api/available-dates/?${serviceIdParam}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    populateDateSelect(data.dates);
                } else {
                    showError('Failed to load available dates: ' + data.error);
                    resetDateAndTimeSelects();
                }
            })
            .catch(error => {
                console.error('Error loading dates:', error);
                showError('Error loading available dates');
                resetDateAndTimeSelects();
            });
    }

    function loadAvailableSlots(serviceIds, date) {
        const serviceIdParam = serviceIds.map(id => `service_id=${id}`).join('&');
        const url = `/api/available-slots/?${serviceIdParam}&date=${date}`;
        console.log('Loading slots from:', url);
        
        fetch(url)
            .then(response => {
                console.log('Response status:', response.status);
                return response.json();
            })
            .then(data => {
                console.log('Slots data:', data);
                if (data.success) {
                    populateTimeSelect(data.slots);
                } else {
                    showError('Failed to load available times: ' + data.error);
                    resetTimeSelect();
                }
            })
            .catch(error => {
                console.error('Error loading slots:', error);
                showError('Error loading available times');
                resetTimeSelect();
            });
    }

    function populateDateSelect(dates) {
        // Clear existing options
        dateSelect.innerHTML = '<option value="">Select a date</option>';
        
        if (dates.length === 0) {
            addLoadingState(dateSelect, 'No available dates');
            return;
        }
        
        dates.forEach(date => {
            const option = document.createElement('option');
            option.value = date.date;
            option.textContent = date.display_date;
            dateSelect.appendChild(option);
        });
        
        // Remove loading state
        removeLoadingState(dateSelect);
    }

    function populateTimeSelect(slots) {
        // Clear existing options
        timeSelect.innerHTML = '<option value="">Select a time</option>';
        
        if (slots.length === 0) {
            addLoadingState(timeSelect, 'No available times - we will call you to schedule');
            timeSelect.disabled = false; // Enable so user can still submit
            return;
        }
        
        slots.forEach(slot => {
            const option = document.createElement('option');
            option.value = slot.start_time;
            option.textContent = slot.display_time;
            timeSelect.appendChild(option);
        });
        
        timeSelect.disabled = false;
        removeLoadingState(timeSelect);
        console.log(`Loaded ${slots.length} time slots`);
    }

    function resetDateAndTimeSelects() {
        resetDateSelect();
        resetTimeSelect();
    }

    function resetDateSelect() {
        dateSelect.innerHTML = '<option value="">Select a date</option>';
        dateSelect.disabled = true;
        addLoadingState(dateSelect, 'Select a service first');
    }

    function resetTimeSelect() {
        timeSelect.innerHTML = '<option value="">Select a time</option>';
        timeSelect.disabled = true;
        addLoadingState(timeSelect, 'Select a date first');
    }

    function addLoadingState(select, text) {
        select.innerHTML = `<option value="">${text}</option>`;
        select.disabled = true;
    }

    function removeLoadingState(select) {
        select.disabled = false;
    }

    function handleFormSubmit(event) {
        // Validate form before submission
        const selectedServices = Array.from(serviceCheckboxes)
            .filter(checkbox => checkbox.checked);
        
        if (selectedServices.length === 0 || !dateSelect.value || !timeSelect.value) {
            event.preventDefault();
            showError('Please select at least one service, date, and time');
            return;
        }
        
        // Show loading state
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = 'Booking...';
        }
    }

    function showError(message) {
        // Create or update error message
        let errorDiv = document.getElementById('appointment-error');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.id = 'appointment-error';
            errorDiv.className = 'alert alert-danger mt-3';
            form.insertBefore(errorDiv, form.firstChild);
        }
        
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        
        // Hide error after 5 seconds
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 5000);
    }

    // Utility function to format time
    function formatTime(timeString) {
        const [hours, minutes] = timeString.split(':');
        const hour = parseInt(hours);
        const ampm = hour >= 12 ? 'PM' : 'AM';
        const displayHour = hour % 12 || 12;
        return `${displayHour}:${minutes} ${ampm}`;
    }
});
