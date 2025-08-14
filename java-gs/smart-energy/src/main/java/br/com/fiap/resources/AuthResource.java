package br.com.fiap.resources;

import javax.ws.rs.Consumes;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.UriInfo;

import br.com.fiap.model.vo.UserVO;
import br.com.fiap.services.AuthenticationService;

@Path("/auth")
public class AuthResource {

    private AuthenticationService authService = new AuthenticationService();

    @POST
    @Path("/login")
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public Response autenticar(UserVO usuario, @Context UriInfo uriInfo) {
        UserVO usuarioAutenticado = authService.autenticarUsuario(usuario);

        if (usuarioAutenticado != null) {
            return Response.ok(usuarioAutenticado).build();
        } else {
            return Response.status(Response.Status.UNAUTHORIZED)
                           .entity("{\"message\":\"Credenciais inválidas.\"}")
                           .build();
        }
    }
}
