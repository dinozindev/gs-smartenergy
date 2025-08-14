import style from "./TermosDeUso.module.css"
import Link from 'next/link';

const TermosDeUso = () => {

    return (
        <>
            <h1 className={style.title}>Termos de uso</h1>
            <div className={style.DivContent}>
                <h2>Responsabilidade do Usuário</h2>
                <p>O usuário concorda em usar os serviços de forma responsável, respeitando as leis aplicáveis e as normas estabelecidas neste documento. O usuário é responsável por manter a confidencialidade de sua conta, caso aplicável, e por todas as atividades realizadas em sua conta.</p>
            </div>
            <div className={style.DivContent}>
                <h2>Limitação de Responsabilidade</h2>
                <p>O serviço é fornecido "no estado em que se encontra", sem garantias expressas ou implícitas de qualquer tipo. A empresa não será responsável por danos diretos, indiretos, acidentais, especiais ou consequenciais decorrentes do uso ou da impossibilidade de uso dos serviços, mesmo que tenha sido avisada sobre a possibilidade de tais danos.</p>
            </div>
            <div className={style.DivContent}>
                <h2>Aceitação dos Termos</h2>
                <p>Ao acessar ou utilizar este site, serviço ou aplicativo, o usuário concorda em cumprir e estar vinculado aos Termos de Uso descritos abaixo, bem como a nossa Política de Privacidade. Caso o usuário não concorde com qualquer parte dos termos, não deverá utilizar nossos serviços.</p>
            </div>
            <div className={style.DivEspaco}></div>
            <Link href="./Cadastro" className={style.voltar}>Voltar</Link>
            <div className={style.DivEspaco}></div>
        </>
    )
}

export default  TermosDeUso;