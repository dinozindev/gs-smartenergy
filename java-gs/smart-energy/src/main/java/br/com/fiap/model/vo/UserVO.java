package br.com.fiap.model.vo;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class UserVO {
	private String cpfUsuario;
    private String nomeUsuario;
    private String senha;
    private String email;
    private String telefone;
    private double gastoMensal;

    public UserVO() {

    }

    public UserVO(String cpfUsuario, String nomeUsuario, String senha, String email, String telefone, double gastoMensal) {
        this.cpfUsuario = cpfUsuario;
        this.nomeUsuario = nomeUsuario;
        this.senha = senha;
        this.email = email;
        this.telefone = telefone;
        this.gastoMensal = gastoMensal;
    }

    public String getCpfUsuario() {
        return cpfUsuario;
    }

    public void setCpfUsuario(String cpfUsuario) {
        this.cpfUsuario = cpfUsuario;
    }

    public String getNomeUsuario() {
        return nomeUsuario;
    }

    public void setNomeUsuario(String nomeUsuario) {
        this.nomeUsuario = nomeUsuario;
    }

    public String getSenha() {
        return senha;
    }

    public void setSenha(String senha) {
        this.senha = senha;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getTelefone() {
        return telefone;
    }

    public void setTelefone(String telefone) {
        this.telefone = telefone;
    }

    public double getGastoMensal() {
        return gastoMensal;
    }

    public void setGastoMensal(double gastoMensal) {
        this.gastoMensal = gastoMensal;
    }
}
