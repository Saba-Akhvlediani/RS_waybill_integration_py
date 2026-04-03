from rs_client import RsClient
from constants import WaybillType
from datetime import datetime, timedelta

# ====== FILL YOUR CREDENTIALS ======
SU = 'saba test:206322102'
SP = 'Saba1234.'

client = RsClient(su=SU, sp=SP)

# 1. Basic connectivity
print("=== 1. IP & Server Time ===")
print("My IP:", client.what_is_my_ip())
print("Server Time:", client.get_server_time())

# 2. Verify credentials
print("\n=== 2. Verify Credentials ===")
creds = client.verify_credentials()
print(creds)
if not creds['valid']:
    print("INVALID CREDENTIALS — stopping here")
    exit()

    # 3. Reference data
print("\n=== 3. Waybill Types ===")
for t in client.get_waybill_types():
    print(f"  {t}")

print("\n=== 4. Waybill Units ===")
for u in client.get_waybill_units():
    print(f"  {u}")

print("\n=== 5. Transport Types ===")
for t in client.get_trans_types():
    print(f"  {t}")

    # 4. TIN lookup
print("\n=== 6. TIN Lookup ===")
test_tin = '000000000'  # replace with a real TIN
name = client.get_name_from_tin(test_tin)
print(f"TIN {test_tin} → {name}")


# 5. VAT check
print("\n=== 7. VAT Payer Check ===")
is_vat = client.is_vat_payer_tin(test_tin)
print(f"TIN {test_tin} VAT payer: {is_vat}")


# 6. Query existing waybills (last 30 days)
print("\n=== 8. My Waybills (seller, last 30 days) ===")
waybills = client.get_waybills(
    start_date=datetime.now() - timedelta(days=30),
    end_date=datetime.now(),
)
print(f"Found {len(waybills)} waybills")
for w in waybills[:3]:
    print(f"  ID={w.get('ID')} STATUS={w.get('STATUS')} BUYER = {w.get('BUYER_TIN')}")


# 7. Query buyer waybills
print("\n=== 9. Buyer Waybills (last 30 days) ===")
buyer_waybills = client.get_buyer_waybills(start_date=datetime.now() - timedelta(days=30),end_date=datetime.now(),)
print(f"Found {len(buyer_waybills)} buyer waybills")
for w in buyer_waybills[:3]:
    print(f"  ID={w.get('ID')} STATUS={w.get('STATUS')} SELLER = {w.get('SELLER_TIN')}")
