// Простой скрипт для навигации по изображениям
document.addEventListener('DOMContentLoaded', function () {
    const galleryItems = document.querySelectorAll('.gallery-item');
    const prevButton = document.getElementById('prev');
    const nextButton = document.getElementById('next');
    let currentIndex = 0;

    function showImage(index) {
        galleryItems.forEach((item, i) => {
            item.style.display = i === index ? 'block' : 'none';
        });
    }

    // Показываем все изображения для этого дизайна
    // Если хотите слайдер, раскомментируйте код ниже:
    /*
    showImage(currentIndex);
    
    nextButton.addEventListener('click', function() {
        currentIndex = (currentIndex + 1) % galleryItems.length;
        showImage(currentIndex);
    });
    
    prevButton.addEventListener('click', function() {
        currentIndex = (currentIndex - 1 + galleryItems.length) % galleryItems.length;
        showImage(currentIndex);
    });
    */
});