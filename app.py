# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dKytdp_0ZriakQqrP3AnaZoLOcyCmrLe
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests
import io

st.set_page_config(page_title="OneStop-RNA Analysis", layout="wide")

st.title("🧬 OneStop-RNA Analysis")
# 🔰 User Guide Panel
with st.expander("📘 USER GUIDE — How to Use This Tool", expanded=True):
    st.markdown("""
    Welcome to **OneStop-RNA Analysis** — a simple tool to perform **differential expression analysis** using RNA-seq raw count matrices and metadata files.

    ### 🔧 Input Requirements

    1. **Raw Count Matrix** (`.csv`):
        - Rows = genes
        - Columns = sample names
        - Values = raw read counts (integers)
        - Example:
            ```
            Gene,Sample1,Sample2,Sample3
            TP53,120,90,300
            BRCA1,450,600,700
            ```

    2. **Metadata File** (`.csv`):
        - Rows = sample names (must match column names in count matrix)
        - Columns = at least one column named **Condition**
        - Values in `Condition` = only two categories (e.g., `Control`, `Treated`)
        - Example:
            ```
            Sample,Condition
            Sample1,Control
            Sample2,Treated
            Sample3,Treated
            ```

    ### ⚠️ Important Notes
    - Sample names **must match** between both files.
    - Tool supports **only two conditions** for differential expression.
    - Count data must not be normalized — raw integer values only.
    - If you're using GEO data, you can get count matrices from tools like **featureCounts**, **htseq-count**, or **DESeq2 (counts)**.

    ### 🧪 What This App Does:
    1. Upload and validate files
    2. Filter low-expressed genes
    3. Perform PCA for visualization
    4. Run differential gene expression analysis (OLS-based)
    5. Show volcano plot and heatmap of top DEGs
    6. Let you download results as CSV and PNG

    ### 🔍 Filtering Settings (Adjustable)
    - Minimum count per gene
    - Minimum number of samples expressing the gene

    ### 🧬 Output Files:
    - `DEG_results.csv`: Differentially expressed genes with log2FC and adjusted p-values
    - `volcano_plot.png`: Visual summary of DE results
    - `heatmap_top20_DEGs.png`: Expression heatmap of top DEGs

    ---
    ⚙️ Developed by *Divya Ranjan Pradhan*. Powered by Streamlit + StatsModels + Seaborn.
    """)

"""**BACKEND starts from here**"""

# === FILE UPLOAD ===
st.header("📂 Upload Files")
counts_file = st.file_uploader("Upload Raw Count Matrix CSV", type="csv", key="counts")
meta_file = st.file_uploader("Upload Metadata CSV", type="csv", key="meta")

if counts_file and meta_file:
    raw_counts = pd.read_csv(counts_file, index_col=0)
    metadata = pd.read_csv(meta_file, index_col=0)

    st.subheader("✅ Data Preview")
    st.write("**Raw Counts (first 5 rows):**")
    st.dataframe(raw_counts.head())
    st.write("**Metadata (first 5 rows):**")
    st.dataframe(metadata.head())

    # === SAMPLE MATCHING CHECK ===
    st.subheader("🔍 Sample Consistency Check")
    sample_mismatch = [s for s in metadata.index if s not in raw_counts.columns]
    if sample_mismatch:
        st.warning(f"These samples in metadata are missing from the count matrix: {sample_mismatch}")
    else:
        st.success("✅ All metadata samples match the count matrix.")

    # Align order
    raw_counts = raw_counts[metadata.index]

    # === GENE FILTERING ===
    st.subheader("🔧 Low-Expression Gene Filtering")
    min_count = st.number_input("Minimum count per gene", value=10, min_value=0)
    min_samples = st.number_input("Minimum number of samples with that count", value=2, min_value=1)

    gene_filter = (raw_counts >= min_count).sum(axis=1) >= min_samples
    filtered_counts = raw_counts[gene_filter]

    st.write(f"Retained {filtered_counts.shape[0]} genes out of {raw_counts.shape[0]}.")
    st.dataframe(filtered_counts.head())

    # === PCA ===
    st.subheader("📊 PCA Plot")
    log_counts = np.log1p(filtered_counts)
    pca = PCA(n_components=2)
    pcs = pca.fit_transform(log_counts.T)

    pca_df = pd.DataFrame(pcs, columns=['PC1', 'PC2'])
    pca_df['Condition'] = metadata.iloc[:, 0].values

    fig_pca, ax_pca = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='Condition', s=100, palette='Set2', ax=ax_pca)
    ax_pca.set_title("PCA of Samples")
    ax_pca.grid(True)
    st.pyplot(fig_pca)

    # === DEG ANALYSIS ===
    st.subheader("🧪 Differential Expression Analysis")
    metadata['Condition'] = metadata['Condition'].astype('category')
    filtered_counts = filtered_counts[metadata.index]
    deg_results = []

    for gene in filtered_counts.index:
        df = pd.DataFrame({
            'Expression': filtered_counts.loc[gene],
            'Condition': metadata['Condition']
        })
        model = smf.ols('Expression ~ Condition', data=df).fit()
        pval = model.pvalues.get('Condition[T.1]', np.nan)
        deg_results.append({
            'Gene': gene,
            'log2FC': model.params.get('Condition[T.1]', 0),
            'pval': pval
        })

    deg_df = pd.DataFrame(deg_results)
    deg_df['adj_pval'] = multipletests(deg_df['pval'], method='fdr_bh')[1]
    deg_df = deg_df.sort_values('adj_pval')

    st.write("Top DEGs:")
    st.dataframe(deg_df.head(10))

    # === VOLCANO PLOT ===
    st.subheader("Volcano Plot")
    log2fc_threshold = st.number_input("Log2 Fold Change Threshold", value=1.0)
    pval_threshold = st.number_input("Adjusted p-value Threshold", value=0.05)

    def categorize_gene(row):
        if row['adj_pval'] < pval_threshold:
            if row['log2FC'] >= log2fc_threshold:
                return 'Upregulated'
            elif row['log2FC'] <= -log2fc_threshold:
                return 'Downregulated'
        return 'Not Significant'

    deg_df['category'] = deg_df.apply(categorize_gene, axis=1)
    fig_volcano, ax_volcano = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=deg_df,
        x='log2FC',
        y=-np.log10(deg_df['adj_pval']),
        hue='category',
        palette={'Upregulated': 'red', 'Downregulated': 'blue', 'Not Significant': 'gray'},
        ax=ax_volcano,
        edgecolor='black', linewidth=0.5
    )
    ax_volcano.axhline(-np.log10(pval_threshold), linestyle='--', color='black')
    ax_volcano.axvline(log2fc_threshold, linestyle='--', color='black')
    ax_volcano.axvline(-log2fc_threshold, linestyle='--', color='black')
    ax_volcano.set_title("Volcano Plot")
    st.pyplot(fig_volcano)

    # === HEATMAP ===
    st.subheader("Heatmap of Top DEGs")
    top_n = st.slider("Select number of top DEGs", 5, 50, 20)
    top_genes = deg_df.nsmallest(top_n, 'adj_pval')['Gene']
    heatmap_data = filtered_counts.loc[top_genes]

    scaler = StandardScaler()
    z_scores = pd.DataFrame(scaler.fit_transform(heatmap_data.T).T, index=heatmap_data.index, columns=heatmap_data.columns)
    condition_colors = metadata['Condition'].astype('category').cat.codes
    palette = sns.color_palette("Set2", len(set(condition_colors)))
    col_colors = pd.Series(condition_colors).map(dict(enumerate(palette)))
    col_colors.index = metadata.index
    col_colors = col_colors.loc[z_scores.columns]

    fig_heatmap = sns.clustermap(z_scores, cmap='vlag', col_colors=col_colors, figsize=(12, 8), xticklabels=True, yticklabels=True)
    st.pyplot(fig_heatmap.fig)

    # === DOWNLOAD BUTTONS ===
    st.subheader("📥 Download Results")
    csv = deg_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download DEG Results (CSV)", csv, "DEG_results.csv", "text/csv")

    volcano_buf = BytesIO()
    fig_volcano.savefig(volcano_buf, format="png")
    st.download_button("Download Volcano Plot", volcano_buf.getvalue(), "volcano_plot.png", "image/png")

    heatmap_buf = BytesIO()
    fig_heatmap.fig.savefig(heatmap_buf, format="png")
    st.download_button("Download Heatmap", heatmap_buf.getvalue(), "heatmap_top_DEGs.png", "image/png")
