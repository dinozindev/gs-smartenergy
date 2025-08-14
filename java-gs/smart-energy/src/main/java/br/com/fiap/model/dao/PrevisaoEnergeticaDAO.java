package br.com.fiap.model.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import br.com.fiap.conexao.Conexao;
import br.com.fiap.model.vo.PrevisaoEnergeticaVO;

public class PrevisaoEnergeticaDAO {
	private Connection minhaConexao;
	private UserDAO userDAO;

    public PrevisaoEnergeticaDAO() throws ClassNotFoundException, SQLException {
        this.minhaConexao = Conexao.getConnection();
        this.userDAO = new UserDAO();
    }

    public boolean inserir(PrevisaoEnergeticaVO previsao) throws SQLException {
    	try {
            String sqlInserir = "INSERT INTO previsao_energetica (PREVISAO_ID, PREVISAO_DATA, PREVISAO_GASTO, PREVISAO_STATUS, CPF_USUARIO) "
                                + "VALUES (?, ?, ?, ?, ?)";
            try (PreparedStatement stmt = minhaConexao.prepareStatement(sqlInserir)) {
                stmt.setString(1, previsao.getIdPrevisao()); 
                stmt.setDate(2, previsao.getData()); 
                stmt.setDouble(3, previsao.getPrevisaoGasto());
                stmt.setString(4, previsao.getStatusPrevisao());
                stmt.setString(5, previsao.getUsuario().getCpfUsuario()); 

                int rows = stmt.executeUpdate();
                if (rows <= 0) {
                    return false; 
                }
            }

            String sqlAtualizarUsuario = "UPDATE usuario SET gasto_mensal = ? WHERE cpf_usuario = ?";
            try (PreparedStatement stmt = minhaConexao.prepareStatement(sqlAtualizarUsuario)) {
                stmt.setDouble(1, previsao.getPrevisaoGasto());  
                stmt.setString(2, previsao.getUsuario().getCpfUsuario()); 

                int rows = stmt.executeUpdate();
                return rows > 0; 
            }

        } catch (SQLException e) {
            throw new SQLException("Erro ao inserir previsão energética e atualizar gasto mensal do usuário.", e);
        }
    }

    public boolean atualizar(PrevisaoEnergeticaVO previsao) throws SQLException {
        String sql = "UPDATE previsao_energetica SET PREVISAO_DATA = ?, PREVISAO_GASTO = ?, PREVISAO_STATUS = ?, CPF_USUARIO = ? "
                + "WHERE PREVISAO_ID = ?";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setDate(1, previsao.getData()); 
            stmt.setDouble(2, previsao.getPrevisaoGasto());
            stmt.setString(3, previsao.getStatusPrevisao());
            stmt.setString(4, previsao.getUsuario().getCpfUsuario());
            stmt.setString(5, previsao.getIdPrevisao());

            int rows = stmt.executeUpdate();
            return rows > 0;
        }
    }

    public boolean deletar(String idPrevisao) throws SQLException {
        String sql = "DELETE FROM previsao_energetica WHERE PREVISAO_ID = ?";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setString(1, idPrevisao);

            int rows = stmt.executeUpdate();
            return rows > 0;
        }
    }

    public PrevisaoEnergeticaVO buscarPorId(String idPrevisao) throws SQLException {
        String sql = "SELECT * FROM previsao_energetica WHERE PREVISAO_ID = ?";
        PrevisaoEnergeticaVO previsao = null;
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setString(1, idPrevisao);

            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    previsao = new PrevisaoEnergeticaVO(
                            rs.getString("PREVISAO_ID"),
                            rs.getDate("PREVISAO_DATA"), 
                            rs.getDouble("PREVISAO_GASTO"),
                            rs.getString("PREVISAO_STATUS"),
                            userDAO.buscarPorCPF(rs.getString("CPF_USUARIO"))
                    );
                }
            }
        }
        return previsao;
    }


    public List<PrevisaoEnergeticaVO> listar() throws SQLException {
        List<PrevisaoEnergeticaVO> previsoes = new ArrayList<>();
        String sql = "SELECT * FROM previsao_energetica";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {

            while (rs.next()) {
                PrevisaoEnergeticaVO previsao = new PrevisaoEnergeticaVO(
                        rs.getString("PREVISAO_ID"),
                        rs.getDate("PREVISAO_DATA"), 
                        rs.getDouble("PREVISAO_GASTO"),
                        rs.getString("PREVISAO_STATUS"),
                        userDAO.buscarPorCPF(rs.getString("CPF_USUARIO"))
                );
                previsoes.add(previsao);
            }
        }
        return previsoes;
    }
    
    
    public String buscarResidenciaPorCpf(String cpf) throws SQLException {
        String sql = "SELECT RESIDENCIA_ENDERECO FROM usuario WHERE CPF_USUARIO = ?";
        String enderecoResidencia = null;
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setString(1, cpf);

            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    enderecoResidencia = rs.getString("RESIDENCIA_ENDERECO");
                }
            }
        }
        return enderecoResidencia;
    }
    
 // No PrevisaoEnergeticaDAO
    public List<PrevisaoEnergeticaVO> buscarPrevisaoPorCpf(String cpfUsuario) throws SQLException {
        List<PrevisaoEnergeticaVO> previsoes = new ArrayList<>();
        String sql = "SELECT * FROM previsao_energetica WHERE CPF_USUARIO = ?";

        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setString(1, cpfUsuario);
            ResultSet rs = stmt.executeQuery();

            while (rs.next()) {
                PrevisaoEnergeticaVO previsao = new PrevisaoEnergeticaVO(
                        rs.getString("PREVISAO_ID"),
                        rs.getDate("PREVISAO_DATA"),
                        rs.getDouble("PREVISAO_GASTO"),
                        rs.getString("PREVISAO_STATUS"),
                        userDAO.buscarPorCPF(rs.getString("CPF_USUARIO"))
                );
                previsoes.add(previsao);
            }
        }

        return previsoes;
    }

    

}
