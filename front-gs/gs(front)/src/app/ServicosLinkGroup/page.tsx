import Link from "next/link";
import Sidebar from "../Sidebar/page";
import styles from "./ServicosLinkGroup.module.css";
import "../reset.css";

const GrupoLinks = () => {
  return (
    <>
      <Sidebar />
      <div className={styles.container}>
        <div className={styles.conteudo}>
          <h1 className={styles.titulo}>Serviços</h1>
          <div className={styles.centralizando}>
            <Link href="./CalculadoraEnergetica_Requests" className={styles.link}>
              Cálculo de Gasto Mensal
            </Link>
            <Link href="./TransicaoEnergetica" className={styles.link}>
              Transição Energética
            </Link>
            <Link href="./CalculoCO2" className={styles.link}>
              Calculadora CO²
            </Link>
            <Link href="./PredicaoContinente" className={styles.link}>
              Predição de Continente
            </Link>
            <div className={styles.divisor}></div>
            <Link href="/" className={styles.voltar}>
              Voltar
            </Link>
          </div>
        </div>
      </div>
    </>
  );
};

export default GrupoLinks;
