landlordview

			<div>Name : {{ j[0] }}</div>
			<div>Email : {{ j[1] }}</div>
			<div>Phone : {{ j[2] }}</div>
			<div>Gender : {{ j[3] }}</div>
			<div>Age : {{ j[4] }}</div>
			<div>Company : {{ j[5] }}</div>
			user_id = {{ j[6] }}

select t.name,t.email,t.gender,t.age,c.name,c.company_id
from tenants as t left outer join company as c on t.tenant_id = c.company_id

以下三个 "user_id" 是landlordview传回的参数 用于获取特定tenant的profile



view_tenantcompany

			<div>Name : {{ j[0] }}</div>
			<div>Address : {{ j[1] }}</div>
			<div>Phone : {{ j[2] }}</div>
			<div>Email : {{ j[3] }}</div>

select c.name,c.address,c.phone,c.email 
from company as c, work_in as w
where c.company_id = w.company_id and w.tenant_id = "user_id"



view_tenantrequirements

			<div>Price : {{ j[0] }}</div>
			<div>Size : {{ j[1] }}</div>
			<div>Type : {{ j[2] }}</div>

select r.price,r.size,r.type
from requirement as r, post as p
where r.requirement_id = p.requirement_id and p.tenant_id = "user_id"



view_tenantlivein

			<div>Size : {{ j[0] }}</div>
			<div>Type : {{ j[1] }}</div>
			<div>Price : {{ j[2] }}</div>
			<div>Apt N umber : {{ j[3] }}</div>
			<div>Address : {{ j[4] }}</div>
			<div>From : {{ j[5] }}</div>
			<div>To : {{ j[6] }}</div>

select a.size,a.type,a.price,a.house_number,b.address,l.from_,l.to_
from apartment_belong as a, building as b, live_in as l
where a.building_id = b.building_id and l.apartment_id = a.apartment_id and l.tenant_id = "user_id"





