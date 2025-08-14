package br.com.fiap.services;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import br.com.fiap.conexao.Conexao;
import br.com.fiap.model.vo.UserVO;

public class AuthenticationService {
	
	private Connection minhaConexao;
	
	public AuthenticationService() {
		try {
			this.minhaConexao = Conexao.getConnection();
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public UserVO autenticarUsuario(UserVO usuario) {
	    String sql = "SELECT * FROM usuario WHERE email = ? AND senha = ?";

	    try (PreparedStatement stmt = minhaConexao.prepareStatement(sql)) {
	        stmt.setString(1, usuario.getEmail());
	        stmt.setString(2, usuario.getSenha());

	        ResultSet rs = stmt.executeQuery();

	        if (rs.next()) { // Usuário encontrado
	            UserVO usuarioAutenticado = new UserVO();
	            usuarioAutenticado.setCpfUsuario(rs.getString("cpf_usuario"));
	            usuarioAutenticado.setNomeUsuario(rs.getString("nome_usuario"));
	            usuarioAutenticado.setEmail(rs.getString("email"));
	            usuarioAutenticado.setSenha(rs.getString("senha"));
	            usuarioAutenticado.setTelefone(rs.getString("telefone"));
	            usuarioAutenticado.setGastoMensal(rs.getDouble("gasto_mensal"));

	            return usuarioAutenticado;
	        }

	    } catch (SQLException e) {
	        e.printStackTrace();
	    }

	    return null; // Usuário não encontrado ou erro na consulta
	}
}
