package br.com.fiap.model.vo;

public class EmissaoCarbonoVO {
	private int idEmissao;
	private TipoFonteVO tipoFonte;
	private double emissao;
	
	public EmissaoCarbonoVO() {
		
	}
	
	public EmissaoCarbonoVO(int idEmissao, TipoFonteVO tipoFonte, double emissao) {
		this.idEmissao = idEmissao;
		this.tipoFonte = tipoFonte;
		this.emissao = emissao;
	}

	/**
	 * @return the idEmissao
	 */
	public int getIdEmissao() {
		return idEmissao;
	}

	/**
	 * @param idEmissao the idEmissao to set
	 */
	public void setIdEmissao(int idEmissao) {
		this.idEmissao = idEmissao;
	}

	/**
	 * @return the tipoFonte
	 */
	public TipoFonteVO getTipoFonte() {
		return tipoFonte;
	}

	/**
	 * @param tipoFonte the tipoFonte to set
	 */
	public void setTipoFonte(TipoFonteVO tipoFonte) {
		this.tipoFonte = tipoFonte;
	}

	/**
	 * @return the emissao
	 */
	public double getEmissao() {
		return emissao;
	}

	/**
	 * @param emissao the emissao to set
	 */
	public void setEmissao(double emissao) {
		this.emissao = emissao;
	}
	
	
}
