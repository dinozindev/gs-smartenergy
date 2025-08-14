package br.com.fiap.model.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import br.com.fiap.conexao.Conexao;
import br.com.fiap.model.vo.EmissaoCarbonoVO;
import br.com.fiap.model.vo.TipoFonteVO;

public class EmissaoCarbonoDAO {
    private Connection minhaConexao;

    public EmissaoCarbonoDAO() throws ClassNotFoundException, SQLException {
        this.minhaConexao = Conexao.getConnection();
    }

    public boolean inserir(EmissaoCarbonoVO emissao) throws SQLException {
        String sql = "INSERT INTO emissoes_carbono (TIPO_FONTE_ID, EMISSAO) VALUES (?, ?)";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setInt(1, emissao.getTipoFonte().getIdTipoFonte());
            stmt.setDouble(2, emissao.getEmissao());

            int rows = stmt.executeUpdate();
            return rows > 0;
        }
    }

    public boolean atualizar(EmissaoCarbonoVO emissao) throws SQLException {
        String sql = "UPDATE emissoes_carbono SET TIPO_FONTE_ID = ?, EMISSAO = ? WHERE EMISSAO_ID = ?";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setInt(1, emissao.getTipoFonte().getIdTipoFonte());
            stmt.setDouble(2, emissao.getEmissao());
            stmt.setInt(3, emissao.getIdEmissao());

            int rows = stmt.executeUpdate();
            return rows > 0;
        }
    }

    public boolean deletar(int idEmissao) throws SQLException {
        String sql = "DELETE FROM emissoes_carbono WHERE EMISSAO_ID = ?";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setInt(1, idEmissao);

            int rows = stmt.executeUpdate();
            return rows > 0;
        }
    }

    public EmissaoCarbonoVO buscarPorId(int idEmissao) throws SQLException {
        String sql = "SELECT * FROM emissoes_carbono WHERE EMISSAO_ID = ?";
        EmissaoCarbonoVO emissao = null;
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setInt(1, idEmissao);

            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    emissao = new EmissaoCarbonoVO(
                        rs.getInt("EMISSAO_ID"),
                        new TipoFonteVO(rs.getInt("TIPO_FONTE_ID"), null), // Assumindo que o TipoFonteVO tem um construtor parcial
                        rs.getDouble("EMISSAO")
                    );
                }
            }
        }
        return emissao;
    }

    public List<EmissaoCarbonoVO> listar() throws SQLException {
        List<EmissaoCarbonoVO> emissoes = new ArrayList<>();
        String sql = "SELECT * FROM emissoes_carbono";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {

            while (rs.next()) {
                EmissaoCarbonoVO emissao = new EmissaoCarbonoVO(
                    rs.getInt("EMISSAO_ID"),
                    new TipoFonteVO(rs.getInt("TIPO_FONTE_ID"), null), 
                    rs.getDouble("EMISSAO")
                );
                emissoes.add(emissao);
            }
        }
        return emissoes;
    }
}
