import tabula

pdf_path = "Docs\Catalogo-WEGA-Linha-Leve-2023-2024.pdf"
output_path = "Docs\Tabela.csv"

try:
    tabula.convert_into(pdf_path, output_path, output_format="csv", pages='all')
    print(f"Tabelas convertidas para com sucesso!")
except Exception as e:
    print(f"Ocorreu um erro ao converter o PDF: {e}")
    print("Certifique-se de que o Java esteja instalado e configurado corretamente.")
    print("Se as tabelas não forem bem definidas, outras abordagens podem ser necessárias.")