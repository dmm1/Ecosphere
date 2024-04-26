/*
 * Copyright (c)  designbeat.at. All rights reserved.
 * This code is part of the Ecosphere project, available at https://github.com/dmm1/ecosphere
 * path: /static/js/ui/ecosphere-theme.js
 */
(function () {
  'use strict';

  var themeStorageKey = "tablerTheme";
  var defaultTheme = "light";

  // This function cycles to the next theme
  function cycleTheme() {
    var currentTheme = localStorage.getItem(themeStorageKey) || defaultTheme;
    var nextTheme;

    switch (currentTheme) {
      case 'light':
        nextTheme = 'dark';
        break;
      case 'dark':
        nextTheme = 'fancy';
        break;
      case 'fancy':
        nextTheme = 'light';
        break;
      default:
        nextTheme = 'light';
        break;
    }

    // Set the new theme in localStorage and on the document body
    localStorage.setItem(themeStorageKey, nextTheme);
    document.body.setAttribute("data-bs-theme", nextTheme);

    // Ensure the icons are updated
    updateIconVisibility(nextTheme);
  }

  // This function updates which icon is visible based on the current theme
  function updateIconVisibility(currentTheme) {
    var themes = ['light', 'dark', 'fancy'];
    themes.forEach(theme => {
      var icon = document.querySelector('.hide-theme-' + theme);
      if (icon) {
        icon.style.display = (theme === currentTheme) ? 'none' : 'inline-block';
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function() {
    var currentTheme = localStorage.getItem(themeStorageKey) || defaultTheme;
    document.body.setAttribute("data-bs-theme", currentTheme);
    updateIconVisibility(currentTheme);
  });

  window.cycleTheme = cycleTheme;
})();
