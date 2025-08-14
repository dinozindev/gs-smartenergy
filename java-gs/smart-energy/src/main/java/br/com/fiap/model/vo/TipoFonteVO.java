package br.com.fiap.model.vo;

public class TipoFonteVO {
	private int idTipoFonte;
	private String nome;
	
	public TipoFonteVO() {
		
	}
	
	public TipoFonteVO(int idTipoFonte, String nome) {
		this.idTipoFonte = idTipoFonte;
		this.nome = nome;
	}

	/**
	 * @return the idTipoFonte
	 */
	public int getIdTipoFonte() {
		return idTipoFonte;
	}

	/**
	 * @param idTipoFonte the idTipoFonte to set
	 */
	public void setIdTipoFonte(int idTipoFonte) {
		this.idTipoFonte = idTipoFonte;
	}

	/**
	 * @return the nome
	 */
	public String getNome() {
		return nome;
	}

	/**
	 * @param nome the nome to set
	 */
	public void setNome(String nome) {
		this.nome = nome;
	}
	
}
