"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "../Sidebar/page";
import styles from "./CadastroResidencia.module.css";

const CadastroResidencia = () => {
  const [cep, setCep] = useState("");
  const [idResidencia, setIdResidencia] = useState("");
  const [logradouro, setLogradouro] = useState("");
  const [bairro, setBairro] = useState("");
  const [localidade, setLocalidade] = useState("");
  const [estado, setEstado] = useState("");
  const [numero, setNumero] = useState(""); 
  const [complemento, setComplemento] = useState("");
  const router = useRouter(); 

  // useEffect(() => {
  //   const usuario = localStorage.getItem('usuario');
  //       if (!usuario) {
  //           router.push('/Cadastro');
  //       }
  // }, [router])

  const buscarEndereco = async (cep) => {
    try {
      const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
      const data = await response.json();
      if (!data.erro) {
        setLogradouro(data.logradouro);
        setBairro(data.bairro);
        setLocalidade(data.localidade);
        setEstado(data.estado);
      } else {
        alert("CEP não encontrado.");
      }
    } catch (error) {
      console.error("Erro ao buscar CEP:", error);
    }
  };

  const handleCepChange = (e) => {
    const newCep = e.target.value;
    setCep(newCep);
    if (newCep.length === 8) {
      buscarEndereco(newCep);
    }
  };


  const salvarResidencia = async () => {
    const usuario = JSON.parse(localStorage.getItem("usuario")); 
    const cpfUsuario = usuario.cpfUsuario;
  
    const formatarCep = (cep) => {
      return cep.replace(/(\d{5})(\d{3})/, '$1-$2');
    };
  
    const cepFormatado = formatarCep(cep);
  
    const residencia = {
      idResidencia,
      cep: cepFormatado,
      logradouro,
      complemento,
      bairro,
      localidade,
      estado,
      numero,
      cpfUsuario,
    };
  
    try {
      const response = await fetch("http://127.0.0.1:8080/residencias", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(residencia),
      });
  
      if (!response.ok) {
        const errorMessage = await response.text();
        console.error("Erro da API:", errorMessage);
        throw new Error(`Erro: ${errorMessage}`);
      }
  
      const data = await response.json(); 
      alert("Cadastro realizado com sucesso!");
      residencia.idResidencia = data.id_residencia; 
      localStorage.setItem("residencia", JSON.stringify(residencia));
      router.push("/");
    } catch (error) {
      console.error("Erro ao salvar a residência:", error);
      alert("Erro ao salvar a residência.");
    }
  };

  const voltarPagina = () => {
    router.push("/");
  };

  return (
    <>
      <Sidebar />
      <div className={styles.container}>
        <h1 className={styles.titulo}>Cadastro de Residência</h1>
        <form onSubmit={
          (e) => {e.preventDefault();
          salvarResidencia();}
        }>
          <input
            type="text"
            value={cep}
            onChange={handleCepChange}
            maxLength="8"
            required
            placeholder="CEP"
            className={styles.input}
          />
          <input
            type="text"
            value={logradouro}
            onChange={(e) => setLogradouro(e.target.value)}
            required
            placeholder="Logradouro"
            className={styles.input}
          />
          <input
            type="text"
            value={complemento}
            onChange={(e) => setComplemento(e.target.value)}
            placeholder="Complemento"
            className={styles.input}
          />
          <input
            type="text"
            value={bairro}
            onChange={(e) => setBairro(e.target.value)}
            required
            placeholder="Bairro"
            className={styles.input}
          />
          <input
            type="text"
            value={localidade}
            onChange={(e) => setLocalidade(e.target.value)}
            required
            placeholder="Cidade"
            className={styles.input}
          />
          <input
            type="text"
            value={estado}
            onChange={(e) => setEstado(e.target.value)}
            required
            placeholder="Estado"
            className={styles.input}
          />
          <input
            type="text"
            value={numero}
            onChange={(e) => setNumero(e.target.value)}
            required
            placeholder="Número"
            className={styles.input}
          />
          <div className={styles.divisor}></div>
          <button
            type="button"
            onClick={salvarResidencia}
            className={styles.botaoSalvar}
          >
            Salvar Residência
          </button>
        </form>
        <button
          type="button"
          onClick={voltarPagina}
          className={styles.botaoVoltar}
        >
          Voltar
        </button>
      </div>
    </>
  );
};

export default CadastroResidencia;


//Caso nao consiga rodar as APIs utilize o codigo abaixo que demonstra a funcionalidade sendo uma versão apenas para o desenvolvimento

// "use client";

// import { useState } from "react";
// import { useRouter } from "next/navigation";
// import Sidebar from "../Sidebar/page";
// import styles from "./CadastroResidencia.module.css";

// const CadastroResidencia = () => {
//   const [cep, setCep] = useState("");
//   const [logradouro, setLogradouro] = useState("");
//   const [bairro, setBairro] = useState("");
//   const [localidade, setLocalidade] = useState("");
//   const [estado, setEstado] = useState("");
//   const [numero, setNumero] = useState("");
//   const [complemento, setComplemento] = useState("");
//   const router = useRouter();

//   const buscarEndereco = async (cep: string) => {
//     try {
//       const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
//       const data = await response.json();
//       if (!data.erro) {
//         setLogradouro(data.logradouro);
//         setBairro(data.bairro);
//         setLocalidade(data.localidade);
//         setEstado(data.uf);
//       } else {
//         alert("CEP não encontrado.");
//       }
//     } catch (error) {
//       console.error("Erro ao buscar CEP:", error);
//     }
//   };

//   const handleCepChange = (e: React.ChangeEvent<HTMLInputElement>) => {
//     const newCep = e.target.value;
//     setCep(newCep);
//     if (newCep.length === 8) {
//       buscarEndereco(newCep);
//     }
//   };

//   const salvarResidencia = async () => {
//     const usuario = JSON.parse(localStorage.getItem("usuario") || "{}");
//     const cpfUsuario = usuario?.cpfUsuario || "teste";

//     const residencia = {
//       cep,
//       logradouro,
//       complemento,
//       bairro,
//       localidade,
//       estado,
//       numero,
//       cpfUsuario,
//     };

//     try {
//       const response = await fetch("http://127.0.0.1:8080/residencias", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify(residencia),
//       });

//       if (response.ok) {
//         alert("Cadastro realizado com sucesso!");
//       } else {
//         console.warn("Erro ao salvar a residência. Redirecionando...");
//       }
//     } catch (error) {
//       console.error("Erro ao salvar residência:", error);
//     } finally {
//       router.push("/");
//     }
//   };

//   const voltarPagina = () => {
//     router.push("/");
//   };

//   return (
//     <>
//       <Sidebar />
//       <div className={styles.container}>
//         <h1 className={styles.titulo}>Cadastro de Residência</h1>
//         <form
//           onSubmit={(e) => {
//             e.preventDefault();
//             salvarResidencia();
//           }}
//         >
//           <input
//             type="text"
//             value={cep}
//             onChange={handleCepChange}
//             maxLength={8}
//             required
//             placeholder="CEP"
//             className={styles.input}
//           />
//           <input
//             type="text"
//             value={logradouro}
//             onChange={(e) => setLogradouro(e.target.value)}
//             required
//             placeholder="Logradouro"
//             className={styles.input}
//           />
//           <input
//             type="text"
//             value={complemento}
//             onChange={(e) => setComplemento(e.target.value)}
//             placeholder="Complemento"
//             className={styles.input}
//           />
//           <input
//             type="text"
//             value={bairro}
//             onChange={(e) => setBairro(e.target.value)}
//             required
//             placeholder="Bairro"
//             className={styles.input}
//           />
//           <input
//             type="text"
//             value={localidade}
//             onChange={(e) => setLocalidade(e.target.value)}
//             required
//             placeholder="Cidade"
//             className={styles.input}
//           />
//           <input
//             type="text"
//             value={estado}
//             onChange={(e) => setEstado(e.target.value)}
//             required
//             placeholder="Estado"
//             className={styles.input}
//           />
//           <input
//             type="text"
//             value={numero}
//             onChange={(e) => setNumero(e.target.value)}
//             required
//             placeholder="Número"
//             className={styles.input}
//           />
//           <div className={styles.divisor}></div>
//           <button
//             type="submit"
//             className={styles.botaoSalvar}
//           >
//             Salvar Residência
//           </button>
//         </form>
//         <button
//           type="button"
//           onClick={voltarPagina}
//           className={styles.botaoVoltar}
//         >
//           Voltar
//         </button>
//       </div>
//     </>
//   );
// };

// export default CadastroResidencia;
