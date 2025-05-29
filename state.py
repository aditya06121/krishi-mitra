import pandas as pd

def load_crop_data(file_path):
    """Load the crop data from CSV file"""
    return pd.read_csv(file_path)

def detect_crop(data, state, district, season):
    """Detect crops based on state, district, and season"""
    filtered = data[
        (data['State'].str.lower() == state.lower()) & 
        (data['District'].str.lower() == district.lower()) & 
        (data['Season'].str.lower() == season.lower())
    ]
    
    if filtered.empty:
        return "No crops found for the given criteria."
    
    # Get unique crops
    crops = filtered['Crop'].unique()
    
    if len(crops) == 1:
        return f"The crop grown in {state}, {district} during {season} is: {crops[0]}"
    else:
        return f"Multiple crops grown in {state}, {district} during {season}: {', '.join(crops)}"

def main():
    # Load your CSV file (replace with your actual file path)
    file_path = 'crop_data.csv'
    try:
        crop_data = load_crop_data(file_path)
    except FileNotFoundError:
        print("Error: CSV file not found. Please check the file path.")
        return
    
    # Get user input
    state = input("Enter the state: ")
    district = input("Enter the district: ")
    season = input("Enter the season (Kharif/Whole Year/etc.): ")
    
    # Detect and display crop
    result = detect_crop(crop_data, state, district, season)
    print(result)

if __name__ == "__main__":
    main()