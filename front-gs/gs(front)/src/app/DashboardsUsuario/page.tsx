"use client";
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import styles from './DashboardsUsuario.module.css';
import Sidebar from '../Sidebar/page';

const Dashboard = () => {
    const [cpfUsuario, setCpfUsuario] = useState<string>("");
    const [telefone, setTelefone] = useState<string>("");
    const [nomeUsuario, setNome] = useState<string>("");
    const [email, setEmail] = useState<string>("");
    const [senha, setSenha] = useState<string>("");
    const [gastoMensal, setGastoMensal] = useState(0);
    const [bio, setBio] = useState<string>("");
    const [imagem, setImagem] = useState<string | null>(null);
    const router = useRouter();

    useEffect(() => {
        const isLoggedIn = localStorage.getItem("usuario");
        if (!isLoggedIn) {
            router.push("/login"); 
            return;
        }

        const userCredentials = JSON.parse(isLoggedIn);
        setCpfUsuario(userCredentials.cpfUsuario);
        setTelefone(userCredentials.telefone);
        setNome(userCredentials.nomeUsuario);
        setEmail(userCredentials.email);
        setSenha(userCredentials.senha);
        setGastoMensal(userCredentials.gastoMensal);
        setBio(localStorage.getItem("userBio") || "");
        setImagem(localStorage.getItem("userImage") || null);

        
    }, []);
    
    const handleSave = () => {
        const updatedCredentials = {
            cpfUsuario,
            nomeUsuario,
            email,
            senha,
            telefone,
            gastoMensal
        };

        fetch(`http://127.0.0.1:8080/usuarios/${cpfUsuario}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedCredentials),
        })
            .then(response => {
                if (response.ok) {
                    localStorage.setItem("usuario", JSON.stringify(updatedCredentials));
                    localStorage.setItem("userBio", bio);
                    if (imagem) localStorage.setItem("userImage", imagem);
                    alert("Dados atualizados com sucesso!");
                    router.push('/Perfil');
                } else {
                    alert("Erro ao atualizar dados.");
                }
            })
            .catch(error => console.error("Erro ao atualizar dados:", error));
    };

    const handleDelete = () => {
        fetch(`http://127.0.0.1:8080/usuarios/${cpfUsuario}`, { 
            method: 'DELETE',
        })
            .then(response => {
                if (response.ok) {
                    localStorage.removeItem("usuario");
                    localStorage.removeItem("residencia");
                    localStorage.removeItem("userBio");
                    localStorage.removeItem("userImage");
                    alert("Usuário excluído com sucesso!");
                    router.push("/");
                } else {
                    alert("Erro ao excluir usuário.");
                }
            })
            .catch(error => console.error("Erro ao excluir usuário:", error));
    };

    const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setImagem(reader.result as string);
            };
            reader.readAsDataURL(file);
        }
    };

    return (
        <>
            <Sidebar></Sidebar>
            <div className={styles.containermaior}>
                <div className={styles.container}>
                    <h1 className={styles.title}>Gerenciar Usuário</h1>
                    <div className={styles.formGroup}>
                        <label className={styles.label}>CPF: </label>
                        <input type="text" value={cpfUsuario} onChange={(e) => setCpfUsuario(e.target.value)} disabled className={styles.input} />
                    </div>
                    <div className={styles.formGroup}>
                        <label className={styles.label}>Nome: </label>
                        <input type="text" value={nomeUsuario} onChange={(e) => setNome(e.target.value)} className={styles.input} />
                    </div>
                    <div className={styles.formGroup}>
                        <label className={styles.label}>Email:</label>
                        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} disabled className={styles.input} placeholder='exemplo@gmail.com'/>
                    </div>
                    <div className={styles.formGroup}>
                        <label className={styles.label}>Senha:</label>
                        <input type="password" value={senha} onChange={(e) => setSenha(e.target.value)} className={styles.input} placeholder='SeNhAsEgUrA123' />
                    </div>
                    <div className={styles.formGroup}>
                        <label className={styles.label}>Telefone:</label>
                        <input type=im"text" value={telefone} onChange={(e) => setTelefone(e.target.value)} className={styles.input} />
                    </div>
                    <div className={styles.formGroup}>
                        <label className={styles.label}>Bio:</label>
                        <textarea
                        placeholder='Minha bio :]'
                            value={bio}
                            onChange={(e) => setBio(e.target.value)}
                            className={styles.textarea}
                            maxLength={100}
                        />
                    </div>
                    <div className={styles.formGroup}>
                        <label className={styles.label}>Foto de Perfil:</label>
                        <input type="file" accept="image/*" onChange={handleImageChange} className={styles.input} />
                        {imagem && <img src={imagem} alt="Pré-visualização da imagem" className={styles.previewImage} />}
                    </div>
                    <button onClick={handleSave} className={styles.botaoSalvar}>Salvar</button>
                    <button onClick={handleDelete} className={styles.botaoExcluir}>Excluir Usuário</button>

                    <div className={styles.veiculosContainer}>
                    </div>
                </div>
            </div>
        </>
    );
};

export default Dashboard;



// Caso nao consiga rodar as APIs utilize o codigo abaixo que demonstra a funcionalidade sendo uma versão apenas para o desenvolvimento

// "use client";
// import { useState, useEffect } from "react";
// import { useRouter } from "next/navigation";
// import styles from "./DashboardsUsuario.module.css";
// import Sidebar from "../Sidebar/page";

// const Dashboard = () => {
//   const [cpfUsuario, setCpfUsuario] = useState<string>("");
//   const [telefone, setTelefone] = useState<string>("");
//   const [nomeUsuario, setNome] = useState<string>("");
//   const [email, setEmail] = useState<string>("");
//   const [senha, setSenha] = useState<string>("");
//   const [gastoMensal, setGastoMensal] = useState(0);
//   const [bio, setBio] = useState<string>("");
//   const [imagem, setImagem] = useState<string | null>(null);
//   const router = useRouter();

//   useEffect(() => {
//     const userCredentials = JSON.parse(localStorage.getItem("usuario") || "{}");
//     setCpfUsuario(userCredentials.cpfUsuario || "");
//     setTelefone(userCredentials.telefone || "");
//     setNome(userCredentials.nomeUsuario || "");
//     setEmail(userCredentials.email || "");
//     setSenha(userCredentials.senha || "");
//     setGastoMensal(userCredentials.gastoMensal || 0);
//     setBio(localStorage.getItem("userBio") || "");
//     setImagem(localStorage.getItem("userImage") || null);
//   }, []);

//   const handleSave = () => {
//     const updatedCredentials = {
//       cpfUsuario,
//       nomeUsuario,
//       email,
//       senha,
//       telefone,
//       gastoMensal,
//     };

//     try {
//       localStorage.setItem("usuario", JSON.stringify(updatedCredentials));
//       localStorage.setItem("userBio", bio);
//       if (imagem) localStorage.setItem("userImage", imagem);
//       alert("Dados atualizados com sucesso!");
//       router.push("/Perfil");
//     } catch (error) {
//       console.error("Erro ao salvar os dados:", error);
//       alert("Erro ao salvar os dados.");
//     }
//   };

//   const handleDelete = () => {
//     try {
//       localStorage.removeItem("usuario");
//       localStorage.removeItem("userBio");
//       localStorage.removeItem("userImage");
//       alert("Usuário excluído com sucesso!");
//       router.push("/");
//     } catch (error) {
//       console.error("Erro ao excluir o usuário:", error);
//       alert("Erro ao excluir o usuário.");
//     }
//   };

//   const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
//     const file = e.target.files?.[0];
//     if (file) {
//       const reader = new FileReader();
//       reader.onloadend = () => {
//         setImagem(reader.result as string);
//       };
//       reader.readAsDataURL(file);
//     }
//   };

//   return (
//     <>
//       <Sidebar />
//       <div className={styles.containermaior}>
//         <div className={styles.container}>
//           <h1 className={styles.title}>Gerenciar Usuário</h1>
//           <div className={styles.formGroup}>
//             <label className={styles.label}>CPF:</label>
//             <input
//               type="text"
//               value={cpfUsuario}
//               onChange={(e) => setCpfUsuario(e.target.value)}
//               disabled
//               className={styles.input}
//             />
//           </div>
//           <div className={styles.formGroup}>
//             <label className={styles.label}>Nome:</label>
//             <input
//               type="text"
//               value={nomeUsuario}
//               onChange={(e) => setNome(e.target.value)}
//               className={styles.input}
//             />
//           </div>
//           <div className={styles.formGroup}>
//             <label className={styles.label}>Email:</label>
//             <input
//               type="email"
//               value={email}
//               onChange={(e) => setEmail(e.target.value)}
//               disabled
//               className={styles.input}
//               placeholder="exemplo@gmail.com"
//             />
//           </div>
//           <div className={styles.formGroup}>
//             <label className={styles.label}>Senha:</label>
//             <input
//               type="password"
//               value={senha}
//               onChange={(e) => setSenha(e.target.value)}
//               className={styles.input}
//               placeholder="SeNhAsEgUrA123"
//             />
//           </div>
//           <div className={styles.formGroup}>
//             <label className={styles.label}>Telefone:</label>
//             <input
//               type="text"
//               value={telefone}
//               onChange={(e) => setTelefone(e.target.value)}
//               className={styles.input}
//             />
//           </div>
//           <div className={styles.formGroup}>
//             <label className={styles.label}>Bio:</label>
//             <textarea
//               placeholder="Minha bio :]"
//               value={bio}
//               onChange={(e) => setBio(e.target.value)}
//               className={styles.textarea}
//               maxLength={100}
//             />
//           </div>
//           <div className={styles.formGroup}>
//             <label className={styles.label}>Foto de Perfil:</label>
//             <input
//               type="file"
//               accept="image/*"
//               onChange={handleImageChange}
//               className={styles.input}
//             />
//             {imagem && (
//               <img
//                 src={imagem}
//                 alt="Pré-visualização da imagem"
//                 className={styles.previewImage}
//               />
//             )}
//           </div>
//           <button onClick={handleSave} className={styles.botaoSalvar}>
//             Salvar
//           </button>
//           <button onClick={handleDelete} className={styles.botaoExcluir}>
//             Excluir Usuário
//           </button>
//         </div>
//       </div>
//     </>
//   );
// };

// export default Dashboard;
