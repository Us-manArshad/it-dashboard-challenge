import os
from it_dashboard import ITDashboard
from constants import URL, KEYWORD, AGENCY_EXCEL_NAME, INVESTMENT_EXCEL_NAME, OPEN_AGENCY, DOWNLOAD_DIR

if not os.path.exists(DOWNLOAD_DIR):
    os.mkdir(DOWNLOAD_DIR)


if __name__ == "__main__":
    dashboard = ITDashboard(url=URL)
    try:
        dashboard.click_on_dive_in(KEYWORD)
        dashboard.search_for_agencies()
        dashboard.write_agencies_to_excel(AGENCY_EXCEL_NAME)
        dashboard.open_agency(OPEN_AGENCY)
        dashboard.write_investment_excel(INVESTMENT_EXCEL_NAME)
        dashboard.download_pdfs()
        dashboard.compare_pdf_with_title()
    finally:
        dashboard.close_all_browsers()
