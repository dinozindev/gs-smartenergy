package br.com.fiap.model.vo;

public class ProjetoSustentavelVO {
	private int idProjeto;
	private String descricao;
	private double custo;
	private String status;
	private TipoFonteVO tipoFonte;
	private RegiaoSustentavelVO regiaoSustentavel;
	
	public ProjetoSustentavelVO() {
		
	}
	
	public ProjetoSustentavelVO(int idProjeto, String descricao, double custo, String status, TipoFonteVO tipoFonte,
			RegiaoSustentavelVO regiaoSustentavel) {
		this.idProjeto = idProjeto;
		this.descricao = descricao;
		this.custo = custo;
		this.status = status;
		this.tipoFonte = tipoFonte;
		this.regiaoSustentavel = regiaoSustentavel;
	}

	/**
	 * @return the idProjeto
	 */
	public int getIdProjeto() {
		return idProjeto;
	}

	/**
	 * @param idProjeto the idProjeto to set
	 */
	public void setIdProjeto(int idProjeto) {
		this.idProjeto = idProjeto;
	}

	/**
	 * @return the descricao
	 */
	public String getDescricao() {
		return descricao;
	}

	/**
	 * @param descricao the descricao to set
	 */
	public void setDescricao(String descricao) {
		this.descricao = descricao;
	}

	/**
	 * @return the custo
	 */
	public double getCusto() {
		return custo;
	}

	/**
	 * @param custo the custo to set
	 */
	public void setCusto(double custo) {
		this.custo = custo;
	}

	/**
	 * @return the status
	 */
	public String getStatus() {
		return status;
	}

	/**
	 * @param status the status to set
	 */
	public void setStatus(String status) {
		this.status = status;
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
	 * @return the regiaoSustentavel
	 */
	public RegiaoSustentavelVO getRegiaoSustentavel() {
		return regiaoSustentavel;
	}

	/**
	 * @param regiaoSustentavel the regiaoSustentavel to set
	 */
	public void setRegiaoSustentavel(RegiaoSustentavelVO regiaoSustentavel) {
		this.regiaoSustentavel = regiaoSustentavel;
	}
	
	
}
