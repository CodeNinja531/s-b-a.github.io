import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

// Replace with your actual Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDFfl6qcOS-N7ErxULvMVJ5rrjet8VWHac",
  authDomain: "ict-sba-sports-day-helper.firebaseapp.com",
  projectId: "ict-sba-sports-day-helper",
  storageBucket: "ict-sba-sports-day-helper.firebasestorage.app",
  messagingSenderId: "992447656779",
  appId: "1:992447656779:web:57c3014598f34661086ece"
};

/**
 * Initializes the Firebase app and returns the auth object.
 * @returns {object} The Firebase auth object.
 */
function initializeFirebaseAndGetAuth() {
  const app = initializeApp(firebaseConfig);
  const auth = getAuth(app);
  return auth;
}

// Example usage (optional, can be removed or modified as needed)
// const firebaseAuth = initializeFirebaseAndGetAuth();
// console.log("Firebase Auth initialized:", firebaseAuth);