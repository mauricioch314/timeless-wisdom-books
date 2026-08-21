document.querySelectorAll('[data-auto-gallery]').forEach((gallery)=>{
  const lang=gallery.dataset.autoGallery;
  const labels=(gallery.dataset.labels||'Image').split('|');
  for(let i=1;i<=12;i++){
    const button=document.createElement('button');
    const image=document.createElement('img');
    button.type='button'; button.setAttribute('aria-label',`${labels[0]} ${i}`);
    image.loading='lazy'; image.src=`assets/nonfiction/12-leyes/${lang}/${i}.jpg`; image.alt=`${labels[1]||labels[0]} ${i}`;
    button.appendChild(image); gallery.appendChild(button);
  }
});
document.querySelectorAll('[data-tesla-gallery]').forEach((gallery)=>{
  const lang=gallery.dataset.teslaGallery;
  const label=gallery.dataset.label||'Chapter';
  for(let i=1;i<=6;i++){
    const button=document.createElement('button'), image=document.createElement('img');
    button.type='button'; button.setAttribute('aria-label',`${label} ${i}`);
    image.loading='lazy'; image.src=`traducciones/biografia/tesla/${lang}/${i}.jpg`; image.alt=`${label} ${i}`;
    button.appendChild(image); gallery.appendChild(button);
  }
});
document.querySelectorAll('[data-gallery],[data-auto-gallery],[data-tesla-gallery]').forEach((gallery)=>{
  const modal=document.querySelector('.modal');
  const enlarged=modal?.querySelector('img');
  gallery.querySelectorAll('button').forEach((button)=>{
    button.addEventListener('click',()=>{
      if(!modal||!enlarged)return;
      const image=button.querySelector('img');
      enlarged.src=image.src;
      enlarged.alt=image.alt;
      modal.classList.add('open');
      document.body.style.overflow='hidden';
    });
  });
});
document.querySelectorAll('.modal').forEach((modal)=>{
  const close=()=>{
    modal.classList.remove('open');
    document.body.style.overflow='';
  };
  modal.addEventListener('click',(event)=>{if(event.target===modal||event.target.tagName==='BUTTON')close()});
  document.addEventListener('keydown',(event)=>{if(event.key==='Escape')close()});
});
