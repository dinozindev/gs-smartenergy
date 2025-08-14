import Image from "next/image";
import Sidebar from "./Sidebar/page";
import styles from "./homeestilo.module.css";
import "./reset.css";
import Link from "next/link";
export default function Home() {
  return (
   <>
    <div className={styles.container}> 
       <img src="./Imagens/Logo.png" alt="" className={styles.logo} />
      
       <Link href="./Sobre" className={styles.link}>Sobre</Link>
       <Link href="./ServicosLinkGroup" className={styles.link}>Serviços</Link>
       <Link href="./Equipe" className={styles.link}>Equipe</Link>
       <Link href="./Projetos" className={styles.link}>Projetos</Link>


       <h1 className={styles.titulo}>Energia Inteligente e Soluções Sustentáveis</h1>
       <p className={styles.texto}>Descubra como prever seu consumo. Acesse nosso sistema de predição agora!</p>
       <Link href="./ServicosLinkGroup" className={styles.botao}>Confira</Link>
    </div>
   </>
  );
}
