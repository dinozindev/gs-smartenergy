package br.com.fiap.model.bo;

import java.sql.SQLException;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import br.com.fiap.model.dao.UserDAO;
import br.com.fiap.model.vo.UserVO;

public class UserBO {
	private UserDAO userDAO = null;

    public boolean inserir(UserVO usuario) throws SQLException, ClassNotFoundException {
    	userDAO = new UserDAO();
    	
        if (usuario == null) {
            throw new IllegalArgumentException("Usuário não pode ser nulo");
        }
        if (usuario.getCpfUsuario() == null || usuario.getCpfUsuario().isEmpty()) {
            throw new IllegalArgumentException("CPF do usuário é obrigatório");
        }
        if (usuario.getNomeUsuario() == null || usuario.getNomeUsuario().isEmpty()) {
            throw new IllegalArgumentException("Nome do usuário é obrigatório");
        }
        if (usuario.getEmail() == null || usuario.getEmail().isEmpty()) {
            throw new IllegalArgumentException("Email do usuário é obrigatório");
        }
        if (usuario.getTelefone() == null || usuario.getTelefone().isEmpty()) {
            throw new IllegalArgumentException("Telefone do usuário é obrigatório");
        }
        if (usuario.getSenha() == null || usuario.getSenha().isEmpty()) {
            throw new IllegalArgumentException("Senha do usuário é obrigatória");
        }
        if (userDAO.buscarPorCPF(usuario.getCpfUsuario()) != null) {
            throw new IllegalArgumentException("Já existe um usuário com esse CPF");
        }

        return userDAO.inserir(usuario);
    }

    public boolean atualizar(UserVO usuario) throws SQLException, ClassNotFoundException {
    	userDAO = new UserDAO();
        validarDados(usuario);

        if (userDAO.buscarPorCPF(usuario.getCpfUsuario()) == null) {
            throw new IllegalArgumentException("Usuário não encontrado para atualização");
        }

        return userDAO.atualizar(usuario);
    }

    public boolean deletar(String cpfUsuario) throws SQLException, ClassNotFoundException {
    	userDAO = new UserDAO();
        if (cpfUsuario == null || cpfUsuario.isEmpty()) {
            throw new IllegalArgumentException("CPF do usuário é obrigatório para exclusão");
        }

        if (userDAO.buscarPorCPF(cpfUsuario) == null) {
            throw new IllegalArgumentException("Usuário não encontrado para exclusão");
        }

        return userDAO.deletar(cpfUsuario);
    }

    public List<UserVO> listar() throws SQLException, ClassNotFoundException {
    	userDAO = new UserDAO();

    	return userDAO.selecionarTodos();
    }
    
    public UserVO buscarPorCpf(String cpf) throws SQLException, ClassNotFoundException {
    	userDAO = new UserDAO();
    	
        if (cpf == null || cpf.isEmpty()) {
            throw new IllegalArgumentException("CPF do usuário é obrigatório para busca");
        }

        UserVO usuario = userDAO.buscarPorCPF(cpf);
        if (usuario == null) {
            throw new IllegalArgumentException("Usuário não encontrado com o CPF fornecido");
        }

        return usuario;
    }

    public UserVO buscarPorNome(String nome) throws SQLException, ClassNotFoundException {
    	userDAO = new UserDAO();
    	
        if (nome == null || nome.isEmpty()) {
            throw new IllegalArgumentException("Nome do usuário é obrigatório para busca");
        }

        UserVO usuario = userDAO.buscarPorNomeUsuario(nome);
        if (usuario == null) {
            throw new IllegalArgumentException("Usuário não encontrado com o nome fornecido");
        }

        return usuario;
    }

    private void validarDados(UserVO usuario) {
        if (usuario == null) {
            throw new IllegalArgumentException("Usuário não pode ser nulo");
        }
        if (usuario.getCpfUsuario() == null || usuario.getCpfUsuario().isEmpty()) {
            throw new IllegalArgumentException("CPF do usuário é obrigatório");
        }
        if (!validarCPF(usuario.getCpfUsuario())) {
            throw new IllegalArgumentException("CPF inválido");
        }
        if (usuario.getNomeUsuario() == null || usuario.getNomeUsuario().isEmpty()) {
            throw new IllegalArgumentException("Nome do usuário é obrigatório");
        }
        if (usuario.getEmail() == null || usuario.getEmail().isEmpty()) {
            throw new IllegalArgumentException("Email do usuário é obrigatório");
        }
        if (!validarEmail(usuario.getEmail())) {
            throw new IllegalArgumentException("Email inválido");
        }
        if (usuario.getTelefone() == null || usuario.getTelefone().isEmpty()) {
            throw new IllegalArgumentException("Telefone do usuário é obrigatório");
        }
        if (usuario.getSenha() == null || usuario.getSenha().isEmpty()) {
            throw new IllegalArgumentException("Senha do usuário é obrigatória");
        }
        if (usuario.getSenha().length() <= 6) {
            throw new IllegalArgumentException("Senha do usuário deve ter mais que 6 caracteres");
        }
    }

    private boolean validarCPF(String cpf) {
        String regex = "^[0-9]{11}$";
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(cpf);
        return matcher.matches();
    }

    private boolean validarEmail(String email) {
        String regex = "^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$";
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(email);
        return matcher.matches();
    }
}
