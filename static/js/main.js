$(document).ready(function() {
    setTimeout(function() {
        $('.alert').alert('close');
    }, 5000);

    $('.table').on('click', '.delete-btn', function(e) {
        if (!confirm('Are you sure you want to delete this record? This action cannot be undone.')) {
            e.preventDefault();
        }
    });

    $('.select-all').on('change', function() {
        $('.select-item').prop('checked', $(this).prop('checked'));
    });
});
