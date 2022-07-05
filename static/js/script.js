/* This is the script that will detect if the user has clicked on the cookie consent banner, and will store a cookie
in the user's device once they click on "I Accept" (source: Godson Thomas's code from
https://github.com/Godsont/Cookie-Consent-Banner/blob/master/main.js ) */

const cookieContainer = document.querySelector(".cookie-container");
const cookieButton = document.querySelector(".cookie-btn");

cookieButton.addEventListener("click", () => {
  cookieContainer.classList.remove("active");
  localStorage.setItem("cookieBannerDisplayed", "true");
});

setTimeout(() => {
  if (!localStorage.getItem("cookieBannerDisplayed")) {
    cookieContainer.classList.add("active");
  }
}, 2000);