const prevBtns = document.querySelectorAll(".btn-prev");
const nextBtns = document.querySelectorAll(".btn-next");
const progress = document.getElementById("progress");
const formSteps = document.querySelectorAll(".form-step");
const progressSteps = document.querySelectorAll(".progress-step");

let formStepsNum = parseInt(localStorage.getItem("formStep")) || 0;

// استرجاع البيانات المحفوظة من localStorage
const fields = ['databrith', 'gender', 'nationality', 'residence', 'city', 'language', 'file', 'image'];

fields.forEach(field => {
    const input = document.getElementById(field);
    if (input) {
        input.value = localStorage.getItem(field) || '';
    }
});

// تحديث نموذج الخطوات
updateFormSteps();

nextBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
        // حفظ البيانات في localStorage
        saveData();
        formStepsNum++;
        updateFormSteps();
        updateProgressbar();
    });
});

prevBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
        saveData();
        formStepsNum--;
        updateFormSteps();
        updateProgressbar();
    });
});

// تحديث نموذج الخطوات
function updateFormSteps() {
    formSteps.forEach((formStep, index) => {
        formStep.classList.remove("form-step-active");

        // إذا كانت الخطوة هي الثالثة، اجعلها غير نشطة
        if (index === 2 && formStepsNum < 2) {
            formStep.classList.remove("form-step-active");
        } else if (index === formStepsNum) {
            formStep.classList.add("form-step-active");
        }
    });

    // حفظ رقم الخطوة الحالي في localStorage
    localStorage.setItem("formStep", formStepsNum);
}

// حفظ البيانات في localStorage
function saveData() {
    const databrith = document.getElementById('databrith');
    const gender = document.querySelector('input[name="gender"]:checked');
    const nationality = document.getElementById('nationality');
    const residence = document.getElementById('residence');
    const city = document.getElementById('city');
    const language = document.getElementById('language');

    localStorage.setItem('databrith', databrith.value);
    localStorage.setItem('gender', gender ? gender.value : '');
    localStorage.setItem('nationality', nationality.value);
    localStorage.setItem('residence', residence.value);
    localStorage.setItem('city', city.value);
    localStorage.setItem('language', language.value);
}

// تحديث شريط التقدم
function updateProgressbar() {
    progressSteps.forEach((progressStep, idx) => {
        if (idx < formStepsNum + 1) {
            progressStep.classList.add("progress-step-active");
        } else {
            progressStep.classList.remove("progress-step-active");
        }
    });

    const progressActive = document.querySelectorAll(".progress-step-active");
    progress.style.width = ((progressActive.length - 1) / (progressSteps.length - 1)) * 100 + "%";
}

// التعامل مع ملفات السحب والإفلات
const dropAreaFile = document.getElementById('drop-area');
dropAreaFile.addEventListener('dragover', (event) => {
    event.preventDefault();
    dropAreaFile.style.backgroundColor = '#e9f5ff';
});

dropAreaFile.addEventListener('dragleave', () => {
    dropAreaFile.style.backgroundColor = '';
});

dropAreaFile.addEventListener('drop', (event) => {
    event.preventDefault();
    const files = event.dataTransfer.files;
    if (files.length) {
        handleFiles(files);
    }
});

dropAreaFile.addEventListener('click', () => {
    document.getElementById('fileElem').click();
});

function handleFiles(files) {
    const file = files[0];
    localStorage.setItem('file', file.name);
}

// التعامل مع الصور
const dropAreaImage = document.getElementById('drop-area-image');
dropAreaImage.addEventListener('dragover', (event) => {
    event.preventDefault();
    dropAreaImage.style.backgroundColor = '#e9f5ff';
});

dropAreaImage.addEventListener('dragleave', () => {
    dropAreaImage.style.backgroundColor = '';
});

dropAreaImage.addEventListener('drop', (event) => {
    event.preventDefault();
    const files = event.dataTransfer.files;
    if (files.length) {
        handleFile(files[0]);
    }
});

dropAreaImage.addEventListener('click', () => {
    document.getElementById('imageElem').click();
});

function handleFile(event) {
    const file = event.target.files[0];
    localStorage.setItem('image', file.name);
}
