package br.com.fiap.model.vo;

public class RegiaoSustentavelVO {
	private int idRegiaoSustentavel;
	private String nome;
	
	public RegiaoSustentavelVO() {
		
	}
	
	public RegiaoSustentavelVO(int idRegiaoSustentavel, String nome) {
		this.idRegiaoSustentavel = idRegiaoSustentavel;
		this.nome = nome;
	}

	/**
	 * @return the idRegiaoSustentavel
	 */
	public int getIdRegiaoSustentavel() {
		return idRegiaoSustentavel;
	}

	/**
	 * @param idRegiaoSustentavel the idRegiaoSustentavel to set
	 */
	public void setIdRegiaoSustentavel(int idRegiaoSustentavel) {
		this.idRegiaoSustentavel = idRegiaoSustentavel;
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

