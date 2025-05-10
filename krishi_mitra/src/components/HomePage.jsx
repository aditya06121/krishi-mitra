import { useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link, useNavigate } from "react-router-dom";
import { LogOut } from "lucide-react";

export default function HomePage() {
  const [temperature, setTemperature] = useState(23);

  useEffect(() => {
    const interval = setInterval(() => {
      setTemperature((prevTemp) => prevTemp + (Math.random() < 0.5 ? -1 : 1));
    }, 60000);

    return () => clearInterval(interval);
  }, []);

  const location = useLocation();
  const userData = location.state?.userData;

  const { i18n, t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState(t("Language"));

  const toggleDropdown = () => setIsOpen((prev) => !prev);

  const selectLanguage = (label, code) => {
    i18n.changeLanguage(code);
    setSelectedLanguage(t(label)); // Translate the selected language name
    setIsOpen(false);
  };

  const languages = [
    { label: "English", code: "en" },
    { label: "Hindi", code: "hi" },
    { label: "Kannada", code: "kn" },
  ];

  const navigate = useNavigate();
  const onLogout = () => {
    navigate("/loginpage");
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center bg-cover bg-center relative"
      style={{ backgroundImage: "url('./farm2.jpg')" }}
    >
      <div className="fixed top-5 left-5 right-5 bottom-5 px-9 py-4 backdrop-blur-md bg-white/20 border border-white/30 rounded-2xl shadow-md">
        <div className="flex justify-between items-center space-x-4">
          <button
            onClick={onLogout}
            className="fixed top-6 left-6 z-50 flex items-center gap-2 px-4 py-2 rounded-full bg-red-700 hover:bg-red-400 text-white shadow-lg transition"
            title="Logout"
          >
            <LogOut className="w-5 h-5" />
            <span className="hidden sm:inline">Logout</span>
          </button>
          <h1 className="w-full text-center py-4 text-5xl font-semibold text-green-900 tracking-wide">
            {t("KRISHI MITRA")}
          </h1>
          <div className="fixed top-11 text-green-900 text-lg right-100">
            {temperature}°C ☀️
          </div>
          <div className="flex items-center space-x-2">
            <h2 className="text-lg text-green-900">{t("Hello")},</h2>
            <h2 className="text-lg text-green-900">
              {t(userData?.name) || t("User")}
            </h2>
          </div>
        </div>

        <div className="mt-6 flex justify-around items-center flex-wrap px-4 gap-6">
          {/* Marketplace */}
          <Link to="/market">
            <div className="flex items-center space-x-2 text-green-700 hover:text-green-900 hover:scale-130 transition duration-300 bg-white/20 px-6 py-3 rounded-full border border-white/30 shadow-sm">
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                viewBox="0 0 24 24"
              >
                <path d="M3 9l1 11a1 1 0 001 1h14a1 1 0 001-1l1-11"></path>
                <path d="M5 9V6a2 2 0 012-2h10a2 2 0 012 2v3"></path>
              </svg>
              <span>{t("Marketplace")}</span>
            </div>
          </Link>
          {/* Schemes */}
          <Link to="/schemes" state={{ userData }}>
            <div className="flex items-center space-x-2 text-green-700 hover:text-green-900 hover:scale-130 transition duration-300 bg-white/20 px-6 py-3 rounded-full border border-white/30 shadow-sm">
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                viewBox="0 0 24 24"
              >
                <path d="M5 13l4 4L19 7"></path>
              </svg>
              <span>{t("Schemes")}</span>
            </div>
          </Link>
          {/* Profile */}
          <Link to="/profile" state={{ userData }}>
            <div className="flex items-center space-x-2 text-green-700 hover:text-green-900 hover:scale-130 transition duration-300 bg-white/20 px-6 py-3 rounded-full border border-white/30 shadow-sm">
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                viewBox="0 0 24 24"
              >
                <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4z"></path>
                <path d="M4 20v-1c0-2.21 3.58-4 8-4s8 1.79 8 4v1"></path>
              </svg>
              <span>{t("Profile")}</span>
            </div>
          </Link>

          {/* Language Selector */}
          <div className="relative inline-block text-left">
            <div
              onClick={toggleDropdown}
              className="flex items-center space-x-2 text-green-700 hover:text-green-900 hover:scale-130 transition duration-300 bg-white/20 px-6 py-3 rounded-full border border-white/30 shadow-sm cursor-pointer"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                viewBox="0 0 24 24"
              >
                <path d="M3 5h18"></path>
                <path d="M3 12h18"></path>
                <path d="M3 19h18"></path>
              </svg>
              <span>{selectedLanguage}</span>
            </div>

            {isOpen && (
              <div className="absolute z-10 mt-2 w-40 bg-white rounded-md shadow-lg ring-1 ring-black/10">
                <ul className="py-1 text-sm text-gray-700">
                  {languages.map(({ label, code }) => (
                    <li
                      key={code}
                      className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                      onClick={() => selectLanguage(label, code)}
                    >
                      {t(label)} {/* Translate language names */}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
        <div className="text-center text-lg font-medium mt-6">
          Interactive dashboard showing crop distribution across India, click to
          know more!
        </div>

        <div className="fixed top-60 left-60 z-50 flex items-center">
          <iframe
            title="Map"
            src={`./map.html`}
            width="900"
            height="400"
            style={{
              border: "0",
              borderRadius: "32px",
              boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
            }}
          ></iframe>
        </div>
        <a href="http://localhost:8501/" target="_blank">
          <div className="fixed top-165 left-145 z-50 flex items-center space-x-2 text-green-700 hover:text-green-900 hover:scale-130 transition duration-300 bg-white/20 px-6 py-3 rounded-full border border-white/30 shadow-sm">
            View Detailed Analysis
          </div>
        </a>
      </div>
    </div>
  );
}
