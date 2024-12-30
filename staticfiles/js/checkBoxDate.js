document.getElementById('addDateTime').addEventListener('change', function() {
    const dateTimeSection = document.getElementById('dateTimeSection');
    dateTimeSection.style.display = this.checked ? 'block' : 'none';
});
