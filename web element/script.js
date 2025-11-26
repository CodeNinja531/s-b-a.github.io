let userEmail = '';
let googleClientId = '992447656779-odg7cr1em2rct7p4oe2e4bistsdihisc.apps.googleusercontent.com'; // google clident id
let visible = false;

// --------------------------------------------loging in with google account--------------------------------------------
// copied from google sites
function initializeGoogleSignIn() {
    google.accounts.id.initialize({
        client_id: googleClientId,
        callback: CredentialResponse,
        auto_select: false,
        prompt_parent_id: 'g_id_signin'
    });
    google.accounts.id.renderButton(
        document.querySelector('.auth-button'),
        { theme: "outline", size: "large", type: "standard", text: "signin_with", shape: "rectangular" }
    );
}

// standard decoding function for JSON
function parseJwt(token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
        atob(base64)
            .split('')
            .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
            .join('')
    );
    return JSON.parse(jsonPayload);
}

function CredentialResponse(response) {
    const token = response.credential;
    const user = parseJwt(token);

    // Store user info
    localStorage.setItem('loggedInUser', JSON.stringify({ email: user.email, name: user.name, picture: user.picture }));

    // Prompt for gender if not already stored
    if (!localStorage.getItem('userGender')) {
        const gender = prompt("Please enter your gender (e.g., Male, Female, Other):");
        if (gender) {
            localStorage.setItem('userGender', gender);
        }
    }

    updateLoginUI();
    
    fetch('http://localhost:3000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: user.email })
    })
        .then(res => res.json())
        .then(data => {
            console.log("Backend login successful:", data);
        })
        .catch(err => console.error('Backend login failed:', err));
}

// for the login button
function updateLoginUI() {
    const authButtonDiv = document.querySelector('.auth-button');
    authButtonDiv.innerHTML = '';
    authButtonDiv.onclick = null;

    const loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));
    if (loggedInUser) {
        // pfp
        const profileImage = document.createElement('img');
        profileImage.src = loggedInUser.picture;
        profileImage.alt = 'Profile Picture';
        profileImage.style.width = '30px';
        profileImage.style.height = '30px';
        profileImage.style.borderRadius = '50%';

        // name
        const displayNameSpan = document.createElement('span');
        displayNameSpan.textContent = loggedInUser.name;

        // logout-button
        const logoutButton = document.createElement('button');
        logoutButton.classList.add('logout-button');
        logoutButton.onclick = logout;
        authButtonDiv.appendChild(profileImage);
        authButtonDiv.appendChild(displayNameSpan);
        authButtonDiv.onclick = toggleLogoutButton;
        authButtonDiv.parentNode.insertBefore(logoutButton, authButtonDiv.nextSibling);
        visible = false;
    } else {
        // google official sign-in button
        google.accounts.id.renderButton(
            authButtonDiv,
            { theme: "outline", size: "large", type: "standard", text: "signin_with", shape: "rectangular" }
        );
        authButtonDiv.innerHTML = '';
        authButtonDiv.classList.add('auth-button');
        authButtonDiv.onclick = null;
        const existingLogoutButton = document.querySelector('.logout-button');
        if (existingLogoutButton) {
            existingLogoutButton.remove();
        }
        visible = false;
    }
}

// --------------------------------------------loging in with google account--------------------------------------------

function toggleLogoutButton() {
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.style.display = visible ? 'none' : 'block';
        visible = !visible;
    }
}

function logout() {
    localStorage.removeItem('loggedInUser');
    updateLoginUI();
    location.reload();
}


function getUserInfo() {
    const loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));
    if (loggedInUser && loggedInUser.name) {
        return { displayName: loggedInUser.name };
    } else {
        return { displayName: null };
    }
}

function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const main = document.querySelector('main');
    sidebar.classList.toggle('hidden');
    main.classList.toggle('collapsed');
}

document.addEventListener('DOMContentLoaded', () => {
    fetch("menu.html")
    .then(response => response.text())
    .then(html => {
        document.getElementById("menu-container").innerHTML = html;
    });

    if (typeof google !== 'undefined' && google.accounts && google.accounts.id) {
        initializeGoogleSignIn();
        updateLoginUI();
    }
});
