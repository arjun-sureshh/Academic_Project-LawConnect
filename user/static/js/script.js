function togglePasswordVisibility() {
  var passwordInputs = document.querySelectorAll('input[type="password"]');
  passwordInputs.forEach(function(input) {
    var icon = input.nextElementSibling;
    if (input.type === 'password') {
      input.type = 'text';
      icon.classList.remove('eye');
      icon.classList.add('eye-off');
    } else {
      input.type = 'password';
      icon.classList.remove('eye-off');
      icon.classList.add('eye');
    }
  });
}

document.querySelectorAll('.toggle-password').forEach(function(icon) {
  icon.addEventListener('click', togglePasswordVisibility);
});