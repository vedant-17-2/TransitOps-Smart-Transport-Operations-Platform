/**
 * =============================================================
 * FILE: auth.js
 * PURPOSE: Handles all client‑side authentication logic for the
 *          TransitOps login page, including:
 *          – Form validation (email format, empty fields)
 *          – Credential matching against predefined users
 *          – Show / hide password toggle
 *          – Error & success message display
 *          – Saving user data to LocalStorage
 *          – Redirecting to the dashboard after login
 *          – Logout utility (clears stored session)
 *
 * FUNCTIONS:
 *   validateEmail(email)       → boolean
 *   validatePassword(password) → boolean
 *   authenticateUser(email, password) → object | null
 *   showError(message)
 *   showSuccess(message)
 *   saveUser(user)
 *   togglePassword()
 *   redirectUser()
 *   logout()
 * =============================================================
 */

/* =============================================================
   1. PREDEFINED USERS
   ---------------------------------------------------------
   An array of authorised user objects. Each object stores
   the user's display name, email, password, and role.
   In a production app these would live server‑side; here
   they are kept client‑side for demonstration purposes.
   ============================================================= */
const USERS = [
  {
    name: 'Admin User',
    email: 'admin@transitops.com',
    password: 'Admin@123',
    role: 'Admin'
  },
  {
    name: 'Dispatcher User',
    email: 'dispatcher@transitops.com',
    password: 'Dispatch@123',
    role: 'Dispatcher'
  },
  {
    name: 'Fleet Manager',
    email: 'fleet@transitops.com',
    password: 'Fleet@123',
    role: 'Fleet Manager'
  },
  {
    name: 'Safety Officer',
    email: 'safety@transitops.com',
    password: 'Safety@123',
    role: 'Safety Officer'
  }
];


/* =============================================================
   2. DOM REFERENCES
   ---------------------------------------------------------
   Cache references to frequently‑used DOM elements so we
   don't re‑query the document on every interaction.
   ============================================================= */
const loginForm       = document.getElementById('loginForm');
const emailInput      = document.getElementById('emailInput');
const passwordInput   = document.getElementById('passwordInput');
const toggleBtn       = document.getElementById('togglePasswordBtn');
const messageArea     = document.getElementById('messageArea');
const loginBtn        = document.getElementById('loginBtn');
const btnText         = document.getElementById('btnText');
const spinner         = document.getElementById('loadingSpinner');
const rememberMe      = document.getElementById('rememberMeCheckbox');


/* =============================================================
   3. VALIDATION FUNCTIONS
   ============================================================= */

/**
 * validateEmail – Checks whether the supplied string is a
 * structurally valid email address using a standard regex.
 *
 * @param  {string}  email – The email string to test.
 * @return {boolean} True if the format is valid.
 */
function validateEmail(email) {
  // Standard email regex pattern
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  return emailRegex.test(email.trim());
}

/**
 * validatePassword – Checks that the password is not empty
 * and meets a minimum length of 6 characters.
 *
 * @param  {string}  password – The password string to test.
 * @return {boolean} True if the password passes basic checks.
 */
function validatePassword(password) {
  // Password must exist and be at least 6 characters
  return password.trim().length >= 6;
}


/* =============================================================
   4. AUTHENTICATION FUNCTION
   ============================================================= */

/**
 * authenticateUser – Compares the provided email and password
 * against the USERS array. Matching is case‑insensitive for
 * the email but case‑sensitive for the password.
 *
 * @param  {string}       email    – User‑supplied email.
 * @param  {string}       password – User‑supplied password.
 * @return {object|null}  The matched user object, or null.
 */
function authenticateUser(email, password) {
  const normalised = email.trim().toLowerCase();

  // Find a user whose email and password both match
  const user = USERS.find(function (u) {
    return u.email.toLowerCase() === normalised && u.password === password;
  });

  return user || null;
}


/* =============================================================
   5. MESSAGE DISPLAY FUNCTIONS
   ============================================================= */

/**
 * showError – Renders a red error banner inside the message
 * area and applies the "input--error" style to the relevant
 * input fields.
 *
 * @param {string} message – The error text to display.
 */
function showError(message) {
  // Remove any previous state classes
  messageArea.classList.remove('message--success', 'message--visible');

  // Apply error styling and make it visible
  messageArea.textContent = message;
  messageArea.classList.add('message--error', 'message--visible');
}

/**
 * showSuccess – Renders a green success banner inside the
 * message area.
 *
 * @param {string} message – The success text to display.
 */
function showSuccess(message) {
  // Remove any previous state classes
  messageArea.classList.remove('message--error', 'message--visible');

  // Apply success styling and make it visible
  messageArea.textContent = message;
  messageArea.classList.add('message--success', 'message--visible');
}

/**
 * clearMessages – Hides the message area and removes all
 * error highlights from input fields.
 */
function clearMessages() {
  messageArea.classList.remove(
    'message--error',
    'message--success',
    'message--visible'
  );
  messageArea.textContent = '';

  emailInput.classList.remove('input--error');
  passwordInput.classList.remove('input--error');
}


/* =============================================================
   6. LOCAL STORAGE FUNCTIONS
   ============================================================= */

/**
 * saveUser – Persists the authenticated user's details into
 * LocalStorage so downstream pages (e.g. dashboard) can
 * identify the logged‑in user without another auth call.
 *
 * Stored keys:
 *   • userName      – Display name
 *   • userEmail     – Email address
 *   • userRole      – Role (Admin, Dispatcher, etc.)
 *   • loginTime     – ISO 8601 timestamp of login
 *   • isLoggedIn    – Boolean flag ("true")
 *
 * @param {object} user – The matched user object.
 */
function saveUser(user) {
  localStorage.setItem('userName',   user.name);
  localStorage.setItem('userEmail',  user.email);
  localStorage.setItem('userRole',   user.role);
  localStorage.setItem('loginTime',  new Date().toISOString());
  localStorage.setItem('isLoggedIn', 'true');
}

/**
 * logout – Removes all user‑related keys from LocalStorage,
 * effectively ending the session.
 */
function logout() {
  localStorage.removeItem('userName');
  localStorage.removeItem('userEmail');
  localStorage.removeItem('userRole');
  localStorage.removeItem('loginTime');
  localStorage.removeItem('isLoggedIn');
}


/* =============================================================
   7. SHOW / HIDE PASSWORD TOGGLE
   ============================================================= */

/**
 * togglePassword – Switches the password field between
 * type="password" (hidden) and type="text" (visible), and
 * swaps the eye icon accordingly.
 */
function togglePassword() {
  const isHidden = passwordInput.type === 'password';

  // Toggle input type
  passwordInput.type = isHidden ? 'text' : 'password';

  // Toggle icons
  const eyeOpen   = toggleBtn.querySelector('.eye-open');
  const eyeClosed = toggleBtn.querySelector('.eye-closed');

  eyeOpen.style.display   = isHidden ? 'none'  : 'block';
  eyeClosed.style.display = isHidden ? 'block' : 'none';

  // Update accessible label
  toggleBtn.setAttribute(
    'aria-label',
    isHidden ? 'Hide password' : 'Show password'
  );
}


/* =============================================================
   8. REDIRECT FUNCTION
   ============================================================= */

/**
 * redirectUser – Navigates the browser to the dashboard page
 * after a short delay (to let the user read the success
 * message).
 */
function redirectUser() {
  window.location.href = 'dashboard.html';
}


/* =============================================================
   9. LOADING STATE HELPERS
   ============================================================= */

/**
 * setLoading – Toggles the button's loading spinner and
 * disables / enables the form controls.
 *
 * @param {boolean} isLoading – True to enter loading state.
 */
function setLoading(isLoading) {
  if (isLoading) {
    loginBtn.classList.add('loading');
    loginBtn.disabled = true;
    btnText.textContent = 'Signing In…';
  } else {
    loginBtn.classList.remove('loading');
    loginBtn.disabled = false;
    btnText.textContent = 'Sign In';
  }
}


/* =============================================================
   10. FORM SUBMISSION HANDLER
   ---------------------------------------------------------
   Orchestrates the complete login flow:
     1. Clear previous messages.
     2. Read inputs.
     3. Validate email (empty → format).
     4. Validate password (empty → length).
     5. Show spinner & simulate network delay.
     6. Authenticate.
     7. On success → save user, show message, redirect.
     8. On failure → show error.
   ============================================================= */
loginForm.addEventListener('submit', function (event) {
  // Prevent native form submission
  event.preventDefault();

  // 1. Clear old messages and error highlights
  clearMessages();

  // 2. Capture input values
  const email    = emailInput.value;
  const password = passwordInput.value;

  /* ----------------------------------------------------------
     3. EMAIL VALIDATION
     ---------------------------------------------------------- */

  // 3a. Check for empty email
  if (!email.trim()) {
    showError('Please enter your email address.');
    emailInput.classList.add('input--error');
    emailInput.focus();
    return;
  }

  // 3b. Check for valid email format
  if (!validateEmail(email)) {
    showError('Please enter a valid email address.');
    emailInput.classList.add('input--error');
    emailInput.focus();
    return;
  }

  /* ----------------------------------------------------------
     4. PASSWORD VALIDATION
     ---------------------------------------------------------- */

  // 4a. Check for empty password
  if (!password.trim()) {
    showError('Please enter your password.');
    passwordInput.classList.add('input--error');
    passwordInput.focus();
    return;
  }

  // 4b. Check minimum password length
  if (!validatePassword(password)) {
    showError('Password must be at least 6 characters.');
    passwordInput.classList.add('input--error');
    passwordInput.focus();
    return;
  }

  /* ----------------------------------------------------------
     5. START LOADING STATE
     ---------------------------------------------------------- */
  setLoading(true);

  /* ----------------------------------------------------------
     6. SIMULATE NETWORK DELAY & AUTHENTICATE
     ---------------------------------------------------------
     A 1.2‑second timeout mimics a real API call, letting the
     user see the spinner and creating a realistic UX.
     ---------------------------------------------------------- */
  setTimeout(function () {

    // 6a. Attempt authentication
    const user = authenticateUser(email, password);

    if (user) {
      /* -------------------------------------------------------
         7. SUCCESS PATH
         ------------------------------------------------------- */

      // 7a. Save user data to LocalStorage
      saveUser(user);

      // 7b. Show success feedback
      showSuccess('Login successful! Redirecting…');

      // 7c. Brief pause for user to read message, then redirect
      setTimeout(function () {
        redirectUser();
      }, 1200);

    } else {
      /* -------------------------------------------------------
         8. FAILURE PATH
         ------------------------------------------------------- */

      // 8a. End loading state
      setLoading(false);

      // 8b. Show error message
      showError('Invalid email or password. Please try again.');
      emailInput.classList.add('input--error');
      passwordInput.classList.add('input--error');
    }
  }, 1200);
});


/* =============================================================
   11. EVENT LISTENERS
   ============================================================= */

// Toggle password visibility when the eye button is clicked
toggleBtn.addEventListener('click', togglePassword);

// Clear error highlights when the user starts typing
emailInput.addEventListener('input', function () {
  emailInput.classList.remove('input--error');
  clearMessages();
});

passwordInput.addEventListener('input', function () {
  passwordInput.classList.remove('input--error');
  clearMessages();
});


/* =============================================================
   12. AUTO‑FILL FROM REMEMBER ME (On Page Load)
   ---------------------------------------------------------
   If the user previously checked "Remember me", their email
   is restored from LocalStorage for convenience.
   ============================================================= */
(function initRememberMe() {
  const savedEmail = localStorage.getItem('rememberedEmail');
  if (savedEmail) {
    emailInput.value = savedEmail;
    rememberMe.checked = true;
  }
})();

// Save / remove the email when the checkbox changes
rememberMe.addEventListener('change', function () {
  if (rememberMe.checked) {
    localStorage.setItem('rememberedEmail', emailInput.value);
  } else {
    localStorage.removeItem('rememberedEmail');
  }
});

// Also update the stored email as the user types (if checked)
emailInput.addEventListener('input', function () {
  if (rememberMe.checked) {
    localStorage.setItem('rememberedEmail', emailInput.value);
  }
});
