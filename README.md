https://land-use-for-community-energy-sheffield.streamlit.app/

Community Energy Land Allocation Dashboard
This project is a dashboard designed to identify and prioritize land parcels for community-owned renewable energy projects. By combining data on land availability, solar potential, and fuel poverty, the dashboard helps policymakers and community groups make data-driven decisions that tackle both climate change and social equity..

The project was developed in response to Challenge 1: Land Use for Community Energy, a challenge proposed by the South Yorkshire Sustainability Centre and Sheffield City Council.

🌟 Key Features:

1. Data Upload: Easily upload your own land data in CSV or Excel format.

2. Interactive Map: Visualize land parcels on a map, with the ability to color-code points based on various metrics like Score, Solar Irradiance, and Fuel Poverty Index.

3. Customizable Scoring: Adjust the weighting of social, technical, economic, and fairness criteria to rank land parcels based on your priorities.

4. Impact Estimates: Quantify the potential of each project by estimating energy generation (kWh), the number of households that can be supported, and potential CO₂ savings.

5. Filtering: Filter land parcels to show only those that are currently available.

🚀 How It Works
The dashboard processes your uploaded data through a series of calculations to generate a final "Score" for each land parcel. This score is a weighted average of key factors, allowing you to identify the most suitable sites quickly.

🏆🔢🎉 Scoring Criteria

The dashboard calculates a composite score based on the following weighted criteria:

- Social: Based on the FuelPovertyIndex. Higher scores are given to areas with greater fuel poverty.

- Technical: Based on SolarIrradiance. Higher scores are given to parcels with more sunlight.

- Economic: Based on GridDistance. Parcels closer to the grid receive higher scores.

- Fairness: Based on ExistingProjects. Areas with fewer existing projects are scored higher to promote equitable distribution

📈💹 Impact Estimates

The dashboard also provides key impact metrics based on the data provided:

- Energy Production (kWh): Area_m2 x SolarIrradiance x PANEL_EFFICIENCY

- Households Supported: Energy_kWh / HOUSEHOLD_CONSUMPTION

- CO₂ Savings: (Energy_kWh x CARBON_FACTOR) / 1000

🛠️ Setup and Usage
This dashboard is built using Streamlit, a powerful Python library for creating web applications.

Installation
1. Clone this repository:

git clone [https://github.com/your-username/community-energy-dashboard.git](https://github.com/your-username/community-energy-dashboard.git)
cd community-energy-dashboard

2. Install the required packages:

pip install -r requirements.txt

Running the Dashboard
1. Make sure you have the required packages installed.

2. Run the application from your terminal:

streamlit run dashboard_app.py

3. The dashboard will open in your web browser. Use the sidebar to upload a data file (e.g., land_data.csv) and adjust the settings.

📄 License
This project is licensed under the MIT License.


