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
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.UriBuilder;
import javax.ws.rs.core.UriInfo;

import br.com.fiap.model.bo.PrevisaoEnergeticaBO;
import br.com.fiap.model.vo.PrevisaoEnergeticaVO;

@Path("/previsao-energetica")
public class PrevisaoEnergeticaResource {

	private PrevisaoEnergeticaBO previsaoEnergeticaBO;

    public PrevisaoEnergeticaResource() {
        try {
            previsaoEnergeticaBO = new PrevisaoEnergeticaBO();
        } catch (SQLException e) {

            throw new WebApplicationException("Erro ao inicializar o BO de previsão energética: " + e.getMessage(), Response.Status.INTERNAL_SERVER_ERROR);
        } catch (ClassNotFoundException e) {
			e.printStackTrace();
		}
    }


    @POST
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public Response cadastrarPrevisaoEnergetica(PrevisaoEnergeticaVO previsao, @Context UriInfo uriInfo) {
        try {
            PrevisaoEnergeticaVO novaPrevisao = previsaoEnergeticaBO.inserir(previsao);
            UriBuilder builder = uriInfo.getAbsolutePathBuilder();
            builder.path(novaPrevisao.getIdPrevisao());

            return Response.created(builder.build()).entity(novaPrevisao).build();
        } catch (IllegalArgumentException e) {
            return Response.status(Response.Status.BAD_REQUEST).entity("Dados inválidos: " + e.getMessage()).build();
        } catch (Exception e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR).entity("Erro interno ao cadastrar previsão energética: " + e.getMessage()).build();
        }
    }


    @PUT
    @Path("/{idPrevisao}")
    @Consumes(MediaType.APPLICATION_JSON)
    public Response atualizarPrevisaoEnergetica(@PathParam("idPrevisao") String idPrevisao, PrevisaoEnergeticaVO novaPrevisao) {
        try {
            PrevisaoEnergeticaVO previsaoAtualizada = previsaoEnergeticaBO.atualizar(idPrevisao, novaPrevisao);
            return Response.ok(previsaoAtualizada).build();
        } catch (IllegalArgumentException e) {
            return Response.status(Response.Status.BAD_REQUEST).entity("Dados inválidos: " + e.getMessage()).build();
        } catch (Exception e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR).entity("Erro interno ao atualizar previsão energética: " + e.getMessage()).build();
        }
    }


    @DELETE
    @Path("/{idPrevisao}")
    public Response deletarPrevisaoEnergetica(@PathParam("idPrevisao") String idPrevisao) {
        try {
            previsaoEnergeticaBO.deletar(idPrevisao);
            return Response.noContent().build();  
        } catch (IllegalArgumentException e) {
            return Response.status(Response.Status.BAD_REQUEST).entity("Previsão energética não encontrada: " + e.getMessage()).build();
        } catch (Exception e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR).entity("Erro interno ao deletar previsão energética: " + e.getMessage()).build();
        }
    }


    @GET
    @Produces(MediaType.APPLICATION_JSON)
    public Response listarPrevisoesEnergeticas() {
        try {
            List<PrevisaoEnergeticaVO> previsoes = previsaoEnergeticaBO.listar();
            return Response.ok(previsoes).build();
        } catch (Exception e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR).entity("Erro ao listar previsões energéticas: " + e.getMessage()).build();
        }
    }


    @GET
    @Path("/{idPrevisao}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response buscarPrevisaoEnergeticaPorId(@PathParam("idPrevisao") String idPrevisao) {
        try {
            PrevisaoEnergeticaVO previsao = previsaoEnergeticaBO.buscarPorId(idPrevisao);
            return Response.ok(previsao).build();
        } catch (IllegalArgumentException e) {
            return Response.status(Response.Status.NOT_FOUND).entity("Previsão energética não encontrada: " + e.getMessage()).build();
        } catch (Exception e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR).entity("Erro ao buscar previsão energética: " + e.getMessage()).build();
        }
    }
    
  

    @GET
    @Path("/buscarPrevisaoPorCpf/{cpfUsuario}")
    @Produces("application/json")
    public Response buscarPrevisaoPorCpf(@PathParam("cpfUsuario") String cpfUsuario) {
        try {
            List<PrevisaoEnergeticaVO> previsoes = previsaoEnergeticaBO.listarPrevisaoPorCpf(cpfUsuario);
            return Response.ok(previsoes).build();
        } catch (IllegalArgumentException e) {
            throw new WebApplicationException("CPF inválido: " + e.getMessage(), Response.Status.BAD_REQUEST);
        } catch (RuntimeException e) {
            throw new WebApplicationException("Erro interno no servidor ao listar previsões por CPF: " + e.getMessage(), Response.Status.INTERNAL_SERVER_ERROR);
        }
    }
    
    @GET
    @Path("/buscarResidenciaPorCpf/{cpfUsuario}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response buscarResidenciaPorCpf(@PathParam("cpfUsuario") String cpfUsuario) {
        try {
            return Response.ok(previsaoEnergeticaBO.listar()).build(); 
        } catch (RuntimeException e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR).entity("Erro interno: " + e.getMessage()).build();
        }
    }
}
