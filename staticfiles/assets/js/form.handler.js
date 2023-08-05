const imgCropOption = document.getElementById("img-crop-option");
const imgContainer = document.getElementById("img-container");
const imgField = document.getElementById("img-field");
const imgEditBtn = document.getElementById("img-edit-btn");
const imgInput = document.getElementById("img-input");
const croppingDetailsInput = document.getElementById("cropping-details");
const selectCategory = document.getElementById("select-category");
const selectSubcategory = document.getElementById("select-subcategory");
const loadingSpinner = document.getElementById("loading-spinner");
const resetForm = document.getElementById("reset-form");
const deleteObject = document.getElementById("delete-object");
const confirmEdit = document.getElementById("confirm-edit");
const cancelEdit = document.getElementById("cancel-edit");
const formAlert = document.getElementById("form-alert");
const defaultImgUrl = (imgField) ? imgField.src : null;
let cropper;
let imgBase64Str = '';
let imgFormat = '';
let croppingDetails = {};

// Information Fields
const informationFieldsContainer = document.getElementById("info-fields");

if(informationFieldsContainer) {
    const addInformationField = document.getElementById("add-info-field");
    const removeInformationField = document.getElementById("remove-info-field");

    if(addInformationField && removeInformationField) {
        addInformationField.addEventListener('click', function () {
            const bnHeader = document.createElement('h6');
            bnHeader.className = "dash-data-col";
            bnHeader.textContent = "Information (Bangla):";

            const bnKeyField = document.createElement('input');
            bnKeyField.className = "form-control text-center data-input mb-3";
            bnKeyField.type = 'text';
            bnKeyField.name = "name_bn[]";
            bnKeyField.placeholder = "Information name (Bangla)";

            const bnValueField = document.createElement('input');
            bnValueField.className = "form-control text-center data-input";
            bnValueField.type = 'text';
            bnValueField.name = "details_bn[]";
            bnValueField.placeholder = "Information details (Bangla)";

            const bnInformationDiv = document.createElement('div');
            bnInformationDiv.className = "col prof-col pt-3";
            bnInformationDiv.appendChild(bnHeader);
            bnInformationDiv.appendChild(bnKeyField);
            bnInformationDiv.appendChild(bnValueField);

            const enHeader = document.createElement('h6');
            enHeader.className = "dash-data-col";
            enHeader.textContent = "Information (English):";

            const enKeyField = document.createElement('input');
            enKeyField.className = "form-control text-center data-input mb-3";
            enKeyField.type = 'text';
            enKeyField.name = "name_en[]";
            enKeyField.placeholder = "Information name (English)";

            const enValueField = document.createElement('input');
            enValueField.className = "form-control text-center data-input";
            enValueField.type = 'text';
            enValueField.name = "details_en[]";
            enValueField.placeholder = "Information details (English)";

            const enInformationDiv = document.createElement('div');
            enInformationDiv.className = "col prof-col pt-3";
            enInformationDiv.appendChild(enHeader);
            enInformationDiv.appendChild(enKeyField);
            enInformationDiv.appendChild(enValueField);

            const informationFieldDiv = document.createElement('div');
            informationFieldDiv.appendChild(bnInformationDiv);
            informationFieldDiv.appendChild(enInformationDiv);

            informationFieldsContainer.appendChild(informationFieldDiv);
        });

        removeInformationField.addEventListener('click', function (event) {
            let totalChildren = informationFieldsContainer.childElementCount;
            let lastChild = informationFieldsContainer.lastElementChild;
            let tempCount = informationCount;
            if (tempCount === 0) {
                tempCount++;
            }
            if (lastChild && totalChildren > tempCount) {
                informationFieldsContainer.removeChild(lastChild);
            }
        });
    }
}

if(resetForm) {
    resetForm.addEventListener('click', function (event) {
        imgInput.value = '';
        imgField.src = defaultImgUrl;
    });
}

function confirmed(url) {
    const confirmYes = document.getElementById("confirm-yes");
    if(form && confirmYes) {
        confirmYes.addEventListener('click', function () {
            $("#confirmation").modal('hide');
            form.action = url;
            form.submit();
        });
    }
}

if(deleteObject) {
    deleteObject.addEventListener('click', function (event) {
        event.preventDefault();
        let url = this.getAttribute("data-href");
        if(informationCount === 0) {
            $("#modal-body").empty().append("<p>Do you want to delete the subcategory permanently?</p>");
        } else if(informationCount > 0) {
            $("#modal-body").empty().append("<p>Do you want to delete the subcategory permanently?</p><div class=\"alert alert-warning d-flex align-items-center\" role=\"alert\"><svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" fill=\"currentColor\" class=\"bi bi-exclamation-triangle-fill flex-shrink-0 me-2\" viewBox=\"0 0 16 16\" role=\"img\" aria-label=\"Warning:\"><path d=\"M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z\"></path></svg><div>All other information related to this subcategory will be permanently deleted.</div></div>");
        }
        $("#confirmation").modal('show');
        confirmed(url);
    });
}

if(informationCount) {
    for (let i = 1; i <= informationCount; i++) {
        const selector = document.getElementById("delete-data-object-" + i);
        if(selector) {
            selector.addEventListener('click', function (event) {
                event.preventDefault();
                let url = this.getAttribute("data-href");
                $("#modal-body").empty().append("<p>Do you want to delete the information of the subcategory permanently?</p>");
                $("#confirmation").modal('show');
                confirmed(url);
            });
        }
    }
}

function showFormAlert(message) {
    if(formAlert) {
        const alertBtn = document.createElement('button');
        alertBtn.className = "btn-close";
        alertBtn.type = 'button';
        alertBtn.setAttribute("data-bs-dismiss", "alert");
        alertBtn.setAttribute("aria-label", "Close");

        const alertDiv = document.createElement('div');
        alertDiv.className = "alert alert-danger alert-dismissible fade show text-center";
        alertDiv.role = 'alert';
        alertDiv.textContent = message;
        alertDiv.appendChild(alertBtn);

        formAlert.appendChild(alertDiv);
        if(formAlert.classList.contains("d-none")) {
            formAlert.classList.remove("d-none");
        }
    }
}

if(form) {
    form.addEventListener('submit', function (event) {
        let invalidFlag = false;
        if(loadingSpinner) {
            loadingSpinner.classList.remove("d-none");
        }
        if(informationFieldsContainer) {
            let inputElements = informationFieldsContainer.querySelectorAll("input:not([type=\"hidden\"])");
            let isEmpty = Array.from(inputElements).map(input => input.value === '');
            let temp, flag = [], validFlag = [], isInvalid = false;
            for(let i = 0; i < isEmpty.length; i += 4) {
                temp = isEmpty.slice(i, i + 4);
                flag.push(temp.every(value => value) || temp.every(value => !value));
                validFlag.push(temp.every(value => !value));
            }
            for(let i = 0, j = 0; i < isEmpty.length && j < validFlag.length; i += 4, j++) {
                if(validFlag[j] && !isEmpty[i] && !isEmpty[i + 2] && inputElements[i].value === inputElements[i + 2].value) {
                    isInvalid = true;
                    break;
                }
            }
            if(!flag.every(value => value) || isInvalid) {
                event.preventDefault();
                invalidFlag = true;
                showFormAlert("Information field: Invalid input");
            }
        }
        if(form.id === "insert-disease-problem" || form.id === "update-disease-problem") {
            const nameInputElements = document.querySelectorAll('input[name^="name_"]');
            if(nameInputElements.length === 2) {
                if(nameInputElements[0].value === nameInputElements[1].value) {
                    event.preventDefault();
                    invalidFlag = true;
                    showFormAlert("Disease/Problem field: Invalid input");
                }
            } else {
                event.preventDefault();
                invalidFlag = true;
                showFormAlert("Disease/Problem field: Invalid form");
            }
        }
        if(invalidFlag && loadingSpinner) {
            loadingSpinner.classList.add("d-none");
        }
    });
}

if(selectCategory) {
    selectCategory.addEventListener('change', function() {
        const selectedCategory = this.options[this.selectedIndex];
        const href = selectedCategory.dataset.href;
        if(href) {
            window.location.href = href;
        }
    });
}

if(selectSubcategory) {
    selectSubcategory.addEventListener('change', function() {
        const selectedSubcategory = this.options[this.selectedIndex];
        const href = selectedSubcategory.dataset.href;
        if(href) {
            window.location.href = href;
        }
    });
}

function isImageSizeValid(image) {
    let startIndex = image.indexOf("base64,") + 7;
    imgBase64Str = image.substr(startIndex);
    imgFormat = image.split(';')[0].split('/')[1];
    let decoded = atob(imgBase64Str);

    return decoded.length < DATA_UPLOAD_MAX_MEMORY_SIZE;
}

function readImage(input) {
    if(input.files && input.files[0]) {
        let fileReader = new FileReader();

        fileReader.onload = function (event) {
            disableImageOverlay();
            let image = event.target.result;
            let valid = isImageSizeValid(image);

            if(!valid) {
                alert("Upload an image smaller than 10 MB");
                if(cancelEdit) {
                    cancelEdit.click();
                }
                return;
            }

            imgField.src = image;

            cropper = new Cropper(imgField, {
                viewMode: 3,
                aspectRatio: 1,
                movable: false,
                zoomable: false,
                rotatable: false,
                scalable: false,
                crop(event) {
                    croppingDetails = event.detail;
                },
            });
        };

        fileReader.readAsDataURL(input.files[0]);
    }
}

function showOverlay(event) {
    imgField.style.opacity = '0.3';
    imgEditBtn.classList.remove("d-none");
}

function hideOverlay(event) {
    imgField.style.opacity = '1';
    imgEditBtn.classList.add("d-none");
}

function clickImgInput(event) {
    imgInput.click();
}

function enableImageOverlay() {
    if(imgContainer) {
        imgContainer.addEventListener('mouseover', showOverlay);
        imgContainer.addEventListener('mouseout', hideOverlay);
    }

    if(imgEditBtn) {
        imgEditBtn.addEventListener('click', clickImgInput);
    }
}

function disableImageOverlay() {
    if(imgContainer) {
        imgContainer.removeEventListener('mouseover', showOverlay);
        imgContainer.removeEventListener('mouseout', hideOverlay);
    }

    if(imgEditBtn) {
        imgEditBtn.removeEventListener('click', clickImgInput);
    }

    imgField.style.opacity = '1';
    imgEditBtn.classList.add("d-none");
    imgCropOption.classList.remove("d-none");
    imgEditBtn.disabled = true;
    imgInput.disabled = true;

    if(confirmEdit) {
        confirmEdit.addEventListener('click', function (event) {
            let croppedCanvas = cropper.getCroppedCanvas();
            if (croppedCanvas) {
                imgField.src = croppedCanvas.toDataURL();
            }
            croppingDetailsInput.value = JSON.stringify(croppingDetails);
            cropper.destroy();
            imgCropOption.classList.add("d-none");
            imgEditBtn.disabled = false;
            imgInput.disabled = false;
            enableImageOverlay();
        });
    }

    if(cancelEdit) {
        cancelEdit.addEventListener('click', function (event) {
            if (cropper) {
                cropper.destroy();
            }
            imgCropOption.classList.add("d-none");
            imgEditBtn.disabled = false;
            imgInput.disabled = false;
            imgInput.value = '';
            imgField.src = defaultImgUrl;
            enableImageOverlay();
        });
    }
}

enableImageOverlay();
