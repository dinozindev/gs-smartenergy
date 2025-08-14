package br.com.fiap.resources;

import br.com.fiap.model.bo.TipoFonteBO;
import br.com.fiap.model.vo.TipoFonteVO;

import javax.ws.rs.*;
import javax.ws.rs.core.*;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.List;

@Path("/tipos-fonte")
public class TipoFonteResource {

    private TipoFonteBO tipoFonteBO;

    public TipoFonteResource() throws SQLException {
        Connection connection = DriverManager.getConnection("jdbc:seu_banco", "usuario", "senha");
        this.tipoFonteBO = new TipoFonteBO(connection);
    }

    @POST
    @Consumes(MediaType.APPLICATION_JSON)
    public Response inserirTipoFonte(TipoFonteVO tipoFonteVO, @Context UriInfo uriInfo) throws SQLException {
        tipoFonteBO.inserir(tipoFonteVO);
        UriBuilder builder = uriInfo.getAbsolutePathBuilder();
        builder.path(String.valueOf(tipoFonteVO.getIdTipoFonte()));
        return Response.created(builder.build()).build();
    }

    @PUT
    @Path("/{idTipoFonte}")
    @Consumes(MediaType.APPLICATION_JSON)
    public Response atualizarTipoFonte(TipoFonteVO tipoFonteVO, @PathParam("idTipoFonte") int id) throws SQLException {
        tipoFonteVO.setIdTipoFonte(id);
        tipoFonteBO.atualizar(tipoFonteVO);
        return Response.ok().build();
    }

    @DELETE
    @Path("/{idTipoFonte}")
    public Response deletarTipoFonte(@PathParam("idTipoFonte") int id) throws SQLException {
        tipoFonteBO.deletar(id);
        return Response.ok().build();
    }

    @GET
    @Path("/{idTipoFonte}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response buscarPorId(@PathParam("idTipoFonte") int id) throws SQLException {
        TipoFonteVO tipoFonte = tipoFonteBO.buscarPorId(id);
        if (tipoFonte != null) {
            return Response.ok(tipoFonte).build();
        }
        return Response.status(Response.Status.NOT_FOUND).build();
    }

    @GET
    @Produces(MediaType.APPLICATION_JSON)
    public List<TipoFonteVO> listarTipoFontes() throws SQLException {
        return tipoFonteBO.listar();
    }
}
