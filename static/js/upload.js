function acceptMatches(file, acceptAttr) {
    if (!acceptAttr) return true;
    const patterns = acceptAttr.split(',').map(p => p.trim());
    return patterns.some(pattern => {
        if (pattern.endsWith('/*')) {
            return file.type.startsWith(pattern.slice(0, -1));
        }
        return file.type === pattern;
    });
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.upload-area').forEach(area => {
        const input = area.querySelector('input[type="file"]');
        if (!input) return;

        const errorEl = document.createElement('p');
        errorEl.className = 'upload-error';
        area.insertAdjacentElement('afterend', errorEl);

        const kindLabel = input.accept.startsWith('video') ? 'video' : 'image';

        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(event => {
            area.addEventListener(event, e => {
                e.preventDefault();
                e.stopPropagation();
            });
        });

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

        function updateLabel() {
            const label = area.querySelector('p strong');
            if (label && input.files.length > 0) {
                label.textContent = input.files.length === 1
                    ? input.files[0].name
                    : `${input.files.length} files selected`;
            }
        }

        function tryAssign(fileList) {
            const files = Array.from(fileList);
            const invalid = files.find(f => !acceptMatches(f, input.accept));

            if (invalid) {
                errorEl.textContent = `"${invalid.name}" isn't a valid ${kindLabel} file.`;
                return;
            }

            errorEl.textContent = '';

            if (!input.multiple && files.length > 1) {
                const singleFile = new DataTransfer();
                singleFile.items.add(files[0]);
                input.files = singleFile.files;
            } else if (fileList instanceof FileList) {
                input.files = fileList;
            }

            updateLabel();
        }

        area.addEventListener('drop', e => tryAssign(e.dataTransfer.files));
        input.addEventListener('change', () => tryAssign(input.files));
    });
});