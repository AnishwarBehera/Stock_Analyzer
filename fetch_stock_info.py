import yfinance as yf
import os
from document_loader import extract_text_from_pdf
from summarization_engine import summarize_document_gemini
from langchain_openai import OpenAI
from dotenv import load_dotenv
import re
load_dotenv()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import google.generativeai as genai



def fetch_company_info(stock_name):


    # SCRAPER_API_KEY=os.getenv('SCRAPER_API_KEY')
    # scraper_api_proxy = f"http://scraperapi:{SCRAPER_API_KEY}@proxy-server.scraperapi.com:8001"

    chrome_options = Options()
    chrome_options.add_argument("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.3")
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument(f'--proxy-server={scraper_api_proxy}')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Open Screener.in homepage
        driver.get("https://www.screener.in/")

        wait = WebDriverWait(driver, 10)

        search_box = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div[2]/div/div/div/input")))
        search_box.clear()

        for char in stock_name:
            search_box.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))  


        time.sleep(2)

        search_box.send_keys(Keys.ENTER)



        time.sleep(3)
        
        data = {}

        try:
            pe_ratio = driver.find_element(By.XPATH, """//*[@id="top-ratios"]/li[4]/span[2]/span""").text
            data["PE Ratio"] = pe_ratio
        except Exception:
            data["PE Ratio"] = "N/A"

        try:
            market_cap = driver.find_element(By.XPATH, """//*[@id="top-ratios"]/li[1]/span[2]/span""").text
            data["Market Cap"] = market_cap
        except Exception:
            data["Market Cap"] = "N/A"

        try:
            book_value = driver.find_element(By.XPATH, """//*[@id="top-ratios"]/li[5]/span[2]/span""").text
            data["Book Value"] = book_value
        except Exception:
            data["Book Value"] = "N/A"
        
        try:
            current_price = driver.find_element(By.XPATH, """//*[@id="top-ratios"]/li[2]/span[2]/span""").text
            data["Current Price"] = current_price
        except Exception:
            data["Current Price"] = "N/A"

# Extract Strengths (Pros)
        pros_list = []
        try:
            pros_elements = driver.find_elements(By.XPATH, """//*[@id="analysis"]/div/div[1]/ul/li""")
            for element in pros_elements:
                pros_list.append(element.text.strip())
            if not pros_list:
                pros_list = ["N/A"]  
        except Exception:
            pros_list = ["N/A"]

        data["Strengths (Pros)"] = pros_list

 
        cons_list = []
        try:
            cons_elements = driver.find_elements(By.XPATH, """//*[@id="analysis"]/div/div[2]/ul/li""")
            for element in cons_elements:
                cons_list.append(element.text.strip())
            if not cons_list:
                cons_list = ["N/A"]  
        except Exception:
            cons_list = ["N/A"]

        data["Weaknesses (Cons)"] = cons_list

        

        compounded_sales_growth = "N/A"
        compounded_sales_xpath_variants = [
            """//*[@id="profit-loss"]/div[4]/table[1]/tbody""",
            """//*[@id="profit-loss"]/div[3]/table[1]/tbody"""
        ]

        for xpath in compounded_sales_xpath_variants:
            try:
                ten_years_growth = driver.find_element(By.XPATH, f"{xpath}//tr[td[contains(text(),'10 Years:')]]/td[2]").text
                five_years_growth = driver.find_element(By.XPATH, f"{xpath}//tr[td[contains(text(),'5 Years:')]]/td[2]").text
                three_years_growth = driver.find_element(By.XPATH, f"{xpath}//tr[td[contains(text(),'3 Years:')]]/td[2]").text
                ttm_growth = driver.find_element(By.XPATH, f"{xpath}//tr[td[contains(text(),'TTM:')]]/td[2]").text
                compounded_sales_growth = {
                    "10 Years": ten_years_growth,
                    "5 Years": five_years_growth,
                    "3 Years": three_years_growth,
                    "TTM": ttm_growth
                }
                break  
            except Exception:
                continue  

        data["Compounded Sales Growth"] = compounded_sales_growth

        compounded_profit_growth = "N/A"
        compounded_profit_xpath_base_variants = [
            """//*[@id="profit-loss"]/div[4]/table[2]/tbody""",
            """//*[@id="profit-loss"]/div[3]/table[2]/tbody"""
        ]

        for xpath in compounded_profit_xpath_base_variants:
            try:
                ten_years_profit_growth = driver.find_element(By.XPATH, f"{xpath}//tr[td[contains(text(),'10 Years:')]]/td[2]").text
                five_years_profit_growth = driver.find_element(By.XPATH, f"{xpath}//tr[td[contains(text(),'5 Years:')]]/td[2]").text
                three_years_profit_growth = driver.find_element(By.XPATH, f"{xpath}//tr[td[contains(text(),'3 Years:')]]/td[2]").text
                ttm_profit_growth = driver.find_element(By.XPATH, f"{xpath}//tr[td[contains(text(),'TTM:')]]/td[2]").text

                compounded_profit_growth = {
                    "10 Years": ten_years_profit_growth,
                    "5 Years": five_years_profit_growth,
                    "3 Years": three_years_profit_growth,
                    "TTM": ttm_profit_growth
                }
                break  
            except Exception:
                continue  

        data["Compounded Profit Growth"] = compounded_profit_growth
        
        # Extract Return on Equity with multiple XPaths
        return_on_equity = "N/A"
        return_on_equity_xpath_base_variants = [
            """//*[@id="profit-loss"]/div[4]/table[4]/tbody""",
            """//*[@id="profit-loss"]/div[3]/table[4]/tbody"""
        ]

        for xpath in return_on_equity_xpath_base_variants:
            try:
                ten_years_roe = driver.find_element(By.XPATH, f"{xpath}//tr[td[contains(text(),'10 Years:')]]/td[2]").text
                five_years_roe = driver.find_element(By.XPATH, f"{xpath}//tr[td[contains(text(),'5 Years:')]]/td[2]").text
                three_years_roe = driver.find_element(By.XPATH, f"{xpath}//tr[td[contains(text(),'3 Years:')]]/td[2]").text
                ttm_roe = driver.find_element(By.XPATH, f"{xpath}//tr[td[contains(text(),'Last Year:')]]/td[2]").text

                return_on_equity = {
                    "10 Years": ten_years_roe,
                    "5 Years": five_years_roe,
                    "3 Years": three_years_roe,
                    "Last Year": ttm_roe
                }
                break  
            except Exception:
                continue  

        data["Return on Equity"] = return_on_equity

        stock_price_cagr="N/A"
        stock_price_cagr_xpath_base_variants=[
            """//*[@id="profit-loss"]/div[4]/table[5]/tbody""",
            """//*[@id="profit-loss"]/div[3]/table[3]/tbody"""
        ]
        for xpath in stock_price_cagr_xpath_base_variants:
            try:
                ten_years_roe = driver.find_element(By.XPATH, f"{xpath}//tr[td[contains(text(),'10 Years:')]]/td[2]").text
                five_years_roe = driver.find_element(By.XPATH, f"{xpath}//tr[td[contains(text(),'5 Years:')]]/td[2]").text
                three_years_roe = driver.find_element(By.XPATH, f"{xpath}//tr[td[contains(text(),'3 Years:')]]/td[2]").text
                ttm_roe = driver.find_element(By.XPATH, f"{xpath}//tr[td[contains(text(),'1 Year:')]]/td[2]").text

                stock_price_cagr = {
                    "10 Years": ten_years_roe,
                    "5 Years": five_years_roe,
                    "3 Years": three_years_roe,
                    "1 Year": ttm_roe
                }
                break  
            except Exception:
                continue  
        data["Stock Price CAGR"] = stock_price_cagr
        return data

    except Exception as e:
        print(f"Error fetching data from Screener.in: {e}")
        return None
    finally:
        driver.quit()

# Example usage
# stock_name = "Jio Financial Services"
# fundamental_data = fetch_company_info(stock_name)
# if fundamental_data:
#     print(fundamental_data)
# else:
#     print("No financial data available.")







# def generate_assessment(company_name, summary, stock_info):
#     try:

        

#         openai_api_key = os.getenv("OPENAI_API_KEY")
#         if openai_api_key is None:
#             return "Error: OpenAI API key is not set."

#         llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)

#         # Prepare prompt for AI
#         prompt = """
#         Company Analysis Report:

#         Company Name: {company_name}

#         Market Cap: {market_cap}
#         Current Price: {current_price}
#         P/E Ratio: {pe_ratio}
#         Book Value: {book_value}

#         Compounded Sales Growth:
#         10 Years: {sales_growth_10_years}
#         5 Years: {sales_growth_5_years}
#         3 Years: {sales_growth_3_years}
#         TTM: {sales_growth_ttm}

#         Compounded Profit Growth:
#         10 Years: {profit_growth_10_years}
#         5 Years: {profit_growth_5_years}
#         3 Years: {profit_growth_3_years}
#         TTM: {profit_growth_ttm}

#         Return on Equity:
#         10 Years: {roe_10_years}
#         5 Years: {roe_5_years}
#         3 Years: {roe_3_years}
#         Last Year: {roe_last_year}

#         Stock Price CAGR:
#         10 Years: {price_cagr_10_years}
#         5 Years: {price_cagr_5_years}
#         3 Years: {price_cagr_3_years}
#         1 Year: {price_cagr_1_year}

#         Strengths (Pros):
#         {pros}

#         Weaknesses (Cons):
#         {cons}

#         Document Summary:
#         {document_summary}

#         Based on the provided financial information, strengths, weaknesses, and document summary, please provide an overall assessment of the company's potential for future growth and its suitability as an investment opportunity. Consider key factors such as financial performance, growth prospects, market position, and risks.
#         """.format(
#             company_name=company_name,
#             market_cap=stock_info.get('Market Cap', 'N/A'),
#             current_price=stock_info.get('Current Price', 'N/A'),
#             pe_ratio=stock_info.get('PE Ratio', 'N/A'),
#             book_value=stock_info.get('Book Value', 'N/A'),
#             sales_growth_10_years=stock_info.get('Compounded Sales Growth', {}).get('10 Years', 'N/A'),
#             sales_growth_5_years=stock_info.get('Compounded Sales Growth', {}).get('5 Years', 'N/A'),
#             sales_growth_3_years=stock_info.get('Compounded Sales Growth', {}).get('3 Years', 'N/A'),
#             sales_growth_ttm=stock_info.get('Compounded Sales Growth', {}).get('TTM', 'N/A'),
#             profit_growth_10_years=stock_info.get('Compounded Profit Growth', {}).get('10 Years', 'N/A'),
#             profit_growth_5_years=stock_info.get('Compounded Profit Growth', {}).get('5 Years', 'N/A'),
#             profit_growth_3_years=stock_info.get('Compounded Profit Growth', {}).get('3 Years', 'N/A'),
#             profit_growth_ttm=stock_info.get('Compounded Profit Growth', {}).get('TTM', 'N/A'),
#             roe_10_years=stock_info.get('Return on Equity', {}).get('10 Years', 'N/A'),
#             roe_5_years=stock_info.get('Return on Equity', {}).get('5 Years', 'N/A'),
#             roe_3_years=stock_info.get('Return on Equity', {}).get('3 Years', 'N/A'),
#             roe_last_year=stock_info.get('Return on Equity', {}).get('Last Year', 'N/A'),
#             price_cagr_10_years=stock_info.get('Stock Price CAGR', {}).get('10 Years', 'N/A'),
#             price_cagr_5_years=stock_info.get('Stock Price CAGR', {}).get('5 Years', 'N/A'),
#             price_cagr_3_years=stock_info.get('Stock Price CAGR', {}).get('3 Years', 'N/A'),
#             price_cagr_1_year=stock_info.get('Stock Price CAGR', {}).get('1 Year', 'N/A'),
#             pros="\n".join(stock_info.get('Strengths (Pros)', [])),
#             cons="\n".join(stock_info.get('Weaknesses (Cons)', [])),
#             document_summary=summary
#         )

#         # Get AI assessment
#         assessment = llm(prompt)
#         return assessment
#     except Exception as e:
#         return f"Error generating assessment: {str(e)}"



def generate_assessment(company_name, summary, stock_info):
    try:
        # Ensure stock_info is a dictionary
        if not isinstance(stock_info, dict):
            return "Error: stock_info is not a dictionary."

        # Debugging: Check all entries in stock_info
        for key, value in stock_info.items():
            if isinstance(value, dict):
                print(f"{key} is a dictionary: {value}")
            elif isinstance(value, list):
                print(f"{key} is a list: {value}")
            else:
                print(f"{key} is a {type(value)} with value: {value}")

        # openai_api_key = os.getenv("OPENAI_API_KEY")
        # if openai_api_key is None:
        #     return "Error: OpenAI API key is not set."

        # llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)

        gemini_api_key = os.getenv("GEMINI_API_KEY")

        # Initialize the Gemini generative model
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Prepare prompt for AI
        prompt = f"""
        Company Analysis Report:

        Company Name: {company_name}
        Market Cap: {stock_info.get('Market Cap', 'N/A')}
        Current Price: {stock_info.get('Current Price', 'N/A')}
        PE Ratio: {stock_info.get('PE Ratio', 'N/A')}
        Book Value: {stock_info.get('Book Value', 'N/A')}

        Compounded Sales Growth 10 Years: {stock_info.get('Compounded Sales Growth', {}).get('10 Years', 'N/A') if isinstance(stock_info.get('Compounded Sales Growth'), dict) else 'N/A'}
        Compounded Sales Growth 5 Years: {stock_info.get('Compounded Sales Growth', {}).get('5 Years', 'N/A') if isinstance(stock_info.get('Compounded Sales Growth'), dict) else 'N/A'}
        Compounded Sales Growth 3 Years: {stock_info.get('Compounded Sales Growth', {}).get('3 Years', 'N/A') if isinstance(stock_info.get('Compounded Sales Growth'), dict) else 'N/A'}
        Compounded Sales Growth TTM: {stock_info.get('Compounded Sales Growth', {}).get('TTM', 'N/A') if isinstance(stock_info.get('Compounded Sales Growth'), dict) else 'N/A'}

        Strengths (Pros): {', '.join(stock_info.get('Strengths (Pros)', [])) if isinstance(stock_info.get('Strengths (Pros)'), list) else 'N/A'}
        Weaknesses (Cons): {', '.join(stock_info.get('Weaknesses (Cons)', [])) if isinstance(stock_info.get('Weaknesses (Cons)'), list) else 'N/A'}

        Compuneded Profit Growth 10 Years: {stock_info.get('Compounded Profit Growth', {}).get('10 Years', 'N/A') if isinstance(stock_info.get('Compounded Profit Growth'), dict) else 'N/A'}
        Compuneded Profit Growth 5 Years: {stock_info.get('Compounded Profit Growth', {}).get('5 Years', 'N/A') if isinstance(stock_info.get('Compounded Profit Growth'), dict) else 'N/A'}
        Compuneded Profit Growth 3 Years: {stock_info.get('Compounded Profit Growth', {}).get('3 Years', 'N/A') if isinstance(stock_info.get('Compounded Profit Growth'), dict) else 'N/A'}
        Compuneded Profit Growth TTM: {stock_info.get('Compounded Profit Growth', {}).get('TTM', 'N/A') if isinstance(stock_info.get('Compounded Profit Growth'), dict) else 'N/A'}

        Return on Equity 10 Years: {stock_info.get('Return on Equity', {}).get('10 Years', 'N/A') if isinstance(stock_info.get('Return on Equity'), dict) else 'N/A'}
        Return on Equity 5 Years: {stock_info.get('Return on Equity', {}).get('5 Years', 'N/A') if isinstance(stock_info.get('Return on Equity'), dict) else 'N/A'}
        Return on Equity 3 Years: {stock_info.get('Return on Equity', {}).get('3 Years', 'N/A') if isinstance(stock_info.get('Return on Equity'), dict) else 'N/A'}
        Return on Equity Last Year: {stock_info.get('Return on Equity', {}).get('Last Year', 'N/A') if isinstance(stock_info.get('Return on Equity'), dict) else 'N/A'}

        Stock Price CAGR 10 Years: {stock_info.get('Stock Price CAGR', {}).get('10 Years', 'N/A') if isinstance(stock_info.get('Stock Price CAGR'), dict) else 'N/A'}
        Stock Price CAGR 5 Years: {stock_info.get('Stock Price CAGR', {}).get('5 Years', 'N/A') if isinstance(stock_info.get('Stock Price CAGR'), dict) else 'N/A'}
        Stock Price CAGR 3 Years: {stock_info.get('Stock Price CAGR', {}).get('3 Years', 'N/A') if isinstance(stock_info.get('Stock Price CAGR'), dict) else 'N/A'}
        Stock Price CAGR 1 Year: {stock_info.get('Stock Price CAGR', {}).get('1 Year', 'N/A') if isinstance(stock_info.get('Stock Price CAGR'), dict) else 'N/A'}

        Document Summary:
        {summary}
        Based on the above information, please provide the a detailed summary of the following:

        1. **Company Strength Analysis**: Discuss the positive aspects of the company's performance, including its financial metrics, strengths, and competitive position. Mention how these could contribute to future growth.
        
        2. **Company Weakness Analysis**: Discuss any potential concerns, such as weak financial metrics or challenges in its operations. Mention how these could affect the company's future performance.

        3. **Growth Potential Assessment**: Provide an overview of the company's future growth potential, considering its historical growth, market trends, and competitive advantages.

        4. **Investment Suitability**: Evaluate whether the company would make a good investment opportunity. Provide both a balanced view and a conclusion that considers the company’s strengths and weaknesses.

        5. **Final Conclusion**: Summarize the key points and provide a clear ending to the assessment.

        Make sure to provide a comprehensive analysis with a complete conclusion at the end.
        """

        response = model.generate_content([prompt])
        
        # Check if response is valid and contains candidates
        if response and hasattr(response, "candidates") and response.candidates:
            # Extract the generated text from the response
            return response.candidates[0].content.parts[0].text.strip()
        
        return "Error: Unable to generate the assessment content."


    except Exception as e:
        return f"Error generating assessment: {str(e)}"






import re

def extract_company_name_from_pdf(text):
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key is None:
            return "Error: OpenAI API key is not set."

        llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)

        # Prepare prompt for AI
        prompt = """
        You are given the text of a company report. Your task is to identify the name of the company mentioned in the report.
        Here is the text:
        "{document_text}"
        Please extract the company name only. 
        Make sure to retain any abbreviations with periods (e.g., "C.E.") as part of the company name.
        After extracting the company name, if it contains the word "Limited", change it to "Ltd".
        Do not include extra punctuation or special characters that are not part of the name.
        """.format(document_text=text[:2000])

        company_name = llm(prompt).strip()

        # Additional cleanup to ensure the name is appropriate for Screener
        cleaned_company_name = re.sub(r'\([^)]*\)', '', company_name)  # Remove anything in parentheses
        cleaned_company_name = re.sub(r'[^\w\s\.\&]', '', cleaned_company_name)  # Allow only alphanumeric, whitespace, periods, and &
        cleaned_company_name = cleaned_company_name.strip()

        # Special handling for abbreviations
        # If abbreviations like C.E. are removed, ensure we keep them intact
        abbreviation_pattern = r'\b(?:[A-Z]\.){2,}\b'  # Match abbreviations like "C.E."
        abbreviations = re.findall(abbreviation_pattern, company_name)
        if abbreviations:
            # Join abbreviations with cleaned company name, ensuring no duplicates
            abbreviation_str = " ".join(abbreviations)
            if abbreviation_str not in cleaned_company_name:
                cleaned_company_name = f"{abbreviation_str} {cleaned_company_name}"

        return cleaned_company_name

    except Exception as e:
        return f"Error extracting company name: {str(e)}"

    
    


# # Example usage
# symbol = "MSFT"
# document_summary = "This company has a robust business model and a strong presence in its market."
# company_info = fetch_company_info_and_stock(symbol)
# assessment = generate_assessment(document_summary, company_info)
# print(assessment)