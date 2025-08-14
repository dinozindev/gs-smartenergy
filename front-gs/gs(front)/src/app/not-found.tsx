import Link from 'next/link';
import styles from './not-found.module.css';

export default function NotFound() {
    return (
        <div className={styles.notFoundContainer}>
            <h1 className={styles.errorCode}>404</h1>
            <p className={styles.message}>Oops! Uma pena não ser isso que você procura :(</p>
            <Link href="/">
                <button className={styles.homeButton}>Voltar para a página inicial</button>
            </Link>
        </div>
    );
}
