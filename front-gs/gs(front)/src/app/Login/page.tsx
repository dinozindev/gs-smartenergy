"use client";
import React, { useState, useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { useRouter } from 'next/navigation';
import styles from './Login.module.css';
import Link from 'next/link';
import '../reset.css';

interface LoginData {
    email: string;
    senha: string;
}

const schema = yup.object().shape({
    email: yup.string().email('Email inválido').required('Email é obrigatório'),
    senha: yup.string().min(6, 'A senha deve ter pelo menos 6 caracteres').required('Senha é obrigatória'),
});

const Login: React.FC = () => {
    const { control, handleSubmit, formState: { errors } } = useForm<LoginData>({
        resolver: yupResolver(schema),
    });

    const [errorMessage, setErrorMessage] = useState('');
    const router = useRouter();

    const onSubmit = async (data: LoginData) => {
        try {
            const response = await fetch('http://127.0.0.1:8080/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                const result = await response.json();
                const usuarioData = {
                    cpfUsuario: result.cpfUsuario,
                    nomeUsuario: result.nomeUsuario,
                    email: result.email,
                    senha: result.senha,
                    telefone: result.telefone,
                    gastoMensal: result.gastoMensal
                };
                localStorage.setItem('usuario', JSON.stringify(usuarioData));

                const residenciaResponse = await fetch(`http://127.0.0.1:8080/residencias/${result.cpfUsuario}`);
                if (residenciaResponse.ok) {
                    const residenciaData = await residenciaResponse.json();
                    localStorage.setItem('residencia', JSON.stringify(residenciaData));
                } else {
                    console.log('Usuário não tem residência associada.');
                }

                alert('Login realizado com sucesso!');
                router.push('/');
            } else {
                const errorData = await response.json();
                setErrorMessage(errorData.message || 'Erro no login. Verifique suas credenciais.');
            }
        } catch (error) {
            setErrorMessage('Erro ao tentar conectar à API.');
        }
    };

    useEffect(() => {
        const usuario = localStorage.getItem('usuario');
        if (usuario) {
            router.push('/');
        }
    }, [router]);

    return (
        <>
            <div className={styles.container}>
                <img src="./Imagens/Login.png" alt="" className={styles.imgmaior} />
                <h1 className={styles.titulo}>Login</h1>
                <form onSubmit={handleSubmit(onSubmit)}>
                <div className={styles.formulario}>
                        <Controller
                            name="email"
                            control={control}
                            defaultValue=""
                            render={({ field }) => (
                                <input
                                    {...field}
                                    placeholder={errors.email ? errors.email.message : 'Email'}
                                    className={`${errors.email ? styles.inputError : ''} ${styles.input}`}
                                />
                            )}
                        />
                    </div>
                    <div className={styles.formulario}>
                        <Controller
                            name="senha"
                            control={control}
                            defaultValue=""
                            render={({ field }) => (
                                <input
                                    {...field}
                                    type="password"
                                    placeholder={errors.senha ? errors.senha.message : 'Senha'}
                                    className={`${errors.senha ? styles.inputError : ''} ${styles.input}`}
                                />
                            )}
                        />
                    </div>
                    {errorMessage && <p className={styles.error}>{errorMessage}</p>}

                    <div className={styles.divisor1}></div>
                    <div className={styles.divisor2}></div>

                    <button className={styles.botao} type="submit">
                        Entrar
                    </button>
                    <div className={styles.linkCadastro}>
                        <Link href="/Cadastro">Não tem uma conta? Cadastre-se</Link>
                    </div>

                    <div className={styles.desistirbotao}>
                        <Link className={styles.voltabotao} href={"/"}>Voltar</Link>
                    </div>
                </form>
            </div>
        </>
    );
};

export default Login;


// Caso nao consiga a conexao com a API utilize o codigo abaixo que demonstra a funcionalidade sendo uma versão apenas para o desenvolvimento

// "use client";
// import React, { useState, useEffect } from 'react';
// import { useForm, Controller } from 'react-hook-form';
// import { yupResolver } from '@hookform/resolvers/yup';
// import * as yup from 'yup';
// import { useRouter } from 'next/navigation';
// import styles from './Login.module.css';
// import Link from 'next/link';
// import '../reset.css';

// interface LoginData {
//     email: string;
//     senha: string;
// }

// const schema = yup.object().shape({
//     email: yup.string().email('Email inválido').required('Email é obrigatório'),
//     senha: yup.string().min(6, 'A senha deve ter pelo menos 6 caracteres').required('Senha é obrigatória'),
// });

// const Login: React.FC = () => {
//     const { control, handleSubmit, formState: { errors } } = useForm<LoginData>({
//         resolver: yupResolver(schema),
//     });

//     const [errorMessage, setErrorMessage] = useState('');
//     const router = useRouter();

//     const onSubmit = (data: LoginData) => {
//         console.log('Formulário enviado com os dados:', data);
//         alert('Login enviado.');

//         router.push('/');
//     };

//     useEffect(() => {
//         const usuario = localStorage.getItem('usuario');
//         if (usuario) {
//             router.push('/');
//         }
//     }, [router]);

//     return (
//         <>
//             <div className={styles.container}>
//                 <img src="./Imagens/Login.png" alt="" className={styles.imgmaior} />
//                 <h1 className={styles.titulo}>Login</h1>
//                 <form onSubmit={handleSubmit(onSubmit)}>
//                     <div className={styles.formulario}>
//                         <Controller
//                             name="email"
//                             control={control}
//                             defaultValue=""
//                             render={({ field }) => (
//                                 <input
//                                     {...field}
//                                     placeholder={errors.email ? errors.email.message : 'Email'}
//                                     className={`${errors.email ? styles.inputError : ''} ${styles.input}`}
//                                 />
//                             )}
//                         />
//                     </div>
//                     <div className={styles.formulario}>
//                         <Controller
//                             name="senha"
//                             control={control}
//                             defaultValue=""
//                             render={({ field }) => (
//                                 <input
//                                     {...field}
//                                     type="password"
//                                     placeholder={errors.senha ? errors.senha.message : 'Senha'}
//                                     className={`${errors.senha ? styles.inputError : ''} ${styles.input}`}
//                                 />
//                             )}
//                         />
//                     </div>
//                     {errorMessage && <p className={styles.error}>{errorMessage}</p>}

//                     <div className={styles.divisor1}></div>
//                     <div className={styles.divisor2}></div>

//                     <button className={styles.botao} type="submit">
//                         Entrar
//                     </button>
//                     <div className={styles.linkCadastro}>
//                         <Link href="/Cadastro">Não tem uma conta? Cadastre-se</Link>
//                     </div>

//                     <div className={styles.desistirbotao}>
//                         <Link className={styles.voltabotao} href={"/"}>Voltar</Link>
//                     </div>
//                 </form>
//             </div>
//         </>
//     );
// };

// export default Login;
