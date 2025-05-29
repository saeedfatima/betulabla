<script>
  document.addEventListener('DOMContentLoaded', function () {
    const avatarDropdown = document.querySelector('.dropdown');

    if (avatarDropdown) {
      avatarDropdown.addEventListener('mouseenter', function () {
        const menu = avatarDropdown.querySelector('.dropdown-menu');
        new bootstrap.Dropdown(avatarDropdown.querySelector('[data-bs-toggle="dropdown"]')).show();
      });

      avatarDropdown.addEventListener('mouseleave', function () {
        const menu = avatarDropdown.querySelector('.dropdown-menu');
        new bootstrap.Dropdown(avatarDropdown.querySelector('[data-bs-toggle="dropdown"]')).hide();
      });
    }
  });
</script>
