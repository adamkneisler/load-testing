import random
from faker import Faker
import uuid
import json

def get_account():
	"""
	Returns qo_id for user that was created at setup
	"""
	f = open('/tmp/accounts.json')
	account_data = json.loads(random.choice(f.read().splitlines()))

	return account_data

def get_coupon_code():
	"""
	Get a random coupon code to redeem for
	"""
	coupon_codes = ["GH", "GR"]
	return random.choice(coupon_codes)

	# I was doing a lot of nonsense here that isn't at all necessary
	# but now I refuse to delete it!
	# ------------------------------------------------------------------
	# f = open('/tmp/serialized_codes')
	# lines = f.read().splitlines()
	# code_data = random.choice(lines)
	# f.close()

	# f = open('/tmp/serialized_codes', 'w')
	# for line in lines:
	# 	if line != code_data:
	# 		f.write(line)
	# 		f.write('\n')
	# f.close()

	# code_dict = json.loads(code_data)
	# return list(code_dict.values())[0]

def account_create_payload():
	"""
	Build payload to create an account
	"""
	fake = Faker()

	# Create JSON file of accounts created
	f = open('/tmp/accounts.json', 'a+')

	payload = {}
	payload['first_name'] = fake.first_name()
	payload['last_name'] = fake.last_name()
	payload['email'] = fake.email()
	payload['qo_id'] = str(uuid.uuid4()).replace('-', '')
	payload['qo_token'] = str(uuid.uuid4()).replace('-', '')
	payload['phone_number'] = fake.phone_number()

	json.dump(payload, f)
	f.write('\n')
	f.close()

	return payload

def transaction_payload():
	"""
	Build payload to submit an order
	"""
	account = get_account()
	order_id = str(uuid.uuid4()).replace('-', '')
	
	order_payload = {
		"order_id": order_id,
		"qo_id": account['qo_id'],
		"store_id": "316784",
		"order_details": {
			"price": {
			"total": 18.69,
			"subtotal": 16.99,
			"delivery": 2.99,
			"tax": 1.7
			},
			"items": [
			],
			"order_time": 1484156560141,
			"coupons": []
		},
		"order_time": 1484156567,
		"qo_token": account['qo_token']
		}
	
	write_batch(account, order_payload)
	return order_payload

def write_batch(account, transaction_payload):
	"""
	Function to generate batch file data
	"""
	import datetime

	random_number = random.randint(1,10) # Generate random number
	magic_number = 5 # Use this to determine if we're going to change 
					#the subtotal amount in the header batch to test differing amounts
	
	# If our random number matches the magic number, set a different value for subtotal
	if random_number == magic_number:
		subtotal = "18.79"
	else:
		subtotal = str(transaction_payload['order_details']['price']['subtotal'])
	
	date = str(datetime.date.today())
	time = datetime.datetime.now().strftime("%H:%M:%S")

	header = open('/tmp/header.txt', 'a+')
	detail = open('/tmp/detail.txt', 'a+')

	base_header_line = """"123"|"456"|"789"|"987"|"{0}"|"{1}"|"{2}"|"ORDER PROCESSED"|"Website                       "|"Delivery"|"{3}"|" 0000.00"|" 0000.00"|" 0000.00"|"{4}"|"{5}"|" 00000000{6}"|"{7}"|"Y"|"{8}"\n"""
	header_line= base_header_line.format(
		transaction_payload['store_id'],
		date,
		time,
		account['phone_number'],
		subtotal,
		subtotal,
		str(transaction_payload['order_details']['price']['delivery']),
		transaction_payload['order_id'],
		transaction_payload['qo_id']
	)
	header.write(header_line)
	header.close()

	base_detail_line = """"123"|"456"|"789"|"987"|"{0}"|"{1}"|"{2}"|"{3}"|"{4}"|"{5}"|"{6}"|{7}"|"Order"|""|"Delivery"|"-1"|"NO COUPON"|"N/A"|"Standard"|" {8}"|" 0000.00"|" {9}"|" {10}"|" 0000.00"|" 0000.00"|"{11}"|"Y"|"{12}"\n"""
	
	count = 1
	for item in transaction_payload['order_details']['items']:
		detail_line = base_detail_line.format(
			transaction_payload['store_id'],
			date,
			str(count),
			item['description'],
			str(item['id']),
			item['category'],
			item['category'],
			item['category'],
			str(item['price']),
			str(item['price']),
			str(item['quantity']),
			transaction_payload['order_id'],
			transaction_payload['qo_id']
		)
		detail.write(detail_line)
		count+=1
	detail.close()