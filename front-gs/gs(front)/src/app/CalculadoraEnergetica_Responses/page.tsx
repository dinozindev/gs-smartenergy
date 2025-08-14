"use client";
import Sidebar from "../Sidebar/page";
import { useEffect, useState } from "react";
import styles from "./CalculadoraEnergetica_Responses.module.css";

const CalculadoraEnergeticaResponse = () => {
  const [dados, setDados] = useState(null);
  const [corDiv, setCorDiv] = useState("");
  const [mensagem, setMensagem] = useState("");
  const [statusPost, setStatusPost] = useState<string>("");
  const [envioConcluido, setEnvioConcluido] = useState(false); 
  const [cpfUsuario, setCpfUsuario] = useState(null);

  const mediaConsumo = 150;

  useEffect(() => {
    const dadosArmazenados = JSON.parse(localStorage.getItem("calculoEnergia"));
    const usuario = JSON.parse(localStorage.getItem("usuario"));

    if (dadosArmazenados && dadosArmazenados.totalMensal) {
      setDados(dadosArmazenados);
      setCpfUsuario(usuario?.cpfUsuario || null); 
      calcularStatus(dadosArmazenados.totalMensal);
    } else {
      setMensagem("Não há dados suficientes para exibir o consumo.");
      setCorDiv("grey");
    }
  }, []);

  const calcularStatus = (consumo) => {
    if (consumo < mediaConsumo) {
      setCorDiv("lightgreen");
      setMensagem("Parabéns! Seu consumo está abaixo da média.");
    } else if (consumo === mediaConsumo) {
      setCorDiv("yellow");
      setMensagem("Seu consumo está na média.");
    } else {
      setCorDiv("salmon");
      setMensagem(
        "Seu consumo está acima da média. Considere seguir as dicas para economizar."
      );
    }
  };

  const criarPrevisaoEnergetica = (gastoMensal: number) => {
    if (envioConcluido || !cpfUsuario) return;

    const dataHoje = new Date().toISOString().split('T')[0];

    const previsao = {
      dataPrevisao: dataHoje,
      gastoMensal: gastoMensal,
      status: "CONCLUIDO",
      cpf: cpfUsuario,
    };

    console.log("Dados da previsão:", previsao);

    fetch("http://127.0.0.1:8080/previsoes", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(previsao),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Erro na API: ${response.statusText}`);
        }
        return response.json();
      })
      .then((data) => {
        console.log("Resposta da API:", data);
        setStatusPost("Previsão energética criada com sucesso!");
        setEnvioConcluido(true); 
        
        const usuario = JSON.parse(localStorage.getItem("usuario"));
        usuario.gastoMensal = gastoMensal;

        localStorage.setItem("usuario", JSON.stringify(usuario));

        setDados((prevDados) => ({ ...prevDados, totalMensal: gastoMensal }));
      })
      .catch((error) => {
        console.error("Erro ao criar a previsão energética:", error);
        setStatusPost(`Erro ao criar a previsão energética: ${error.message}`);
      });
  };

  useEffect(() => {
    if (dados && !envioConcluido && dados.totalMensal) {
      criarPrevisaoEnergetica(dados.totalMensal);
    }
  }, [dados, envioConcluido]);

  return (
    <>
      <Sidebar />
      <h2 className={styles.titulo}>O seu gasto mensal é de {dados?.totalMensal || "0"} kWh</h2>
      <div
        className={styles.div}
        style={{
          backgroundColor: corDiv,
          padding: "1rem",
          borderRadius: "8px",
        }}
      >
        <p>{mensagem}</p>
      </div>
      {dados?.totalMensal > mediaConsumo && (
        <div className={styles.contprincipal}>
          <h2>Considere experimentar as seguintes dicas para economizar energia:</h2>
          <p>
            1 - Desligue aparelhos em stand-by.<br />
            2 - Troque lâmpadas por LEDs.<br />
            3 - Ajuste a temperatura da geladeira.<br />
            4 - Use ventiladores em vez de ar-condicionado.<br />
            5 - Lave roupas com água fria.<br />
          </p>
        </div>
      )}
      <div className={styles.status}>{statusPost && <p>{statusPost}</p>}</div>
    </>
  );
};

export default CalculadoraEnergeticaResponse;
