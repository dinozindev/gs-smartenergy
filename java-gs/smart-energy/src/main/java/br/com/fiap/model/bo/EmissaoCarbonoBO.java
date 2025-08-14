package br.com.fiap.model.bo;

import java.sql.SQLException;
import java.util.List;

import br.com.fiap.model.dao.EmissaoCarbonoDAO;
import br.com.fiap.model.vo.EmissaoCarbonoVO;

public class EmissaoCarbonoBO {
    private EmissaoCarbonoDAO emissaoDAO;

    public EmissaoCarbonoBO() {
        try {
			this.emissaoDAO = new EmissaoCarbonoDAO();
		} catch (ClassNotFoundException | SQLException e) {
			e.printStackTrace();
		}
    }

    public boolean inserir(EmissaoCarbonoVO emissao) throws SQLException, ClassNotFoundException {
        validarEmissaoOuLancarExcecao(emissao);
        return emissaoDAO.inserir(emissao);
    }

    public boolean atualizar(EmissaoCarbonoVO emissao) throws SQLException, ClassNotFoundException {
        validarEmissaoOuLancarExcecao(emissao);
        return emissaoDAO.atualizar(emissao);
    }

    public boolean deletar(int idEmissao) throws SQLException, ClassNotFoundException {
        validarIdOuLancarExcecao(idEmissao);
        return emissaoDAO.deletar(idEmissao);
    }

    public EmissaoCarbonoVO buscarPorId(int idEmissao) throws SQLException, ClassNotFoundException {
        validarIdOuLancarExcecao(idEmissao);
        return emissaoDAO.buscarPorId(idEmissao);
    }

    public List<EmissaoCarbonoVO> listar() throws SQLException, ClassNotFoundException {
        return emissaoDAO.listar();
    }


    private void validarEmissaoOuLancarExcecao(EmissaoCarbonoVO emissao) {
        if (!validarEmissao(emissao)) {
            throw new IllegalArgumentException("Dados de emissão de carbono inválidos.");
        }
    }

    private void validarIdOuLancarExcecao(int id) {
        if (id <= 0) {
            throw new IllegalArgumentException("ID inválido.");
        }
    }

    private boolean validarEmissao(EmissaoCarbonoVO emissao) {
        return emissao != null 
                && emissao.getIdEmissao() > 0 
                && emissao.getTipoFonte() != null 
                && emissao.getTipoFonte().getIdTipoFonte() > 0 
                && emissao.getEmissao() >= 0; 
    }
    

}
