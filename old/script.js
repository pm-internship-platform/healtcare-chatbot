// Show current time
function updateTime() {
  const now = new Date();
  document.getElementById("time").innerText =
    "🕒 " + now.toLocaleTimeString();
}
setInterval(updateTime, 1000);

// Font size controls
let fontSize = 16;
function changeFontSize(action) {
  if (action === "increase") fontSize += 2;
  else if (action === "decrease") fontSize -= 2;
  else fontSize = 16;
  document.body.style.fontSize = fontSize + "px";
}

// Slider
let slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("slides");
  let dots = document.getElementsByClassName("dot");
  if (n > slides.length) { slideIndex = 1 }
  if (n < 1) { slideIndex = slides.length }
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex - 1].style.display = "block";
  dots[slideIndex - 1].className += " active";
}

  function googleTranslateElementInit() {
      new google.translate.TranslateElement({
        pageLanguage: 'en',
        includedLanguages: 'en,hi,ta,te',
        layout: google.translate.TranslateElement.InlineLayout.SIMPLE
      }, 'google_translate_element');
    }

    function changeLanguage(lang) {
      var selectField = document.querySelector(".goog-te-combo");
      if (selectField) {
        selectField.value = lang;
        selectField.dispatchEvent(new Event("change"));
      }
    }

// Auto slideshow
setInterval(() => plusSlides(1), 6000);
