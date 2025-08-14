package br.com.fiap.resources;

import java.util.List;

import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import br.com.fiap.model.bo.EmissaoCarbonoBO;
import br.com.fiap.model.vo.EmissaoCarbonoVO;

@Path("/emissao-carbono")
public class EmissaoCarbonoResource {

    private EmissaoCarbonoBO emissaoCarbonoBO;

    public EmissaoCarbonoResource() {
        try {
            emissaoCarbonoBO = new EmissaoCarbonoBO();
        } catch (Exception e) {
            throw new WebApplicationException("Erro ao inicializar o BO de Emissão de Carbono: " + e.getMessage(), Response.Status.INTERNAL_SERVER_ERROR);
        }
    }

    @POST
    @Consumes(MediaType.APPLICATION_JSON)
    public Response inserirEmissao(EmissaoCarbonoVO emissao) {
        try {
            boolean sucesso = emissaoCarbonoBO.inserir(emissao);
            return sucesso ? Response.status(Response.Status.CREATED).build() : Response.status(Response.Status.BAD_REQUEST).build();
        } catch (IllegalArgumentException e) {
            return Response.status(Response.Status.BAD_REQUEST).entity("Dados inválidos: " + e.getMessage()).build();
        } catch (Exception e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR).entity("Erro ao inserir: " + e.getMessage()).build();
        }
    }

    @PUT
    @Path("/{idEmissao}")
    @Consumes(MediaType.APPLICATION_JSON)
    public Response atualizarEmissao(@PathParam("idEmissao") int idEmissao, EmissaoCarbonoVO emissao) {
        try {
            emissao.setIdEmissao(idEmissao);
            boolean sucesso = emissaoCarbonoBO.atualizar(emissao);
            return sucesso ? Response.ok().build() : Response.status(Response.Status.BAD_REQUEST).build();
        } catch (IllegalArgumentException e) {
            return Response.status(Response.Status.BAD_REQUEST).entity("Dados inválidos: " + e.getMessage()).build();
        } catch (Exception e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR).entity("Erro ao atualizar: " + e.getMessage()).build();
        }
    }

    @DELETE
    @Path("/{idEmissao}")
    public Response deletarEmissao(@PathParam("idEmissao") int idEmissao) {
        try {
            boolean sucesso = emissaoCarbonoBO.deletar(idEmissao);
            return sucesso ? Response.noContent().build() : Response.status(Response.Status.NOT_FOUND).build();
        } catch (Exception e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR).entity("Erro ao deletar: " + e.getMessage()).build();
        }
    }

    @GET
    @Path("/{idEmissao}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response buscarEmissaoPorId(@PathParam("idEmissao") int idEmissao) {
        try {
            EmissaoCarbonoVO emissao = emissaoCarbonoBO.buscarPorId(idEmissao);
            return Response.ok(emissao).build();
        } catch (Exception e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR).entity("Erro ao buscar: " + e.getMessage()).build();
        }
    }

    @GET
    @Produces(MediaType.APPLICATION_JSON)
    public Response listarEmissoes() {
        try {
            List<EmissaoCarbonoVO> emissoes = emissaoCarbonoBO.listar();
            return Response.ok(emissoes).build();
        } catch (Exception e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR).entity("Erro ao listar emissões: " + e.getMessage()).build();
        }
    }

    
}
