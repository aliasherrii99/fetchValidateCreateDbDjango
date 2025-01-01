from task3_app.models import CreateDb
from task3_app.fetchSave import change_value
import requests
import json
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

fp_url = "https://fund.fipiran.ir/api/v1/fund/fundcompare"


# for validation data
class DataV(BaseModel):
    model_config = ConfigDict(alias_generator=change_value)
    reg_no: int = Field(alias="regNo")
    name: str
    rank_of_12_month: Optional[int] = None
    rank_of_24_month: Optional[int] = None
    rank_of_36_month: Optional[int] = None
    rank_of_48_month: Optional[int] = None
    rank_of_60_month: Optional[int] = None
    rank_last_update: Optional[str] = None
    fund_type: Optional[int] = None
    type_of_invest: Optional[str] = None
    fund_size: Optional[int] = None
    initiation_date: Optional[str] = None
    daily_efficiency: Optional[float] = None
    weekly_efficiency: Optional[float] = None
    monthly_efficiency: Optional[float] = None
    quarterly_efficiency: Optional[float] = None
    six_month_efficiency: Optional[float] = None
    annual_efficiency: Optional[float] = None
    statistical_nav: Optional[float] = None
    efficiency: Optional[float] = None
    cancel_nav: Optional[float] = None
    issue_nav: Optional[float] = None
    dividend_interval_period: Optional[int] = None
    guaranteed_earning_rate: Optional[float] = None
    data: Optional[str] = None
    net_asset: Optional[int] = None
    estimated_earning_rate: Optional[float] = None
    invested_units: Optional[int] = None
    articles_of_association_link: Optional[str] = None
    prospectus_link: Optional[str] = None
    website_address: Optional[list] = None
    manager: str
    manager_seo_register_no: Optional[int] = None
    guarantor_seo_register_no: Optional[int] = None
    auditor: str
    custodian: str
    guarantor: str
    beta: Optional[float] = None
    alpha: Optional[float] = None
    is_completed: Optional[bool] = None
    five_best: Optional[float] = None
    stock: Optional[float] = None
    bond: Optional[float] = None
    other: Optional[float] = None
    cash: Optional[float] = None
    deposit: Optional[float] = None
    fund_unit: Optional[float] = None
    commodity: Optional[float] = None
    fund_publisher: Optional[int] = None
    small_symbol_name: Optional[str] = None
    ins_code: Optional[str] = None
    fund_watch: Optional[str] = None


# return data from api
def fetch_data_from_api(url):
    response = requests.get(url)
    return json.loads(response.text)


# return validated data from API
def validated_data_from_api():
    my_data = fetch_data_from_api(fp_url)
    data_api = [DataV.model_validate(item) for item in my_data['items']]
    return data_api


# return list of regno in api
def regno_in_api():
    list_regno = []
    for i in validated_data_from_api():
        list_regno.append(i.reg_no)
    return list_regno


# return list of regno in DB
def regno_in_db():
    regno_list = CreateDb.objects.values_list('reg_no', flat=True)
    return list(regno_list)


list_of_regno_in_api = regno_in_api()
list_of_regno_in_db = regno_in_db()


# return list of regno not in db
def regno_not_db():
    list_not_in_db = []
    for i in list_of_regno_in_api:
        if i in list_of_regno_in_db:
            pass
        else:
            list_not_in_db.append(i)
    return list_not_in_db


list_regno_not_in_db = regno_not_db()
validated_data = validated_data_from_api()


# return rows to be added
def new_rows():
    rows_be_add = []
    for i in validated_data:
        if i.reg_no in list_regno_not_in_db:
            rows_be_add.append(i)
    return rows_be_add


rows_be_add_to_db = new_rows()


def save_data_to_db():
    for item in rows_be_add_to_db:
        CreateDb.objects.create(
            reg_no=item.reg_no,
            name=item.name,
            rank_of_12_month=item.rank_of_12_month,
            rank_of_24_month=item.rank_of_24_month,
            rank_of_36_month=item.rank_of_36_month,
            rank_of_48_month=item.rank_of_48_month,
            rank_of_60_month=item.rank_of_60_month,
            rank_last_update=item.rank_last_update,
            fund_type=item.fund_type,
            type_of_invest=item.type_of_invest,
            fund_size=item.fund_size,
            initiation_date=item.initiation_date,
            daily_efficiency=item.daily_efficiency,
            weekly_efficiency=item.weekly_efficiency,
            monthly_efficiency=item.monthly_efficiency,
            quarterly_efficiency=item.quarterly_efficiency,
            six_month_efficiency=item.six_month_efficiency,
            annual_efficiency=item.annual_efficiency,
            statistical_nav=item.statistical_nav,
            efficiency=item.efficiency,
            cancel_nav=item.cancel_nav,
            issue_nav=item.issue_nav,
            dividend_interval_period=item.dividend_interval_period,
            guaranteed_earning_rate=item.guaranteed_earning_rate,
            data=item.data,
            net_asset=item.net_asset,
            estimated_earning_rate=item.estimated_earning_rate,
            invested_units=item.invested_units,
            articles_of_association_link=item.articles_of_association_link,
            prospectus_link=item.prospectus_link,
            website_address=item.website_address,
            manager=item.manager,
            manager_seo_register_no=item.manager_seo_register_no,
            guarantor_seo_register_no=item.guarantor_seo_register_no,
            auditor=item.auditor,
            custodian=item.custodian,
            guarantor=item.guarantor,
            beta=item.beta,
            alpha=item.alpha,
            is_completed=item.is_completed,
            five_best=item.five_best,
            stock=item.stock,
            bond=item.bond,
            other=item.other,
            cash=item.cash,
            deposit=item.deposit,
            fund_unit=item.fund_unit,
            commodity=item.commodity,
            fund_publisher=item.fund_publisher,
            small_symbol_name=item.small_symbol_name,
            ins_code=item.ins_code,
            fund_watch=item.fund_watch,
        )
