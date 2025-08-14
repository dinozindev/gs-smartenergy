package br.com.fiap.model.vo;

import java.sql.Date;
import java.util.UUID;

public class PrevisaoEnergeticaVO {
	private String idPrevisao;
    private Date data;
    private double previsaoGasto;
    private String statusPrevisao;
    private UserVO usuario;
    
    public PrevisaoEnergeticaVO() {
    	
    }

    public PrevisaoEnergeticaVO(String idPrevisao, Date data, double previsaoGasto, String statusPrevisao, UserVO usuario ) {
        this.idPrevisao = idPrevisao;
        this.data = data;
        this.previsaoGasto = previsaoGasto;
        this.statusPrevisao = statusPrevisao;
        this.usuario = usuario;
    }
    
    public PrevisaoEnergeticaVO(Date data, double previsaoGasto, String statusPrevisao, UserVO usuario ) {
        this.idPrevisao = UUID.randomUUID().toString();
        this.data = data;
        this.previsaoGasto = previsaoGasto;
        this.statusPrevisao = statusPrevisao;
        this.usuario = usuario;
    }

    public String getIdPrevisao() {
        return idPrevisao;
    }

    public void setIdPrevisao(String idPrevisao) {
        this.idPrevisao = idPrevisao;
    }

    public Date getData() {
        return data;
    }

    public void setData(Date data) {
        this.data = data;
    }

    public double getPrevisaoGasto() {
        return previsaoGasto;
    }

    public void setPrevisaoGasto(double previsaoGasto) {
        this.previsaoGasto = previsaoGasto;
    }

    public String getStatusPrevisao() {
        return statusPrevisao;
    }

    public void setStatusPrevisao(String statusPrevisao) {
        this.statusPrevisao = statusPrevisao;
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
