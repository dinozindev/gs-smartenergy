package br.com.fiap.model.dao;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

import br.com.fiap.model.vo.TipoFonteVO;

public class TipoFonteDAO {
    private Connection connection;

    public TipoFonteDAO(Connection connection) {
        this.connection = connection;
    }

    public boolean inserir(TipoFonteVO tipoFonte) throws SQLException {
        String sql = "INSERT INTO tipo_fontes (ID_TIPO_FONTE, NOME_FONTE) VALUES (?, ?)";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setInt(1, tipoFonte.getIdTipoFonte());
            stmt.setString(2, tipoFonte.getNome());
            return stmt.executeUpdate() > 0;
        }
    }

    public boolean atualizar(TipoFonteVO tipoFonte) throws SQLException {
        String sql = "UPDATE tipo_fontes SET NOME_FONTE = ? WHERE ID_TIPO_FONTE = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, tipoFonte.getNome());
            stmt.setInt(2, tipoFonte.getIdTipoFonte());
            return stmt.executeUpdate() > 0;
        }
    }

    public boolean deletar(int idTipoFonte) throws SQLException {
        String sql = "DELETE FROM tipo_fontes WHERE ID_TIPO_FONTE = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setInt(1, idTipoFonte);
            return stmt.executeUpdate() > 0;
        }
    }

    public TipoFonteVO buscarPorId(int idTipoFonte) throws SQLException {
        String sql = "SELECT * FROM tipo_fontes WHERE ID_TIPO_FONTE = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setInt(1, idTipoFonte);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return new TipoFonteVO(
                        rs.getInt("ID_TIPO_FONTE"),
                        rs.getString("NOME_FONTE")
                    );
                }
            }
        }
        return null;
    }

    public List<TipoFonteVO> listar() throws SQLException {
        String sql = "SELECT * FROM tipo_fontes";
        List<TipoFonteVO> listaTipoFontes = new ArrayList<>();
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                listaTipoFontes.add(new TipoFonteVO(
                    rs.getInt("ID_TIPO_FONTE"),
                    rs.getString("NOME_FONTE")
                ));
            }
        }
        return listaTipoFontes;
    }
}
