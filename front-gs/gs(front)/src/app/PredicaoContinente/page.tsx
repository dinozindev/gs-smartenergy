"use client";
import React, { useState } from "react";
import styles from "./PredicaoContinente.module.css";
import Sidebar from "../Sidebar/page";

const PredicaoContinente = () => {
  const [formData, setFormData] = useState({
    population: "",
    coal_electricity: "",
    biofuel_electricity: "",
    fossil_electricity: "",
    gas_electricity: "",
    hydro_electricity: "",
    nuclear_electricity: "",
    oil_electricity: "",
    other_renewable_exc_biofuel_electricity: "",
    solar_electricity: "",
    wind_electricity: "",
    greenhouse_gas_emissions: "",
  });

  const [result, setResult] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:5000/predict_classification_continent", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      setResult(`Continente previsto: ${data.prediction}`);
    } catch (error) {
      console.error("Error:", error);
      setResult("Error predicting continent.");
    }
  };

  const labels: Record<string, string> = {
    population: "População:ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ",
    coal_electricity: "Geração em TWh ao ano a partir de carvão:",
    biofuel_electricity: "Geração em TWh ao ano a partir de biocombustível:",
    fossil_electricity: "Geração em TWh ao ano a partir de combustíveis fósseis:",
    gas_electricity: "Geração em TWh ao ano a partir de gases naturais:",
    hydro_electricity: "Geração em TWh ao ano a partir de hidrelétricas:",
    nuclear_electricity: "Geração em TWh ao ano a partir de usinas nucleares:",
    oil_electricity: "Geração em TWh ao ano a partir de óleo:",
    other_renewable_exc_biofuel_electricity: "Geração em TWh ao ano a partir de outras fontes renováveis (geotérmica, maré):",
    solar_electricity: "Geração em TWh ao ano a partir de energia solar:",
    wind_electricity: "Geração em TWh ao ano a partir de energia eólica:",
    greenhouse_gas_emissions: "Emissões de Carbono em Milhões de Toneladas ao ano:"
  };

  return (
    <div>
      <Sidebar/>
      <h1 className={styles.titulo}>Predição de Continente</h1>
      <p className={styles.texto}>Para maior precisão, utilize valores realistas (Ex: a China gera em média 7500 TWh por ano, portanto utilize valores baixos)</p>
      <form onSubmit={handleSubmit} className={styles.formulario}>
        {Object.keys(formData).map((key) => (
          <div key={key}>
            <label className={styles.label}>{labels[key]}</label>
            <input
              className={styles.input}
              type="number"
              name={key}
              value={formData[key as keyof typeof formData]}
              onChange={handleChange}
              required
            />
          </div>
        ))}
        <div className={styles.divisor}></div>
        <button type="submit" className={styles.botao}>Prever</button>
        <div className={styles.divisor}></div>
        {result && <p className={styles.resultado}>{result}</p>}
      </form>
      
    </div>
  );
};

export default PredicaoContinente;