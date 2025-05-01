# OneStop-RNA-Analysis
The field of transcriptomics has been revolutionized by the advent of RNA sequencing (RNA-Seq), a high-throughput method that enables researchers to study the complete set of RNA transcripts present in a biological sample. Unlike traditional microarrays, RNA-Seq offers a more comprehensive and unbiased view of the transcriptome with higher resolution and sensitivity. It has become a critical tool in understanding gene expression dynamics, alternative splicing, non-coding RNAs, and the molecular mechanisms underlying various diseases and physiological processes.
Despite its widespread adoption, RNA-Seq data analysis often remains inaccessible to many researchers and students due to the technical challenges involved—such as familiarity with command-line tools, R programming, and complex statistical methods. This creates a gap between experimental data generation and its biological interpretation, especially for those without formal computational training.
To bridge this gap, the OneStop-RNA Analysis application was developed as a lightweight, user-friendly web-based tool that enables differential gene expression analysis using RNA-Seq count data. Built with Python and Streamlit, the app supports key functionalities such as low-expression filtering, normalization, Principal Component Analysis (PCA), linear modelling, volcano plot generation, and heatmap visualization. It only requires users to upload two CSV files, a raw count matrix and a metadata file, and outputs meaningful statistical and graphical summaries.
The purpose of this tool is to serve as an accessible and educational platform for conducting basic transcriptomic analyses. It enables biologists, students, and early-stage researchers to perform RNA-Seq differential expression studies without needing advanced programming skills.
About OneStop-RNA Analysis
The objective of building this web application was to automate the steps required for RNA Seq analysis and to provide a no-code, GUI based method for users to perform RNA Seq analysis
![image](https://github.com/user-attachments/assets/5dd6baab-885a-42c6-a311-d9d725d602dd)
Data Input
•	Count Matrix (.csv): Contains Rows having genes and columns having the sample ids.
•	Metadata file (.csv): contains rows having sample ids and columns having sample condition information (like condition and treated)

The Output after analysis would seem as follows:
![image](https://github.com/user-attachments/assets/d55adcaa-81d8-4d59-9ccf-3b134516850a)
![image](https://github.com/user-attachments/assets/f55908f0-b653-4ff4-abb5-f1ee806d3983)
![image](https://github.com/user-attachments/assets/08fbf6e1-78f7-49ad-914a-aa8ae02f2cba)
![image](https://github.com/user-attachments/assets/2f50d0f6-f5cf-4fc7-a1f5-f0819fee92f0)
![image](https://github.com/user-attachments/assets/7b650e28-b9af-4b9c-9705-80365c30178d)
![image](https://github.com/user-attachments/assets/2560e85b-116b-4d6b-8c17-95b3b2290039)
![image](https://github.com/user-attachments/assets/38df2196-992d-4cd7-8ed4-54b41c3891b8)
![image](https://github.com/user-attachments/assets/ce3a3139-9f69-4caa-a80a-9eb152c8aea3)
![image](https://github.com/user-attachments/assets/42ef27e4-c769-481c-8e6b-e898702ac6a1)









