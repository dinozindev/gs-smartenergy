package br.com.fiap.model.vo;

import java.util.UUID;

public class ResidenciaVO {
	private String idResidencia;
    private String cep;
    private String logradouro;
    private String complemento;
    private String bairro;
    private String localidade;
    private String estado;
    private int numero;
    private UserVO usuario;
    
    public ResidenciaVO() {
    	
    }
    
    public ResidenciaVO(String cep, String logradouro, String complemento, String bairro, String localidade, String estado, int numero, UserVO usuario) {
        this.idResidencia = UUID.randomUUID().toString();
        this.cep = cep;
        this.logradouro = logradouro;
        this.complemento = complemento;
        this.bairro = bairro;
        this.localidade = localidade;
        this.estado = estado;
        this.numero = numero;
        this.usuario = usuario;
    }


    public ResidenciaVO(String idResidencia, String cep, String logradouro, String complemento, String bairro, String localidade, String estado, int numero, UserVO usuario) {
        this.idResidencia = idResidencia;
        this.cep = cep;
        this.logradouro = logradouro;
        this.complemento = complemento;
        this.bairro = bairro;
        this.localidade = localidade;
        this.estado = estado;
        this.numero = numero;
        this.usuario = usuario;
    }
    
    
    public String getIdResidencia() {
        return idResidencia;
    }

    public void setIdResidencia(String idResidencia) {
        this.idResidencia = idResidencia;
    }

    public String getCep() {
        return cep;
    }

    public void setCep(String cep) {
        this.cep = cep;
    }

    public String getLogradouro() {
        return logradouro;
    }

    public void setLogradouro(String logradouro) {
        this.logradouro = logradouro;
    }

    public String getComplemento() {
        return complemento;
    }

    public void setComplemento(String complemento) {
        this.complemento = complemento;
    }

    public String getBairro() {
        return bairro;
    }

    public void setBairro(String bairro) {
        this.bairro = bairro;
    }

    public String getLocalidade() {
        return localidade;
    }

    public void setLocalidade(String localidade) {
        this.localidade = localidade;
    }

    public String getEstado() {
        return estado;
    }

    public void setEstado(String estado) {
        this.estado = estado;
    }

    public int getNumero() {
        return numero;
    }

    public void setNumero(int numero) {
        this.numero = numero;
    }

	/**
	 * @return the usuario
	 */
	public UserVO getUsuario() {
		return usuario;
	}

	/**
	 * @param usuario the usuario to set
	 */
	public void setUsuario(UserVO usuario) {
		this.usuario = usuario;
	}
	
	
}
