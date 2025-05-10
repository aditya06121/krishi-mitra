import React, { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom"; // Import useNavigate from React Router

export default function LoginPage({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate(); // Initialize the navigate function

  // In LoginPage.jsx
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await axios.post("http://localhost:3000/login", {
        email,
        password,
      });

      console.log("Login successful:", response.data);
      setLoading(false);
      localStorage.setItem("user", JSON.stringify(response.data.user));

      // Call the onLogin prop with true to update authentication state
      onLogin(true);

      navigate("/home", { state: { userData: response.data.user } });
    } catch (err) {
      setLoading(false);
      if (err.response) {
        setError(err.response.data.message);
      } else {
        setError("Something went wrong. Please try again later.");
      }
    }
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center bg-cover bg-center"
      style={{ backgroundImage: "url('./farm.jpg')" }}
    >
      <div className="bg-white/10 backdrop-blur-md rounded-2xl shadow-2xl p-8 max-w-md w-full text-white border border-white/20">
        <h2 className="text-3xl font-bold mb-6 text-center">Login</h2>

        <form className="space-y-5" onSubmit={handleSubmit}>
          <div>
            <label className="block text-sm font-medium mb-1" htmlFor="email">
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-2 rounded-lg bg-white/20 placeholder-white text-white focus:outline-none focus:ring-2 focus:ring-white"
            />
          </div>

          <div>
            <label
              className="block text-sm font-medium mb-1"
              htmlFor="password"
            >
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-2 rounded-lg bg-white/20 placeholder-white text-white focus:outline-none focus:ring-2 focus:ring-white"
            />
          </div>

          {error && <p className="text-red-400 text-sm">{error}</p>}

          <button
            type="submit"
            className="w-full bg-white text-blue-600 font-semibold py-2 rounded-lg hover:bg-blue-100 transition duration-200"
            disabled={loading}
          >
            {loading ? "Signing In..." : "Sign In"}
          </button>
        </form>

        <div className="mt-6 text-center text-sm">
          <p>
            Don't have an account?{" "}
            <Link
              to="/register"
              className="underline text-white hover:text-gray-200"
            >
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
