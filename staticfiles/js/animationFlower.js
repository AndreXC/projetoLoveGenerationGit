window.onload = () => {
    setTimeout(() => {
      const bouquet = document.querySelector('.bouquet');
      bouquet.classList.add('active');
  
      // Simula um "pulso" ao chegar ao centro
      setTimeout(() => {
        bouquet.style.transform = 'scale(1)';
      }, 2000);
    }, 500);
  
  }
  
  
  