document.addEventListener("DOMContentLoaded", function () {
    const quantityInput = document.getElementById("quantity");
    const minusBtn = document.querySelector(".quantity-btn.minus");
    const plusBtn = document.querySelector(".quantity-btn.plus");

    minusBtn.addEventListener("click", function () {
        let currentValue = parseInt(quantityInput.value);
        if (currentValue > 1) {
            quantityInput.value = currentValue - 1;
        }
    });

    plusBtn.addEventListener("click", function () {
        let currentValue = parseInt(quantityInput.value);
        quantityInput.value = currentValue + 1;
    });
    
});

document.addEventListener('DOMContentLoaded', function() {
    var photoInput = document.getElementById('photoInput');
    var photoPreview = document.getElementById('photoPreview');

    // Display default image on page load
    photoPreview.style.display = 'block';


    photoInput.addEventListener('change', function() {
        var reader = new FileReader();
        
        reader.onload = function(e) {
            photoPreview.src = e.target.result;
            photoPreview.style.display = 'block'; // Show the image
            
            // Apply CSS styles
            photoPreview.style.height = '100%';
            photoPreview.style.width = '100%';
            photoPreview.style.paddingTop = '10%';
            photoPreview.style.borderRadius = '10px';
            photoInput.style.display = 'none';
        }
        
        reader.readAsDataURL(this.files[0]);
    });
});
