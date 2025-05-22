// window.onload = function() {
//     document.getElementById("fullName").value = localStorage.getItem("fullName") || "";
//     document.getElementById("email").value = localStorage.getItem("email") || "";
//     document.getElementById("password").value = "";
//     document.getElementById("confirmPassword").value = "";
//     updateSubmitButton();
// };

// function checkPasswordStrength(password) {
//     const passwordStrengthError = document.getElementById("passwordError");
//     const strengthCriteria = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$/;

//     if (!password) {
//         passwordStrengthError.textContent = "الحقل مطلوب";
//         return false;
//     } else if (strengthCriteria.test(password)) {
//         passwordStrengthError.textContent = "كلمة مرور قوية";
//         return true;
//     } else {
//         passwordStrengthError.textContent = "يجب أن تحتوي كلمة المرور على حروف كبيرة وصغيرة وأرقام، وطول 8 أحرف على الأقل";
//         return false;
//     }
// }

// function validateForm() {
//     let fullName = document.getElementById("fullName").value;
//     let email = document.getElementById("email").value;
//     let password = document.getElementById("password").value;
//     let confirmPassword = document.getElementById("confirmPassword").value;

//     let nameError = document.getElementById("nameError");
//     let emailError = document.getElementById("emailError");
//     let passwordError = document.getElementById("passwordError");
//     let confirmPasswordError = document.getElementById("confirmPasswordError");

//     nameError.textContent = emailError.textContent = passwordError.textContent = confirmPasswordError.textContent = "";
//     let valid = true;

//     if (!fullName) {
//         nameError.textContent = "الحقل مطلوب";
//         valid = false;
//     } else if (/^\d+$/.test(fullName)) {
//         nameError.textContent = "الاسم لا يمكن أن يكون أرقامًا فقط";
//         valid = false;
//     } else if (/[^A-Za-zأ-ي\s]/.test(fullName)) {
//         nameError.textContent = "يرجى إدخال اسم صحيح بدون أرقام أو رموز";
//         valid = false;
//     }

//     if (!email) {
//         emailError.textContent = "الحقل مطلوب";
//         valid = false;
//     } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
//         emailError.textContent = "يرجى إدخال بريد إلكتروني صحيح";
//         valid = false;
//     }

//     if (!password) {
//         passwordError.textContent = "الحقل مطلوب";
//         valid = false;
//     } else {
//         valid = valid && checkPasswordStrength(password);
//     }

//     if (confirmPassword !== password) {
//         confirmPasswordError.textContent = "كلمة المرور غير متطابقة";
//         valid = false;
//     }

//     updateSubmitButton();
//     return valid;
// }

// function updateSubmitButton() {
//     let submitButton = document.querySelector("button[type='submit']");
//     submitButton.disabled = !validateForm();
// }

// document.querySelector("form").addEventListener("submit", function(event) {
//     if (!validateForm()) {
//         event.preventDefault();
//     }

//     const formData = new FormData(document.getElementById('registrationForm'));

//     fetch("/account/register/", {
//         method: "POST",
//         body: formData,
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.success) {
//             alert("تم التسجيل بنجاح");
//         } else {
//             alert("حدث خطأ أثناء التسجيل");
//         }
//     })
//     .catch(error => {
//         console.error("حدث خطأ في إرسال البيانات:", error);
//     });

//     localStorage.setItem("fullName", document.getElementById("fullName").value);
//     localStorage.setItem("email", document.getElementById("email").value);
// });

// document.querySelectorAll(".form-control").forEach(input => {
//     input.addEventListener("input", function() {
//         validateForm();
//     });
// });
