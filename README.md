# Budget Analysis 💰

A comprehensive personal finance management and analysis tool that automates bank statement processing, transaction categorization, and budget insights powered by AI.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Workflow](#workflow)
- [Technologies](#technologies)
- [Data Flow](#data-flow)
- [Future Enhancements](#future-enhancements)

---

## 🎯 Overview

This project streamlines personal financial management by:

1. **Extracting** transaction data from bank statements (PDF format)
2. **Cleaning** and standardizing the data
3. **Categorizing** transactions automatically using intelligent mapping rules
4. **Analyzing** spending patterns and income trends
5. **Visualizing** insights through interactive dashboards
6. **Generating** AI-powered financial recommendations

The system uses AI assistance (ChatGPT/Gemini) to maintain and update transaction categorization rules monthly, ensuring accuracy while minimizing manual classification efforts.

---

## ✨ Features

### Core Functionality

- **PDF Bank Statement Extraction**: Automated reading of bank PDFs using Camelot library
- **Smart Categorization**: AI-assisted transaction classification with customizable rules
- **Data Cleaning**: Personal data removal and text normalization (Poland-specific)
- **Statistical Analysis**: Comprehensive spending and income analysis
- **Interactive Dashboard**: Streamlit-based visualization with filters
- **Tableau Integration**: Export data for advanced BI visualizations
- **AI Financial Reports**: Automated budget analysis and recommendations
- **PDF Report Generation**: Summary statistics exported as professional PDFs

### Smart Features

- **Monthly AI Updates**: Automatically identifies new transaction types for dictionary expansion
- **Dual Dataset Support**: Real personal data + fake data for testing
- **Multi-Level Categorization**: Main categories and detailed subcategories
- **Transaction Filtering**: By date range, category, and subcategory
- **Financial Metrics**: Total spending, averages, min/max values, transaction frequency

---

## 📁 Project Structure

```
Budget Analysis/
│
├── financial_analysis.ipynb          # Main analysis notebook
├── streamlit_app.py                  # Interactive dashboard
├── AI_financial_report.py            # Generated financial report (Python variable)
│
├── Data_for_AI/                      # Data exported for AI analysis
│   ├── data_to_update_mapping.xlsx  # Monthly export for dictionary update
│   ├── df_complete_after_categorization.csv
│   ├── fake_combined_after_categorization.csv
│   ├── fake_combined_before_categorization.csv
│   └── Update promt for budget analyze.pdf
│
├── Data_for_tableau/                 # Data for Tableau visualizations
│   ├── Income.csv
│   ├── Income_Sub_Cat_grupped.csv
│   ├── Spendings.csv
│   ├── Spendings_Cat_groupped.csv
│   └── Spendings_SubCat_groupped.csv
│
├── Old Bank Data/                    # Historical bank statements (PDFs)
├── New Bank Data/                    # Recent bank statements (PDFs)
├── fake_data/                        # Test data (Excel files)
│
├── Budget Analysis.twb               # Tableau workbook
├── prompts.txt                       # AI prompts for dictionary updates & analysis
├── Ideas.txt                         # Future enhancement ideas
└── README.md                         # This file
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8+
- pip package manager
- Tableau (optional, for advanced visualizations)

### Required Libraries

```bash
pip install pandas
pip install camelot-py
pip install opencv-python
pip install PyPDF2
pip install fpdf2
pip install streamlit
pip install seaborn
pip install matplotlib
pip install numpy
```

Or install from a requirements file:

```bash
pip install -r requirements.txt
```

---

## 💻 Usage

### 1. **Prepare Bank Data**

Place your bank statement PDFs in the appropriate folder:

- New statements → `New Bank Data/`
- Old statements → `Old Bank Data/`

### 2. **Run the Analysis Notebook**

Open and execute `financial_analysis.ipynb` in Jupyter:

```bash
jupyter notebook financial_analysis.ipynb
```

The notebook will:

- Extract tables from PDFs
- Clean and standardize data
- Apply categorization rules
- Generate analysis dataframes
- Export data to CSV and Tableau formats

### 3. **Update Transaction Dictionary (Monthly)**

1. After running the notebook, an Excel file is generated: `Data_for_AI/data_to_update_mapping.xlsx`
2. Copy the "Prompt for updating Dictionary every month" from `prompts.txt`
3. Paste the Excel data and prompt into ChatGPT or Gemini
4. The AI will identify new transaction keywords and suggest updates
5. Update the `mapping_rules` dictionary in the notebook with new entries

### 4. **View Interactive Dashboard**

Run the Streamlit app to explore your budget:

```bash
streamlit run streamlit_app.py
```

**Available Filters:**

- Date range slider
- Main category selection
- Sub-category selection (dynamic based on selected main category)

**Dashboard Views:**

- Income overview and sources
- Spending by main category (pie/bar charts)
- Spending by sub-category (detailed breakdown)
- Monthly trends
- Statistical summaries (totals, averages, min/max)

### 5. **Generate Financial Insights**

For AI-powered financial analysis:

1. Generate the PDF summary: `Update promt for budget analyze.pdf`
2. Use the "Prompt for AI financial advices" from `prompts.txt`
3. Paste the PDF tables and prompt into ChatGPT/Gemini
4. Receive personalized budget recommendations
5. The analysis output is saved as `AI_financial_report.py`

### 6. **Tableau Visualization**

Open `Budget Analysis.twb` in Tableau Desktop:

- Pre-configured income and spending dashboards
- Filter by category and time period
- Export for presentations or further analysis

---

## 🔄 Workflow

```
Bank Statements (PDFs)
        ↓
Extract Tables (Camelot)
        ↓
Clean Data (Standardization)
        ↓
Apply Categorization Rules
        ↓
├─→ CSV Export (for AI analysis)
├─→ Tableau Export (for BI)
└─→ Streamlit Dashboard
        ↓
Monthly Update Cycle
        ↓
ChatGPT/Gemini (Expand Dictionary)
        ↓
Update mapping_rules
        ↓
Re-run Notebook (with new rules)
```

---

## 🛠️ Technologies

| Technology               | Purpose                       |
| ------------------------ | ----------------------------- |
| **Python 3.8+**          | Core language                 |
| **Pandas**               | Data manipulation & analysis  |
| **Camelot**              | PDF table extraction          |
| **Streamlit**            | Interactive web dashboard     |
| **Matplotlib & Seaborn** | Data visualization            |
| **FPDF2**                | PDF generation                |
| **Tableau**              | Advanced BI visualizations    |
| **ChatGPT/Gemini API**   | AI-powered dictionary updates |

---

## 📊 Data Flow

### Data Processing Pipeline

```python
# 1. Extract from PDFs
tables = camelot.read_pdf(file_path, pages="all", flavor="lattice")

# 2. Clean data
df = first_data_cleaning(df)
df = data_cleaning_for_gpt(df)  # Remove personal identifiable info

# 3. Categorize
df[["Main_Category", "Sub_Category"]] = df.apply(
    lambda row: pd.Series(adding_categories(row["Description"])),
    axis=1
)

# 4. Analyze
df_analysis = df.groupby("Main_Category").agg({
    "Amt": ["sum", "mean", "min", "max"],
    "Description": "count"
})
```

### Data Schema

**Transaction Columns:**

- `Posting Date` - Date of posting
- `Data of Transaction` - Transaction date
- `Description` - Transaction description (merchant)
- `Amt` - Amount (positive/negative)
- `Acc Balance after opp` - Account balance after operation
- `Main_Category` - Primary category (e.g., "Income", "Eating out")
- `Sub_Category` - Subcategory (e.g., "Salary", "MCDONALDS")

**Sample Categories:**

- Income: Salary, BLIK, External Transfers
- Daily Purchase: Groceries, Pharmacies, Electronics
- Eating out: Fast food, Restaurants, Coffee
- Transport: Fuel, Trains/Buses, Taxi
- Fixed Costs: Rent, Internet, Utilities
- Entertainment: Cinema, Events
- And many more...

---

## 🎯 Key Functions

### `reading_pdf_from_folder(folder_name)`

Extracts all tables from PDFs in a folder and concatenates them into a single DataFrame.

### `first_data_cleaning(df)`

Standardizes column names, handles missing values, and converts amounts to float.

### `data_cleaning_for_gpt(df)`

Removes sensitive information (account numbers, phone numbers) before sharing with AI.

### `adding_categories(description)`

Maps transaction descriptions to Main and Sub categories using regex keyword matching.

---

## 📈 Analysis Features

The notebook generates comprehensive statistics including:

- **Income Analysis:**
  - Total income by source
  - Average transaction size
  - Frequency of deposits
- **Spending Analysis:**
  - Total by category and subcategory
  - Average transaction size
  - Min/max transaction amounts
  - Transaction frequency (identifying habits)

- **Budget Insights:**
  - Spending leaks (high-frequency small transactions)
  - Single high-impact expenses
  - Category trends over time
  - Income vs. expenses comparison

---

## 🚧 Future Enhancements

Planned features (from `Ideas.txt`):

- [ ] **Multi-person Household Support**
  - Compare and combine expenses between household members
  - Shared vs. individual expense tracking
- [ ] **Improved Data Cleaning**
  - More efficient PII removal
  - Automated file organization
- [ ] **Forecasting**
  - Predict spending for future months
  - Budget trend analysis
- [ ] **Advanced Visualizations**
  - Plotly integration for interactive charts
  - Month-over-month comparisons
  - Spending projections
- [ ] **Automation**
  - Direct bank API integration
  - Scheduled PDF processing
  - Automated monthly reports

---

## 📝 Notes

### Language & Localization

- The project is configured for **Polish bank data**
- Transaction descriptions are in Polish
- Mapping rules include Polish merchant names
- Can be easily adapted for other countries

### Data Privacy

- Personal data (names, addresses, account numbers) is removed before sharing with AI
- The `data_cleaning_for_gpt()` function handles basic PII removal
- **Manual review recommended** for additional sensitive information

### Monthly Workflow

1. Export new statements to `New Bank Data/`
2. Run the notebook
3. Export `data_to_update_mapping.xlsx`
4. Use AI to expand the dictionary
5. Update mapping rules
6. Re-run for final categorization

---

## 📞 Support

For issues or questions:

1. Check `prompts.txt` for detailed AI prompts
2. Review `Ideas.txt` for known limitations
3. Examine the notebook cells for data validation steps

---

## 📄 License

Personal project - feel free to adapt and extend for your needs.

---

## 🎉 Getting Started

1. Clone/download this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Place your bank PDFs in `New Bank Data/` folder
4. Run `financial_analysis.ipynb`
5. Launch dashboard: `streamlit run streamlit_app.py`
6. Explore your budget! 📊

---

**Last Updated:** February 2026  
**Project Status:** Active Development
