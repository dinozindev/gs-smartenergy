"use client";
import Sidebar from "../Sidebar/page";
import { useEffect, useState } from "react";
import styles from "./Projetos.module.css";

interface Projeto {
  id_projeto: number;
  descricao: string;
  custo: number;
  status: string;
  id_tipo_fonte: number;
  id_regiao: number;
}

const tipoFonteMap: { [key: number]: string } = {
    1: "Solar",
    2: "Eólica",
    3: "Hidrelétrica",
    4: "Geotérmica",
    5: "Biomassa",
  };

  const regiaoMap: { [key: number]: string } = {
    1: "Norte",
    2: "Sul",
    3: "Leste",
    4: "Oeste",
    5: "Centro-Oeste",
  };

const Projetos = () => {
  const [projetos, setProjetos] = useState<Projeto[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8080/projetos")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Erro ao buscar projetos");
        }
        return response.json();
      })
      .then((data) => setProjetos(data))
      .catch((error) => {
        console.error("Erro ao buscar projetos:", error);
      });
  }, []);

  return (
    <>
      <Sidebar />
      <h1 className={styles.titulo}>Projetos</h1>
      <div className={styles.container}>
        {projetos.length > 0 ? (
          projetos.map((projeto) => (
            <div key={projeto.id_projeto} className={styles.projetoContainer}>
              <h2 className={styles.nomeProjeto}>Projeto ID: {projeto.id_projeto}</h2>
              <p className={styles.descricao}>Descrição: {projeto.descricao}</p>
              <p className={styles.custo}>Custo: R$ {projeto.custo.toFixed(2)}</p>
              <p className={styles.status}>Status: {projeto.status}</p>
              <p className={styles.tipoFonte}>Tipo de Fonte: {tipoFonteMap[projeto.id_tipo_fonte]}</p>
              <p className={styles.regiao}>Região: {regiaoMap[projeto.id_regiao]}</p>
            </div>
          ))
        ) : (
          <p>Carregando projetos...</p>
        )}
      </div>
    </>
  );
};

export default Projetos;




// caso não consiga fazer as APIs rodarem voce pode suar o código abaixo que demonstra a funcionalidade


// "use client";
// import Sidebar from "../Sidebar/page";
// import { useEffect, useState } from "react";
// import styles from "./Projetos.module.css";

// interface Projeto {
//   id_projeto: number;
//   descricao: string;
//   custo: number;
//   status: string;
//   id_tipo_fonte: number;
//   id_regiao: number;
// }

// const tipoFonteMap: { [key: number]: string } = {
//   1: "Solar",
//   2: "Eólica",
//   3: "Hidrelétrica",
//   4: "Geotérmica",
//   5: "Biomassa",
// };

// const regiaoMap: { [key: number]: string } = {
//   1: "Norte",
//   2: "Sul",
//   3: "Leste",
//   4: "Oeste",
//   5: "Centro-Oeste",
// };

// const Projetos = () => {
//   const [projetos, setProjetos] = useState<Projeto[]>([]);
//   const [error, setError] = useState<string | null>(null);

//   // Dados fictícios para simulação
//   const dadosFicticios: Projeto[] = [
//     {
//       id_projeto: 1,
//       descricao: "Parque Solar Belo Horizonte",
//       custo: 5000000,
//       status: "Em andamento",
//       id_tipo_fonte: 1,
//       id_regiao: 3,
//     },
//     {
//       id_projeto: 2,
//       descricao: "Usina Eólica Ventos do Sul",
//       custo: 7500000,
//       status: "Concluído",
//       id_tipo_fonte: 2,
//       id_regiao: 2,
//     },
//     {
//       id_projeto: 3,
//       descricao: "Hidrelétrica Rio Claro",
//       custo: 12000000,
//       status: "Planejamento",
//       id_tipo_fonte: 3,
//       id_regiao: 1,
//     },
//   ];

//   useEffect(() => {
//     fetch("http://127.0.0.1:8080/projetos")
//       .then((response) => {
//         if (!response.ok) {
//           throw new Error("Erro ao buscar projetos");
//         }
//         return response.json();
//       })
//       .then((data) => setProjetos(data))
//       .catch((error) => {
//         // console.error("Erro ao buscar projetos:", error);
//         setProjetos(dadosFicticios); // Usar dados fictícios em caso de erro
//         setError("");
//       });
//   }, []);

//   return (
//     <>
//       <Sidebar />
//       <h1 className={styles.titulo}>Projetos</h1>
//       {error && <p style={{ color: "red" }}>{error}</p>}
//       <div className={styles.container}>
//         {projetos.map((projeto) => (
//           <div key={projeto.id_projeto} className={styles.projetoContainer}>
//             <h2 className={styles.nomeProjeto}>Projeto ID: {projeto.id_projeto}</h2>
//             <p className={styles.descricao}>Descrição: {projeto.descricao}</p>
//             <p className={styles.custo}>Custo: R$ {projeto.custo.toFixed(2)}</p>
//             <p className={styles.status}>Status: {projeto.status}</p>
//             <p className={styles.tipoFonte}>Tipo de Fonte: {tipoFonteMap[projeto.id_tipo_fonte]}</p>
//             <p className={styles.regiao}>Região: {regiaoMap[projeto.id_regiao]}</p>
//           </div>
//         ))}
//       </div>
//     </>
//   );
// };

// export default Projetos;
