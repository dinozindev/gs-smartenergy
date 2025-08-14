import fs from "fs";
import path from "path";

export default function handler(req, res) {
  if (req.method === "POST") {
    // Caminho do arquivo JSON
    const filePath = path.join(process.cwd(), "Data", "residencias.json");

    // Dados enviados pelo cliente
    const novaResidencia = req.body;

    try {
      // Lê o arquivo existente ou cria um novo se não existir
      const fileContent = fs.existsSync(filePath)
        ? JSON.parse(fs.readFileSync(filePath, "utf-8"))
        : [];

      // Adiciona a nova residência
      fileContent.push(novaResidencia);

      // Salva o arquivo atualizado
      fs.writeFileSync(filePath, JSON.stringify(fileContent, null, 2), "utf-8");

      // Retorna sucesso
      res.status(200).json({ message: "Residência salva com sucesso!" });
    } catch (error) {
      console.error("Erro ao salvar a residência:", error);
      res.status(500).json({ message: "Erro ao salvar a residência." });
    }
  } else {
    // Método não permitido
    res.setHeader("Allow", ["POST"]);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
