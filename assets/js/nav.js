(function () {
  function insertNav() {
    var nav = document.createElement('nav');
    nav.innerHTML =
      '<div class="nav-container">' +
        '<a class="nav-logo" href="index.html">Glambient</a>' +
        '<div class="nav-links">' +
          '<ul class="menu-left">' +
            '<li><a href="index.html">Home</a></li>' +
            '<li><a href="about.html">About</a></li>' +
            '<li><a href="gallery.html">Gallery</a></li>' +
          '</ul>' +
          '<ul class="menu-right">' +
            '<li><a href="video.html">Videos</a></li>' +
            '<li><a href="packages.html">Packages</a></li>' +
            '<li><a href="contact.html">Contact</a></li>' +
          '</ul>' +
        '</div>' +
      '</div>';
    document.body.insertBefore(nav, document.body.firstChild);
  }

  if (document.body) {
    insertNav();
  } else {
    document.addEventListener('DOMContentLoaded', insertNav);
  }
}());
