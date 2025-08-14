package br.com.fiap.model.bo;

import br.com.fiap.model.dao.TipoFonteDAO;
import br.com.fiap.model.vo.TipoFonteVO;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.List;

public class TipoFonteBO {
    private TipoFonteDAO tipoFonteDAO;

    public TipoFonteBO(Connection connection) {
        this.tipoFonteDAO = new TipoFonteDAO(connection);
    }

    public boolean inserir(TipoFonteVO tipoFonte) throws SQLException {
        if (tipoFonte.getNome() == null || tipoFonte.getNome().isEmpty()) {
            throw new IllegalArgumentException("Nome do tipo de fonte não pode ser vazio.");
        }
        return tipoFonteDAO.inserir(tipoFonte);
    }

    public boolean atualizar(TipoFonteVO tipoFonte) throws SQLException {
        if (tipoFonte.getIdTipoFonte() <= 0) {
            throw new IllegalArgumentException("ID do tipo de fonte inválido.");
        }
        return tipoFonteDAO.atualizar(tipoFonte);
    }

    public boolean deletar(int idTipoFonte) throws SQLException {
        if (idTipoFonte <= 0) {
            throw new IllegalArgumentException("ID do tipo de fonte inválido.");
        }
        return tipoFonteDAO.deletar(idTipoFonte);
    }

    public TipoFonteVO buscarPorId(int idTipoFonte) throws SQLException {
        return tipoFonteDAO.buscarPorId(idTipoFonte);
    }

    public List<TipoFonteVO> listar() throws SQLException {
        return tipoFonteDAO.listar();
    }
}
