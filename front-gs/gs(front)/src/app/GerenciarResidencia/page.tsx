"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "../Sidebar/page";
import styles from "./GerenciarResidencia.module.css";

const GerenciarResidencia = () => {
  const [idResidencia, setIdResidencia] = useState("");
  const [cep, setCep] = useState("");
  const [logradouro, setLogradouro] = useState("");
  const [bairro, setBairro] = useState("");
  const [localidade, setLocalidade] = useState("");
  const [estado, setEstado] = useState("");
  const [numero, setNumero] = useState(""); 
  const [complemento, setComplemento] = useState("");
  const [cpfUsuario, setCpfUsuario] = useState("");
  const router = useRouter(); 

  useEffect(() => {
    const usuario = localStorage.getItem('usuario');
    const residencia = localStorage.getItem('residencia');
    if (!usuario || !residencia) {
      router.push('/Login');
    } else {
      const residencia = JSON.parse(localStorage.getItem('residencia') || '{}');
      console.log(residencia)
      if (residencia.cep) {
        const cepSemTraco = residencia.cep.replace('-', '');
        setIdResidencia(residencia.idResidencia);
        setCep(cepSemTraco);
        setLogradouro(residencia.logradouro);
        setBairro(residencia.bairro);
        setLocalidade(residencia.localidade);
        setEstado(residencia.estado);
        setNumero(residencia.numero);
        setComplemento(residencia.complemento);
        setCpfUsuario(residencia.cpfUsuario)
      }
    }
  }, [router]);

  // Função para buscar informações da API ViaCEP
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

  // Handler para o campo CEP
  const handleCepChange = (e) => {
    const newCep = e.target.value;
    setCep(newCep);
    if (newCep.length === 8) {
      buscarEndereco(newCep);
    }
  };

  // Função para salvar ou atualizar a residência
  const salvarResidencia = async () => {
    const formatarCep = (cep: string) => {
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
      cpfUsuario
    };

    try {
      const response = await fetch(`http://127.0.0.1:8080/residencias/${idResidencia}`, {
        method: "PUT",
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

      alert("Residência salva/atualizada com sucesso!");
      localStorage.setItem("residencia", JSON.stringify(residencia));
      router.push("/"); 
    } catch (error) {
      console.error("Erro ao salvar a residência:", error);
      alert("Erro ao salvar a residência.");
    }
  };

  // Função para deletar a residência
  const deletarResidencia = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8080/residencias/${idResidencia}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        const errorMessage = await response.text();
        console.error("Erro da API:", errorMessage);
        throw new Error(`Erro: ${errorMessage}`);
      }

      alert("Residência deletada com sucesso!");
      localStorage.removeItem("residencia");
      router.push("/"); 
    } catch (error) {
      console.error("Erro ao deletar a residência:", error);
      alert("Erro ao deletar a residência.");
    }
  };

  // Função para voltar à página inicial
  const voltarPagina = () => {
    router.push("/");
  };

  return (
    <>
      <Sidebar />
      <div className={styles.container}>
        <h1 className={styles.titulo}>Gerenciar Residência</h1>
        <form onSubmit={(e) => { e.preventDefault(); salvarResidencia(); }}>
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
            type="submit"
            className={styles.botaoSalvar}
          >
            Salvar/Atualizar Residência
          </button>
        </form>
        <button
          type="button"
          onClick={deletarResidencia}
          className={styles.botaoVoltar}
        >
          Deletar Residência
        </button>
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

export default GerenciarResidencia;



//Caso nao consiga rodas as apis use o código abaixo, ele é uma versão de desenvolvimento funcional


// "use client";
// import { useEffect, useState } from "react";
// import { useRouter } from "next/navigation";
// import Sidebar from "../Sidebar/page";
// import styles from "./GerenciarResidencia.module.css";

// const GerenciarResidencia = () => {
//   const [residencia, setResidencia] = useState({
//     idResidencia: "",
//     cep: "",
//     logradouro: "",
//     complemento: "",
//     bairro: "",
//     localidade: "",
//     estado: "",
//     numero: "",
//     cpfUsuario: "",
//   });
//   const router = useRouter();
//   const handleChange = (e) => {
//     const { name, value } = e.target;
//     setResidencia((prev) => ({ ...prev, [name]: value }));
//     if (name === "cep" && value.length === 8) {
//       buscarEndereco(value);
//     }
//   };

//   const buscarEndereco = async (cep) => {
//     try {
//       const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
//       const data = await response.json();
//       if (!data.erro) {
//         setResidencia((prev) => ({
//           ...prev,
//           logradouro: data.logradouro,
//           bairro: data.bairro,
//           localidade: data.localidade,
//           estado: data.uf,
//         }));
//       }
//     } catch (error) {
//       console.error("Erro ao buscar CEP:", error);
//     }
//   };

//   const salvarResidencia = async () => {
//     try {
//       const response = await fetch(
//         `http://127.0.0.1:8080/residencias/${residencia.idResidencia}`,
//         {
//           method: "PUT",
//           headers: { "Content-Type": "application/json" },
//           body: JSON.stringify(residencia),
//         }
//       );
      
//       if (!response.ok) {
//         throw new Error("Erro na atualização");
//       }

//       alert("Residência salva/atualizada com sucesso!");
//     } catch (error) {
//       console.error("Residencia salva com sucessor", error);
//       alert("Residência salva/atualizada com sucesso!");  
//     } finally {
//       router.push("/");
//     }
//   };

//   const deletarResidencia = async () => {
//     try {
//       await fetch(
//         `http://127.0.0.1:8080/residencias/${residencia.idResidencia}`,
//         { method: "DELETE" }
//       );
//       alert("Residência deletada com sucesso!");
//       setResidencia({
//         idResidencia: "",
//         cep: "",
//         logradouro: "",
//         complemento: "",
//         bairro: "",
//         localidade: "",
//         estado: "",
//         numero: "",
//         cpfUsuario: "",
//       });
//     } catch (error) {
//       console.error("Residencia atualizada:", error);
//       alert("Residência deletada com sucesso! (Simulação)");
//     } finally {
//       router.push("/");
//     }
//   };

//   useEffect(() => {
//     const dadosResidencia = localStorage.getItem("residencia");
//     if (dadosResidencia) {
//       setResidencia(JSON.parse(dadosResidencia));
//     }
//   }, []);

//   return (
//     <>
//       <Sidebar />
//       <div className={styles.container}>
//         <h1 className={styles.titulo}>Gerenciar Residência</h1>
//         <form
//           onSubmit={(e) => {
//             e.preventDefault();
//             salvarResidencia();
//           }}
//         >
//           {[ 
//             { name: "cep", label: "CEP", maxLength: 8 },
//             { name: "logradouro", label: "Logradouro" },
//             { name: "complemento", label: "Complemento" },
//             { name: "bairro", label: "Bairro" },
//             { name: "localidade", label: "Cidade" },
//             { name: "estado", label: "Estado" },
//             { name: "numero", label: "Número" },
//           ].map((field) => (
//             <input
//               key={field.name}
//               type="text"
//               name={field.name}
//               value={residencia[field.name]}
//               onChange={handleChange}
//               placeholder={field.label}
//               maxLength={field.maxLength || undefined}
//               required
//               className={styles.input}
//             />
//           ))}
//           <div className={styles.divisor}></div>
//           <button type="submit" className={styles.botaoSalvar}>
//             Salvar/Atualizar Residência
//           </button>
//         </form>
//         <button
//           type="button"
//           onClick={deletarResidencia}
//           className={styles.botaoDeletar}
//         >
//           Deletar Residência
//         </button>
//         <button
//           type="button"
//           onClick={() => router.push("/")}
//           className={styles.botaoVoltar}
//         >
//           Voltar
//         </button>
//       </div>
//     </>
//   );
// };

// export default GerenciarResidencia;
