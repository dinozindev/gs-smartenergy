package br.com.fiap.model.bo;

import java.sql.SQLException;
import java.util.List;

import br.com.fiap.model.dao.ProjetoSustentavelDAO;
import br.com.fiap.model.vo.ProjetoSustentavelVO;

public class ProjetoSustentavelBO {
    ProjetoSustentavelDAO projetoDAO = null;

    public boolean inserir(ProjetoSustentavelVO projeto) throws SQLException, ClassNotFoundException {
        projetoDAO = new ProjetoSustentavelDAO();

        if (!validarProjeto(projeto)) {
            throw new IllegalArgumentException("Dados do projeto sustentavel inválidos.");
        }
        return projetoDAO.inserir(projeto);
    }

    public boolean atualizar(ProjetoSustentavelVO projeto) throws SQLException, ClassNotFoundException {
        projetoDAO = new ProjetoSustentavelDAO();

        if (!validarProjeto(projeto)) {
            throw new IllegalArgumentException("Dados do projeto sustentavel inválidos.");
        }
        return projetoDAO.atualizar(projeto);
    }

    public boolean deletar(int idProjeto) throws SQLException, ClassNotFoundException {
        projetoDAO = new ProjetoSustentavelDAO();

        if (idProjeto <= 0) {
            throw new IllegalArgumentException("ID inválido.");
        }
        return projetoDAO.deletar(idProjeto);
    }

    public ProjetoSustentavelVO buscarPorId(int idProjeto) throws SQLException, ClassNotFoundException {
        projetoDAO = new ProjetoSustentavelDAO();

        if (idProjeto <= 0) {
            throw new IllegalArgumentException("ID inválido.");
        }
        return projetoDAO.buscarPorId(idProjeto);
    }

    public List<ProjetoSustentavelVO> listar() throws SQLException, ClassNotFoundException {
        projetoDAO = new ProjetoSustentavelDAO();
        return projetoDAO.listar();
    }

    private boolean validarProjeto(ProjetoSustentavelVO projeto) {
        if (projeto == null) return false;
        if (projeto.getDescricao() == null || projeto.getDescricao().isEmpty()) return false;
        if (projeto.getCusto() <= 0) return false;
        if (projeto.getStatus() == null || projeto.getStatus().isEmpty()) return false;
        if (projeto.getTipoFonte() == null || projeto.getTipoFonte().getIdTipoFonte() <= 0) return false;
        if (projeto.getRegiaoSustentavel() == null || projeto.getRegiaoSustentavel().getIdRegiaoSustentavel() <= 0) return false;
        return true; 
    }
}