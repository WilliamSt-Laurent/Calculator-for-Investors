# write your code here
import csv
from sqlalchemy import Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

main_menu = "MAIN MENU"
crud_menu = "CRUD MENU"
top_ten_menu = "TOP TEN MENU"
main_menu_options = ["0 Exit", "1 CRUD operations", "2 Show top ten companies by criteria"]
crud_menu_options = ["0 Back", "1 Create a company", "2 Read a company", "3 Update a company",
                     "4 Delete a company", "5 List all companies"]
top_ten_options = ["0 Back", "1 List by ND/EBITDA", "2 List by ROE", "3 List by ROA"]
options = [main_menu, crud_menu, top_ten_menu]
enter_option_message = "Enter an option:\n"
not_implemented_message = "Not implemented!"
invalid_option_message = "Invalid option!\n"

dict_nb_ebitda = {}
dict_roe = {}
dict_roa = {}


def create_company():
    ticker = input("Enter ticker (in the format 'MOON'):")
    company = input("Enter company (in the format 'Moon Corp'):")
    industries = input("Enter industries (in the format 'Technology'):")
    ebitda = input("Enter ebitda (in the format '987654321'):")
    sales = input("Enter sales (in the format '987654321'):")
    net_profit = input("Enter net profit (in the format '987654321'):")
    market_price = input("Enter market price (in the format '987654321'):")
    net_debt = input("Enter net debt (in the format '987654321'):")
    assets = input("Enter assets (in the format '987654321'):")
    equity = input("Enter equity (in the format '987654321'):")
    cash_equivalent = input("Enter cash equivalents (in the format '987654321'):")
    liabilities = input("Enter liabilities (in the format '987654321'):")

    company_input = Company(
        ticker=ticker,
        name=company,
        sector=industries
    )

    financial_input = Financial(
        ticker=ticker,
        ebitda=ebitda,
        sales=sales,
        net_profit=net_profit,
        market_price=market_price,
        net_debt=net_debt,
        assets=assets,
        equity=equity,
        cash_equivalents=cash_equivalent,
        liabilities=liabilities
    )

    session.add(company_input)
    session.add(financial_input)
    session.commit()
    print("Company created successfully!")


def read_company():
    global current_menu

    company_input = input("Enter company name:")
    query = session.query(Company.name, Company.ticker)
    companies = []

    for name, ticker in query:
        if company_input.lower() in name.lower():
            companies.append((name, ticker))

    if len(companies) == 0:
        print("Company not found!")
    else:
        for index in range(len(companies)):
            print(index, companies[index][0], sep=" ")

        company_number = input("Enter company number:")
        company_name = companies[int(company_number)][0]
        company_ticker = companies[int(company_number)][1]

        print(company_ticker, company_name, sep=" ")

        financials_query = session.query(Financial.market_price,
                                         Financial.net_profit,
                                         Financial.sales,
                                         Financial.assets,
                                         Financial.net_debt,
                                         Financial.ebitda,
                                         Financial.equity,
                                         Financial.liabilities).filter(Financial.ticker == company_ticker)

        market_price, net_profit, sales, assets, net_debt, ebitda, equity, liabilities = financials_query[0]
        print(f"P/E = {round(int(market_price) / int(net_profit), 2) if market_price is not None and net_profit is not None else None}")
        print(f"P/S = {round(int(market_price) / int(sales), 2) if market_price is not None and sales is not None else None}")
        print(f"P/B = {round(int(market_price) / int(assets), 2) if market_price is not None and assets is not None else None}")
        print(f"ND/EBITDA = {round(int(net_debt) / int(ebitda), 2) if net_debt is not None and ebitda is not None else None}")
        print(f"ROE = {round(int(net_profit) / int(equity), 2) if net_profit is not None and equity is not None else None}")
        print(f"ROA = {round(int(net_profit) / int(assets), 2) if net_profit is not None and assets is not None else None}")
        print(f"L/A = {round(int(liabilities) / int(assets), 2) if liabilities is not None and assets is not None else None}")
        print()


def update_company():
    company_name = input("Enter company name:")
    query = session.query(Company.name, Company.ticker)
    companies = []

    for name, ticker in query:
        if company_name.lower() in name.lower():
            companies.append((name, ticker))

    if len(companies) == 0:
        print("Company not found!")
    else:
        for index in range(len(companies)):
            print(index, companies[index][0], sep=" ")

        number_selected = input("Enter company number:")

        ebitda = input("Enter ebitda (in the format '987654321'):")
        sales = input("Enter sales (in the format '987654321'):")
        net_profit = input("Enter net profit (in the format '987654321'):")
        market_price = input("Enter market price (in the format '987654321'):")
        net_debt = input("Enter net debt (in the format '987654321'):")
        assets = input("Enter assets (in the format '987654321'):")
        equity = input("Enter equity (in the format '987654321'):")
        cash_equivalents = input("Enter cash equivalents (in the format '987654321'):")
        liabilities = input("Enter liabilities (in the format '987654321'):")

        ticker_to_update = companies[int(number_selected)][1]

        financial_query = session.query(Financial).filter(Financial.ticker == ticker_to_update)
        financial_query.update({
            "ebitda": ebitda,
            "sales": sales,
            "net_profit": net_profit,
            "market_price": market_price,
            "net_debt": net_debt,
            "assets": assets,
            "equity": equity,
            "cash_equivalents": cash_equivalents,
            "liabilities": liabilities
        })
        session.commit()
        print("Company updated successfully!")


def delete_company():
    company_name = input("Enter company name:")
    query = session.query(Company.name, Company.ticker)
    companies = []

    for name, ticker in query:
        if company_name.lower() in name.lower():
            companies.append((name, ticker))

    if len(companies) == 0:
        print("Company not found!")
    else:
        for index in range(len(companies)):
            print(index, companies[index][0], sep=" ")

        number_selected = input("Enter company number:")

        ticker_to_delete = companies[int(number_selected)][1]

        financial_query = session.query(Company).filter(Company.ticker == ticker_to_delete)
        financial_query.delete()
        session.commit()
        print("Company deleted successfully!")


def list_company():
    print("COMPANY LIST")
    company_list = session.query(Company.ticker, Company.name, Company.sector).order_by(Company.ticker)
    for ticker, name, sector in company_list:
        print(ticker, name, sector, sep=" ")


current_menu = main_menu

Base = declarative_base()


class Company(Base):
    __tablename__ = "companies"
    ticker = Column(String(10), primary_key=True)
    name = Column(String(30))
    sector = Column(String(30))


class Financial(Base):
    __tablename__ = "financial"
    ticker = Column(String(10), primary_key=True)
    ebitda = Column(Float)
    sales = Column(Float)
    net_profit = Column(Float)
    market_price = Column(Float)
    net_debt = Column(Float)
    assets = Column(Float)
    equity = Column(Float)
    cash_equivalents = Column(Float)
    liabilities = Column(Float)


engine = create_engine('sqlite:///investor.db', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

"""
with open('companies.csv', 'r') as companies:
    filter_reader = csv.reader(companies, delimiter=",")
    count = 0
    for line in filter_reader:
        if count == 0:
            count += 1
            continue
        company = Company(ticker=line[0], name=line[1], sector=line[2])
        session.add(company)
        count += 1

    session.commit()

companies.close()

with open('financial.csv', 'r') as financials:
    filter_reader = csv.reader(financials, delimiter=",")
    count = 0
    for line in filter_reader:
        if count == 0:
            count += 1
            continue

        financial = Financial(
            ticker=line[0] if line[0] != "" else None,
            ebitda=line[1] if line[1] != "" else None,
            sales=line[2] if line[2] != "" else None,
            net_profit=line[3] if line[3] != "" else None,
            market_price=line[4] if line[4] != "" else None,
            net_debt=line[5] if line[5] != "" else None,
            assets=line[6] if line[6] != "" else None,
            equity=line[7] if line[7] != "" else None,
            cash_equivalents=line[8] if line[8] != "" else None,
            liabilities=line[9] if line[9] != "" else None,
        )
        session.add(financial)
        count += 1

    session.commit()

financials.close()
"""

#print("Database created successfully!")


top_ten_query = session.query(
    Financial.ticker,
    Financial.ebitda,
    Financial.sales,
    Financial.net_profit,
    Financial.market_price,
    Financial.net_debt,
    Financial.assets,
    Financial.equity,
    Financial.cash_equivalents,
    Financial.liabilities
)
for ticker, ebitda, sales, net_profit, market_price, net_debt, assets, equity, cash_equivalent, liabilities in top_ten_query:
    value_ebitda = round(int(net_debt) / int(ebitda), 2) if net_debt is not None and ebitda is not None else None
    value_roe = round(int(net_profit) / int(equity), 2) if net_profit is not None and equity is not None else None
    value_roa = round(int(net_profit) / int(assets), 2) if net_profit is not None and assets is not None else None

    dict_nb_ebitda[ticker] = value_ebitda
    dict_roe[ticker] = value_roe
    dict_roa[ticker] = value_roa

print("Welcome to the Investor Program!")

while True:
    try:
        if current_menu == main_menu:
            print(main_menu, *main_menu_options, sep="\n")
            user_input = int(input(enter_option_message))

            if user_input == 0:
                break
            else:
                current_menu = options[user_input]

        elif current_menu == crud_menu:
            print(crud_menu, *crud_menu_options, sep="\n")
            user_input = int(input(enter_option_message))

            if user_input == 0:
                current_menu = options[user_input]
            elif user_input == 1:
                create_company()
                current_menu = main_menu
            elif user_input == 2:
                read_company()
                current_menu = main_menu
            elif user_input == 3:
                update_company()
                current_menu = main_menu
            elif user_input == 4:
                delete_company()
                current_menu = main_menu
            elif user_input == 5:
                list_company()
                current_menu = main_menu

        elif current_menu == top_ten_menu:
            print(top_ten_menu, *top_ten_options, sep="\n")
            user_input = int(input(enter_option_message))

            if user_input == 0:
                current_menu = options[user_input]

            elif user_input == 1:
                filtered_dict = dict(filter(lambda x: x[1] is not None, dict_nb_ebitda.items()))
                top_ten_ebitda = dict(sorted(filtered_dict.items(), key=lambda x: x[1], reverse=True))

                print("TICKER ND/EBITDA")
                count = 0
                for key, value in top_ten_ebitda.items():
                    if count < 10:
                        print(key, value, sep=" ")
                        count += 1
                    else:
                        break

                current_menu = main_menu
            elif user_input == 2:
                filtered_dict = dict(filter(lambda x: x[1] is not None, dict_roe.items()))
                top_ten_roe = dict(sorted(filtered_dict.items(), key=lambda x: x[1], reverse=True))

                print("TICKER ROE")
                count = 0
                for key, value in top_ten_roe.items():
                    if count < 10:
                        print(key, value, sep=" ")
                        count += 1
                    else:
                        break

                current_menu = main_menu
            elif user_input == 3:
                filtered_dict = dict(filter(lambda x: x[1] is not None, dict_roa.items()))
                top_ten_roa = dict(sorted(filtered_dict.items(), key=lambda x: x[1], reverse=True))

                print("TICKER ROA")
                count = 0
                for key, value in top_ten_roa.items():
                    if count < 10:
                        print(key, value, sep=" ")
                        count += 1
                    else:
                        break
                current_menu = main_menu
            else:
                print(invalid_option_message)
                current_menu = main_menu

    except Exception as error:
        print(invalid_option_message)
        print(error)

print("Have a nice day!")
