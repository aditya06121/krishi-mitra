import React, { useEffect, useState } from "react";
import Papa from "papaparse";
import { useTranslation } from "react-i18next";

const Schemes = () => {
  const { t } = useTranslation();

  const [stateData, setStateData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [selectedState, setSelectedState] = useState("");
  const [selectedIndia, setSelectedIndia] = useState("");

  useEffect(() => {
    Papa.parse("/schemes.csv", {
      download: true,
      header: true,
      complete: (results) => {
        const data = results.data.filter((row) => row["state"]);
        setStateData(data);
        setFilteredData(data);
      },
    });
  }, []);

  const handleStateChange = (e) => {
    const state = e.target.value;
    setSelectedState(state);
    setSelectedIndia("");
    if (state === "") {
      setFilteredData(stateData);
    } else {
      setFilteredData(stateData.filter((row) => row.state.trim() === state));
    }
  };

  const handleIndiaChange = (e) => {
    const val = e.target.value;
    setSelectedIndia(val);
    setSelectedState("");
    if (val === "") {
      setFilteredData([]);
    } else {
      Papa.parse("/india.csv", {
        download: true,
        header: true,
        complete: (results) => {
          const clean = results.data.filter((row) =>
            Object.values(row).some((v) => v)
          );
          setFilteredData(clean);
        },
      });
    }
  };

  const renderTable = (data) => {
    if (!data || data.length === 0)
      return <p className="mt-4 text-red-700">{t("no_data")}</p>;

    const headers = Object.keys(data[0]).filter(Boolean);

    return (
      <table className="w-full border mt-4 bg-white shadow-md rounded-lg overflow-hidden">
        <thead className="bg-green-200 text-green-900">
          <tr>
            {headers.map((h) => (
              <th key={h} className="p-3 border-b">
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i} className="hover:bg-green-50">
              {headers.map((h) => (
                <td key={h} className="p-3 border-b">
                  {row[h]?.trim() || ""}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  const uniqueStates = [
    ...new Set(stateData.map((r) => r.state.trim())),
  ].sort();

  return (
    <div className="p-6 bg-gradient-to-r from-green-200 to-green-300 min-h-screen text-green-900 font-sans">
      <div className="max-w-5xl mx-auto bg-white bg-opacity-70 p-6 rounded-xl shadow-md">
        <h1 className="text-3xl font-bold text-center mb-6">{t("title")}</h1>

        <div className="flex flex-col md:flex-row gap-6 mb-6">
          <div className="flex-1">
            <label htmlFor="stateDropdown" className="font-semibold mb-2 block">
              {t("select_state")}
            </label>
            <select
              id="stateDropdown"
              value={selectedState}
              onChange={handleStateChange}
              className="w-full p-3 border rounded"
            >
              <option value="">{t("all_states")}</option>
              {uniqueStates.map((state) => (
                <option key={state} value={state}>
                  {state}
                </option>
              ))}
            </select>
          </div>

          <div className="flex-1">
            <label htmlFor="indiaDropdown" className="font-semibold mb-2 block">
              {t("select_india")}
            </label>
            <select
              id="indiaDropdown"
              value={selectedIndia}
              onChange={handleIndiaChange}
              className="w-full p-3 border rounded"
            >
              <option value="">{t("load_india")}</option>
              <option value="All">{t("all")}</option>
            </select>
          </div>
        </div>

        <div>{renderTable(filteredData)}</div>
      </div>
    </div>
  );
};

export default Schemes;
