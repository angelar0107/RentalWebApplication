tenantview

viewallapt:
-- @app.route("/viewallapt/", methods=['POST'])
-- def move_forward():
--     #写sql 把东西抓回来
--     apt_list = {}
--     return render_template('tenantview.html', message=apt_list);
			-- <div>Size : {{ j[0] }}</div>
			-- <div>Type : {{ j[1] }}</div>
			-- <div>Price : {{ j[2] }}</div>
			-- <div>Apt N umber : {{ j[3] }}</div>
			-- <div>Address : {{ j[4] }}</div>

select a.size, a.type, a.price, a.house_number, b.address
from apartment_belong as a, buildings as b, offer as o
where a.building_id = b.building_id and a.apartment_id = o.apartment_id and o.availability = "t"


viewalllandlord:
-- @app.route("/viewalllandlord/", methods=['POST'])
-- def move_forward():
--     #写sql 把东西抓回来
--     landlord_list = {}
--     return render_template('tenantview.html', message=landlord_list);
			-- <div>Name : {{ j[0] }}</div>
			-- <div>Gender : {{ j[1] }}</div>
			-- <div>Email : {{ j[2] }}</div>
			-- <div>Age : {{ j[3] }}</div>
			-- <div>Phone : {{ j[4] }}</div>
			-- landlord_id = {{ j[5] }}

select l.name,l.gender,l.email,l.age,l.phone,l.landlord_id
from landlords as l

view_landlord_apt:
			"landlord_id" 为传入参数 这个和之前的"user_id"类似

			-- <div>Size : {{ j[0] }}</div>
			-- <div>Type : {{ j[1] }}</div>
			-- <div>Price : {{ j[2] }}</div>
			-- <div>Apt N umber : {{ j[3] }}</div>
			-- <div>Address : {{ j[4] }}</div>

select a.size,a.type,a.price,a.house_number,b.address
from offer as o,apartment_belong as a, buildings as b
where a.building_id = b.building_id and o.building_id = a.building_id and o.landlord_id = "landlord_id"



viewallbuilding:
-- @app.route("/viewallbuilding/", methods=['POST'])
-- def move_forward():
--     #写sql 把东西抓回来
--     building_list = {}
--     return render_template('tenantview.html', message=building_list);
			-- <div>Address : {{ j[0] }}</div>
			-- <div>Built I n : {{ j[1] }}</div>
			-- <div>Stories : {{ j[2] }}</div>
			-- <div>Units : {{ j[3] }}</div>
			-- <div>Description : {{ j[4] }}</div>
			-- building_id = {{ j[5]}}
select b.address,b.built_in,b.stories,b.units,b.description,b.building_id
from buildings as b


Following 两个 "building_id" 为传入参数

view_building_amen:

			-- <div>Name : {{ j[0] }}</div>
			-- <div>Description : {{ j[1] }}</div>

select am.name,am.description
from amenity as am, has as h
where h.amenity_id = am.amenity_id and h.building_id = "building_id"


view_building_apt:
			-- <div>Size : {{ j[0] }}</div>
			-- <div>Type : {{ j[1] }}</div>
			-- <div>Price : {{ j[2] }}</div>
			-- <div>Apt Number : {{ j[3] }}</div>
select a.size, a.type, a.price,a.house_number
from apartment_belong as a
where a.building_id = "building_id"



tenantview 自身:

根据两个form 不同post 决定如何select，但是调用同一个界面 然后apt_list 传给viewspecial显示
if id = viewspecialtype

select a.size,a.type,a.price,a.house_number
from apartment_belong as a
where a.type = "type"<========表单提交内容

if id = viewspecialprice
select a.size,a.type, a.price,a.house_number
from apartment_belong as a
where a.price <= "price"<========表单提交内容	


render_template('viewspecial.html',apt_list)













