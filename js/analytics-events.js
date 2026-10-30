(() => {
  'use strict';
  // Sends ToolPinch tool-usage events to Google Analytics 4 (G-8WM8MS9X9Y).
  // Events: calculator_use (once per page view), calendar_download, csv_download, print_page.
  const send = (name, params) => {
    if (typeof window.gtag !== 'function') return;
    window.gtag('event', name, Object.assign({ tool_page: location.pathname }, params || {}));
  };
  let used = false;
  const markUsed = how => {
    if (used) return;
    used = true;
    send('calculator_use', { interaction: how });
  };

  document.addEventListener('click', e => {
    const el = e.target.closest('button, a');
    if (!el) return;
    if (el.id === 'payIcs') return send('calendar_download', { file_type: 'ics' });
    if (el.id === 'payCsv' || (el.tagName === 'A' && /\.csv($|\?)/.test(el.getAttribute('href') || ''))) return send('csv_download', { file_type: 'csv' });
    if (el.id === 'payPrint') return send('print_page');
    if (el.matches('[data-action], .mc-calculator button, .mc-calculator [role="button"]')) markUsed('button');
  }, true);

  // Calculators that update as you type count as used on the first real edit.
  document.addEventListener('change', e => {
    if (e.target.closest('.mc-calculator, .mc-smart-calculator')) markUsed('input');
  }, true);
})();
