import React from "react";
import { useLocation } from "react-router-dom";
import { useTranslation } from "react-i18next";

function Profile() {
  const location = useLocation();
  const userData = location.state?.userData;
  const { t } = useTranslation();

  return (
    <div
      className="min-h-screen flex items-center justify-center bg-cover bg-center"
      style={{ backgroundImage: "url('./farm2.jpg')" }}
    >
      <div className="bg-white/60 backdrop-blur-lg rounded-3xl shadow-2xl p-10 w-full max-w-2xl border border-white/30 text-gray-800">
        {/* Title */}
        <h1 className="text-4xl font-bold text-center mb-6">{t("Profile")}</h1>

        {/* Smiley Avatar */}
        <div className="flex justify-center mb-6">
          <div className="text-7xl rounded-full w-32 h-32 flex items-center justify-center border-4 border-white shadow-lg bg-white">
            😊
          </div>
        </div>

        {/* User Info */}
        <div className="grid grid-cols-1 gap-4 text-lg">
          <div className="flex justify-between">
            <strong>{t("name")}:</strong>
            <span>{userData?.name || t("user")}</span>
          </div>
          <div className="flex justify-between">
            <strong>{t("email")}:</strong>
            <span>{userData?.email || "N/A"}</span>
          </div>
          <div className="flex justify-between">
            <strong>{t("occupation")}:</strong>
            <span>{userData?.occupation || "N/A"}</span>
          </div>
          <div className="flex justify-between">
            <strong>{t("age")}:</strong>
            <span>{userData?.age || "21"}</span>
          </div>
          <div className="flex justify-between">
            <strong>{t("gender")}:</strong>
            <span>
              {userData?.gender === true || userData?.gender === "true"
                ? t("female")
                : t("male")}
            </span>
          </div>
          <div className="flex justify-between">
            <strong>{t("phone")}:</strong>
            <span>{userData?.phone || "9876543210"}</span>
          </div>

          {/* New Agricultural Data */}
          <div className="flex justify-between">
            <strong>{t("currentCrop")}:</strong>
            <span>{userData?.currentCrop || t("paddy")}</span>
          </div>
          <div className="flex justify-between">
            <strong>{t("previousCrop")}:</strong>
            <span>{userData?.previousCrop || t("paddy")}</span>
          </div>
          <div className="flex justify-between">
            <strong>{t("previousYield")}:</strong>
            <span>{userData?.previousYield || "975"}</span>
          </div>
          <div className="flex justify-between">
            <strong>{t("currentYield")}:</strong>
            <span>{userData?.currentYield || "980"}</span>
          </div>
          <div className="flex justify-between">
            <strong>{t("nextCrop")}:</strong>
            <span>{userData?.nextCrop || t("cotton")}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Profile;
