(function () {
    'use strict';

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/i;
    const symbolPattern = /[^A-Za-z0-9]/;

    function getOrCreateError(field) {
        let error = field.parentElement.querySelector('.client-error');
        if (!error) {
            error = document.createElement('small');
            error.className = 'client-error';
            field.parentElement.appendChild(error);
        }
        return error;
    }

    function setFieldState(field, message) {
        if (!field) return false;
        const invalid = Boolean(message);
        field.classList.toggle('is-invalid', invalid);
        field.setAttribute('aria-invalid', String(invalid));
        const error = getOrCreateError(field);
        error.textContent = message || '';
        return !invalid;
    }

    function validateEmail(field) {
        if (!field.value.trim()) return setFieldState(field, 'Email address is required.');
        if (!emailPattern.test(field.value.trim())) {
            return setFieldState(field, 'Enter a valid email address, for example ada@example.com.');
        }
        return setFieldState(field, '');
    }

    function passwordRules(value) {
        return {
            length: value.length >= 8,
            number: /\d/.test(value),
            symbol: symbolPattern.test(value),
        };
    }

    function updatePasswordChecklist(field) {
        const checklist = document.querySelector(`[data-password-checklist="${field.id}"]`);
        if (!checklist) return;
        const rules = passwordRules(field.value);
        Object.entries(rules).forEach(([rule, valid]) => {
            const item = checklist.querySelector(`[data-rule="${rule}"]`);
            if (item) item.classList.toggle('valid', valid);
        });
    }

    function validatePassword(field) {
        updatePasswordChecklist(field);
        const rules = passwordRules(field.value);
        if (!field.value) return setFieldState(field, 'Password is required.');
        if (!Object.values(rules).every(Boolean)) {
            return setFieldState(field, 'Use all of the requirements shown below.');
        }
        return setFieldState(field, '');
    }

    function validateMatch(password, confirmation) {
        const status = document.querySelector(`[data-password-match="${confirmation.id}"]`);
        if (!status) return;
        status.classList.remove('match', 'no-match');
        if (!confirmation.value) {
            status.textContent = '';
            return;
        }
        const matches = password.value === confirmation.value;
        status.textContent = matches ? 'Passwords match.' : 'Passwords do not match.';
        status.classList.add(matches ? 'match' : 'no-match');
        setFieldState(confirmation, matches ? '' : 'Passwords do not match.');
    }

    function validateField(field, form, reveal = true) {
        if (!field) return true;
        if (field.type === 'email') {
            if (!reveal) return Boolean(field.value.trim()) && emailPattern.test(field.value.trim());
            return validateEmail(field);
        }
        if (field.name === 'password1') {
            if (!reveal) return Object.values(passwordRules(field.value)).every(Boolean);
            return validatePassword(field);
        }
        if (field.name === 'password2') {
            const password = form.querySelector('[name="password1"]');
            if (!reveal) return Boolean(field.value) && password && field.value === password.value;
            if (!field.value) return setFieldState(field, 'Please confirm your password.');
            validateMatch(password, field);
            return password && field.value === password.value;
        }
        if (field.name === 'phone_number' && !field.value.trim()) {
            return reveal ? setFieldState(field, 'Phone number is required.') : false;
        }
        if (field.type === 'radio') {
            const group = form.querySelectorAll(`[name="${field.name}"]`);
            if (![...group].some((radio) => radio.checked)) {
                return reveal ? setFieldState(group[0], 'Choose an account type.') : false;
            }
            return true;
        }
        if (field.type === 'checkbox' && field.required && !field.checked) {
            return reveal ? setFieldState(field, 'This agreement is required.') : false;
        }
        if (field.required && !field.value.trim()) {
            return reveal ? setFieldState(field, 'This field is required.') : false;
        }
        return reveal ? setFieldState(field, '') : true;
    }

    function fieldsForStep(form) {
        const step = form.dataset.signupStep;
        if (step === '1') {
            return [
                form.querySelector('[name="first_name"]'),
                form.querySelector('[name="last_name"]'),
                form.querySelector('[name="gender"]'),
            ];
        }
        if (step === '2') {
            return [
                form.querySelector('[name="username"]'),
                ...form.querySelectorAll('[name="account_type"]'),
                form.querySelector('[name="password1"]'),
                form.querySelector('[name="password2"]'),
            ];
        }
        if (step === '3') {
            return [
                form.querySelector('[name="email"]'),
                form.querySelector('[name="phone_number"]'),
            ];
        }
        return [...form.querySelectorAll('input[required]')];
    }

    function validateForm(form) {
        const fields = fieldsForStep(form);
        let firstInvalid = null;
        fields.forEach((field) => {
            const valid = validateField(field, form);
            if (!valid && !firstInvalid) firstInvalid = field;
        });

        if (form.dataset.signupStep === '4') {
            const agreements = [...form.querySelectorAll('input[type="checkbox"][required]')];
            agreements.forEach((field) => {
                if (!validateField(field, form) && !firstInvalid) firstInvalid = field;
            });
        }

        if (firstInvalid) {
            firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
            firstInvalid.focus({ preventScroll: true });
            firstInvalid.closest('.form, .form-check')?.classList.add('form-field-highlight');
            window.setTimeout(() => {
                firstInvalid.closest('.form, .form-check')?.classList.remove('form-field-highlight');
            }, 350);
            return false;
        }
        return true;
    }

    function setupPasswordToggles() {
        document.querySelectorAll('[data-password-toggle]').forEach((button) => {
            const field = document.getElementById(button.dataset.passwordToggle);
            if (!field) return;
            button.addEventListener('click', () => {
                const showing = field.type === 'text';
                field.type = showing ? 'password' : 'text';
                button.setAttribute('aria-label', showing ? 'Show password' : 'Hide password');
                const icon = button.querySelector('i');
                icon?.classList.toggle('fa-eye', showing);
                icon?.classList.toggle('fa-eye-slash', !showing);
            });
        });
    }

    function setupCropPreview(form) {
        const input = form.querySelector('[name="profile_image"]');
        const panel = form.querySelector('[data-crop-panel]');
        const preview = form.querySelector('[data-crop-preview]');
        const reset = form.querySelector('[data-crop-reset]');
        if (!input || !panel || !preview) return;

        let selectedFile = null;
        input.addEventListener('change', () => {
            selectedFile = input.files[0] || null;
            if (!selectedFile) {
                panel.hidden = true;
                return;
            }
            const reader = new FileReader();
            reader.onload = (event) => {
                preview.src = event.target.result;
                panel.hidden = false;
            };
            reader.readAsDataURL(selectedFile);
        });

        reset?.addEventListener('click', () => {
            input.value = '';
            selectedFile = null;
            panel.hidden = true;
            preview.removeAttribute('src');
        });

        form.addEventListener('submit', (event) => {
            if (!selectedFile || !window.HTMLCanvasElement) return;
            event.preventDefault();
            const image = new Image();
            image.onload = () => {
                const size = Math.min(image.naturalWidth, image.naturalHeight);
                const canvas = document.createElement('canvas');
                canvas.width = size;
                canvas.height = size;
                const context = canvas.getContext('2d');
                context.drawImage(
                    image,
                    (image.naturalWidth - size) / 2,
                    (image.naturalHeight - size) / 2,
                    size,
                    size,
                    0,
                    0,
                    size,
                    size
                );
                canvas.toBlob((blob) => {
                    if (!blob) {
                        form.submit();
                        return;
                    }
                    const cropped = new File([blob], selectedFile.name, { type: selectedFile.type });
                    const transfer = new DataTransfer();
                    transfer.items.add(cropped);
                    input.files = transfer.files;
                    form.submit();
                }, selectedFile.type || 'image/jpeg', 0.92);
            };
            image.src = preview.src;
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        setupPasswordToggles();
        document.querySelectorAll('form[data-signup-step]').forEach((form) => {
            const fields = fieldsForStep(form);
            const submit = form.querySelector('.signup-submit');

            const refreshButton = () => {
                const valid = fields.every((field) => field && validateField(field, form, false));
                const agreementsValid = form.dataset.signupStep !== '4' ||
                    [...form.querySelectorAll('input[type="checkbox"][required]')].every((field) => field.checked);
                if (submit) submit.disabled = !(valid && agreementsValid);
            };

            fields.forEach((field) => {
                if (!field) return;
                ['input', 'change', 'blur'].forEach((eventName) => {
                    field.addEventListener(eventName, () => {
                        validateField(field, form);
                        if (field.name === 'password1') {
                            const confirmation = form.querySelector('[name="password2"]');
                            if (confirmation) validateMatch(field, confirmation);
                        }
                        if (field.name === 'password2') {
                            validateMatch(form.querySelector('[name="password1"]'), field);
                        }
                        refreshButton();
                    });
                });
            });

            form.querySelectorAll('input[type="checkbox"]').forEach((field) => {
                field.addEventListener('change', refreshButton);
            });

            form.addEventListener('submit', (event) => {
                if (!validateForm(form)) event.preventDefault();
            });

            if (form.dataset.signupStep === '4') setupCropPreview(form);
            refreshButton();
        });
    });
})();