from datetime import datetime




class XmlBuilder:


    def build_auth(self, su, sp):
        # 3 აუთენთიკაციის პარამეტრს მოითხოვს ყველა rs.ge-ს მეთოდი.შიდა გამოყენებისთვის RsClient._auth()

        return {
            'su': su,
            'sp': sp,
        }


    def chek_service_user(self, su, sp):
        #ამოწმებს სერვისის მომხმარებელს

        return {
            'su': su,
            'sp': sp
        }


    def update_service_user(self, user_name, user_password, ip, name, su, sp):
        #მომხმარებლის ინფორმაციის განახლება

        return {
            'user_name': user_name,
            'user_password': user_password,
            'ip': ip,
            'name': name,
            'su': su,
            'sp': sp
        }


    def build_get_service_users(self, user_name, user_password):
        #აბრუნებს სერვისის მომხმარებლებს

        return {
            'user_name': user_name,
            'user_password': user_password
        }


    def get_waybill_types(self, su, sp):

        return {
            'su': su,
            'sp': sp
        }

    def build_waybill(self, seller_tin, buyer_tin, start_address, end_address, driver_tin, car_number, waybill_type,
                      transport_type, goods):

        goods_xml = ''
        for item in goods:
            goods_xml += f"""
            <goods>
                <n>{item['name']}</n>
                <unit_id>{item.get('unit_id', 0)}</unit_id>
                <unit_txt>{item.get('unit_txt', '')}</unit_txt>
                <quantity>{item['quantity']}</quantity>
                <price>{item['price']}</price>
                <bar_code>{item.get('bar_code', '')}</bar_code>
                <akciz_id>{item.get('akciz_id', 0)}</akciz_id>
            </goods>"""

        return f"""
        <waybill>
            <type>{waybill_type}</type>
            <seller_tin>{seller_tin}</seller_tin>
            <buyer_tin>{buyer_tin}</buyer_tin>
            <start_address>{start_address}</start_address>
            <end_address>{end_address}</end_address>
            <driver_tin>{driver_tin}</driver_tin>
            <car_number>{car_number}</car_number>
            <transport_type_id>{transport_type}</transport_type_id>
            <goods_list>{goods_xml}
            </goods_list>
        </waybill>""".strip()


    def build_get_waybills(self, su, sp, start_date, end_date,
                           buyer_tin='', statuses='',
                           car_number='', waybill_number=''):
        """
        get_waybills()-ის პარამეტრები — გამყიდველის ზედნადებების სია.

        თარიღის პარამეტრები:
            begin_date_s/e    → ზედნადების დაწყების თარიღის დიაპაზონი
            create_date_s/e   → შექმნის თარიღის დიაპაზონი
            delivery_date_s/e → მიწოდების თარიღის დიაპაზონი
            close_date_s/e    → დახურვის თარიღის დიაპაზონი

        ჩვენ ყველასთვის ერთსა და იმავე start/end-ს ვიყენებთ.
        full_amount=None ნიშნავს — ამ ველით არ გავფილტრავთ.
        """
        return {
            'su': su,
            'sp': sp,
            'itypes': '',
            'buyer_tin': buyer_tin,
            'statuses': statuses,
            'car_number': car_number,
            'begin_date_s': start_date,
            'begin_date_e': end_date,
            'create_date_s': start_date,
            'create_date_e': end_date,
            'driver_tin': '',
            'delivery_date_s': start_date,
            'delivery_date_e': end_date,
            'full_amount': None,
            'waybill_number': waybill_number,
            'close_date_s': start_date,
            'close_date_e': end_date,
            's_user_ids': '',
            'comment': '',
        }


    def build_get_buyer_waybills(self, su, sp, start_date, end_date, seller_tin='', statuses=''):
        """პარამეტრები რომ მივიღოთ ზედნადებების სია (ვართ მყიდველები)"""
        return {
            'su': su,
            'sp': sp,
            'itypes': '',
            'seller_tin': seller_tin,
            'statuses': statuses,
            'car_number': '',
            'begin_date_s': start_date,
            'begin_date_e': end_date,
            'create_date_s': start_date,
            'create_date_e': end_date,
            'driver_tin': '',
            'delivery_date_s': start_date,
            'delivery_date_e': end_date,
            'full_amount': None,
            'waybill_number': '',
            'close_date_s': start_date,
            'close_date_e': end_date,
            's_user_ids': '',
            'comment': '',
        }