import pandas as pd
import openpyxl
from openpyxl.styles import Font

def write_dataframe_to_excel(dataframe, sheet_name, file_path):
    # Check if the file exists
    try:
        # Load the workbook
        workbook = openpyxl.load_workbook(file_path)
    except FileNotFoundError:
        # Create a new workbook if the file doesn't exist
        workbook = openpyxl.Workbook()
        # Remove the default sheet created and create a new sheet
        workbook.remove(workbook.active)
        workbook.create_sheet(sheet_name)

    # Check if the sheet exists
    if sheet_name not in workbook.sheetnames:
        # Create a new sheet
        workbook.create_sheet(sheet_name)

    # Get the sheet
    sheet = workbook[sheet_name]

    # Convert the DataFrame column names and data to a list of lists
    data = [list(dataframe.columns)] + dataframe.values.tolist()

    # Append the data to the sheet
    for row in data:
        sheet.append(row)

    for cell in sheet[1]:
        cell.font = Font(bold=True)

    # Save the workbook
    workbook.save(file_path)