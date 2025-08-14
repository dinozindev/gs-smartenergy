package br.com.fiap.model.bo;

import java.sql.SQLException;
import java.util.List;
import java.util.UUID;

import br.com.fiap.model.dao.ResidenciaDAO;
import br.com.fiap.model.bo.ResidenciaBO;
import br.com.fiap.model.vo.ResidenciaVO;

public class ResidenciaBO {

    private ResidenciaDAO residenciaDAO;

    public List<ResidenciaVO> listar() throws SQLException {
        try {
			residenciaDAO = new ResidenciaDAO();
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		} catch (SQLException e) {
			e.printStackTrace();
		}
        return residenciaDAO.selecionar();
    }

    public boolean inserir(ResidenciaVO residencia) throws SQLException, ClassNotFoundException {
    	residencia.setIdResidencia(UUID.randomUUID().toString());
        if (!validarResidencia(residencia)) {
            throw new IllegalArgumentException("Dados da residência inválidos.");
        }

        if (usuarioJaTemResidencia(residencia.getUsuario().getCpfUsuario())) {
            throw new IllegalStateException("Usuário já possui uma residência cadastrada.");
        }

        residenciaDAO = new ResidenciaDAO();
        return residenciaDAO.inserir(residencia);
    }

    public boolean atualizar(ResidenciaVO residencia) throws SQLException, ClassNotFoundException {
        if (!validarResidencia(residencia)) {
            throw new IllegalArgumentException("Dados da residência inválidos.");
        }

        residenciaDAO = new ResidenciaDAO();
        return residenciaDAO.atualizar(residencia);
    }

    public boolean deletar(String idResidencia) throws SQLException {
        try {
			residenciaDAO = new ResidenciaDAO();
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		} catch (SQLException e) {
			e.printStackTrace();
		}
        return residenciaDAO.deletar(idResidencia);
    }

    private boolean usuarioJaTemResidencia(String cpfUsuario) throws SQLException {
        try {
			residenciaDAO = new ResidenciaDAO();
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		} catch (SQLException e) {
			e.printStackTrace();
		}
        return residenciaDAO.existeResidenciaAssociada(cpfUsuario);
    }

    private boolean validarResidencia(ResidenciaVO residencia) throws ClassNotFoundException, SQLException {
        if (residencia == null) return false;
        if (!validarCep(residencia.getCep())) return false;
        if (!validarCpf(residencia.getUsuario().getCpfUsuario())) return false;
        if (residencia.getLogradouro() == null || residencia.getLogradouro().isEmpty()) return false;
        if (residencia.getLocalidade() == null || residencia.getLocalidade().isEmpty()) return false;
        if (residencia.getEstado() == null || residencia.getEstado().isEmpty()) return false;
        return true;
    }

    private boolean validarCep(String cep) {
        return cep != null && cep.matches("\\d{5}-\\d{3}");
    }

    private boolean validarCpf(String cpf) {
        return cpf != null && cpf.matches("\\d{11}");
    }
    
    public ResidenciaVO buscarPorId(String idResidencia) throws SQLException {
        try {
            residenciaDAO = new ResidenciaDAO();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return residenciaDAO.buscarPorId(idResidencia);
    }
    
    public ResidenciaVO buscarResidenciaPorCpf(String cpfUsuario) throws SQLException, ClassNotFoundException {
        residenciaDAO = new ResidenciaDAO();
        return residenciaDAO.buscarResidenciaPorCpf(cpfUsuario);
    }


}
