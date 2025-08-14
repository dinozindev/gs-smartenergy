package br.com.fiap.resources;

import java.sql.SQLException;
import java.util.List;

import javax.ws.rs.*;
import javax.ws.rs.core.*;
import br.com.fiap.model.bo.RegiaoSustentavelBO;
import br.com.fiap.model.vo.RegiaoSustentavelVO;

@Path("/regioes-sustentaveis")
public class RegiaoSustentavelResource {

    private RegiaoSustentavelBO regiaoBO;

    public RegiaoSustentavelResource() throws ClassNotFoundException, SQLException {
        this.regiaoBO = new RegiaoSustentavelBO();
    }

    @POST
    @Consumes(MediaType.APPLICATION_JSON)
    public Response inserir(RegiaoSustentavelVO regiao, @Context UriInfo uriInfo) throws SQLException {
        boolean resultado = regiaoBO.inserir(regiao);
        if (!resultado) {
            return Response.status(Response.Status.BAD_REQUEST).build();
        }
        UriBuilder builder = uriInfo.getAbsolutePathBuilder();
        builder.path(String.valueOf(regiao.getIdRegiaoSustentavel()));
        return Response.created(builder.build()).build();
    }

    @PUT
    @Path("/{idRegiao}")
    @Consumes(MediaType.APPLICATION_JSON)
    public Response atualizar(RegiaoSustentavelVO regiao, @PathParam("idRegiao") int id) throws SQLException {
        regiao.setIdRegiaoSustentavel(id);
        boolean resultado = regiaoBO.atualizar(regiao);
        if (!resultado) {
            return Response.status(Response.Status.BAD_REQUEST).build();
        }
        return Response.ok().build();
    }

    @DELETE
    @Path("/{idRegiao}")
    public Response deletar(@PathParam("idRegiao") int id) throws SQLException {
        boolean resultado = regiaoBO.deletar(id);
        if (!resultado) {
            return Response.status(Response.Status.BAD_REQUEST).build();
        }
        return Response.ok().build();
    }

    @GET
    @Path("/{idRegiao}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response buscarPorId(@PathParam("idRegiao") int id) throws SQLException {
        RegiaoSustentavelVO regiao = regiaoBO.buscarPorId(id);
        if (regiao == null) {
            return Response.status(Response.Status.NOT_FOUND).entity("Região Sustentável não encontrada").build();
        }
        return Response.ok(regiao).build();
    }

    @GET
    @Produces(MediaType.APPLICATION_JSON)
    public List<RegiaoSustentavelVO> listar() throws SQLException {
        return regiaoBO.listar();
    }
}
