import React, { useState } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import LoginPage from "./components/LoginPage";
import Register from "./components/Register";
import HomePage from "./components/HomePage";
import "./i18n";
import Profile from "./components/Profile.jsx";
import Market from "./components/Market.jsx";
import Schemes from "./components/Schemes.jsx";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Logic to handle login and set authentication status
  const handleLogin = (success) => {
    if (success) {
      setIsAuthenticated(true); // Set to true when login is successful
    }
  };

  return (
    <Router>
      <Routes>
        {/* Conditional routing */}
        <Route
          path="/"
          element={
            isAuthenticated ? <HomePage /> : <LoginPage onLogin={handleLogin} />
          }
        />
        <Route path="/register" element={<Register />} />
        <Route path="/schemes" element={<Schemes />} />
        <Route path="/market" element={<Market />} />
        <Route path="/Profile" element={<Profile />} />
        <Route
          path="/loginpage"
          element={<LoginPage onLogin={handleLogin} />}
        />
        <Route
          path="/home"
          element={isAuthenticated ? <HomePage /> : <Navigate to="/" />}
        />
      </Routes>
    </Router>
  );
}

export default App;
