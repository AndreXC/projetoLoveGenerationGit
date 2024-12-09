 // Adiciona a classe de animação ao buquê após 500ms
 window.onload = () => {
    setTimeout(() => {
      const bouquet = document.querySelector('.bouquet');
      bouquet.classList.add('active');

      // Simula um "pulso" ao chegar ao centro
      setTimeout(() => {
        bouquet.style.transform = 'scale(1)';
      }, 2000);
    }, 500);

    // Configuração do controle de música
    setupMusic('music.mp3');
  };

  // Função para configurar e controlar a música
  function setupMusic(audioFile) {
    const audio = new Audio(audioFile);
    const musicIcon = document.getElementById('musicIcon');

    musicIcon.addEventListener('click', () => {
      if (audio.paused) {
        audio.play();
        musicIcon.classList.remove('paused');
        musicIcon.classList.add('playing');
      } else {
        audio.pause();
        musicIcon.classList.remove('playing');
        musicIcon.classList.add('paused');
      }
    });
  }