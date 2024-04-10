const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const btnPopup = document.querySelector('.btnlogin-popup');
const iconClose = document.querySelector('.icon-close');
const logoutLink = document.querySelector('.logout-link');

// Funzione per controllare se la sessione è attiva
function isSessionActive() {
    return logoutLink.style.display === 'block';
}

// Aggiungi il gestore di eventi per il clic sul link di registrazione
registerLink.addEventListener('click', () => {
  wrapper.classList.add('active');
  console.log("Register link clicked");
});

// Aggiungi il gestore di eventi per il clic sul link di accesso
loginLink.addEventListener('click', () => {
  wrapper.classList.remove('active');
  console.log("Login link clicked");
});

// Aggiungi il gestore di eventi per il clic sul pulsante di apertura del popup
btnPopup.addEventListener('click', () => {
  wrapper.classList.add('active-popup');
  console.log("Popup button clicked");
});

// Aggiungi il gestore di eventi per il clic sull'icona di chiusura del popup
iconClose.addEventListener('click', () => {
  wrapper.classList.remove('active-popup');
  console.log("Close icon clicked");
});

// Verifica se la sessione è attiva al caricamento della pagina
window.addEventListener('load', () => {
    if (isSessionActive()) {
        btnPopup.style.display = 'none'; // Nascondi il pulsante di login
    } else {
        logoutLink.style.display = 'none'; // Nascondi il link di logout
    }
});
