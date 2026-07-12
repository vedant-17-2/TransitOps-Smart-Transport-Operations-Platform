# TransitOps – Smart Transport Operations Platform

## Login Page

A modern, responsive, professional login page built with **HTML5**, **CSS3**, and **Vanilla JavaScript**. No frameworks or libraries are used.

---

## 📁 Folder Structure

```
project/
│
├── login.html          → Main login page (entry point)
├── css/
│   └── style.css       → All visual styling
├── js/
│   └── auth.js         → Authentication & validation logic
├── images/
│   └── logo.png        → Company logo
└── README.md           → Project documentation (this file)
```

---

## 🚀 Features

| Feature                | Description                                                    |
| ---------------------- | -------------------------------------------------------------- |
| Company Logo           | Displayed at the top of the login card                         |
| Project Title          | "TransitOps" rendered in Outfit font                           |
| Welcome Message        | Friendly prompt for returning users                            |
| Email Input            | With envelope icon and validation                              |
| Password Input         | With lock icon and show/hide toggle                            |
| Show/Hide Password     | Eye icon toggles between masked and plain text                 |
| Remember Me            | Custom checkbox that persists the email in LocalStorage        |
| Forgot Password        | Dummy link (non-functional placeholder)                        |
| Login Button           | Gradient button with shimmer hover effect                      |
| Loading Spinner        | CSS-only spinner inside the button during authentication       |
| Error Messages         | Red banner for validation and credential errors                |
| Success Message        | Green banner on successful authentication                      |
| Footer                 | Copyright branding at the bottom of the card                   |
| Animated Background    | Floating translucent circles behind the card                   |
| Responsive Design      | Optimised for desktop, tablet, and mobile screens              |

---

## 🔑 Test Credentials

| Role            | Email                         | Password       |
| --------------- | ----------------------------- | -------------- |
| Admin           | admin@transitops.com          | Admin@123      |
| Dispatcher      | dispatcher@transitops.com     | Dispatch@123   |
| Fleet Manager   | fleet@transitops.com          | Fleet@123      |
| Safety Officer  | safety@transitops.com         | Safety@123     |

---

## 🔐 Authentication Flow

1. User enters email and password.
2. Client‑side validation checks for empty fields and email format.
3. Credentials are matched against the four predefined users.
4. **On failure** → A red error message is displayed.
5. **On success** → User data is saved to LocalStorage and the browser redirects to `dashboard.html`.

### LocalStorage Keys (set on login)

| Key           | Value                          |
| ------------- | ------------------------------ |
| `userName`    | Display name of the user       |
| `userEmail`   | Email address                  |
| `userRole`    | Role (Admin, Dispatcher, etc.) |
| `loginTime`   | ISO 8601 timestamp             |
| `isLoggedIn`  | `"true"`                       |

---

## 🧩 JavaScript Functions

| Function              | Purpose                                              |
| --------------------- | ---------------------------------------------------- |
| `validateEmail()`     | Tests email format with a regex                      |
| `validatePassword()`  | Checks password is non-empty and ≥ 6 chars           |
| `authenticateUser()`  | Matches credentials against the USERS array          |
| `showError()`         | Displays a red error banner                          |
| `showSuccess()`       | Displays a green success banner                      |
| `saveUser()`          | Persists user data to LocalStorage                   |
| `togglePassword()`    | Toggles password visibility                          |
| `redirectUser()`      | Navigates to `dashboard.html`                        |
| `logout()`            | Clears all user data from LocalStorage               |

---

## 🎨 CSS Highlights

- **CSS Custom Properties** for a centralised design‑token system
- **Flexbox** layout for centering and form structure
- **Gradient background** (`135deg` blue gradient)
- **Box shadows** (sm / md / lg / glow variants)
- **Border radius** (8px–50px tokens)
- **Hover effects** (button shimmer, logo scale, input focus glow)
- **Animations** (card entrance, background shape float, spinner)
- **Media queries** for tablets (≤ 768px), mobile (≤ 480px), and small screens (≤ 360px)
- **Reduced‑motion** media query for accessibility

---

## 📱 Responsive Breakpoints

| Breakpoint | Target       |
| ---------- | ------------ |
| ≤ 768px    | Tablets      |
| ≤ 480px    | Mobile       |
| ≤ 360px    | Small Mobile |

---

## 🛠 How to Run

1. Open the `project/` folder.
2. Open `login.html` in any modern browser.
3. Use one of the test credentials above to log in.

> **Note:** `dashboard.html` is not included in this project. After a successful login the browser will attempt to redirect to `dashboard.html`. Create that file separately to complete the flow.

---

## 📝 Technologies Used

- HTML5
- CSS3 (Flexbox, Custom Properties, Animations, Media Queries)
- Vanilla JavaScript (ES6+)
- Google Fonts (Inter, Outfit)

---

## 📄 License

© 2026 TransitOps – Smart Transport Operations Platform. All rights reserved.
