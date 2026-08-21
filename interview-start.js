(() => {
  const link = [...document.querySelectorAll('.interview-card')].find(card => card.href.includes('7tvandalucia.es'));
  if (!link) return;
  const notes = {
    es: 'La entrevista comienza en el minuto 9:48',
    en: 'The interview begins at 9:48',
    fr: 'L’entretien commence à 9 min 48 s',
    it: 'L’intervista inizia al minuto 9:48',
    pt: 'A entrevista começa aos 9:48',
    de: 'Das Interview beginnt bei Minute 9:48'
  };
  const lang = document.documentElement.lang.slice(0, 2);
  const note = document.createElement('p');
  note.className = 'interview-start-note';
  note.textContent = notes[lang] || notes.es;
  link.querySelector('.interview-info')?.appendChild(note);
  const style = document.createElement('style');
  style.textContent = '.interview-start-note{margin-top:.45rem;color:var(--color-accent);font-size:12px;font-style:italic;letter-spacing:.04em}';
  document.head.appendChild(style);
})();
