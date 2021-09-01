# IT-Dashboard Challenge

This is a repository for IT-Challenge developed with Python, [rpaframework](https://rpaframework.org/releasenotes.html).
### Features

1. **Automate Scrap the** [IT-Dashboard](https://itdashboard.gov/)
2. It will scrap agencies with amount and save it into the Excel file
3. It will open one of the agency and will scrap the Individual Investments into another excel file.
4. It will check in the Individual Investments table that if the **UII** contains link it will open that link and download the PDF file associated with **Download Business Case PDF** button into output folder  
5. Can be test on [robocorp](https://cloud.robocorp.com/)
6. All downloaded PDF's and Excel sheets will be land in **output** folder
7. It will read the downloaded PDF files and get the **Section A** from each PDF then it will compare the values "Name of this Investment" with the column "Investment Title", and the value "Unique Investment Identifier (UII)" with the column "UII"

## Setup (robocorp)

1. [rpaframework](https://rpaframework.org/releasenotes.html)

### Installation

1. Goto [robocorp](https://cloud.robocorp.com/taskoeneg/task/robots) create a bot
2. Add [this](https://github.com/Us-manArshad/it-dashboard.git) repo link in public GIT
3. Goto [assistants](https://cloud.robocorp.com/taskoeneg/task/assistants) and add new assistant linked with robot that you had registered above. 
4. Download and install desktop app of robocorp assistant from [there](https://cloud.robocorp.com/taskoeneg/task/assistants) by click on **Download Robocorp Assistant App**
5. Run the assistant you had created above
6. Bot will start performing the task as mentioned above
7. Your output data will be saved in output folder. click on output when task finished.


## File Structure
### [constants.py](https://github.com/Us-manArshad/it-dashboard-challenge/blob/master/constants.py)

Keyword | Description
| :--- | :---
URL  | *URL of the it-dashboard website*
DOWNLOAD_DIR  | *Download directory name*
AGENCY_EXCEL_NAME  | *Excel file name for agencies*
INVESTMENT_EXCEL_NAME  | *Excel file name for investment table data.*
KEYWORD  | *Button name to click on home page so agencies can be visible*
OPEN_AGENCY  | *Number for which agency you wan to scrap the agency investment table, and download the PDF's*

### [task.py](https://github.com/Us-manArshad/it-dashboard-challenge/blob/master/task.py)
It will initialize the ITDashboard from [it_dashboard.py](https://github.com/Us-manArshad/it-dashboard-challenge/blob/master/it_dashboard.py) instance and call the 
required functions to perform the challenge.

### [it_dashboard.py](https://github.com/Us-manArshad/it-dashboard-challenge/blob/master/it_dashboard.py)
- Have the logic to scrap and create the Excel file for agencies and Investment table,
- Get the uii links and download the PDF's associated with it.
- Read PDF's and compare with "Name of this Investment" with the column "Investment Title", and the value "Unique Investment Identifier (UII)" with the column "UII".

### [conda.yaml](https://github.com/Us-manArshad/it-dashboard-challenge/blob/master/conda.yaml)
Having configuration to set up the environment and [rpaframework](https://rpaframework.org/releasenotes.html) dependencies.

### [robot.yaml](https://github.com/Us-manArshad/it-dashboard-challenge/blob/master/conda.yaml)
Having configuration for robocorp to run the [conda.yaml](https://github.com/Us-manArshad/it-dashboard-challenge/blob/master/conda.yaml) and execute the task.py


You can find more details and a full explanation of the code on [Robocorp documentation](https://robocorp.com/docs/development-guide/browser/rpa-form-challenge)
