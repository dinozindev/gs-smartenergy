package br.com.fiap.model.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import br.com.fiap.conexao.Conexao;
import br.com.fiap.model.vo.UserVO;

public class UserDAO {
	private Connection minhaConexao;

    public UserDAO() throws ClassNotFoundException, SQLException {
        this.minhaConexao = Conexao.getConnection();
    }
    public boolean inserir(UserVO usuario) throws SQLException {
        String sql = "INSERT INTO usuario (cpf_usuario, nome_usuario, email, telefone, senha, gasto_mensal) VALUES (?, ?, ?, ?, ?, ?)";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setString(1, usuario.getCpfUsuario());
            stmt.setString(2, usuario.getNomeUsuario());
            stmt.setString(3, usuario.getEmail());
            stmt.setString(4, usuario.getTelefone());
            stmt.setString(5, usuario.getSenha());
            stmt.setDouble(6, usuario.getGastoMensal());

            int rows = stmt.executeUpdate();
            return rows > 0;
        }
    }
    public boolean atualizar(UserVO usuario) throws SQLException {
        String sql = "UPDATE usuario SET nome_usuario = ?, email = ?, telefone = ?, senha = ?, gasto_mensal = ? WHERE cpf_usuario = ?";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setString(1, usuario.getNomeUsuario());
            stmt.setString(2, usuario.getEmail());
            stmt.setString(3, usuario.getTelefone());
            stmt.setString(4, usuario.getSenha());
            stmt.setDouble(5, usuario.getGastoMensal());
            stmt.setString(6, usuario.getCpfUsuario());

            int rows = stmt.executeUpdate();
            return rows > 0;
        }
    }
    public boolean deletar(String cpfUsuario) throws SQLException {
        String sql = "DELETE FROM usuario WHERE cpf_usuario = ?";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
            stmt.setString(1, cpfUsuario);

            int rows = stmt.executeUpdate();
            return rows > 0;
        }
    }
    public List<UserVO> selecionarTodos() throws SQLException {
        List<UserVO> usuarios = new ArrayList<>();
        String sql = "SELECT * FROM usuario";
        try (PreparedStatement stmt = minhaConexao.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {

            while (rs.next()) {
                UserVO usuario = new UserVO(
                        rs.getString("cpf_usuario"),
                        rs.getString("nome_usuario"),
                        rs.getString("senha"),
                        rs.getString("email"),
                        rs.getString("telefone"),
                        rs.getDouble("gasto_mensal")
                );
                usuarios.add(usuario);
            }
        }
        return usuarios;
    }

    public UserVO buscarPorCPF(String cpf) throws SQLException {
        String sql = "SELECT * FROM usuario WHERE cpf_usuario = ?";
        UserVO usuario = null;
        try (PreparedStatement ps = minhaConexao.prepareStatement(sql)) {
            ps.setString(1, cpf);
            try (ResultSet resultSet = ps.executeQuery()) {
                if (resultSet.next()) {
                    usuario = new UserVO(
                            resultSet.getString("cpf_usuario"),
                            resultSet.getString("nome_usuario"),
                            resultSet.getString("senha"),
                            resultSet.getString("email"),
                            resultSet.getString("telefone"),
                            resultSet.getDouble("gasto_mensal")
                    );
                }
            }
        }
        return usuario;
    }

    public UserVO buscarPorNomeUsuario(String nome) throws SQLException {
        String sql = "SELECT * FROM usuario WHERE nome_usuario = ?";
        UserVO usuario = null;
        try (PreparedStatement ps = minhaConexao.prepareStatement(sql)) {
            ps.setString(1, nome);
            try (ResultSet resultSet = ps.executeQuery()) {
                if (resultSet.next()) {
                    usuario = new UserVO(
                            resultSet.getString("cpf_usuario"),
                            resultSet.getString("nome_usuario"),
                            resultSet.getString("senha"),
                            resultSet.getString("email"),
                            resultSet.getString("telefone"),
                            resultSet.getDouble("gasto_mensal")
                    );
                }
            }
        }
        return usuario;
    }
}
