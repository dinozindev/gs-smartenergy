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

import br.com.fiap.model.bo.ResidenciaBO;
import br.com.fiap.model.vo.ResidenciaVO;

@Path("/residencias")
public class ResidenciaResource {

    private ResidenciaBO residenciaBO = new ResidenciaBO();

    @POST
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public Response inserirResidencia(ResidenciaVO residencia, @Context UriInfo uriInfo) throws ClassNotFoundException, SQLException {
        boolean resultado = residenciaBO.inserir(residencia);
        if (!resultado) {
            return Response.status(Response.Status.BAD_REQUEST).entity(resultado).build();
        }
        UriBuilder builder = uriInfo.getAbsolutePathBuilder();
        builder.path(residencia.getIdResidencia());
        
        return Response.created(builder.build())
                       .entity(residencia)  
                       .build();
    }

    @PUT
    @Path("/{idResidencia}")
    @Consumes(MediaType.APPLICATION_JSON)
    public Response atualizarResidencia(ResidenciaVO residencia, @PathParam("idResidencia") String id) throws ClassNotFoundException, SQLException { 
        residencia.setIdResidencia(id);  
        boolean resultado = residenciaBO.atualizar(residencia);
        if (!resultado) {
            return Response.status(Response.Status.BAD_REQUEST).entity(resultado).build();
        }
        return Response.ok().build();
    }

    @DELETE
    @Path("/{idResidencia}")
    public Response deletarResidencia(@PathParam("idResidencia") String id) throws ClassNotFoundException, SQLException { 
        boolean resultado = residenciaBO.deletar(id);
        if (!resultado) {
            return Response.status(Response.Status.BAD_REQUEST).entity(resultado).build();
        }
        return Response.ok().build();
    }

    @GET
    @Path("/residencia/{idResidencia}")
    @Produces(MediaType.APPLICATION_JSON)
    public ResidenciaVO buscarPorId(@PathParam("idResidencia") String id) throws ClassNotFoundException, SQLException {
        return residenciaBO.buscarPorId(id);
    }

    @GET
    @Produces(MediaType.APPLICATION_JSON)
    public List<ResidenciaVO> listarResidencias() throws ClassNotFoundException, SQLException {
        return residenciaBO.listar(); 
    }

    // rota para buscar residência pelo CPF
    @GET
    @Path("/por-cpf/{cpfUsuario}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response buscarResidenciaPorCpf(@PathParam("cpfUsuario") String cpfUsuario) throws ClassNotFoundException, SQLException {
        ResidenciaVO residencia = residenciaBO.buscarResidenciaPorCpf(cpfUsuario);
        if (residencia != null) {
            return Response.ok(residencia).build();
        } else {
            return Response.status(Response.Status.NOT_FOUND).entity("Residência não encontrada para o CPF: " + cpfUsuario).build();
        }
    }
}
