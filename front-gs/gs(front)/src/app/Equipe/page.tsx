import Sidebar from "../Sidebar/page";
import styles from "./Equipe.module.css"

import { CiLinkedin } from "react-icons/ci";
import { FaGithub } from "react-icons/fa";

const equipe = () => {
    return (
        <>
            <Sidebar></Sidebar>
            <h1 className={styles.title}>Equipe</h1>
            <div className={styles.container}>
                    <div className={styles.div1}>
                        <img src="./Imagens/Roz.png" alt="" className={styles.img}></img>
                        <h2 className={styles.text1}>Rm 558981</h2>
                        <p className={styles.text2}>Uma jovem desenvolvedora da turma 1 TDSB que realiza seu trabalho com excelência</p>
                        <a href="https://www.linkedin.com/in/giovanna-revito-roz-1b4050239/" target="blank" ><CiLinkedin  className={styles.icon1}/></a>
                        <a href="https://github.com/giovannarevitoroz" target="blank"><FaGithub className={styles.icon1}/></a>
                    </div>
                    <div className={`${styles.div1} ${styles.div2}`}>
                        <img src="./Imagens/Kaian.png" alt="" className={styles.img} />
                        <h2 className={styles.text1}>Rm 558986</h2>
                        <p className={styles.text2}>Um jovem desenvolvedor da turma 1 TDSB que realiza seu trabalho com excelência</p>
                        <a href="https://www.linkedin.com/in/kaian-gustavo-b12b2b218/" target="blank" ><CiLinkedin  className={styles.icon1}/></a>
                        <a href="https://github.com/kaianGU" target="blank"><FaGithub className={styles.icon1}/></a>
                    </div>
                    <div className={styles.div1}>
                    <img src="./Imagens/Kenji.png" alt="" className={styles.img} />
                    <h2 className={styles.text1}>Rm 554424</h2>
                        <p className={styles.text2}>Um jovem desenvolvedor da turma 1 TDSB que realiza seu trabalho com excelência</p>
                        <a href="https://www.linkedin.com/in/lucas-kenji-kikuchi-233802287/" target="blank" ><CiLinkedin  className={styles.icon1}/></a>
                        <a href="https://github.com/dinozindev" target="blank"><FaGithub className={styles.icon1}/></a>
                    </div>
            </div>
        </>
    )
}

export default  equipe;