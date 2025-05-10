import React, { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";

export default function RegisterPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    gender: "",
    password: "",
    confirmPassword: "",
    isFarmer: false,
  });

  const handleChange = (e) => {
    const { id, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [id]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    const registrationData = {
      name: formData.name,
      email: formData.email,
      password: formData.password,
      phone: formData.phone,
      occupation: formData.isFarmer ? "farmer" : "customer",
      gender: formData.gender === "female", // true if female, false otherwise
    };

    try {
      const response = await axios.post(
        "http://localhost:3000/register/",
        registrationData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (response.status === 201 || response.status === 200) {
        alert("Registration successful!");
        navigate("/loginpage");
      }
    } catch (error) {
      console.error("Registration failed:", error);
      alert("Registration failed. Please try again.");
    }
  };

  return (
    <div
      className="min-h-screen bg-cover bg-center flex items-center justify-center p-4"
      style={{ backgroundImage: "url('/farmer.jpg')" }}
    >
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-8 max-w-md w-full text-black border border-black/20">
        <h2 className="text-3xl font-bold mb-6 text-center">Register</h2>

        <form className="space-y-5" onSubmit={handleSubmit}>
          <div>
            <label className="block text-sm font-medium mb-1" htmlFor="name">
              Full Name
            </label>
            <input
              id="name"
              type="text"
              value={formData.name}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 rounded-lg bg-white/10 text-black border border-black focus:outline-none focus:ring-2 focus:ring-black"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1" htmlFor="email">
              Email
            </label>
            <input
              id="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 rounded-lg bg-white/10 text-black focus:outline-none focus:ring-2 focus:ring-black border border-black"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1" htmlFor="phone">
              Phone Number
            </label>
            <input
              id="phone"
              type="tel"
              value={formData.phone}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 rounded-lg bg-white/10 text-black focus:outline-none focus:ring-2 focus:ring-black border border-black"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1" htmlFor="gender">
              Gender
            </label>
            <select
              id="gender"
              value={formData.gender}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 rounded-lg bg-white/10 text-black focus:outline-none focus:ring-2 focus:ring-black border border-black"
            >
              <option className="text-black" value="">
                Select
              </option>
              <option className="text-black" value="male">
                Male
              </option>
              <option className="text-black" value="female">
                Female
              </option>
              <option className="text-black" value="other">
                Other
              </option>
            </select>
          </div>

          <div>
            <label
              className="block text-sm font-medium mb-1"
              htmlFor="password"
            >
              Create Password
            </label>
            <input
              id="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 rounded-lg bg-white/10 text-black focus:outline-none focus:ring-2 focus:ring-black border border-black"
            />
          </div>

          <div>
            <label
              className="block text-sm font-medium mb-1"
              htmlFor="confirmPassword"
            >
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              type="password"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 rounded-lg bg-white/10 text-black focus:outline-none focus:ring-2 focus:ring-black border border-black"
            />
          </div>

          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              id="isFarmer"
              checked={formData.isFarmer}
              onChange={handleChange}
              className="accent-black w-4 h-4"
            />
            <label htmlFor="isFarmer" className="text-sm text-black">
              I am a farmer
            </label>
          </div>

          <button
            type="submit"
            className="w-full bg-black text-white font-semibold py-2 rounded-lg hover:bg-gray-800 transition duration-200"
          >
            Sign Up
          </button>
        </form>

        <div className="mt-6 text-center text-sm">
          <p>
            Already have an account?{" "}
            <Link
              to="/loginpage"
              className="underline text-white hover:text-gray-200"
            >
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
