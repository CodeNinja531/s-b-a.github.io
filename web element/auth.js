let userEmail = '';
let googleClientId = '992447656779-odg7cr1em2rct7p4oe2e4bistsdihisc.apps.googleusercontent.com'; // REMEMBER TO REPLACE THIS!
let isLogoutVisible = false; // Track the visibility of the actual logout button

function initializeGoogleSignIn() {
    google.accounts.id.initialize({
        client_id: googleClientId,
        callback: handleCredentialResponse,
        auto_select: false,
        prompt_parent_id: 'g_id_signin'
    });
    google.accounts.id.renderButton(
        document.querySelector('.auth-button'),
        { theme: "outline", size: "large", type: "standard", text: "signin_with", shape: "rectangular" }
    );
    console.log("initializeGoogleSignIn called");
}

function handleCredentialResponse(response) {
    const token = response.credential;
    const user = parseJwt(token); // Decode the JWT to get user info

    // Store user info in localStorage
    localStorage.setItem('loggedInUser', JSON.stringify({ email: user.email, name: user.name, picture: user.picture }));
    console.log("loggedInUser stored in localStorage:", localStorage.getItem('loggedInUser'));

    // Prompt for gender if not already stored
    if (!localStorage.getItem('userGender')) {
        const gender = prompt("Please enter your gender (e.g., Male, Female, Other):");
        if (gender) {
            localStorage.setItem('userGender', gender);
        }
    }

    updateLoginUI(); // Update UI based on local storage

    // Send login request to the backend (optional, depending on your needs)
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

function updateLoginUI() {
    const authButtonDiv = document.querySelector('.auth-button');
    authButtonDiv.innerHTML = ''; // Clear existing content
    authButtonDiv.onclick = null; // Remove any existing onclick handler

    const loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));
    const userGender = localStorage.getItem('userGender');

    console.log("updateLoginUI called");
    console.log("loggedInUser from localStorage:", loggedInUser);

    if (loggedInUser) {
        console.log("User is logged in - updating UI to show name/icon");
        authButtonDiv.style.display = 'flex';
        authButtonDiv.style.flexDirection = 'row'; // Ensure horizontal alignment
        authButtonDiv.style.alignItems = 'center';
        authButtonDiv.style.padding = '8px 12px';
        authButtonDiv.style.backgroundColor = '#2c3e50';
        authButtonDiv.style.color = 'white';
        authButtonDiv.style.borderRadius = '5px';
        authButtonDiv.style.cursor = 'pointer';
        authButtonDiv.style.gap = '10px'; // Space between items

        // Profile Picture
        const profileImage = document.createElement('img');
        profileImage.src = loggedInUser.picture;
        profileImage.alt = 'Profile Picture';
        profileImage.style.width = '30px';
        profileImage.style.height = '30px';
        profileImage.style.borderRadius = '50%';

        // User Display Name
        const displayNameSpan = document.createElement('span');
        displayNameSpan.textContent = loggedInUser.name;

        // Display gender if available
        if (userGender) {
            const genderSpan = document.createElement('span');
            genderSpan.textContent = `Gender: ${userGender}`;
            authButtonDiv.appendChild(genderSpan);
        }

        // Logout Button
        const logoutButton = document.createElement('button');
        logoutButton.id = 'actual-logout-button';
        logoutButton.textContent = 'Logout';
        logoutButton.style.backgroundColor = '#dc3545';
        logoutButton.style.color = 'white';
        logoutButton.style.border = 'none';
        logoutButton.style.padding = '8px 12px';
        logoutButton.style.borderRadius = '5px';
        logoutButton.style.cursor = 'pointer';
        logoutButton.style.marginLeft = '10px'; // Add space to the left
        logoutButton.style.display = 'none'; // Initially hidden
        logoutButton.style.alignSelf = 'center'; // Ensure vertical alignment
        logoutButton.onclick = logout; // Attach logout function

        authButtonDiv.appendChild(profileImage);
        authButtonDiv.appendChild(displayNameSpan);
        authButtonDiv.onclick = toggleLogoutButton; // Attach toggle to the container

        // Insert the logout button after the container
        authButtonDiv.parentNode.insertBefore(logoutButton, authButtonDiv.nextSibling);
        isLogoutVisible = false; // Initialize state
    } else {
        console.log("User is NOT logged in - rendering sign-in button");
        google.accounts.id.renderButton(
            authButtonDiv,
            { theme: "outline", size: "large", type: "standard", text: "signin_with", shape: "rectangular" }
        );
        authButtonDiv.style.display = 'inline-block';
        authButtonDiv.style.flexDirection = '';
        authButtonDiv.style.alignItems = '';
        authButtonDiv.style.padding = '';
        authButtonDiv.style.backgroundColor = '';
        authButtonDiv.style.color = '';
        authButtonDiv.style.borderRadius = '';
        authButtonDiv.style.cursor = 'pointer';
        authButtonDiv.style.gap = '';
        authButtonDiv.onclick = null; // Ensure no toggle action when logged out

        // Ensure any existing logout button is removed
        const existingLogoutButton = document.getElementById('actual-logout-button');
        if (existingLogoutButton) {
            existingLogoutButton.remove();
        }
        isLogoutVisible = false;
    }
}

function toggleLogoutButton() {
    const logoutButton = document.getElementById('actual-logout-button');
    if (logoutButton) {
        logoutButton.style.display = isLogoutVisible ? 'none' : 'block';
        isLogoutVisible = !isLogoutVisible;
    }
}

function logout() {
    console.log("logout called"); // Check if this is logged
    localStorage.removeItem('loggedInUser'); // Clear local storage on logout
    updateLoginUI(); // Update the UI to show the sign-in button again
    location.reload(); // Simple page reload for now
}

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

function getUserInfo() {
    const loggedInUser = JSON.parse(localStorage.getItem('loggedInUser'));
    if (loggedInUser && loggedInUser.name) {
        return { displayName: loggedInUser.name };
    } else {
        console.error("No logged-in user found or user name is missing.");
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
    console.log("DOMContentLoaded event fired");
    if (typeof google !== 'undefined' && google.accounts && google.accounts.id) {
        initializeGoogleSignIn();
        updateLoginUI(); // Initial call to set up the button or user info based on local storage
    } else {
        console.error("Google Identity Services library not loaded properly.");
        // Optionally display a message to the user about the login failure
    }
});
