"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Sidebar from "../Sidebar/page";
import styles from "./Perfil.module.css";

const Perfil = () => {
  const [nomeUsuario, setNomeUsuario] = useState<string | null>(null);
  const [gastoMensal, setGastoMensal] = useState<number>(0);
  const [bio, setBio] = useState<string>("");
  const [imagemUsuario, setImagemUsuario] = useState<string | null>(null);
  const [usuarios, setUsuarios] = useState<any[]>([]);
  const [usuarioPosicao, setUsuarioPosicao] = useState<number | null>(null);
  const router = useRouter();

  useEffect(() => {
    const userCredentials = localStorage.getItem("usuario");
    let parsedUserCredentials: any = null;

    if (userCredentials) {
      parsedUserCredentials = JSON.parse(userCredentials);
      setGastoMensal(parsedUserCredentials.gastoMensal || 0);
      setNomeUsuario(parsedUserCredentials.email.split("@")[0]);
    } else {
      router.push("/");
      return;
    }

    const userBio = localStorage.getItem("userBio");
    const savedImage = localStorage.getItem("userImage");

    if (userBio) {
      setBio(userBio);
    } else {
      setBio("Bem-vindo(a) ao nosso sistema! Edite sua bio para personalizar esta seção.");
    }

    if (savedImage) {
      setImagemUsuario(savedImage);
    }

    const fetchUsuarios = async () => {
        try {
          const response = await fetch("http://127.0.0.1:8080/usuarios");
          if (!response.ok) {
            throw new Error("Erro ao buscar os usuários.");
          }
          const data = await response.json();
      
          setUsuarios(data);
      
          const posicao = data.findIndex(
            (usuario: any) => usuario.cpf_usuario === parsedUserCredentials.cpfUsuario
          );
      
          setUsuarioPosicao(posicao === -1 ? null : posicao + 1); 
        } catch (err) {
          console.error("Erro ao buscar ou processar os usuários:", err);
        }
      };

    fetchUsuarios();
  }, [router]);

  const editarBio = () => {
    router.push("/DashboardsUsuario");
  };

  return (
    <>
      <Sidebar />
      <div className={styles.container}>
        <img
          src={imagemUsuario || "/Imagens/imagenpadraouser.png"}
          alt="Imagem do usuário"
          className={styles.imagemUsuario}
        />
        <p className={styles.paragrafoBio}>
          Olá, sou {nomeUsuario || "Usuário"}. {bio}
        </p>
        <img
          src="/Imagens/penedit.png"
          alt=""
          onClick={editarBio}
          className={styles.editarBio}
        />
        <div className={styles.fundoAgendamentosPerfil}></div>

        <div className={styles.classificção}>
          <h2 className={styles.classificçãoT}>Classificação</h2>
          {usuarioPosicao !== null ? (
            <p>
              Você ocupa a {usuarioPosicao}° posição no ranking de maiores economistas de energia
            </p>
          ) : (
            <p>Você ainda não foi classificado no ranking.</p>
          )}
        </div>
        <div className={styles.divisor}></div>
        <div className={styles.classificção2}>
          <h2>Seus gastos</h2>
          <p>
            Você gastou {gastoMensal} KWh no mês!
          </p>
        </div>
      </div>
    </>
  );
};

export default Perfil;

// "use client";
// import { useEffect, useState } from "react";
// import { useRouter } from "next/navigation";
// import Sidebar from "../Sidebar/page";
// import styles from "./Perfil.module.css";

// const Perfil = () => {
//   const [nomeUsuario, setNomeUsuario] = useState<string | null>("João Silva"); // Dados mockados
//   const [gastoMensal, setGastoMensal] = useState<number>(350); // Dados mockados
//   const [bio, setBio] = useState<string>("Bem-vindo(a) ao nosso sistema! Edite sua bio para personalizar esta seção.");
//   const [imagemUsuario, setImagemUsuario] = useState<string | null>("/Imagens/imagenpadraouser.png"); // Dados mockados
//   const [usuarioPosicao, setUsuarioPosicao] = useState<number | null>(5); // Dados mockados
//   const router = useRouter();

//   useEffect(() => {
//     const userCredentials = localStorage.getItem("usuario");

//     // if (!userCredentials) {
//     //   router.push("/");
//     //   return;
//     // }

//     // const parsedUserCredentials: any = JSON.parse(userCredentials);
//     // setNomeUsuario(parsedUserCredentials.email.split("@")[0]);

//     const userBio = localStorage.getItem("userBio");
//     const savedImage = localStorage.getItem("userImage");

//     if (userBio) {
//       setBio(userBio);
//     }
//     if (savedImage) {
//       setImagemUsuario(savedImage);
//     }
//   }, [router]);

//   const editarBio = () => {
//     router.push("/DashboardsUsuario");
//   };

//   return (
//     <>
//       <Sidebar />
//       <div className={styles.container}>
//         <img
//           src={imagemUsuario || "/Imagens/imagenpadraouser.png"}
//           alt="Imagem do usuário"
//           className={styles.imagemUsuario}
//         />
//         <p className={styles.paragrafoBio}>
//           Olá, sou {nomeUsuario || "Usuário"}. {bio}
//         </p>
//         <img
//           src="/Imagens/penedit.png"
//           alt="Editar bio"
//           onClick={editarBio}
//           className={styles.editarBio}
//         />
//         <div className={styles.fundoAgendamentosPerfil}></div>

//         <div className={styles.classificção}>
//           <h2 className={styles.classificçãoT}>Classificação</h2>
//           {usuarioPosicao !== null ? (
//             <p>
//               Você ocupa a {usuarioPosicao}° posição no ranking de maiores economistas de energia.
//             </p>
//           ) : (
//             <p>Você ainda não foi classificado no ranking.</p>
//           )}
//         </div>

//         <div className={styles.divisor}></div>

//         <div className={styles.classificção2}>
//           <h2>Seus gastos</h2>
//           <p>
//             Você gastou {gastoMensal} KWh no mês!
//           </p>
//         </div>
//       </div>
//     </>
//   );
// };

// export default Perfil;
