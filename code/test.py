from datetime import datetime

def get_fiscal_year(date=None):
    if date is None:
        date = datetime.strptime('2025-04-21', "%Y-%m-%d") 
    
    year = date.year
    if date.month < 4:  # Before April, it's part of the previous fiscal year
        return f"FY {year}"
    else:  # April onwards, it's the current fiscal year
        return f"FY {year+1}"

# Example Usage
print(get_fiscal_year())  # Fiscal Year for today's date
