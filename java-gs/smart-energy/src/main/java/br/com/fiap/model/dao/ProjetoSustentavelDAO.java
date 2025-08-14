package br.com.fiap.model.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import br.com.fiap.conexao.Conexao;
import br.com.fiap.model.vo.ProjetoSustentavelVO;
import br.com.fiap.model.vo.RegiaoSustentavelVO;
import br.com.fiap.model.vo.TipoFonteVO;

public class ProjetoSustentavelDAO {
    private Connection minhaConexao;

    public ProjetoSustentavelDAO() throws ClassNotFoundException, SQLException {
        this.minhaConexao = Conexao.getConnection();
    }

    public boolean inserir(ProjetoSustentavelVO projeto) throws SQLException {
        String sql = "INSERT INTO projetos_sustentaveis (ID_PROJETO, DESCRICAO, CUSTO, STATUS, ID_TIPO_FONTE, ID_REGIAO) "
                   + "VALUES (?, ?, ?, ?, ?, ?)";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setInt(1, projeto.getIdProjeto());
            stmt.setString(2, projeto.getDescricao());
            stmt.setDouble(3, projeto.getCusto());
            stmt.setString(4, projeto.getStatus());
            stmt.setInt(5, projeto.getTipoFonte().getIdTipoFonte());
            stmt.setInt(6, projeto.getRegiaoSustentavel().getIdRegiaoSustentavel());

            int rows = stmt.executeUpdate();
            return rows > 0;
        }
    }

    public boolean atualizar(ProjetoSustentavelVO projeto) throws SQLException {
        String sql = "UPDATE projetos_sustentaveis SET DESCRICAO = ?, CUSTO = ?, STATUS = ?, ID_TIPO_FONTE = ?, ID_REGIAO = ? "
                   + "WHERE ID_PROJETO = ?";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setString(1, projeto.getDescricao());
            stmt.setDouble(2, projeto.getCusto());
            stmt.setString(3, projeto.getStatus());
            stmt.setInt(4, projeto.getTipoFonte().getIdTipoFonte());
            stmt.setInt(5, projeto.getRegiaoSustentavel().getIdRegiaoSustentavel());
            stmt.setInt(6, projeto.getIdProjeto());

            int rows = stmt.executeUpdate();
            return rows > 0;
        }
    }

    public boolean deletar(int idProjeto) throws SQLException {
        String sql = "DELETE FROM projetos_sustentaveis WHERE ID_PROJETO = ?";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setInt(1, idProjeto);

            int rows = stmt.executeUpdate();
            return rows > 0;
        }
    }

    public ProjetoSustentavelVO buscarPorId(int idProjeto) throws SQLException {
        String sql = "SELECT * FROM projetos_sustentaveis WHERE ID_PROJETO = ?";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setInt(1, idProjeto);

            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return new ProjetoSustentavelVO(
                            rs.getInt("ID_PROJETO"),
                            rs.getString("DESCRICAO"),
                            rs.getDouble("CUSTO"),
                            rs.getString("STATUS"),
                            new TipoFonteVO(rs.getInt("ID_TIPO_FONTE"), null),
                            new RegiaoSustentavelVO(rs.getInt("ID_REGIAO"), null) 
                    );
                }
            }
        }
        return null;
    }

    public List<ProjetoSustentavelVO> listar() throws SQLException {
        List<ProjetoSustentavelVO> projetos = new ArrayList<>();
        String sql = "SELECT * FROM projetos_sustentaveis";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {

            while (rs.next()) {
                ProjetoSustentavelVO projeto = new ProjetoSustentavelVO(
                        rs.getInt("ID_PROJETO"),
                        rs.getString("DESCRICAO"),
                        rs.getDouble("CUSTO"),
                        rs.getString("STATUS"),
                        new TipoFonteVO(rs.getInt("ID_TIPO_FONTE"), null), 
                        new RegiaoSustentavelVO(rs.getInt("ID_REGIAO"), null) 
                );
                projetos.add(projeto);
            }
        }
        return projetos;  
    }
}
