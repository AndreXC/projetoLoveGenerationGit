document.addEventListener('DOMContentLoaded', function () {
    const prevButton = document.querySelector('.pagination-button2.prev');
    const nextButton = document.querySelector('.pagination-button2.next');
    const pages = document.querySelectorAll('.page'); // Selecionando as páginas pela classe
    let currentPageIndex = 0; // Página inicial

    // Função para exibir a página baseada no índice
    function showPage(index) {
        pages.forEach((page, i) => {
            if (i === index) {
                page.classList.add('active');
            } else {
                page.classList.remove('active');
            }
        });
    }

    prevButton.addEventListener('click', prevPage);
    nextButton.addEventListener('click', nextPage);

    // Função para exibir a página anterior
    function prevPage() {
        if (currentPageIndex > 0) {
            currentPageIndex--;
            showPage(currentPageIndex);
        }
    }

    // Função para exibir a próxima página
    function nextPage() {
        if (currentPageIndex < pages.length - 1) {
            currentPageIndex++;
            showPage(currentPageIndex);
        }
    }

    // Exibe a página inicial ao carregar
    showPage(currentPageIndex);
});
