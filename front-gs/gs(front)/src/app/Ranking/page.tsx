'use client'
import { useEffect, useState } from "react";
import Sidebar from "../Sidebar/page";

const Ranking = () => {
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Função para buscar usuários do endpoint
  useEffect(() => {
    const fetchUsuarios = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8080/usuarios");
        if (!response.ok) {
          throw new Error("Erro ao buscar os usuários.");
        }
        const data = await response.json();
        setUsuarios(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUsuarios();
  }, []);

  // Exibir os dados ou mensagem de erro
  if (loading) return <p>Carregando...</p>;
  if (error) return <p>{error}</p>;

  return (
    <>
    <Sidebar />
    <div>
      <h1>Ranking de Gasto Mensal</h1>
      <table>
        <thead>
          <tr>
            <th>Posição</th>
            <th>Nome</th>
            <th>Gasto Mensal</th>
          </tr>
        </thead>
        <tbody>
          {usuarios.map((usuario, index) => (
            <tr key={usuario.cpf_usuario}>
              <td>{index + 1}</td>
              <td>{usuario.nome_usuario}</td>
              <td>{usuario.gasto_mensal.toFixed(2)} KWh</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
    </>
  );
};

export default Ranking;



// caso nao consiga fazer a api rodar basta descomentar o codigo abaixo e comentar o acima, voce tera uma visão como desenvolvedor que exibem dados ficticios mas que exibem o perfeito funcionamento do sistema

// 'use client'
// import { useEffect, useState } from "react";
// import Sidebar from "../Sidebar/page";
// import styles from "./Ranking.module.css";

// const Ranking = () => {
//   const [usuarios, setUsuarios] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);

//   // Dados fictícios para simulação
//   const dadosFicticios = [
//     { cpf_usuario: "111.111.111-11", nome_usuario: "João Silva", gasto_mensal: 125.50 },
//     { cpf_usuario: "222.222.222-22", nome_usuario: "Maria Oliveira", gasto_mensal: 110.30 },
//     { cpf_usuario: "333.333.333-33", nome_usuario: "Pedro Santos", gasto_mensal: 98.75 },
//   ];

//   useEffect(() => {
//     const fetchUsuarios = async () => {
//       try {
//         const response = await fetch("http://127.0.0.1:8080/usuarios");
//         if (!response.ok) {
//           throw new Error("Erro ao buscar os usuários.");
//         }
//         const data = await response.json();
//         setUsuarios(data);
//       } catch (err) {
//         console.error(err);
//         setUsuarios(dadosFicticios); // Usar dados fictícios em caso de erro
//         setError("");
//       } finally {
//         setLoading(false);
//       }
//     };

//     fetchUsuarios();
//   }, []);

//   // Exibir os dados ou mensagem de erro
//   if (loading) return <p>Carregando...</p>;

//   return (
//     <>
//       <Sidebar />
//       <div>
//         <h1 className={styles.titulo}>Ranking de Gasto Mensal</h1>
//         <p className={styles.textorecepcao}>Este ranking mostra as casas que obtiveram maior economia de energia no mês de Novembro</p>
//         {error && <p style={{ color: "red" }}>{error}</p>}
//         <table className={styles.rankingContainer}>
//           <thead>
//             <tr>
//               <th className={styles.legenda}>Posição</th>
//               <th className={styles.legenda}>Nome</th>
//               <th className={styles.legenda}>Gasto Mensal</th>
//             </tr>
//           </thead>
//           <div className={styles.divisor1}></div>
//           <tbody>
//             {usuarios.map((usuario, index) => (
//               <tr key={usuario.cpf_usuario}>
//                 <td className={styles.legenda2}>{index + 1}</td>
//                 <td className={styles.legenda3}>{usuario.nome_usuario}</td>
//                 <td className={styles.legenda4}>{usuario.gasto_mensal.toFixed(2)} KWh</td>
//                 <div className={styles.linedivisor}></div>
//               </tr>
//             ))}
//           </tbody>
//         </table>
//       </div>
//     </>
//   );
// };

// export default Ranking;
