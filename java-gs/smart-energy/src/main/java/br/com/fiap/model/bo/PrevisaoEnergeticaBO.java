package br.com.fiap.model.bo;

import java.sql.SQLException;
import java.util.List;
import java.util.UUID;

import br.com.fiap.model.dao.PrevisaoEnergeticaDAO;
import br.com.fiap.model.vo.PrevisaoEnergeticaVO;

public class PrevisaoEnergeticaBO {
    private PrevisaoEnergeticaDAO dao;

    public PrevisaoEnergeticaBO() throws ClassNotFoundException, SQLException {
        this.dao = new PrevisaoEnergeticaDAO();
    }

    public PrevisaoEnergeticaVO inserir(PrevisaoEnergeticaVO previsao) {
        validarPrevisao(previsao);
        try {
        	previsao.setIdPrevisao(UUID.randomUUID().toString());
            boolean sucesso = dao.inserir(previsao);
            if (sucesso) {
                return previsao;
            } else {
                throw new IllegalStateException("Erro ao inserir previsão energética.");
            }
        } catch (SQLException e) {
            throw new RuntimeException("Erro ao acessar o banco de dados: " + e.getMessage(), e);
        }
    }

    public List<PrevisaoEnergeticaVO> listar() {
        try {
            return dao.listar();
        } catch (SQLException e) {
            throw new RuntimeException("Erro ao acessar o banco de dados: " + e.getMessage(), e);
        }
    }

    public PrevisaoEnergeticaVO buscarPorId(String idPrevisao) {
        validarId(idPrevisao);
        try {
            PrevisaoEnergeticaVO previsao = dao.buscarPorId(idPrevisao);
            if (previsao != null) {
                return previsao;
            } else {
                throw new IllegalArgumentException("Previsão não encontrada com o ID informado.");
            }
        } catch (SQLException e) {
            throw new RuntimeException("Erro ao acessar o banco de dados: " + e.getMessage(), e);
        }
    }

    public PrevisaoEnergeticaVO atualizar(String idPrevisao, PrevisaoEnergeticaVO novaPrevisao) {
        validarId(idPrevisao);
        validarPrevisao(novaPrevisao);
        try {
            PrevisaoEnergeticaVO previsaoExistente = buscarPorId(idPrevisao);
            previsaoExistente.setData(novaPrevisao.getData());
            previsaoExistente.setPrevisaoGasto(novaPrevisao.getPrevisaoGasto());
            previsaoExistente.setStatusPrevisao(novaPrevisao.getStatusPrevisao());
            previsaoExistente.setUsuario(novaPrevisao.getUsuario());

            boolean sucesso = dao.atualizar(previsaoExistente);
            if (sucesso) {
                return previsaoExistente;
            } else {
                throw new IllegalStateException("Erro ao atualizar previsão energética.");
            }
        } catch (SQLException e) {
            throw new RuntimeException("Erro ao acessar o banco de dados: " + e.getMessage(), e);
        }
    }

    public void deletar(String idPrevisao) {
        validarId(idPrevisao);
        try {
            boolean sucesso = dao.deletar(idPrevisao);
            if (!sucesso) {
                throw new IllegalArgumentException("Previsão não encontrada ou já removida.");
            }
        } catch (SQLException e) {
            throw new RuntimeException("Erro ao acessar o banco de dados: " + e.getMessage(), e);
        }
    }


    private void validarPrevisao(PrevisaoEnergeticaVO previsao) {
        if (previsao == null) {
            throw new IllegalArgumentException("A previsão energética não pode ser nula.");
        }
        if (previsao.getData() == null) {
            throw new IllegalArgumentException("A data da previsão deve ser informada.");
        }
        if (previsao.getPrevisaoGasto() <= 0) {
            throw new IllegalArgumentException("O gasto previsto deve ser maior que zero.");
        }
        if (previsao.getStatusPrevisao() == null || previsao.getStatusPrevisao().isBlank()) {
            throw new IllegalArgumentException("O status da previsão deve ser informado.");
        }
        if (previsao.getUsuario() == null || 
            previsao.getUsuario().getCpfUsuario() == null || 
            !previsao.getUsuario().getCpfUsuario().matches("\\d{11}")) {
            throw new IllegalArgumentException("O CPF do usuário deve ser válido e conter 11 dígitos.");
        }
    }

    private void validarId(String idPrevisao) {
        if (idPrevisao == null || idPrevisao.isBlank()) {
            throw new IllegalArgumentException("O ID da previsão não pode ser nulo ou vazio.");
        }
    }
    
    public String buscarResidenciaPorCpf(String cpf) throws SQLException {
        return dao.buscarResidenciaPorCpf(cpf);
    }
    
    
    public List<PrevisaoEnergeticaVO> listarPrevisaoPorCpf(String cpfUsuario) {
        if (cpfUsuario == null || cpfUsuario.isEmpty()) {
            throw new IllegalArgumentException("O CPF do usuário não pode ser nulo ou vazio.");
        }
        try {
            return dao.buscarPrevisaoPorCpf(cpfUsuario);
        } catch (SQLException e) {
            throw new RuntimeException("Erro ao acessar o banco de dados: " + e.getMessage(), e);
        }
    }

    
}
