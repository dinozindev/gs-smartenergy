package br.com.fiap.model.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import br.com.fiap.conexao.Conexao;
import br.com.fiap.model.vo.RegiaoSustentavelVO;

public class RegiaoSustentavelDAO {
    private Connection minhaConexao;

    public RegiaoSustentavelDAO() throws ClassNotFoundException, SQLException {
        this.minhaConexao = Conexao.getConnection();
    }

    public boolean inserir(RegiaoSustentavelVO regiao) throws SQLException {
        String sql = "INSERT INTO regioes_sustentaveis (ID_REGIAO, NOME) VALUES (?, ?)";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setInt(1, regiao.getIdRegiaoSustentavel());
            stmt.setString(2, regiao.getNome());
            return stmt.executeUpdate() > 0;
        }
    }

    public boolean atualizar(RegiaoSustentavelVO regiao) throws SQLException {
        String sql = "UPDATE regioes_sustentaveis SET NOME = ? WHERE ID_REGIAO = ?";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setString(1, regiao.getNome());
            stmt.setInt(2, regiao.getIdRegiaoSustentavel());
            return stmt.executeUpdate() > 0;
        }
    }

    public boolean deletar(int idRegiao) throws SQLException {
        String sql = "DELETE FROM regioes_sustentaveis WHERE ID_REGIAO = ?";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setInt(1, idRegiao);
            return stmt.executeUpdate() > 0;
        }
    }

    public RegiaoSustentavelVO buscarPorId(int idRegiao) throws SQLException {
        String sql = "SELECT * FROM regioes_sustentaveis WHERE ID_REGIAO = ?";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setInt(1, idRegiao);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return new RegiaoSustentavelVO(
                        rs.getInt("ID_REGIAO"),
                        rs.getString("NOME")
                    );
                }
            }
        }
        return null;
    }

    public List<RegiaoSustentavelVO> listar() throws SQLException {
        List<RegiaoSustentavelVO> regioes = new ArrayList<>();
        String sql = "SELECT * FROM regioes_sustentaveis";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            while (rs.next()) {
                regioes.add(new RegiaoSustentavelVO(
                    rs.getInt("ID_REGIAO"),
                    rs.getString("NOME")
                ));
            }
        }
        return regioes;
    }
}
