package br.com.fiap.model.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import br.com.fiap.conexao.Conexao;
import br.com.fiap.model.vo.ResidenciaVO;

public class ResidenciaDAO {
	private Connection minhaConexao;
	private UserDAO userDAO;

    public ResidenciaDAO() throws ClassNotFoundException, SQLException {
        this.minhaConexao = Conexao.getConnection();
        this.userDAO = new UserDAO();
    }

    public boolean inserir(ResidenciaVO residencia) throws SQLException {
        String sql = "INSERT INTO residencia (id_residencia, cep, logradouro, complemento, bairro, localidade, estado, numero, cpf_usuario) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setString(1, residencia.getIdResidencia());
            stmt.setString(2, residencia.getCep());
            stmt.setString(3, residencia.getLogradouro());
            stmt.setString(4, residencia.getComplemento());
            stmt.setString(5, residencia.getBairro());
            stmt.setString(6, residencia.getLocalidade());
            stmt.setString(7, residencia.getEstado());
            stmt.setInt(8, residencia.getNumero());
            stmt.setString(9, residencia.getUsuario().getCpfUsuario()); 

            int rows = stmt.executeUpdate();
            return rows > 0;
        }
    }

    public boolean atualizar(ResidenciaVO residencia) throws SQLException {
        String sql = "UPDATE residencia SET cep = ?, logradouro = ?, complemento = ?, bairro = ?, localidade = ?, estado = ?, numero = ?, cpf_usuario = ? WHERE id_residencia = ?";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setString(1, residencia.getCep());
            stmt.setString(2, residencia.getLogradouro());
            stmt.setString(3, residencia.getComplemento());
            stmt.setString(4, residencia.getBairro());
            stmt.setString(5, residencia.getLocalidade());
            stmt.setString(6, residencia.getEstado());
            stmt.setInt(7, residencia.getNumero());
            stmt.setString(8, residencia.getUsuario().getCpfUsuario());
            stmt.setString(9, residencia.getIdResidencia());

            int rows = stmt.executeUpdate();
            return rows > 0;
        }
    }

    public boolean deletar(String idResidencia) throws SQLException {
        String sql = "DELETE FROM residencia WHERE id_residencia = ?";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setString(1, idResidencia);

            int rows = stmt.executeUpdate();
            return rows > 0;
        }
    }

    public ResidenciaVO buscarPorId(String idResidencia) throws SQLException {
        String sql = "SELECT * FROM residencia WHERE id_residencia = ?";
        ResidenciaVO residencia = null;
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setString(1, idResidencia);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    residencia = new ResidenciaVO(
                            rs.getString("id_residencia"),
                            rs.getString("cep"),
                            rs.getString("logradouro"),
                            rs.getString("complemento"),
                            rs.getString("bairro"),
                            rs.getString("localidade"),
                            rs.getString("estado"),
                            rs.getInt("numero"),
                            userDAO.buscarPorCPF(rs.getString("cpf_usuario"))
                            
                    );
                }
            }
        }
        return residencia;
    }


    public List<ResidenciaVO> selecionar() throws SQLException {
        List<ResidenciaVO> residencias = new ArrayList<>();
        String sql = "SELECT * FROM residencia";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {

            while (rs.next()) {
                ResidenciaVO residencia = new ResidenciaVO(
                        rs.getString("id_residencia"),
                        rs.getString("cep"),
                        rs.getString("logradouro"),
                        rs.getString("complemento"),
                        rs.getString("bairro"),
                        rs.getString("localidade"),
                        rs.getString("estado"),
                        rs.getInt("numero"),
                        userDAO.buscarPorCPF(rs.getString("cpf_usuario"))
                );
                residencias.add(residencia);
            }
        }
        return residencias;
    }
    
    public boolean existeResidenciaAssociada(String cpfUsuario) throws SQLException {
        String sql = "SELECT COUNT(*) FROM residencia WHERE cpf_usuario = ?";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setString(1, cpfUsuario);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt(1) > 0;  
                }
            }
        }
        return false;  
    }
    
    public ResidenciaVO buscarResidenciaPorCpf(String cpfUsuario) throws SQLException {
        String sql = "SELECT * FROM residencia WHERE cpf_usuario = ?";
        ResidenciaVO residencia = null;

        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setString(1, cpfUsuario);

            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    residencia = new ResidenciaVO(
                            rs.getString("id_residencia"),
                            rs.getString("cep"),
                            rs.getString("logradouro"),
                            rs.getString("complemento"),
                            rs.getString("bairro"),
                            rs.getString("localidade"),
                            rs.getString("estado"),
                            rs.getInt("numero"),
                            userDAO.buscarPorCPF(rs.getString("cpf_usuario"))
                    );
                }
            }
        }

        return residencia;
    }

}
