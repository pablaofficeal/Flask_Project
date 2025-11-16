// Функция для показа/скрытия пароля
function setupPasswordToggle(passwordId, toggleId) {
    const passwordInput = document.getElementById(passwordId);
    const toggleButton = document.getElementById(toggleId);

    toggleButton.addEventListener('click', function () {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);

        // Меняем иконку
        const icon = this.querySelector('i');
        if (type === 'password') {
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        } else {
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        }
    });
}

// Настройка переключателей пароля
setupPasswordToggle('password', 'togglePassword');

// Обработка формы - форма отправляется автоматически на сервер

document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Предотвращаем стандартное поведение формы

    const formData = new FormData(this);
});