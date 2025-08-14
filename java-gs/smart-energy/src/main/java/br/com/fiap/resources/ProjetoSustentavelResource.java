package br.com.fiap.resources;

import java.sql.SQLException;
import java.util.List;

import javax.ws.rs.Consumes;
import javax.ws.rs.DELETE;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.PUT;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.UriBuilder;
import javax.ws.rs.core.UriInfo;

import br.com.fiap.model.bo.ProjetoSustentavelBO;
import br.com.fiap.model.vo.ProjetoSustentavelVO;

@Path("/projetos-sustentaveis")
public class ProjetoSustentavelResource {

    private ProjetoSustentavelBO projetoBO = new ProjetoSustentavelBO();

    @POST
    @Consumes(MediaType.APPLICATION_JSON)
    public Response inserirProjetoSustentavel(ProjetoSustentavelVO projeto, @Context UriInfo uriInfo) throws ClassNotFoundException, SQLException {
        boolean resultado = projetoBO.inserir(projeto);
        if (!resultado) {
            return Response.status(Response.Status.BAD_REQUEST).entity(resultado).build();
        }
        UriBuilder builder = uriInfo.getAbsolutePathBuilder();
        builder.path(String.valueOf(projeto.getIdProjeto()));
        return Response.created(builder.build()).build();
    }

    @PUT
    @Path("/{idProjeto}")
    @Consumes(MediaType.APPLICATION_JSON)
    public Response atualizarProjetoSustentavel(ProjetoSustentavelVO projeto, @PathParam("idProjeto") int id) throws ClassNotFoundException, SQLException { 
        projeto.setIdProjeto(id);  
        boolean resultado = projetoBO.atualizar(projeto);
        if (!resultado) {
            return Response.status(Response.Status.BAD_REQUEST).entity(resultado).build();
        }
        return Response.ok().build();
    }

    @DELETE
    @Path("/{idProjeto}")
    public Response deletarProjetoSustentavel(@PathParam("idProjeto") int id) throws ClassNotFoundException, SQLException { 
        boolean resultado = projetoBO.deletar(id);
        if (!resultado) {
            return Response.status(Response.Status.BAD_REQUEST).entity(resultado).build();
        }
        return Response.ok().build();
    }

    @GET
    @Path("/{idProjeto}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response buscarPorId(@PathParam("idProjeto") int id) throws ClassNotFoundException, SQLException {
        ProjetoSustentavelVO projeto = projetoBO.buscarPorId(id);
        if (projeto != null) {
            return Response.ok(projeto).build();
        } else {
            return Response.status(Response.Status.NOT_FOUND).entity("Projeto Sustentável não encontrado para o ID: " + id).build();
        }
    }

    @GET
    @Produces(MediaType.APPLICATION_JSON)
    public List<ProjetoSustentavelVO> listarProjetosSustentaveis() throws ClassNotFoundException, SQLException {
        return projetoBO.listar(); 
    }

    @GET
    @Path("/por-regiao/{idRegiao}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response buscarProjetosPorRegiao(@PathParam("idRegiao") int idRegiao) throws ClassNotFoundException, SQLException {
        List<ProjetoSustentavelVO> projetos = projetoBO.listar(); 
        if (!projetos.isEmpty()) {
            return Response.ok(projetos).build();
        } else {
            return Response.status(Response.Status.NOT_FOUND).entity("Nenhum projeto encontrado para a região com ID: " + idRegiao).build();
        }
    }
}
