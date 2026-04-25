(function () {
  const root = document.documentElement;
  const key = 'queryweave-theme';
  const toggle = document.getElementById('theme-toggle');

  const saved = localStorage.getItem(key);
  if (saved === 'light') {
    root.classList.remove('dark');
  } else {
    root.classList.add('dark');
  }

  if (toggle) {
    toggle.addEventListener('click', function () {
      const isDark = root.classList.toggle('dark');
      localStorage.setItem(key, isDark ? 'dark' : 'light');
    });
  }
})();
