document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.upload-area').forEach(area => {
        const input = area.querySelector('input[type="file"]');
        if (!input) return;

        // Prevent browser from opening dragged file
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(event => {
            area.addEventListener(event, e => {
                e.preventDefault();
                e.stopPropagation();
            });
        });

        // Visual feedback while dragging over
        ['dragenter', 'dragover'].forEach(event => {
            area.addEventListener(event, () => {
                area.style.borderColor = 'var(--color-accent)';
                area.style.background = 'var(--color-accent-soft)';
            });
        });

        ['dragleave', 'drop'].forEach(event => {
            area.addEventListener(event, () => {
                area.style.borderColor = '';
                area.style.background = '';
            });
        });

        // On drop, pass files to the hidden input
        area.addEventListener('drop', e => {
            input.files = e.dataTransfer.files;

            // Show filename so user knows it was received
            const label = area.querySelector('p strong');
            if (label && input.files.length > 0) {
                label.textContent = input.files.length === 1
                    ? input.files[0].name
                    : `${input.files.length} files selected`;
            }
        });

        // Same feedback on click-to-select
        input.addEventListener('change', () => {
            const label = area.querySelector('p strong');
            if (label && input.files.length > 0) {
                label.textContent = input.files.length === 1
                    ? input.files[0].name
                    : `${input.files.length} files selected`;
            }
        });
    });
});