package br.com.fiap.model.bo;

import java.sql.SQLException;
import java.util.List;

import br.com.fiap.model.dao.RegiaoSustentavelDAO;
import br.com.fiap.model.vo.RegiaoSustentavelVO;

public class RegiaoSustentavelBO {
    private RegiaoSustentavelDAO regiaoDAO;

    public RegiaoSustentavelBO() throws ClassNotFoundException, SQLException {
        this.regiaoDAO = new RegiaoSustentavelDAO();
    }

    public boolean inserir(RegiaoSustentavelVO regiao) throws SQLException {
        return regiaoDAO.inserir(regiao);
    }

    public boolean atualizar(RegiaoSustentavelVO regiao) throws SQLException {
        return regiaoDAO.atualizar(regiao);
    }

    public boolean deletar(int idRegiao) throws SQLException {
        return regiaoDAO.deletar(idRegiao);
    }

    public RegiaoSustentavelVO buscarPorId(int idRegiao) throws SQLException {
        return regiaoDAO.buscarPorId(idRegiao);
    }

    public List<RegiaoSustentavelVO> listar() throws SQLException {
        return regiaoDAO.listar();
    }
}
