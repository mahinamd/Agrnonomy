$(document).ready(function () {
    const mainPassShowBtn = document.getElementById("main-pass-show-btn");
    const confirmPassShowBtn = document.getElementById("confirm-pass-show-btn");
    const passwordShowBtn = document.getElementById("password-show-btn");
    const phoneInputFieldShowBtn = document.getElementById("phone-input-field-show-btn");
    const emailInputFieldShowBtn = document.getElementById("email-input-field-show-btn");
    const itiInputField = document.getElementById("iti-input-field");
    const phoneInputField = document.getElementById("phone-input-field");
    const emailInputField = document.getElementById("email-input-field");
    const googleOauthBtn = document.getElementById("google-oauth-btn");

    if (mainPassShowBtn) {
        mainPassShowBtn.addEventListener('click', function (event) {
            const mainPassInputField = document.getElementById("main-pass-input-field");
            const mainPassEyeIcon = document.getElementById("main-pass-eye-icon");
            if (mainPassInputField && mainPassEyeIcon) {
                if (mainPassInputField.type === "password") {
                    mainPassInputField.type = "text";
                    mainPassEyeIcon.className = "fas fa-eye-slash";
                } else {
                    mainPassInputField.type = "password";
                    mainPassEyeIcon.className = "fas fa-eye";
                }
            }
        });
    }

    if (confirmPassShowBtn) {
        confirmPassShowBtn.addEventListener('click', function (event) {
            const confirmPassInputField = document.getElementById("confirm-pass-input-field");
            const confirmPassEyeIcon = document.getElementById("confirm-pass-eye-icon");
            if (confirmPassInputField && confirmPassEyeIcon) {
                if (confirmPassInputField.type === "password") {
                    confirmPassInputField.type = "text";
                    confirmPassEyeIcon.className = "fas fa-eye-slash";
                } else {
                    confirmPassInputField.type = "password";
                    confirmPassEyeIcon.className = "fas fa-eye";
                }
            }
        });
    }

    if (passwordShowBtn) {
        passwordShowBtn.addEventListener('click', function (event) {
            const passwordInputField = document.getElementById("password-input-field");
            const passwordEyeIcon = document.getElementById("password-eye-icon");
            if (passwordInputField && passwordEyeIcon) {
                if (passwordInputField.type === "password") {
                    passwordInputField.type = "text";
                    passwordEyeIcon.className = "fas fa-eye-slash";
                } else {
                    passwordInputField.type = "password";
                    passwordEyeIcon.className = "fas fa-eye";
                }
            }
        });
    }

    if (itiInputField) {
        const iti = window.intlTelInput(itiInputField, {
            initialCountry: "bd",
            separateDialCode: true,
            utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@18.1.1/build/js/utils.js",
        });

        itiInputField.addEventListener('blur', function () {
            if (phoneInputField) {
                phoneInputField.value = iti.getNumber();
            }
        });
    }

    if (phoneInputFieldShowBtn) {
        phoneInputFieldShowBtn.addEventListener('click', function (event) {
            if (itiInputField && phoneInputField && emailInputField) {
                itiInputField.disabled = false;
                phoneInputField.disabled = false;
                let itiDiv = document.querySelector(".iti");
                if (itiDiv && itiDiv.classList.contains("d-none")) {
                    itiDiv.classList.remove("d-none");
                }
                if (itiInputField.classList.contains("d-none")) {
                    itiInputField.classList.remove("d-none");
                }
                if (!itiInputField.hasAttribute("required")) {
                    itiInputField.setAttribute('required', '');
                }
                if (!phoneInputField.hasAttribute("required")) {
                    phoneInputField.setAttribute('required', '');
                }
                if (!emailInputField.classList.contains("d-none")) {
                    emailInputField.classList.add("d-none");
                }
                if (emailInputField.hasAttribute("required")) {
                    emailInputField.removeAttribute('required');
                }
                if (emailInputFieldShowBtn.classList.contains("active")) {
                    emailInputFieldShowBtn.classList.remove("active");
                }
                if (!phoneInputFieldShowBtn.classList.contains("active")) {
                    phoneInputFieldShowBtn.classList.add("active");
                }
                emailInputField.value = '';
                emailInputField.disabled = true;
            }
        });
    }

    if (emailInputFieldShowBtn) {
        emailInputFieldShowBtn.addEventListener('click', function (event) {
            if (itiInputField && phoneInputField && emailInputField) {
                emailInputField.disabled = false;
                let itiDiv = document.querySelector(".iti");
                if (itiDiv && !itiDiv.classList.contains("d-none")) {
                    itiDiv.classList.add("d-none");
                }
                if (!itiInputField.classList.contains("d-none")) {
                    itiInputField.classList.add("d-none");
                }
                if (itiInputField.hasAttribute("required")) {
                    itiInputField.removeAttribute('required');
                }
                if (phoneInputField.hasAttribute("required")) {
                    phoneInputField.removeAttribute('required');
                }
                if (emailInputField.classList.contains("d-none")) {
                    emailInputField.classList.remove("d-none");
                }
                if (!emailInputField.hasAttribute("required")) {
                    emailInputField.setAttribute('required', '');
                }
                if (!emailInputFieldShowBtn.classList.contains("active")) {
                    emailInputFieldShowBtn.classList.add("active");
                }
                if (phoneInputFieldShowBtn.classList.contains("active")) {
                    phoneInputFieldShowBtn.classList.remove("active");
                }
                itiInputField.value = '';
                phoneInputField.value = '';
                itiInputField.disabled = true;
                phoneInputField.disabled = true;
            }
        });
    }

    if (form && googleOauthBtn) {
        googleOauthBtn.addEventListener('click', function (event) {
            const requiredInputFields = form.querySelectorAll('input[required]');
            requiredInputFields.forEach(function(inputField) {
                if (!(inputField.id.includes("recaptcha") || inputField.className.includes("recaptcha"))) {
                    inputField.value = '';
                    inputField.removeAttribute('required');
                }
            });
            const googleOauthHiddenInputField = document.getElementById("google-oauth-hidden-input-field");
            if (googleOauthHiddenInputField) {
                googleOauthHiddenInputField.value = 'yes';
            } else {
                const hiddenInputField = document.createElement("input");
                hiddenInputField.setAttribute("id", "google-oauth-hidden-input-field");
                hiddenInputField.setAttribute("class", "form-control d-none");
                hiddenInputField.setAttribute("type", "hidden");
                hiddenInputField.setAttribute("name", "google_oauth");
                hiddenInputField.setAttribute("value", "yes");
                hiddenInputField.setAttribute("required", "");
                form.appendChild(hiddenInputField);
            }
        });
    }
});
