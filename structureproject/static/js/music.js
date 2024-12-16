document.addEventListener('DOMContentLoaded', function() {
  // Adiciona a classe de animação ao buquê após 500ms
  setTimeout(() => {
      const bouquet = document.querySelector('.bouquet');
      if (bouquet) {
          bouquet.classList.add('active');

          // Simula um "pulso" ao chegar ao centro
          setTimeout(() => {
              bouquet.style.transform = 'scale(1)';
          }, 2000);
      }
  }, 500);


});

// Função para configurar e controlar a música
function setupMusic(musicFiles) {
  let currentIndex = Math.floor(Math.random() * musicFiles.length); // Seleciona música inicial aleatória
  const audio = new Audio(musicFiles[currentIndex]);
  const musicIcon = document.getElementById('musicIcon');

  // Define o evento de término para tocar a próxima música
  audio.addEventListener('ended', () => {
      currentIndex = (currentIndex + 1) % musicFiles.length; // Avança para a próxima música
      audio.src = musicFiles[currentIndex];
      audio.play();
  });

  if (musicIcon) {
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
}
