// FUNCTION DROPDOWN
document.addEventListener('DOMContentLoaded', function () {
    const profileLink = document.querySelector('.profile');
    const dropdown = document.querySelector('.dropdown-content');

    // Menampilkan atau menyembunyikan dropdown saat profil di-klik
    profileLink.addEventListener('click', function (event) {
        event.preventDefault(); // Mencegah tindakan default link
        dropdown.classList.toggle('show');
    });

    // Menutup dropdown saat user mengklik di luar dropdown
    document.addEventListener('click', function (event) {
        if (!dropdown.contains(event.target) && !profileLink.contains(event.target)) {
            dropdown.classList.remove('show');
        }
    });
});

