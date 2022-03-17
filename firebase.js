import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.8/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.6.8/firebase-analytics.js";
const firebaseConfig = {
    apiKey: "AIzaSyAQ2FU-OaJzklkEafaWYyMV6kwRzWf-_jU",
    authDomain: "sem4project-95dfc.firebaseapp.com",
    projectId: "sem4project-95dfc",
    storageBucket: "sem4project-95dfc.appspot.com",
    messagingSenderId: "1022736212561",
    appId: "1:1022736212561:web:963267d1f68daa1501ce70",
    measurementId: "G-Y89N81WJR6"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);
firebase.analytics();