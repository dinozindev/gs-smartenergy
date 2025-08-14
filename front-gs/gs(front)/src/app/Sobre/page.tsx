import Sidebar from "../Sidebar/page";
import styles from "./Sobre.module.css";

const Sobre = () => {

    return (

        <>
        <Sidebar></Sidebar>
            <p className={styles.texto}>
            <span className={styles.negrito}>Mudando o mundo por meio da tecnologia sustentavel</span><br />
            </p>
            <p className={styles.texto3}>
            A Smartenergy é uma empresa comprometida em transformar o setor energético, oferecendo soluções inovadoras e sustentáveis para otimizar o consumo e a gestão de energia. 
            </p>      
            <img src="./Imagens/Logo.png" alt=""  className={styles.imgLOGO}/>
            <p className={styles.texto2}>
            <span className={styles.negrito}>Objetivo</span><br />
           </p>
           <div className={styles.espaco}></div>
           <p className={styles.texto4}>
            Nosso objetivo é fornecer tecnologias e serviços que integrem eficiência energética, inteligência e conectividade, capacitando empresas e residências a reduzir custos e impactar positivamente o meio ambiente. Por meio de sistemas de monitoramento, automação e análise de dados, buscamos não apenas a economia, mas também a criação de um futuro mais inteligente e sustentável para todos.
            </p>   
        </>
    )
}

export default  Sobre;